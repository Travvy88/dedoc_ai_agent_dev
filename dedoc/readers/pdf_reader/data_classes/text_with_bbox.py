from typing import List, Optional

from dedocutils.data_structures import BBox

import logging

logger = logging.getLogger(__name__)

from dedoc.data_structures.annotation import Annotation
from dedoc.readers.pdf_reader.data_classes.word_with_bbox import WordWithBBox


# region CLASS_TextWithBBox [DOMAIN(8): DocumentProcessing; CONCEPT(7): Reader; TECH(6): Python]
class TextWithBBox:

    # region METHOD___init__ [DOMAIN(7): DocumentProcessing; CONCEPT(6): Method; TECH(6): Python]
    def __init__(self,
                 bbox: BBox,
                 page_num: int,
                 line_num: int,
                 words: List[WordWithBBox],
                 uid: Optional[str] = None,
                 label: Optional[str] = None,
                 annotations: List[Annotation] = None) -> None:
        from uuid import uuid1

        self.bbox = bbox
        self.page_num = page_num
        self.line_num = line_num
        self.words = words
        self.label = label
        self.annotations = [] if annotations is None else annotations
        self.uid = f"bbox_{uuid1()}" if uid is None else uid

    # endregion METHOD___init__
    @property
    # region METHOD_text [DOMAIN(7): DocumentProcessing; CONCEPT(6): Method; TECH(6): Python]
    def text(self) -> str:
        return " ".join(word.text for word in self.words if word.text != "") + "\n"

    # region METHOD___str__ [DOMAIN(7): DocumentProcessing; CONCEPT(6): Method; TECH(6): Python]
    # endregion METHOD_text
    def __str__(self) -> str:
        return f"TextWithBBox(bbox = {self.bbox}, page = {self.page_num}, text = {self.text})"

    # region METHOD___repr__ [DOMAIN(7): DocumentProcessing; CONCEPT(6): Method; TECH(6): Python]
    # endregion METHOD___str__
    def __repr__(self) -> str:
        return self.__str__()

    # region METHOD_to_dict [DOMAIN(7): DocumentProcessing; CONCEPT(6): Method; TECH(6): Python]
    # endregion METHOD___repr__
    def to_dict(self) -> dict:
        from collections import OrderedDict

        res = OrderedDict()
        res["uid"] = self.uid
        res["_uid"] = self.uid
        res["bbox"] = self.bbox.to_dict()
        res["words"] = [word.to_dict() for word in self.words]
        res["page_num"] = self.page_num
        res["line_num"] = self.line_num
        res["text"] = self.text
        res["label"] = self.label
# endregion CLASS_TextWithBBox
        return res

    # endregion METHOD_to_dict


# region MODULE_CONTRACT [DOMAIN(8): DocumentProcessing; CONCEPT(7): Reader_text_with_bbox; TECH(6): Python, dedoc]
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
## CLASS [10][TextWithBBox reader/processor] => TextWithBBox
## @usecases
## - [read]: System (Pipeline) → ParseDocument(PDF) → UnstructuredDocument
def _module_contract():
    pass
# endregion MODULE_CONTRACT
# GREP_SUMMARY: text_with_bbox, dedoc, reader, PDF, PdfReader, BaseReader, PDF, pdfminer, tabby, OCR, tables, image, txtlayer, columns, orientation, paragraphs, metadata, extraction, line, bbox, TextWithBBox
# STRUCTURE: ▶ Init ┌PDF file┐ → [TextWithBBox] ○ can_read? → ○ read → [__init__ → text → __str__] → ⊕ UnstructuredDocument(lines, tables, attachments)
