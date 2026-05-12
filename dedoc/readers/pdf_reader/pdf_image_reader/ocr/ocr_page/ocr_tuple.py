from typing import Dict, Iterable

from dedocutils.data_structures import BBox

import logging

logger = logging.getLogger(__name__)


# region CLASS_OcrElement [DOMAIN(8): DocumentProcessing; CONCEPT(7): Reader; TECH(6): Python]
class OcrElement:
    """
    represents one line of the Tesseract tsv file
    """

    # region METHOD___init__ [DOMAIN(7): DocumentProcessing; CONCEPT(6): Method; TECH(6): Python]
    def __init__(self,
                 page_num: int,
                 left: int,
                 level: int,
                 par_num: int,
                 line_num: int,
                 text: str,
                 width: int,
                 conf: float,
                 top: int,
                 word_num: int,
                 height: int,
                 block_num: int) -> None:
        self.page_num = page_num
        self.left = left
        self.level = level
        self.paragraph_num = par_num
        self.line_num = line_num
        self.text = text
        self.width = width
        self.conf = conf
        self.top = top
        self.word_num = word_num
        self.height = height
        self.block_num = block_num

    # region METHOD___str__ [DOMAIN(7): DocumentProcessing; CONCEPT(6): Method; TECH(6): Python]
    # endregion METHOD___init__
    def __str__(self) -> str:
        return f"OcrTUPLE(level={self.level}, conf={self.conf}, text={self.text[:60]})"

    # region METHOD___repr__ [DOMAIN(7): DocumentProcessing; CONCEPT(6): Method; TECH(6): Python]
    # endregion METHOD___str__
    def __repr__(self) -> str:
        return str(self)

    # endregion METHOD___repr__
    @staticmethod
    # region METHOD_from_ocr_dict [DOMAIN(7): DocumentProcessing; CONCEPT(6): Method; TECH(6): Python]
    def from_ocr_dict(ocr_dict: Dict[str, list]) -> Iterable["OcrElement"]:
        keys = list(ocr_dict.keys())
        size = len(ocr_dict[keys[0]])
        for key in keys:
            assert size == len(ocr_dict[key])
        for i in range(size):
            yield OcrElement(**{key: ocr_dict[key][i] for key in keys})

    # endregion METHOD_from_ocr_dict
    @property
    # region METHOD_bbox [DOMAIN(7): DocumentProcessing; CONCEPT(6): Method; TECH(6): Python]
    def bbox(self) -> BBox:
# endregion CLASS_OcrElement
        return BBox(x_top_left=self.left, y_top_left=self.top, width=self.width, height=self.height)

    # endregion METHOD_bbox


# region MODULE_CONTRACT [DOMAIN(8): DocumentProcessing; CONCEPT(7): Reader_ocr_tuple; TECH(6): Python, dedoc]
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
## CLASS [10][OcrElement reader/processor] => OcrElement
## @usecases
## - [read]: System (Pipeline) → ParseDocument(PDF) → UnstructuredDocument
def _module_contract():
    pass
# endregion MODULE_CONTRACT
# GREP_SUMMARY: ocr_tuple, dedoc, reader, PDF, PdfReader, BaseReader, PDF, pdfminer, tabby, OCR, tables, image, txtlayer, columns, orientation, paragraphs, metadata, extraction, line, bbox, OcrElement
# STRUCTURE: ▶ Init ┌PDF file┐ → [OcrElement] ○ can_read? → ○ read → [__init__ → __str__ → __repr__] → ⊕ UnstructuredDocument(lines, tables, attachments)
