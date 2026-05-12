# region MODULE_CONTRACT [DOMAIN(8): DocumentProcessing; CONCEPT(9): AttachmentHandling; TECH(7): Orchestration, DedocManager]
## @modulecontract
## @purpose Orchestrate the handling of document attachments: iterate over UnstructuredDocument attachments, optionally parse them via DedocManager (recursion with depth limit), and collect parsed results with metadata.
## @scope Attachment handling orchestration: recursion depth control, per-attachment parsing or metadata-only extraction, error resilience (DedocError → empty document), metadata enrichment.
## @input UnstructuredDocument (with attachments), DedocManager (document parser), parameters dict.
## @output List of ParsedDocument objects (one per attachment, with metadata).
## @links [USES_API(10): DedocManager.parse, DedocManager.document_metadata_extractor]
## @links [USES_API(9): ParsedDocument, UnstructuredDocument, AttachedFile, DocumentMetadata]
## @links [USES_API(7): dedoc.utils.parameter_utils.get_param_with_attachments]
## @links [USES_API(6): dedoc.utils.utils.get_empty_content]
## @links [USES_API(5): DedocError]
## @invariants
## - handle_attachments ALWAYS returns List[ParsedDocument] (may be empty).
## - Recursion depth (recursion_deep_attachments) is decremented per level; stops at 0.
## - If with_attachments is false or recursion depth exhausted, returns empty list.
## - DedocError on a single attachment is caught; the attachment is replaced with an empty ParsedDocument containing metadata.
## - Logging of attachment processing is rate-limited to at most one message per 3 seconds.
## @rationale
## Q: Why catch DedocError and return empty ParsedDocument instead of propagating?
## A: One broken attachment should not prevent processing of other attachments. Returning an empty document with metadata preserves the attachment's identity (filename, uid) for downstream consumers.
## Q: Why rate-limit attachment processing logs?
## A: Documents can have hundreds of attachments; logging each one individually floods the log. A 3-second throttle keeps the log informative without spamming.
## @changes
## LAST_CHANGE: [v1.0.0 – Semantic markup + LDD logging added]
## @modulemap
## CLASS 10[Orchestrates attachment processing with recursion + error resilience] => AttachmentsHandler
## METHOD 5[Constructor: stores config and logger] => __init__
## METHOD 9[Main handler: iterates attachments, parses or metadata-only] => handle_attachments
## METHOD 6[Creates an empty ParsedDocument with metadata for failed attachments] => __get_empty_document
## @usecases
## - [handle_attachments]: DedocManager => HandleDocumentAttachments => List[ParsedDocument]
def _module_contract():
    pass
# endregion MODULE_CONTRACT
# GREP_SUMMARY: attachments, handler, orchestration, recursion, depth, DedocManager, parse, metadata, error_resilience, DedocError, rate_limit
# STRUCTURE: ▶ Init ┌config, logger┐ → ⚡ handle_attachments(document_parser, document, params) → ◇ with_attachments?recursion_deep≥0? → ○ ∀attachment: ○ rate_limited_log → ○ need_content_analysis? → ◇ document_parser.parse or __get_empty_document → ⊕ metadata enrichment → ∑ ↔ catch DedocError→__get_empty_document → ⎋ List[ParsedDocument]

from typing import List, Optional

from dedoc.common.exceptions.dedoc_error import DedocError
from dedoc.data_structures.attached_file import AttachedFile
from dedoc.data_structures.document_metadata import DocumentMetadata
from dedoc.data_structures.parsed_document import ParsedDocument
from dedoc.data_structures.unstructured_document import UnstructuredDocument
from dedoc.dedoc_manager import DedocManager

import logging

logger = logging.getLogger(__name__)


# region CLASS_AttachmentsHandler [DOMAIN(8): DocumentProcessing; CONCEPT(9): AttachmentHandling; TECH(7): Orchestration]
## @purpose Orchestrate the complete attachment handling lifecycle: iterate attachments, control recursion depth, parse or extract metadata, and handle errors gracefully.
class AttachmentsHandler:
    # region METHOD___init__ [DOMAIN(8): DocumentProcessing; CONCEPT(5): Initialization; TECH(4): PythonConfig]
    ## @purpose Initialize the attachment handler with configuration and a logger.
    ## @io Optional[dict] -> None
    ## @complexity 3
    def __init__(self, *, config: Optional[dict] = None) -> None:
        self.config = {} if config is None else config
        self.logger = self.config.get("logger", logging.getLogger())
        logger.debug(f"[IMP:4][AttachmentsHandler][INIT] Initialized")
    # endregion METHOD___init__

    # region METHOD_handle_attachments [DOMAIN(9): DocumentProcessing; CONCEPT(9): AttachmentHandling; TECH(8): Recursion, Orchestration]
    ## @purpose Process all attachments of an UnstructuredDocument: parse each (with recursion depth control) or extract metadata only, with error resilience.
    ## @uses DedocManager.parse, DedocManager.document_metadata_extractor, __get_empty_document
    ## @io DedocManager, UnstructuredDocument, dict -> List[ParsedDocument]
    ## @complexity 8
    def handle_attachments(self, document_parser: DedocManager, document: UnstructuredDocument, parameters: dict) -> List[ParsedDocument]:
        import copy
        import os
        import time
        from dedoc.utils.parameter_utils import get_param_with_attachments

        attachments = []
        recursion_deep_attachments = int(parameters.get("recursion_deep_attachments", 10)) - 1

        if not get_param_with_attachments(parameters) or recursion_deep_attachments < 0:
            logger.debug(f"[IMP:6][AttachmentsHandler][HANDLE] Skipping: with_attachments=false or recursion_deep={recursion_deep_attachments + 1}")
            return attachments

        logger.info(f"[IMP:7][AttachmentsHandler][HANDLE] Processing {len(document.attachments)} attachments, recursion_deep={recursion_deep_attachments + 1}")

        previous_log_time = time.time()

        for i, attachment in enumerate(document.attachments):
            current_time = time.time()
            if current_time - previous_log_time > 3:
                previous_log_time = current_time  # not log too often
                self.logger.info(f"Handle attachment {i} of {len(document.attachments)}")
                logger.debug(f"[IMP:5][AttachmentsHandler][HANDLE] Progress: {i}/{len(document.attachments)}")

            if not attachment.get_original_filename():  # TODO check for docx https://jira.ispras.ru/browse/TLDR-185
                logger.debug(f"[IMP:4][AttachmentsHandler][HANDLE] Skipping attachment {i}: no original filename")
                continue

            parameters_copy = copy.deepcopy(parameters)
            parameters_copy["is_attached"] = True
            parameters_copy["recursion_deep_attachments"] = str(recursion_deep_attachments)

            try:
                if attachment.need_content_analysis:
                    parsed_file = document_parser.parse(attachment.get_filename_in_path(), parameters=parameters_copy)
                    logger.debug(f"[IMP:5][AttachmentsHandler][HANDLE] Parsed attachment: {attachment.original_name}")
                else:
                    parsed_file = self.__get_empty_document(document_parser=document_parser, attachment=attachment, parameters=parameters_copy)
                    logger.debug(f"[IMP:5][AttachmentsHandler][HANDLE] Metadata-only for attachment: {attachment.original_name}")

                parsed_file.metadata.file_name = attachment.original_name  # initial name of the attachment
                parsed_file.metadata.temporary_file_name = os.path.split(attachment.get_filename_in_path())[-1]  # actual name in the file system
            except DedocError:
                # return empty ParsedDocument with Meta information
                parsed_file = self.__get_empty_document(document_parser=document_parser, attachment=attachment, parameters=parameters_copy)
                logger.warning(f"[IMP:9][AttachmentsHandler][HANDLE] DedocError for attachment {attachment.original_name}, returning empty document")

            parsed_file.metadata.uid = attachment.uid
            attachments.append(parsed_file)

        logger.info(f"[IMP:9][AttachmentsHandler][HANDLE] Finished processing. Total parsed attachments: {len(attachments)}")
        return attachments
    # endregion METHOD_handle_attachments

    # region METHOD___get_empty_document [DOMAIN(7): DocumentProcessing; CONCEPT(7): FallbackHandling; TECH(6): MetadataExtraction]
    ## @purpose Create an empty ParsedDocument with extracted metadata as a fallback when attachment parsing fails or is disabled.
    ## @uses DedocManager.document_metadata_extractor, dedoc.utils.utils.get_empty_content, DocumentMetadata
    ## @io DedocManager, AttachedFile, dict -> ParsedDocument
    ## @complexity 4
    def __get_empty_document(self, document_parser: DedocManager, attachment: AttachedFile, parameters: dict) -> ParsedDocument:
        from dedoc.utils.utils import get_empty_content
        metadata = document_parser.document_metadata_extractor.extract(
            file_path=attachment.get_filename_in_path(),
            original_filename=attachment.get_original_filename(),
            parameters=parameters
        )
        metadata = DocumentMetadata(**metadata)
        logger.debug(f"[IMP:5][AttachmentsHandler][GET_EMPTY] Created empty document for {attachment.original_name}")
        return ParsedDocument(content=get_empty_content(), metadata=metadata)
    # endregion METHOD___get_empty_document
# endregion CLASS_AttachmentsHandler
