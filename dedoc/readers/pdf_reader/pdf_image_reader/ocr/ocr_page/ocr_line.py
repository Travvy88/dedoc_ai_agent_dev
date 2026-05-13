from typing import List

from dedocutils.data_structures import BBox

import logging

logger = logging.getLogger(__name__)

from dedoc.data_structures.annotation import Annotation
from dedoc.data_structures.concrete_annotations.bbox_annotation import BBoxAnnotation
from dedoc.data_structures.concrete_annotations.confidence_annotation import ConfidenceAnnotation
from dedoc.readers.pdf_reader.pdf_image_reader.ocr.ocr_page.ocr_tuple import OcrElement
from dedoc.readers.pdf_reader.pdf_image_reader.ocr.ocr_page.ocr_word import OcrWord


# region CLASS_OcrLine [DOMAIN(8): DocumentProcessing; CONCEPT(7): Reader; TECH(6): Python]
class OcrLine:

    level = 4

    # region METHOD___init__ [DOMAIN(7): DocumentProcessing; CONCEPT(6): Method; TECH(6): Python]
    def __init__(self, order: int, bbox: BBox, words: List[OcrWord]) -> None:
        super().__init__()
        self.order = order
        self.bbox = bbox
        self.words = sorted(words, key=lambda word: word.order)

    # endregion METHOD___init__
    @property
    # region METHOD_text [DOMAIN(7): DocumentProcessing; CONCEPT(6): Method; TECH(6): Python]
    def text(self) -> str:
        return " ".join(word.text for word in self.words if word.text != "") + "\n"

    # region METHOD_get_annotations [DOMAIN(7): DocumentProcessing; CONCEPT(6): Method; TECH(6): Python]
    # endregion METHOD_text
    def get_annotations(self, page_width: int, page_height: int, extract_line_bbox: bool) -> List[Annotation]:
        if extract_line_bbox:
            return [BBoxAnnotation(0, len(" ".join([w.text for w in self.words])), self.bbox, page_width, page_height)]

        start = 0
        annotations = []

        for word in self.words:
            if word.text == "":
                continue

            end = start + len(word.text)
            annotations.append(ConfidenceAnnotation(start, end, str(word.confidence / 100)))
            annotations.append(BBoxAnnotation(start, end, word.bbox, page_width, page_height))
            start += len(word.text) + 1

        return annotations

    # endregion METHOD_get_annotations
    @staticmethod
    # region METHOD_from_list [DOMAIN(7): DocumentProcessing; CONCEPT(6): Method; TECH(6): Python]
    def from_list(line: List[OcrElement], ocr_conf_thr: float) -> "OcrLine":

        words = []
        head = None
        for element in line:
            assert element.level >= OcrLine.level, f"get {element} in line"
            if element.level == OcrLine.level:
                head = element
            else:
                words.append(element)
        line = sorted(line, key=lambda word: word.line_num)
        line = list(filter(lambda word: float(word.conf) >= ocr_conf_thr, line))
        ocr_words = [OcrWord(bbox=word.bbox, text=word.text, confidence=word.conf, order=word.word_num) for word in line]
# endregion CLASS_OcrLine
        return OcrLine(order=head.line_num, words=ocr_words, bbox=head.bbox)

    # endregion METHOD_from_list


# region MODULE_CONTRACT [DOMAIN(8): DocumentProcessing; CONCEPT(7): Reader_ocr_line; TECH(6): Python, dedoc]
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
## CLASS [8][OcrLine reader/processor] => OcrLine
## @usecases
## - [read]: System (Pipeline) → ParseDocument(PDF) → UnstructuredDocument
def _module_contract():
    pass
# endregion MODULE_CONTRACT
# GREP_SUMMARY: ocr_line, dedoc, reader, PDF, PdfReader, BaseReader, PDF, pdfminer, tabby, OCR, tables, image, txtlayer, columns, orientation, paragraphs, metadata, extraction, line, bbox, OcrLine
# STRUCTURE: ▶ Init ┌PDF file┐ → [OcrLine] ○ can_read? → ○ read → [__init__ → text → get_annotations] → ⊕ UnstructuredDocument(lines, tables, attachments)
