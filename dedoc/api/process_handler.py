# region MODULE_CONTRACT [DOMAIN(9): DocumentProcessing, ProcessManagement; CONCEPT(8): RequestHandling, MultiprocessingCancellation; TECH(9): Multiprocessing, AsyncIO, PickleIPC]
## @modulecontract
## @purpose Implement document parsing request handlers with support for client disconnect cancellation via multiprocessing. Provides a synchronous handler and an async handler with child process isolation.
## @scope Request processing pipeline — synchronous parsing (ProcessHandler) and cancellable multiprocessing parsing (CancellationProcessHandler).
## @input Request, parameters dict, file_path, tmpdir.
## @output Optional[ParsedDocument] — parsed document or None if cancelled.
## @links [USES_API(9): multiprocessing.Process, multiprocessing.Queue; USES_API(8): anyio.get_cancelled_exc_class; READS_DATA_FROM(9): dedoc.dedoc_manager.DedocManager, dedoc.api.cancellation]
## @invariants
## - CancellationProcessHandler.process is always restarted if terminated (None check in handle).
## - _parse_file runs in a background process with signal isolation to prevent master process termination.
## - Pickle is used for IPC (Queue) between master and child processes.
## @rationale
## Q: Why multiprocessing for cancellation?
## A: FastAPI's asyncio cannot forcefully terminate CPU-bound document parsing. A separate process allows full process termination on client disconnect, freeing resources immediately.
## Q: Why pickle-based IPC?
## A: Python's multiprocessing.Queue requires picklable objects. Pickle is the standard serialization for this use case, though it requires ParsedDocument and DedocError to be picklable.
## @changes
## LAST_CHANGE: [v1.0.0 – Initial creation with semantic markup]
## @modulemap
## CLASS 7[Abstract base for process handlers] => AbstractProcessHandler
## METHOD 5[Attaches base64-encoded data to attachment metadata] => _add_base64_info_to_attachments
## CLASS 8[Synchronous document handler using DedocManager directly] => ProcessHandler
## CLASS 10[Async handler with multiprocessing child process for cancellable parsing] => CancellationProcessHandler
## METHOD 9[Handle request with client disconnect monitoring and IPC] => CancellationProcessHandler.handle
## METHOD 9[Background child process loop — parses files from input queue] => _parse_file
## @usecases
## - [ProcessHandler]: ApiEndpoint => ParseDocumentSynchronously => ReturnResult
## - [CancellationProcessHandler]: ApiEndpoint => ParseWithDisconnectSupport => CancelOnClientDisconnect
def _module_contract():
    pass
# endregion MODULE_CONTRACT
# GREP_SUMMARY: process, handler, cancellation, multiprocessing, pickle, IPC, queue, async, parsing, document, client disconnect
# STRUCTURE: ▶ Request → ProcessHandler: ◇ manager.parse(file) → ⊕ result.to_api_schema() → ⎋ ParsedDocument | CancellationProcessHandler: ⚡ input_queue.put → ◇ child Process._parse_file → ⚡ output_queue.get → ⊕ result → ⎋ ParsedDocument

import asyncio
import base64
import logging
import os
import pickle
import signal
import traceback
from abc import abstractmethod
from multiprocessing import Process, Queue
from typing import Optional
from urllib.request import Request

from anyio import get_cancelled_exc_class

from dedoc.api.cancellation import cancel_on_disconnect
from dedoc.api.schema import ParsedDocument
from dedoc.common.exceptions.dedoc_error import DedocError
from dedoc.config import get_config
from dedoc.dedoc_manager import DedocManager

logger = logging.getLogger(__name__)

# region CLASS_AbstractProcessHandler [DOMAIN(8): ProcessManagement; CONCEPT(7): HandlerAbstraction; TECH(7): ABC, AbstractMethod]
## @purpose Abstract base class for document processing handlers. Defines the handle interface and shared utility for base64 attachment encoding.
class AbstractProcessHandler:

    # region METHOD___init__ [DOMAIN(7): Initialization; CONCEPT(6): LoggerInjection; TECH(5): Constructor]
    ## @purpose Initialize the handler with a logger instance for diagnostic output.
    ## @io (Logger) -> None
    ## @complexity 2
    def __init__(self, logger: logging.Logger) -> None:
        self.logger = logger
        self.logger.debug(f"[IMP:4][AbstractProcessHandler][INIT] Handler initialized")
    # endregion METHOD___init__

    # region METHOD_handle [DOMAIN(9): DocumentProcessing; CONCEPT(8): RequestHandling; TECH(7): AbstractMethod]
    ## @purpose Abstract method: process a document parsing request. Must be implemented by subclasses.
    ## @io (Request, dict, str, str) -> Optional[ParsedDocument]
    ## @complexity 1
    @abstractmethod
    async def handle(self, request: Request, parameters: dict, file_path: str, tmpdir: str) -> Optional[ParsedDocument]:
        pass
    # endregion METHOD_handle

    # region METHOD__add_base64_info_to_attachments [DOMAIN(7): AttachmentProcessing; CONCEPT(6): Base64Encoding; TECH(6): FileIO, Base64]
    ## @purpose Read attachment files from disk and encode them as base64, storing the result in the attachment's metadata attribute.
    ## @io (ParsedDocument, str) -> None
    ## @complexity 4
    def _add_base64_info_to_attachments(self, document_tree: ParsedDocument, attachments_dir: str) -> None:
        self.logger.debug(f"[IMP:4][AbstractProcessHandler][ADD_BASE64] Processing {len(document_tree.attachments)} attachments")
        for attachment in document_tree.attachments:
            with open(os.path.join(attachments_dir, attachment.metadata.temporary_file_name), "rb") as attachment_file:
                attachment.metadata.add_attribute("base64", base64.b64encode(attachment_file.read()).decode("utf-8"))
    # endregion METHOD__add_base64_info_to_attachments
# endregion CLASS_AbstractProcessHandler

# region CLASS_ProcessHandler [DOMAIN(8): DocumentProcessing; CONCEPT(8): SynchronousParsing; TECH(7): DedocManager]
## @purpose Simple synchronous document handler. Uses DedocManager directly without multiprocessing — suitable for environments where cancellation is not required.
class ProcessHandler(AbstractProcessHandler):
    """
    Simple synchronous document handler.
    """

    # region METHOD___init__ [DOMAIN(7): Initialization; CONCEPT(6): ManagerSetup; TECH(6): Constructor]
    ## @purpose Initialize the synchronous handler with a DedocManager instance and log the handler type.
    ## @io (Logger) -> None
    ## @complexity 3
    def __init__(self, logger: logging.Logger) -> None:
        super().__init__(logger=logger)
        self.manager = DedocManager(config=get_config())
        self.logger.info("[IMP:9][ProcessHandler][INIT] Using ProcessHandler, do not support parsing process termination")
    # endregion METHOD___init__

    # region METHOD_handle [DOMAIN(9): DocumentProcessing; CONCEPT(8): SynchronousParsing; TECH(8): DedocManagerParse]
    ## @purpose Parse a document file synchronously using DedocManager, optionally adding base64 attachment data for HTML output format.
    ## @uses DedocManager.parse, _add_base64_info_to_attachments
    ## @io (Request, dict, str, str) -> Optional[ParsedDocument]
    ## @complexity 6
    async def handle(self, request: Request, parameters: dict, file_path: str, tmpdir: str) -> Optional[ParsedDocument]:
        try:
            return_format = str(parameters.get("return_format", "json")).lower()
            self.logger.info(f"[IMP:7][ProcessHandler][HANDLE] Parsing file: {os.path.basename(file_path)}, format: {return_format}")
            document_tree = self.manager.parse(file_path, parameters={**dict(parameters), "attachments_dir": tmpdir})

            if return_format == "html":
                self._add_base64_info_to_attachments(document_tree, tmpdir)
            return document_tree.to_api_schema()

        except DedocError as e:
            self.logger.error(f"[IMP:9][ProcessHandler][DEDOC_ERROR] Exception {e}: {e.msg_api}\n{traceback.format_exc()}")
            raise e
        except Exception as e:
            exc_message = f"Exception {e}\n{traceback.format_exc()}"
            self.logger.error(f"[IMP:10][ProcessHandler][UNHANDLED_ERROR] {exc_message}")
            raise e
    # endregion METHOD_handle
# endregion CLASS_ProcessHandler

# region CLASS_CancellationProcessHandler [DOMAIN(10): ProcessManagement; CONCEPT(9): CancellableParsing; TECH(9): Multiprocessing, IPC, AsyncIO]
## @purpose Handler for file parsing with support for client disconnection. Spawns a child process for CPU-bound parsing and terminates it on disconnect, keeping the API available for new connections.
##
## Algorithm:
## 1. Master process monitors client connection (via cancel_on_disconnect)
## 2. Child process waits on input_queue for tasks
## 3. Master sends task via pickle to input_queue
## 4. Child parses using DedocManager
## 5. Result is sent back via output_queue (pickle)
## 6. On disconnect: child process terminated, new process spawned on next request
class CancellationProcessHandler(AbstractProcessHandler):
    """
    Class for file parsing by DedocManager with support for client disconnection.
    If client disconnects during file parsing, the process of parsing is fully terminated and API is available to receive new connections.

    Handler uses the following algorithm:
    1. Master process is used for checking current connection (client disconnect)
    2. Child process is working on the background and waiting for the input file in the input_queue
    3. Master process calls the child process for parsing and transfers data through the input_queue
    4. Child process is parsing file using DedocManager
    5. The result of parsing is transferred to the master process through the output_queue
    6. If client disconnects, the child process is terminated. The new child process with queues will start with the new request
    """

    # region METHOD___init__ [DOMAIN(9): ProcessManagement; CONCEPT(8): ProcessSpawn; TECH(8): Multiprocessing, Queue]
    ## @purpose Initialize the cancellable handler: create input/output queues and spawn a background child process for parsing.
    ## @io (Logger) -> None
    ## @complexity 5
    def __init__(self, logger: logging.Logger) -> None:
        super().__init__(logger=logger)
        self.input_queue = Queue()
        self.output_queue = Queue()
        self.process = Process(target=self._parse_file, args=[self.input_queue, self.output_queue])
        self.process.start()
        self.logger.info("[IMP:9][CancellationProcessHandler][INIT] Using CancellationProcessHandler, support parsing process termination when client disconnects")
    # endregion METHOD___init__

    # region METHOD_handle [DOMAIN(10): ProcessManagement; CONCEPT(9): DisconnectHandling; TECH(9): AsyncIO, Executor, CancelScope]
    ## @purpose Handle a parsing request with client disconnect support. Sends task to child process via queue, monitors connection, terminates child on disconnect.
    ## @uses cancel_on_disconnect, loop.run_in_executor
    ## @io (Request, dict, str, str) -> Optional[ParsedDocument]
    ## @complexity 9
    async def handle(self, request: Request, parameters: dict, file_path: str, tmpdir: str) -> Optional[ParsedDocument]:
        """
        Handle request in a separate process.
        Checks for client disconnection and terminate the child process if client disconnected.
        """
        if self.process is None:
            self.logger.info("[IMP:9][CancellationProcessHandler][HANDLE] Initialization of a new parsing process")
            self.__init__(logger=self.logger)

        self.logger.info(f"[IMP:7][CancellationProcessHandler][HANDLE] Putting file to the input queue: {os.path.basename(file_path)}")
        self.input_queue.put(pickle.dumps((parameters, file_path, tmpdir)), block=True)

        loop = asyncio.get_running_loop()
        async with cancel_on_disconnect(request, self.logger):
            try:
                future = loop.run_in_executor(None, self.output_queue.get)
                result = await future
            except get_cancelled_exc_class():
                self.logger.warning("[IMP:8][CancellationProcessHandler][HANDLE] Terminating the parsing process")
                if self.process is not None:
                    self.process.terminate()
                self.process = None
                future.cancel(DedocError)
                return None

        result = pickle.loads(result)
        if isinstance(result, ParsedDocument):
            self.logger.info("[IMP:9][CancellationProcessHandler][HANDLE] Got the result from the output queue")
            return result

        raise DedocError.from_dict(result)
    # endregion METHOD_handle

    # region METHOD__parse_file [DOMAIN(10): ProcessManagement; CONCEPT(9): BackgroundParsing; TECH(9): Multiprocessing, SignalIsolation, Pickle]
    ## @purpose Background child process entry point: waits for tasks on input_queue, parses documents via DedocManager, and returns results via output_queue. Uses signal isolation to protect the master process.
    ## @uses DedocManager.parse, pickle.loads, pickle.dumps
    ## @io (Queue, Queue) -> None (runs indefinitely)
    ## @complexity 9
    def _parse_file(self, input_queue: Queue, output_queue: Queue) -> None:
        """
        Function for file parsing in a separate (child) process.
        It's a background process, i.e. it is waiting for a task in the input queue.
        The result of parsing is returned in the output queue.

        Operations with `signal` are used for saving master process while killing child process.
        See the issue for more details: https://github.com/fastapi/fastapi/issues/1487
        """
        signal.set_wakeup_fd(-1)
        signal.signal(signal.SIGTERM, signal.SIG_DFL)
        signal.signal(signal.SIGINT, signal.SIG_DFL)

        manager = DedocManager(config=get_config())
        manager.logger.info("[IMP:9][_parse_file][INIT] Parsing process is waiting for the task in the input queue")

        while True:
            file_path = None
            try:
                parameters, file_path, tmp_dir = pickle.loads(input_queue.get(block=True))
                manager.logger.info(f"[IMP:7][_parse_file][TASK_RECEIVED] Parsing process got task from the input queue: {os.path.basename(file_path)}")
                return_format = str(parameters.get("return_format", "json")).lower()
                document_tree = manager.parse(file_path, parameters={**dict(parameters), "attachments_dir": tmp_dir})

                if return_format == "html":
                    self._add_base64_info_to_attachments(document_tree, tmp_dir)

                output_queue.put(pickle.dumps(document_tree.to_api_schema()), block=True)
                manager.logger.info(f"[IMP:9][_parse_file][TASK_DONE] Parsing process put task to the output queue: {os.path.basename(file_path)}")
            except DedocError as e:
                tb = traceback.format_exc()
                manager.logger.error(f"[IMP:10][_parse_file][DEDOC_ERROR] Exception {e}: {e.msg_api}\n{tb}")
                output_queue.put(pickle.dumps(e.__dict__), block=True)
            except Exception as e:
                exc_message = f"Exception {e}\n{traceback.format_exc()}"
                filename = "" if file_path is None else os.path.basename(file_path)
                manager.logger.error(f"[IMP:10][_parse_file][UNHANDLED_ERROR] {exc_message}")
                output_queue.put(pickle.dumps({"msg": exc_message, "filename": filename}), block=True)
    # endregion METHOD__parse_file
# endregion CLASS_CancellationProcessHandler
