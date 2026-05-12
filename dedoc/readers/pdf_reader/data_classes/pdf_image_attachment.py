from dedoc.data_structures.attached_file import AttachedFile
from dedoc.readers.pdf_reader.data_classes.tables.location import Location

import logging

logger = logging.getLogger(__name__)


# region CLASS_PdfImageAttachment [DOMAIN(8): DocumentProcessing; CONCEPT(7): Reader; TECH(6): Python]
class PdfImageAttachment(AttachedFile):

    # region METHOD___init__ [DOMAIN(7): DocumentProcessing; CONCEPT(6): Method; TECH(6): Python]
    def __init__(self, original_name: str, tmp_file_path: str, need_content_analysis: bool, uid: str, location: Location, order: int = -1) -> None:
        self.location = location
        self.order = order
# endregion CLASS_PdfImageAttachment
        super().__init__(original_name=original_name, tmp_file_path=tmp_file_path, need_content_analysis=need_content_analysis, uid=uid)

    # endregion METHOD___init__


# region MODULE_CONTRACT [DOMAIN(8): DocumentProcessing; CONCEPT(7): Reader_pdf_image_attachment; TECH(6): Python, dedoc]
## @modulecontract
## @purpose Read and parse PDF documents, extracting lines with metadata, tables, and attachments into UnstructuredDocument.
## @scope Data model definitions.
## @input [File path (str), parameters (Optional[dict]) — document on disk.]
## @output [UnstructuredDocument with lines, tables, attachments, and warnings.]
## @links [USES_API(9): dedoc.data_structures.*; USES_API(8): dedoc.readers.BaseReader]
## @invariants
## - read() ALWAYS returns an UnstructuredDocument.
## @rationale
## Q: Why is this reader separated from others?
## A: Each reader handles one format family — isolation prevents format coupling and simplifies extension.
## @changes
## LAST_CHANGE: [v1.0.0 – Added SEMANTIC TEMPLATE markup and LDD logging.]
## @modulemap
## CLASS [2][PdfImageAttachment reader/processor] => PdfImageAttachment
## @usecases
## - [read]: System (Pipeline) → ParseDocument(PDF) → UnstructuredDocument
def _module_contract():
    pass
# endregion MODULE_CONTRACT
# GREP_SUMMARY: pdf_image_attachment, dedoc, reader, PDF, PdfReader, BaseReader, PDF, pdfminer, tabby, OCR, tables, image, txtlayer, columns, orientation, paragraphs, metadata, extraction, line, bbox, PdfImageAttachment
# STRUCTURE: ▶ Init ┌PDF file┐ → [PdfImageAttachment] ○ can_read? → ○ read → [__init__] → ⊕ UnstructuredDocument(lines, tables, attachments)
