# region MODULE_CONTRACT [DOMAIN(8): DocumentProcessing; CONCEPT(8): AttachmentExtraction; TECH(7): xlsx, OpenXML]
## @modulecontract
## @purpose Extract embedded attachments (images, charts, OLE objects) from Excel (.xlsx) files via ZIP+OLE introspection.
## @scope xlsx file attachment extraction: reads zip archive, locates media/embeddings in xl/ folder, parses OLE streams.
## @input File path to .xlsx document; optional parameters dict (with_attachments, need_content_analysis, attachments_dir).
## @output List of AttachedFile objects extracted from the xlsx archive.
## @links [USES_API(9): AbstractOfficeAttachmentsExtractor._get_attachments]
## @links [USES_API(8): recognized_extensions.excel_like_format, recognized_mimes.excel_like_format]
## @invariants
## - extract ALWAYS returns a List[AttachedFile] (may be empty).
## - Parameters dict defaults to {} if None is passed.
## @rationale
## Q: Why delegate to _get_attachments with attachments_dir="xl"?
## A: xlsx is an OpenXML format; the media folder resides under xl/ in the zip. The base class handles the zip iteration and OLE parsing generically.
## @changes
## LAST_CHANGE: [v1.0.0 – Semantic markup + LDD logging added]
## @modulemap
## CLASS 8[Extracts attachments from .xlsx files] => ExcelAttachmentsExtractor
## METHOD 5[Constructor: registers recognized excel extensions/mimes] => __init__
## METHOD 8[Main extraction entry point for xlsx] => extract
## @usecases
## - [extract]: DedocManager => ExtractXlsxAttachments => List[AttachedFile]
def _module_contract():
    pass
# endregion MODULE_CONTRACT
# GREP_SUMMARY: xlsx, excel, attachments, extractor, OpenXML, zip, ole, media, embeddings
# STRUCTURE: ▶ Init ┌recognized excel extensions/mimes┐ → ⚡ extract(file_path) → ○ split path → ◇ _get_attachments(attachments_dir="xl") → ⊕ List[AttachedFile] → ⎋

from typing import List, Optional

from dedoc.attachments_extractors.concrete_attachments_extractors.abstract_office_attachments_extractor import AbstractOfficeAttachmentsExtractor
from dedoc.data_structures.attached_file import AttachedFile

import logging

logger = logging.getLogger(__name__)


# region CLASS_ExcelAttachmentsExtractor [DOMAIN(8): DocumentProcessing; CONCEPT(8): AttachmentExtraction; TECH(7): xlsx, OpenXML]
## @purpose Extract embedded files (images, OLE objects, charts) from Excel .xlsx archives.
class ExcelAttachmentsExtractor(AbstractOfficeAttachmentsExtractor):
    # region METHOD___init__ [DOMAIN(8): DocumentProcessing; CONCEPT(5): Initialization; TECH(4): PythonConfig]
    ## @purpose Initialize the xlsx extractor with recognized excel-like file extensions and MIME types.
    ## @uses dedoc.extensions.recognized_extensions, dedoc.extensions.recognized_mimes
    ## @io Optional[dict] -> None
    ## @complexity 2
    def __init__(self, *, config: Optional[dict] = None) -> None:
        from dedoc.extensions import recognized_extensions, recognized_mimes
        super().__init__(config=config, recognized_extensions=recognized_extensions.excel_like_format, recognized_mimes=recognized_mimes.excel_like_format)
        logger.debug(f"[IMP:4][ExcelAttachmentsExtractor][INIT] Initialized with excel-like format recognition")
    # endregion METHOD___init__

    # region METHOD_extract [DOMAIN(8): DocumentProcessing; CONCEPT(8): AttachmentExtraction; TECH(7): xlsx, zipfile]
    ## @purpose Extract all attachments from the given .xlsx file by delegating to the generic Office-format extraction with attachments_dir="xl".
    ## @uses AbstractOfficeAttachmentsExtractor._get_attachments
    ## @io str, Optional[dict] -> List[AttachedFile]
    ## @complexity 3
    def extract(self, file_path: str, parameters: Optional[dict] = None) -> List[AttachedFile]:
        import os

        parameters = {} if parameters is None else parameters
        tmpdir, filename = os.path.split(file_path)
        logger.debug(f"[IMP:4][ExcelAttachmentsExtractor][EXTRACT] Extracting from xlsx: {filename}")
        result = self._get_attachments(tmpdir=tmpdir, filename=filename, parameters=parameters, attachments_dir="xl")
        logger.info(f"[IMP:9][ExcelAttachmentsExtractor][EXTRACT] Extracted {len(result)} attachments from xlsx: {filename}")
        return result
    # endregion METHOD_extract
# endregion CLASS_ExcelAttachmentsExtractor
