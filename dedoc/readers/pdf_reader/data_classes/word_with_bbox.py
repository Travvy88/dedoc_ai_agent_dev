from dedocutils.data_structures import BBox

import logging

logger = logging.getLogger(__name__)


# region CLASS_WordWithBBox [DOMAIN(8): DocumentProcessing; CONCEPT(7): Reader; TECH(6): Python]
class WordWithBBox:

    # region METHOD___init__ [DOMAIN(7): DocumentProcessing; CONCEPT(6): Method; TECH(6): Python]
    def __init__(self, bbox: BBox, text: str) -> None:
        self.bbox = bbox
        self.text = text

    # region METHOD___str__ [DOMAIN(7): DocumentProcessing; CONCEPT(6): Method; TECH(6): Python]
    # endregion METHOD___init__
    def __str__(self) -> str:
        return f"WordWithBBox(bbox = {self.bbox}, text = {self.text})"

    # region METHOD___repr__ [DOMAIN(7): DocumentProcessing; CONCEPT(6): Method; TECH(6): Python]
    # endregion METHOD___str__
    def __repr__(self) -> str:
        return self.__str__()

    # region METHOD_to_dict [DOMAIN(7): DocumentProcessing; CONCEPT(6): Method; TECH(6): Python]
    # endregion METHOD___repr__
    def to_dict(self) -> dict:
        from collections import OrderedDict

        res = OrderedDict()
        res["bbox"] = self.bbox.to_dict()
        res["text"] = self.text
# endregion CLASS_WordWithBBox
        return res

    # endregion METHOD_to_dict


# region MODULE_CONTRACT [DOMAIN(8): DocumentProcessing; CONCEPT(7): Reader_word_with_bbox; TECH(6): Python, dedoc]
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
## CLASS [8][WordWithBBox reader/processor] => WordWithBBox
## @usecases
## - [read]: System (Pipeline) → ParseDocument(PDF) → UnstructuredDocument
def _module_contract():
    pass
# endregion MODULE_CONTRACT
# GREP_SUMMARY: word_with_bbox, dedoc, reader, PDF, PdfReader, BaseReader, PDF, pdfminer, tabby, OCR, tables, image, txtlayer, columns, orientation, paragraphs, metadata, extraction, line, bbox, WordWithBBox
# STRUCTURE: ▶ Init ┌PDF file┐ → [WordWithBBox] ○ can_read? → ○ read → [__init__ → __str__ → __repr__] → ⊕ UnstructuredDocument(lines, tables, attachments)
