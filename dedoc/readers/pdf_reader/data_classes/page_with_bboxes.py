from typing import List, Optional

from numpy import ndarray

import logging

logger = logging.getLogger(__name__)

from dedoc.readers.pdf_reader.data_classes.pdf_image_attachment import PdfImageAttachment
from dedoc.readers.pdf_reader.data_classes.text_with_bbox import TextWithBBox


# region CLASS_PageWithBBox [DOMAIN(8): DocumentProcessing; CONCEPT(7): Reader; TECH(6): Python]
class PageWithBBox:

    # region METHOD___init__ [DOMAIN(7): DocumentProcessing; CONCEPT(6): Method; TECH(6): Python]
    def __init__(self, image: Optional[ndarray], bboxes: List[TextWithBBox], page_num: int, attachments: List[PdfImageAttachment] = None,
                 pdf_page_width: Optional[int] = None, pdf_page_height: Optional[int] = None) -> None:
        self.image = image
        self.bboxes = bboxes
        self.page_num = page_num
        self.attachments = [] if attachments is None else attachments
        self.pdf_page_width = pdf_page_width
# endregion CLASS_PageWithBBox
        self.pdf_page_height = pdf_page_height

    # endregion METHOD___init__


# region MODULE_CONTRACT [DOMAIN(8): DocumentProcessing; CONCEPT(7): Reader_page_with_bboxes; TECH(6): Python, dedoc]
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
## CLASS [2][PageWithBBox reader/processor] => PageWithBBox
## @usecases
## - [read]: System (Pipeline) → ParseDocument(PDF) → UnstructuredDocument
def _module_contract():
    pass
# endregion MODULE_CONTRACT
# GREP_SUMMARY: page_with_bboxes, dedoc, reader, PDF, PdfReader, BaseReader, PDF, pdfminer, tabby, OCR, tables, image, txtlayer, columns, orientation, paragraphs, metadata, extraction, line, bbox, PageWithBBox
# STRUCTURE: ▶ Init ┌PDF file┐ → [PageWithBBox] ○ can_read? → ○ read → [__init__] → ⊕ UnstructuredDocument(lines, tables, attachments)
