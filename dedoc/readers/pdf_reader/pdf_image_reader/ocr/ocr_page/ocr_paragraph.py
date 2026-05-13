from collections import defaultdict
from typing import List

import logging

logger = logging.getLogger(__name__)

from dedocutils.data_structures import BBox

from dedoc.readers.pdf_reader.pdf_image_reader.ocr.ocr_page.ocr_line import OcrLine
from dedoc.readers.pdf_reader.pdf_image_reader.ocr.ocr_page.ocr_tuple import OcrElement


# region CLASS_OcrParagraph [DOMAIN(8): DocumentProcessing; CONCEPT(7): Reader; TECH(6): Python]
class OcrParagraph:

    level = 3

    # region METHOD___init__ [DOMAIN(7): DocumentProcessing; CONCEPT(6): Method; TECH(6): Python]
    def __init__(self, order: int, bbox: BBox, lines: List[OcrLine]) -> None:
        super().__init__()
        self.order = order
        self.bbox = bbox
        self.lines = sorted(lines, key=lambda line: line.order)

    # endregion METHOD___init__
    @property
    # region METHOD_text [DOMAIN(7): DocumentProcessing; CONCEPT(6): Method; TECH(6): Python]
    def text(self) -> str:
        return "\n".join(line.text for line in self.lines)

    # endregion METHOD_text
    @staticmethod
    # region METHOD_from_list [DOMAIN(7): DocumentProcessing; CONCEPT(6): Method; TECH(6): Python]
    def from_list(paragraph: List[OcrElement], ocr_conf_thr: float) -> "OcrParagraph":
        line2element = defaultdict(list)
        head = None
        for element in paragraph:
            if element.level > OcrParagraph.level:
                line2element[element.line_num].append(element)
            else:
                head = element

        lines = [OcrLine.from_list(line=line2element[key], ocr_conf_thr=ocr_conf_thr) for key in sorted(line2element.keys())]
# endregion CLASS_OcrParagraph
        return OcrParagraph(order=head.paragraph_num, lines=lines, bbox=head.bbox)

    # endregion METHOD_from_list


# region MODULE_CONTRACT [DOMAIN(8): DocumentProcessing; CONCEPT(7): Reader_ocr_paragraph; TECH(6): Python, dedoc]
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
## CLASS [6][OcrParagraph reader/processor] => OcrParagraph
## @usecases
## - [read]: System (Pipeline) → ParseDocument(PDF) → UnstructuredDocument
def _module_contract():
    pass
# endregion MODULE_CONTRACT
# GREP_SUMMARY: ocr_paragraph, dedoc, reader, PDF, PdfReader, BaseReader, PDF, pdfminer, tabby, OCR, tables, image, txtlayer, columns, orientation, paragraphs, metadata, extraction, line, bbox, OcrParagraph
# STRUCTURE: ▶ Init ┌PDF file┐ → [OcrParagraph] ○ can_read? → ○ read → [__init__ → text → from_list] → ⊕ UnstructuredDocument(lines, tables, attachments)
