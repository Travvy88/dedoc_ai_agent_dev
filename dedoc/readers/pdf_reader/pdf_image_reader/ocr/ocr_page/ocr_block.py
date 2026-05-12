from collections import defaultdict
from typing import List

import logging

logger = logging.getLogger(__name__)

from dedocutils.data_structures import BBox

from dedoc.readers.pdf_reader.pdf_image_reader.ocr.ocr_page.ocr_paragraph import OcrParagraph
from dedoc.readers.pdf_reader.pdf_image_reader.ocr.ocr_page.ocr_tuple import OcrElement


# region CLASS_OcrBlock [DOMAIN(8): DocumentProcessing; CONCEPT(7): Reader; TECH(6): Python]
class OcrBlock:
    level = 2

    # region METHOD___init__ [DOMAIN(7): DocumentProcessing; CONCEPT(6): Method; TECH(6): Python]
    def __init__(self, order: int, bbox: BBox, paragraphs: List[OcrParagraph]) -> None:
        super().__init__()
        self.order = order
        self.bbox = bbox
        self.paragraphs = paragraphs

    # endregion METHOD___init__
    @property
    # region METHOD_text [DOMAIN(7): DocumentProcessing; CONCEPT(6): Method; TECH(6): Python]
    def text(self) -> str:
        return "".join(paragraph.text for paragraph in self.paragraphs)

    # endregion METHOD_text
    @staticmethod
    # region METHOD_from_list [DOMAIN(7): DocumentProcessing; CONCEPT(6): Method; TECH(6): Python]
    def from_list(elements: List[OcrElement], ocr_conf_thr: float) -> "OcrBlock":
        paragraph2elements = defaultdict(list)
        head = None
        for element in elements:
            if element.level > OcrBlock.level:
                paragraph2elements[element.paragraph_num].append(element)
            elif element.level == OcrBlock.level:
                head = element
            else:
                raise ValueError(f"Some element {element} has level greater than this {OcrBlock.level}")
        paragraphs = [OcrParagraph.from_list(paragraph2elements[key], ocr_conf_thr) for key in sorted(paragraph2elements.keys())]
# endregion CLASS_OcrBlock
        return OcrBlock(paragraphs=paragraphs, order=head.block_num, bbox=head.bbox)

    # endregion METHOD_from_list


# region MODULE_CONTRACT [DOMAIN(8): DocumentProcessing; CONCEPT(7): Reader_ocr_block; TECH(6): Python, dedoc]
## @modulecontract
## @purpose Read and parse PDF documents, extracting lines with metadata, tables, and attachments into UnstructuredDocument.
## @scope OCR processing pipeline for document images.
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
## CLASS [6][OcrBlock reader/processor] => OcrBlock
## @usecases
## - [read]: System (Pipeline) → ParseDocument(PDF) → UnstructuredDocument
def _module_contract():
    pass
# endregion MODULE_CONTRACT
# GREP_SUMMARY: ocr_block, dedoc, reader, PDF, PdfReader, BaseReader, PDF, pdfminer, tabby, OCR, tables, image, txtlayer, columns, orientation, paragraphs, metadata, extraction, line, bbox, OcrBlock
# STRUCTURE: ▶ Init ┌PDF file┐ → [OcrBlock] ○ can_read? → ○ read → [__init__ → text → from_list] → ⊕ UnstructuredDocument(lines, tables, attachments)
