# region MODULE_CONTRACT [DOMAIN(8): DocumentProcessing; CONCEPT(9): AttachmentExtraction; TECH(8): PDF, pypdf, Annotations]
## @modulecontract
## @purpose Extract attachments from PDF files: root-level embedded files (via /EmbeddedFiles catalog), page-level file annotations (/FileAttachment), and text annotations (/Text /Comment notes) as JSON attachments.
## @scope PDF attachment extraction: catalog traversal for embedded files, page-level annotation iteration, note conversion to JSON.
## @input File path to .pdf document; optional parameters dict.
## @output List of AttachedFile objects (embedded files, file-attached annotations, note JSONs).
## @links [USES_API(9): pypdf.PdfReader, pypdf.PageObject]
## @links [USES_API(8): AbstractAttachmentsExtractor._content2attach_file]
## @links [USES_API(7): dedoc.utils.parameter_utils.get_param_attachments_dir, get_param_need_content_analysis]
## @links [USES_API(6): dedoc.utils.utils.convert_datetime, dedoc.utils.utils.get_unique_name]
## @invariants
## - extract ALWAYS returns a List[AttachedFile] (may be empty).
## - PdfReadError during __get_root_attachments or __get_page_level_attachments is caught; extraction continues from remaining sources.
## - Notes (/Text + /Comment) are serialized as .json files with content, modified_time, created_time, size, author.
## @rationale
## Q: Why handle root and page-level attachments separately?
## A: PDF spec defines attachments at both levels; root-level for document-wide embedded files, page-level for per-page annotations. Both must be collected for completeness.
## Q: Why convert PDF notes to JSON attachments?
## A: PDF text annotations (/Text subtype /Comment) are human-readable notes. Converting to JSON makes them processable by downstream readers that can't parse raw PDF annotation objects.
## @changes
## LAST_CHANGE: [v1.0.0 – Semantic markup + LDD logging added]
## @modulemap
## CLASS 9[Extracts attachments from .pdf files] => PDFAttachmentsExtractor
## METHOD 5[Constructor: registers recognized pdf extensions/mimes] => __init__
## METHOD 9[Main extraction: root attachments + page-level + notes] => extract
## METHOD 7[Extracts annotations (/FileAttachment, /Text /Comment) from a page] => __get_notes
## METHOD 6[Iterates all pages to collect per-page annotations] => __get_page_level_attachments
## METHOD 8[Extracts root-level /EmbeddedFiles from catalog] => __get_root_attachments
## METHOD 6[Converts note metadata to (filename.json, bytes) tuple] => __create_note
## @usecases
## - [extract]: DedocManager => ExtractPdfAttachments => List[AttachedFile]
def _module_contract():
    pass
# endregion MODULE_CONTRACT
# GREP_SUMMARY: pdf, attachments, extractor, pypdf, PdfReader, annotations, /FileAttachment, /EmbeddedFiles, notes, /Text, /Comment, catalog, page
# STRUCTURE: ▶ Init ┌recognized pdf extensions/mimes┐ → ⚡ extract(file_path) → ○ pdf.open → ◇ __get_root_attachments(reader) → ⊕ root files → ◇ __get_page_level_attachments(reader) → ⊕ page annotations → ◇ _content2attach_file → ⎋ List[AttachedFile]; ◇ __get_root_attachments → ○ catalog["/Root"]["/Names"]["/EmbeddedFiles"]["/Names"] → ∀file: ⊕ (name, data) → ⎋; ◇ __get_page_level_attachments → ○ ∀page: __get_notes(page) → ⊕ → ⎋; ◇ __get_notes → ○ ∀annot: 〈/FileAttachment?→⊕｜/Text+/Comment?→__create_note→⊕〉 → ⎋

from typing import List, Optional, Tuple

from pypdf import PageObject, PdfReader

from dedoc.attachments_extractors.abstract_attachment_extractor import AbstractAttachmentsExtractor
from dedoc.data_structures.attached_file import AttachedFile

import logging

logger = logging.getLogger(__name__)


# region CLASS_PDFAttachmentsExtractor [DOMAIN(8): DocumentProcessing; CONCEPT(9): AttachmentExtraction; TECH(8): PDF, pypdf]
## @purpose Extract attachments from PDF files: root-level embedded files, page-level file annotations, and text annotation notes.
class PDFAttachmentsExtractor(AbstractAttachmentsExtractor):
    # region METHOD___init__ [DOMAIN(8): DocumentProcessing; CONCEPT(5): Initialization; TECH(4): PythonConfig]
    ## @purpose Initialize the PDF extractor with recognized pdf-like file extensions and MIME types.
    ## @uses dedoc.extensions.recognized_extensions, dedoc.extensions.recognized_mimes
    ## @io Optional[dict] -> None
    ## @complexity 2
    def __init__(self, *, config: Optional[dict] = None) -> None:
        from dedoc.extensions import recognized_extensions, recognized_mimes
        super().__init__(config=config, recognized_extensions=recognized_extensions.pdf_like_format, recognized_mimes=recognized_mimes.pdf_like_format)
        logger.debug(f"[IMP:4][PDFAttachmentsExtractor][INIT] Initialized with pdf-like format recognition")
    # endregion METHOD___init__

    # region METHOD_extract [DOMAIN(9): DocumentProcessing; CONCEPT(9): AttachmentExtraction; TECH(8): pypdf, PdfReader]
    ## @purpose Extract all attachments from a PDF: root-level embedded files, page-level file annotations, and text notes (as JSON).
    ## @uses __get_root_attachments, __get_page_level_attachments, AbstractAttachmentsExtractor._content2attach_file
    ## @io str, Optional[dict] -> List[AttachedFile]
    ## @complexity 7
    def extract(self, file_path: str, parameters: Optional[dict] = None) -> List[AttachedFile]:
        import os
        from dedoc.utils.parameter_utils import get_param_attachments_dir, get_param_need_content_analysis
        from pypdf.errors import PdfReadError

        parameters = {} if parameters is None else parameters
        filename = os.path.basename(file_path)

        logger.debug(f"[IMP:6][PDFAttachmentsExtractor][EXTRACT] Extracting from pdf: {filename}")

        with open(file_path, "rb") as handler:
            try:
                reader = PdfReader(handler)
            except Exception as e:
                self.logger.warning(f"can't handle {filename}, get {e}")
                logger.critical(f"[IMP:10][PDFAttachmentsExtractor][EXTRACT] Cannot open PDF {filename}: {e}")
                return []
            attachments = []
            try:
                root_attachments = self.__get_root_attachments(reader)
                attachments.extend(root_attachments)
                logger.info(f"[IMP:7][PDFAttachmentsExtractor][EXTRACT] Root attachments found: {len(root_attachments)}")
            except PdfReadError:
                self.logger.warning(f"{filename} is broken")
                logger.warning(f"[IMP:9][PDFAttachmentsExtractor][EXTRACT] PdfReadError during root attachment extraction for {filename}")
            try:
                page_attachments = self.__get_page_level_attachments(reader)
                attachments.extend(page_attachments)
                logger.info(f"[IMP:7][PDFAttachmentsExtractor][EXTRACT] Page-level attachments found: {len(page_attachments)}")
            except PdfReadError:
                self.logger.warning(f"{filename} is broken")
                logger.warning(f"[IMP:9][PDFAttachmentsExtractor][EXTRACT] PdfReadError during page-level attachment extraction for {filename}")

        need_content_analysis = get_param_need_content_analysis(parameters)
        attachments_dir = get_param_attachments_dir(parameters, file_path)
        logger.info(f"[IMP:9][PDFAttachmentsExtractor][EXTRACT] Total raw attachments from {filename}: {len(attachments)}")
        return self._content2attach_file(content=attachments, tmpdir=attachments_dir, need_content_analysis=need_content_analysis, parameters=parameters)
    # endregion METHOD_extract

    # region METHOD___get_notes [DOMAIN(7): PDFAnnotation; CONCEPT(8): AnnotationExtraction; TECH(7): pypdf, PageObject]
    ## @purpose Extract annotations from a single PDF page: /FileAttachment annotations and /Text /Comment notes.
    ## @uses dedoc.utils.utils.convert_datetime, __create_note
    ## @io PageObject -> List[Tuple[str, bytes]]
    ## @complexity 7
    def __get_notes(self, page: PageObject) -> List[Tuple[str, bytes]]:
        from dedoc.utils.utils import convert_datetime

        attachments = []
        if "/Annots" in page.keys():
            for annot in page["/Annots"]:
                # Other subtypes, such as /Link, cause errors
                subtype = annot.get_object().get("/Subtype")
                if subtype == "/FileAttachment":
                    name = annot.get_object()["/FS"]["/UF"]
                    data = annot.get_object()["/FS"]["/EF"]["/F"].get_data()  # The file containing the stream data.
                    attachments.append([name, data])
                    logger.debug(f"[IMP:5][PDFAttachmentsExtractor][GET_NOTES] FileAttachment: {name}")
                if subtype == "/Text" and annot.get_object().get("/Name") == "/Comment":  # it is messages (notes) in PDF
                    note = annot.get_object()
                    created_time = convert_datetime(note["/CreationDate"]) if "/CreationDate" in note else None
                    modified_time = convert_datetime(note["/M"]) if "/M" in note else None
                    user = note.get("/T")
                    data = note.get("/Contents", "")

                    name, content = self.__create_note(content=data, modified_time=modified_time, created_time=created_time, author=user)
                    attachments.append((name, bytes(content)))
                    logger.debug(f"[IMP:5][PDFAttachmentsExtractor][GET_NOTES] Note/Comment: {name}")
        return attachments
    # endregion METHOD___get_notes

    # region METHOD___get_page_level_attachments [DOMAIN(7): PDFAnnotation; CONCEPT(7): PageIteration; TECH(6): pypdf]
    ## @purpose Iterate over all pages in the PDF reader and collect attachments from each page.
    ## @uses __get_notes
    ## @io PdfReader -> List[Tuple[str, bytes]]
    ## @complexity 3
    def __get_page_level_attachments(self, reader: PdfReader) -> List[Tuple[str, bytes]]:
        attachments = []
        for i, page in enumerate(reader.pages):
            attachments_on_page = self.__get_notes(page)
            attachments.extend(attachments_on_page)
            logger.debug(f"[IMP:3][PDFAttachmentsExtractor][PAGE_ATTACH] Page {i}: {len(attachments_on_page)} attachments")
        return attachments
    # endregion METHOD___get_page_level_attachments

    # region METHOD___get_root_attachments [DOMAIN(8): PDFStructure; CONCEPT(8): CatalogTraversal; TECH(7): pypdf, PDFCatalog]
    ## @purpose Extract root-level embedded files from the PDF catalog's /Names → /EmbeddedFiles dictionary.
    ## @io PdfReader -> List[Tuple[str, bytes]]
    ## @complexity 6
    def __get_root_attachments(self, reader: PdfReader) -> List[Tuple[str, bytes]]:
        import uuid

        attachments = []
        catalog = reader.trailer["/Root"]
        if "/Names" in catalog.keys() and "/EmbeddedFiles" in catalog["/Names"].keys() and "/Names" in catalog["/Names"]["/EmbeddedFiles"].keys():
            file_names = catalog["/Names"]["/EmbeddedFiles"]["/Names"]
            logger.debug(f"[IMP:7][PDFAttachmentsExtractor][ROOT_ATTACH] Found {len(file_names)} entries in /EmbeddedFiles")
            for f in file_names:
                if isinstance(f, str):
                    data_index = file_names.index(f) + 1
                    dict_object = file_names[data_index].get_object()
                    if "/EF" in dict_object and "/F" in dict_object["/EF"]:
                        data = dict_object["/EF"]["/F"].get_data()
                        name = dict_object.get("/UF", f"pdf_attach_{uuid.uuid4()}")
                        attachments.append((name, data))
                        logger.debug(f"[IMP:5][PDFAttachmentsExtractor][ROOT_ATTACH] Embedded file: {name}")
        return attachments
    # endregion METHOD___get_root_attachments

    # region METHOD___create_note [DOMAIN(7): DataSerialization; CONCEPT(7): NoteSerialization; TECH(5): json]
    ## @purpose Serialize a PDF text note into a JSON file with metadata (content, timestamps, author, size).
    ## @uses dedoc.utils.utils.get_unique_name, json.dumps
    ## @io str, int, int, str, Optional[int] -> Tuple[str, bytes]
    ## @complexity 4
    def __create_note(self, content: str, modified_time: int, created_time: int, author: str, size: int = None) -> [str, bytes]:
        import json
        from dedoc.utils.utils import get_unique_name

        filename = get_unique_name("note.json")
        note_dict = {
            "content": content,
            "modified_time": modified_time,
            "created_time": created_time,
            "size": size if size else len(content),
            "author": author
        }
        encode_data = json.dumps(note_dict).encode("utf-8")
        logger.debug(f"[IMP:5][PDFAttachmentsExtractor][CREATE_NOTE] Created note: {filename}")
        return filename, encode_data
    # endregion METHOD___create_note
# endregion CLASS_PDFAttachmentsExtractor
