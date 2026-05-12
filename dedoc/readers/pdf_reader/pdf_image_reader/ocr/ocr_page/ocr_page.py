from collections import defaultdict
from typing import Dict, Iterable, List

import logging

logger = logging.getLogger(__name__)

from dedoc.readers.pdf_reader.pdf_image_reader.ocr.ocr_page.ocr_block import OcrBlock
from dedoc.readers.pdf_reader.pdf_image_reader.ocr.ocr_page.ocr_line import OcrLine
from dedoc.readers.pdf_reader.pdf_image_reader.ocr.ocr_page.ocr_paragraph import OcrParagraph
from dedoc.readers.pdf_reader.pdf_image_reader.ocr.ocr_page.ocr_tuple import OcrElement


# region CLASS_OcrPage [DOMAIN(8): DocumentProcessing; CONCEPT(7): Reader; TECH(6): Python]
class OcrPage:
    """
    Represents OCR results from the Tesseract. You may see the description in
    https://www.tomrochette.com/tesseract-tsv-format

    Output of the Tesseract has a hierarchical structure:
    Pages (level 1) are divided on Blocks (level 2),
    Blocks are divided on Paragraph (level 3),
    Paragraphs are divided on Lines (level 4)
    Lines are divided on Words (level 5)
    Originally only words have text content, but we will extract text from the lower level

    _______________________________________________________________________________________
    |                                                                                      |
    |   _______________________________________                                            |
    |  |  __________________________________   |                                           |
    |  |  |  line level 4                  |   |                                           |
    |  |  | consists of words level 5      |   |                                           |
    |  |  ---------------------------------    |                                           |
    |  |   paragraph (level 3)                 |                                           |
    |  |                                       |                                           |
    |  |                                       |                                           |
    |  |                                       |                                           |
    |  |                                       |                                           |
    |  |                                       |                                           |
    |  -----------------------------------------                                           |
    |  block (level 2)                                                                     |
    |                                                                                      |
    |                                                                                      |
    |                                                                                      |
    |                                                                                      |
    |                                                                                      |
    |                                                                                      |
    |                                                                                      |
    |                                                                                      |
    |                                                                                      |
    |                                                                                      |
    ----------------------------------------------------------------------------------------
    Page (level 1)
    """

    level = 1

    # region METHOD___init__ [DOMAIN(7): DocumentProcessing; CONCEPT(6): Method; TECH(6): Python]
    def __init__(self, blocks: List[OcrBlock]) -> None:
        self.blocks = sorted(blocks, key=lambda block: block.order)

    # endregion METHOD___init__
    @property
    # region METHOD_text [DOMAIN(7): DocumentProcessing; CONCEPT(6): Method; TECH(6): Python]
    def text(self) -> str:
        return "\n".join(blocks.text for blocks in self.blocks)

    # endregion METHOD_text
    @staticmethod
    # region METHOD_from_dict [DOMAIN(7): DocumentProcessing; CONCEPT(6): Method; TECH(6): Python]
    def from_dict(ocr_dict: Dict[str, List], ocr_conf_thr: float) -> "OcrPage":
        tuples = OcrElement.from_ocr_dict(ocr_dict)
        block2elements = defaultdict(list)
        for element in tuples:
            if element.level > OcrPage.level:
                block2elements[element.block_num].append(element)
        blocks = []
        for key in sorted(block2elements.keys()):
            elements = block2elements[key]
            blocks.append(OcrBlock.from_list(elements, ocr_conf_thr))
        return OcrPage(blocks=blocks)

    # endregion METHOD_from_dict
    @property
    # region METHOD_paragraphs [DOMAIN(7): DocumentProcessing; CONCEPT(6): Method; TECH(6): Python]
    def paragraphs(self) -> Iterable[OcrParagraph]:
        for block in self.blocks:
            for paragraph in block.paragraphs:
                yield paragraph

    # endregion METHOD_paragraphs
    @property
    # region METHOD_lines [DOMAIN(7): DocumentProcessing; CONCEPT(6): Method; TECH(6): Python]
    def lines(self) -> Iterable[OcrLine]:
        for paragraph in self.paragraphs:
            for line in paragraph.lines:
# endregion CLASS_OcrPage
                yield line

    # endregion METHOD_lines


# region MODULE_CONTRACT [DOMAIN(8): DocumentProcessing; CONCEPT(7): Reader_ocr_page; TECH(6): Python, dedoc]
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
## CLASS [10][OcrPage reader/processor] => OcrPage
## @usecases
## - [read]: System (Pipeline) → ParseDocument(PDF) → UnstructuredDocument
def _module_contract():
    pass
# endregion MODULE_CONTRACT
# GREP_SUMMARY: ocr_page, dedoc, reader, PDF, PdfReader, BaseReader, PDF, pdfminer, tabby, OCR, tables, image, txtlayer, columns, orientation, paragraphs, metadata, extraction, line, bbox, OcrPage
# STRUCTURE: ▶ Init ┌PDF file┐ → [OcrPage] ○ can_read? → ○ read → [__init__ → text → from_dict] → ⊕ UnstructuredDocument(lines, tables, attachments)
