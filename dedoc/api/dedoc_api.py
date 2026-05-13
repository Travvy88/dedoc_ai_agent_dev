# region MODULE_CONTRACT [DOMAIN(9): DocumentProcessing, FastAPIEndpoints; CONCEPT(8): RESTAPI, DocumentUpload; TECH(9): FastAPI, Starlette, Uvicorn]
## @modulecontract
## @purpose Define the FastAPI application with all REST endpoints for the dedoc document parsing service: file upload, static file serving, version info, multi-format output rendering, and error handling.
## @scope FastAPI application setup — route definitions, static files mounting, process handler initialization, exception handlers, and server launch.
## @input HTTP requests (multipart upload, query parameters).
## @output FastAPI Response objects (JSON, HTML, PlainText, FileResponse).
## @links [USES_API(9): fastapi.FastAPI, fastapi.responses, starlette.responses; READS_DATA_FROM(8): dedoc.api.api_args, dedoc.api.api_utils, dedoc.api.process_handler, dedoc.api.schema, dedoc.config]
## @invariants
## - All endpoints return valid Response objects.
## - Exception handlers catch DedocError and generic Exception.
## - /upload endpoint accepts multipart form data with file and query parameters.
## @rationale
## Q: Why separate ProcessHandler instances based on ENABLE_CANCELLATION?
## A: CancellationProcessHandler uses multiprocessing for true process isolation during disconnect. For environments where cancellation is not needed, ProcessHandler is simpler and avoids multiprocessing overhead.
## @changes
## LAST_CHANGE: [v1.0.0 – Initial creation with semantic markup]
## @modulemap
## FUNC 5[Root endpoint redirects to index.html] => get_info
## FUNC 5[Serves static files from configured directories] => get_static_file
## FUNC 4[Returns dedoc version string] => get_version
## FUNC 4[Resolves static file path from request params] => _get_static_file_path
## FUNC 10[Main upload endpoint — parses document and returns formatted result] => upload
## FUNC 7[Example document upload endpoint for testing] => upload_example
## FUNC 6[DedocError exception handler — returns structured JSON error] => exception_handler
## FUNC 5[Generic exception handler — returns 500 with traceback] => any_exception_handler
## FUNC 3[Returns the FastAPI app instance] => get_api
## FUNC 4[Launches uvicorn server on configured port] => run_api
## @usecases
## - [upload]: Client => POST multipart file + parameters => Receive parsed document JSON/HTML
## - [run_api]: Operator => Execute launch script => Start dedoc API server
def _module_contract():
    pass
# endregion MODULE_CONTRACT
# GREP_SUMMARY: FastAPI, endpoints, upload, document, parsing, REST, API, HTML, JSON, static, version, exception, cancellation, uvicorn
# STRUCTURE: ▶ FastAPI() → mount /web StaticFiles → ◇ Routes ┌GET /, /static_file, /version, /upload_example; POST /upload┐ → ⊕ Response → ◇ ExceptionHandlers → run_api: uvicorn

import dataclasses
import importlib
import json
import logging
import os
import tempfile
import traceback
from typing import Optional

from fastapi import Depends, FastAPI, File, Request, Response, UploadFile
from fastapi.responses import ORJSONResponse, UJSONResponse
from fastapi.staticfiles import StaticFiles
from starlette.responses import FileResponse, HTMLResponse, JSONResponse, PlainTextResponse

import dedoc.version
from dedoc.api.api_args import QueryParameters
from dedoc.api.api_utils import json2collapsed_tree, json2html, json2tree, json2txt
from dedoc.api.process_handler import CancellationProcessHandler, ProcessHandler
from dedoc.api.schema.parsed_document import ParsedDocument
from dedoc.common.exceptions.dedoc_error import DedocError
from dedoc.common.exceptions.missing_file_error import MissingFileError
from dedoc.config import get_config
from dedoc.utils.parameter_utils import get_bool_value
from dedoc.utils.utils import save_upload_file

config = get_config()
logger = config["logger"]
PORT = config["api_port"]
ENABLE_CANCELLATION = get_bool_value(os.getenv("ENABLE_CANCELLATION"), True)
static_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "web")
static_files_dirs = config.get("static_files_dirs")

app = FastAPI()
app.mount("/web", StaticFiles(directory=config.get("static_path", static_path)), name="web")
module_api_args = importlib.import_module(config["import_path_init_api_args"])
process_handler = CancellationProcessHandler(logger=logger) if ENABLE_CANCELLATION else ProcessHandler(logger=logger)

logger.info(f"[IMP:9][dedoc_api][INIT] API initialized. Cancellation={'enabled' if ENABLE_CANCELLATION else 'disabled'}, port={PORT}")

# region FUNC_get_info [DOMAIN(5): WebRouting; CONCEPT(4): RootEndpoint; TECH(5): FastAPI, FileResponse]
## @purpose Serve the root URL "/" with the static index.html page. Required to avoid 404 from rest-plus bug when root is not defined.
## @io None -> FileResponse
## @complexity 2
@app.get("/")
def get_info() -> Response:
    """
    Root URL "/" is need start with simple Flask before rest-plus. API otherwise you will get 404 Error.
    It is bug of rest-plus lib.
    """
    return FileResponse(os.path.join(static_path, "index.html"))
# endregion FUNC_get_info

# region FUNC_get_static_file [DOMAIN(5): WebRouting; CONCEPT(5): StaticFileServing; TECH(5): FastAPI, QueryParams]
## @purpose Serve static files from configured directories based on query parameters (fname and directory).
## @uses _get_static_file_path
## @io Request -> FileResponse
## @complexity 3
@app.get("/static_file")
def get_static_file(request: Request) -> Response:
    path = _get_static_file_path(request)
    return FileResponse(path)
# endregion FUNC_get_static_file

# region FUNC_get_version [DOMAIN(4): SystemInfo; CONCEPT(3): VersionReporting; TECH(4): FastAPI, PlainTextResponse]
## @purpose Return the current dedoc version as a plain text response.
## @io None -> PlainTextResponse
## @complexity 1
@app.get("/version")
def get_version() -> Response:
    return PlainTextResponse(dedoc.version.__version__)
# endregion FUNC_get_version

# region FUNC__get_static_file_path [DOMAIN(5): FileResolution; CONCEPT(4): PathSecurity; TECH(5): osPath, QueryParams]
## @purpose Resolve the absolute path to a static file from request query parameters (fname, directory), ensuring the path is within configured directories.
## @io Request -> str
## @complexity 3
def _get_static_file_path(request: Request) -> str:
    file = request.query_params.get("fname")
    directory_name = request.query_params.get("directory")
    directory = static_files_dirs[directory_name] if directory_name is not None and directory_name in static_files_dirs else static_path
    return os.path.abspath(os.path.join(directory, file))
# endregion FUNC__get_static_file_path

# region FUNC_upload [DOMAIN(9): DocumentProcessing; CONCEPT(9): MainParsingEndpoint; TECH(9): FastAPI, MultipartUpload, AsyncProcessing]
## @purpose Main dedoc API endpoint: receives a file upload via multipart form, parses it using the process handler, and returns the result in the requested format (json, html, plain_text, tree, etc.).
## @uses process_handler.handle, json2html, json2txt, json2tree, json2collapsed_tree
## @io (Request, UploadFile, QueryParameters) -> Response
## @complexity 9
@app.post("/upload", response_model=ParsedDocument)
async def upload(request: Request, file: UploadFile = File(...), query_params: QueryParameters = Depends()) -> Response:
    parameters = dataclasses.asdict(query_params)
    if not file or file.filename == "":
        raise MissingFileError("Error: Missing content in request_post file parameter", version=dedoc.version.__version__)

    logger.info(f"[IMP:7][dedoc_api][UPLOAD] Received file: {file.filename}, parameters: {parameters}")

    with tempfile.TemporaryDirectory() as tmpdir:
        file_path = save_upload_file(file, tmpdir)
        document_tree = await process_handler.handle(request=request, parameters=parameters, file_path=file_path, tmpdir=tmpdir)

    if document_tree is None:
        return JSONResponse(status_code=499, content={})

    return_format = str(parameters.get("return_format", "json")).lower()
    logger.info(f"[IMP:8][dedoc_api][UPLOAD_FORMAT] Return format: {return_format}")

    if return_format == "html":
        html_content = json2html(
            text="",
            paragraph=document_tree.content.structure,
            tables=document_tree.content.tables,
            attachments=document_tree.attachments,
            tabs=0
        )
        return HTMLResponse(content=html_content)

    if return_format == "plain_text":
        txt_content = json2txt(paragraph=document_tree.content.structure)
        return PlainTextResponse(content=txt_content)

    if return_format == "tree":
        html_content = json2tree(paragraph=document_tree.content.structure)
        return HTMLResponse(content=html_content)

    if return_format == "ujson":
        return UJSONResponse(content=document_tree.model_dump())

    if return_format == "collapsed_tree":
        html_content = json2collapsed_tree(paragraph=document_tree.content.structure)
        return HTMLResponse(content=html_content)

    if return_format == "pretty_json":
        return PlainTextResponse(content=json.dumps(document_tree.model_dump(), ensure_ascii=False, indent=2))

    logger.info(f"[IMP:9][dedoc_api][UPLOAD_RESULT] Send result. File {file.filename} with parameters {parameters}")
    return ORJSONResponse(content=document_tree.model_dump())
# endregion FUNC_upload

# region FUNC_upload_example [DOMAIN(7): DocumentProcessing; CONCEPT(6): ExampleEndpoint; TECH(7): FastAPI, StaticExamples]
## @purpose Serve an example document parsing result from the static examples directory for testing and demonstration purposes.
## @uses process_handler.handle, json2html
## @io (Request, str, Optional[str]) -> Response
## @complexity 6
@app.get("/upload_example")
async def upload_example(request: Request, file_name: str, return_format: Optional[str] = None) -> Response:
    file_path = os.path.join(static_path, "examples", file_name)
    parameters = {} if return_format is None else {"return_format": return_format}
    logger.debug(f"[IMP:4][dedoc_api][UPLOAD_EXAMPLE] Example file: {file_name}, return_format: {return_format}")

    with tempfile.TemporaryDirectory() as tmpdir:
        document_tree = await process_handler.handle(request=request, parameters=parameters, file_path=file_path, tmpdir=tmpdir)

    if return_format == "html":
        html_page = json2html(
            text="",
            paragraph=document_tree.content.structure,
            tables=document_tree.content.tables,
            attachments=document_tree.attachments,
            tabs=0
        )
        return HTMLResponse(content=html_page)
    return ORJSONResponse(content=document_tree.model_dump(), status_code=200)
# endregion FUNC_upload_example

# region FUNC_exception_handler [DOMAIN(6): ErrorHandling; CONCEPT(6): DedocErrorResponse; TECH(6): FastAPI, ExceptionHandler]
## @purpose Catch DedocError exceptions and return a structured JSON error response with message, filename, version, and metadata.
## @io (Request, DedocError) -> JSONResponse
## @complexity 4
@app.exception_handler(DedocError)
async def exception_handler(request: Request, exc: DedocError) -> Response:
    logger.error(f"[IMP:9][dedoc_api][DEDOC_ERROR] {exc.msg}, code={exc.code}, filename={exc.filename}")
    result = {"message": exc.msg}
    if exc.filename:
        result["file_name"] = exc.filename
    if exc.version:
        result["dedoc_version"] = exc.version
    if exc.metadata:
        result["metadata"] = exc.metadata
    return JSONResponse(status_code=exc.code, content=result)
# endregion FUNC_exception_handler

# region FUNC_any_exception_handler [DOMAIN(6): ErrorHandling; CONCEPT(5): FallbackErrorHandler; TECH(5): FastAPI, Traceback]
## @purpose Catch all unhandled exceptions and return a 500 JSON response with the exception message and full traceback.
## @io (Request, Exception) -> JSONResponse
## @complexity 3
@app.exception_handler(Exception)
async def any_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    logger.critical(f"[IMP:10][dedoc_api][UNHANDLED_ERROR] Exception: {exc}\n{traceback.format_exc()}")
    return JSONResponse(status_code=500, content={"message": f"Exception {exc}\n{traceback.format_exc()}"})
# endregion FUNC_any_exception_handler

# region FUNC_get_api [DOMAIN(4): AppConfiguration; CONCEPT(3): AppInstance; TECH(3): FastAPI]
## @purpose Return the configured FastAPI application instance for external launchers or testing.
## @io None -> FastAPI
## @complexity 1
def get_api() -> FastAPI:
    return app
# endregion FUNC_get_api

# region FUNC_run_api [DOMAIN(5): ServerLaunch; CONCEPT(4): UvicornStart; TECH(5): Uvicorn, ASGI]
## @purpose Launch the dedoc API server using uvicorn on the configured host (0.0.0.0) and port.
## @uses uvicorn.run
## @io (FastAPI) -> None
## @complexity 2
def run_api(app: FastAPI) -> None:
    import uvicorn
    logger.info(f"[IMP:9][dedoc_api][RUN_API] Starting uvicorn on 0.0.0.0:{int(PORT)}")
    uvicorn.run(app=app, host="0.0.0.0", port=int(PORT))
# endregion FUNC_run_api
