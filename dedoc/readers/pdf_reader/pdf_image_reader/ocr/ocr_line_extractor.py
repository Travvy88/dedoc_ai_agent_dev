from typing import Iterable, List

import numpy as np

import logging

logger = logging.getLogger(__name__)

from dedoc.readers.pdf_reader.data_classes.page_with_bboxes import PageWithBBox
from dedoc.readers.pdf_reader.data_classes.text_with_bbox import TextWithBBox
from dedoc.readers.pdf_reader.data_classes.word_with_bbox import WordWithBBox
from dedoc.readers.pdf_reader.pdf_image_reader.ocr.ocr_engine_abstract import OCREngineAbstract


# region CLASS_OCRLineExtractor [DOMAIN(8): DocumentProcessing; CONCEPT(7): Reader; TECH(6): Python]
class OCRLineExtractor:

    # region METHOD___init__ [DOMAIN(7): DocumentProcessing; CONCEPT(6): Method; TECH(6): Python]
    def __init__(self, *, config: dict, engine: "OCREngineAbstract") -> None:
        self.config = config
        self.engine = engine

    # region METHOD_split_image2lines [DOMAIN(7): DocumentProcessing; CONCEPT(6): Method; TECH(6): Python]
    # endregion METHOD___init__
    def split_image2lines(self, image: np.ndarray, page_num: int, language: str = "rus+eng", is_one_column_document: bool = True) -> PageWithBBox:
        bboxes = self.__split_image2bboxes(image=image, page_num=page_num, language=language, is_one_column_document=is_one_column_document)

        filtered_bboxes = list(self._filtered_bboxes(bboxes))
        if len(filtered_bboxes) >= 0:
            new_parsed_doc = PageWithBBox(page_num=page_num, bboxes=filtered_bboxes, image=image)
            return new_parsed_doc

    # region METHOD___split_image2bboxes [DOMAIN(7): DocumentProcessing; CONCEPT(6): Method; TECH(6): Python]
    # endregion METHOD_split_image2lines
    def __split_image2bboxes(self, image: np.ndarray, page_num: int, language: str, is_one_column_document: bool) -> List[TextWithBBox]:
        ocr_result = self.engine.recognize_page(image=image, language=language, is_one_column=is_one_column_document)

        height, width = image.shape[:2]
        extract_line_bbox = self.config.get("labeling_mode", False)

        # BUG_FIX_CONTEXT: enumerate() assigns sequential 0-based line_num to TextWithBBox based on
        # iteration order of ocr_result.lines. This is safe because TesseractOCREngine pre-sorts lines
        # by (block_num, par_num, line_num) compound key before populating OCRResult.lines. The
        # enumerate ordinal therefore matches the correct document reading order. The old engine code
        # used a single line_num key, causing paragraph-block collisions that produced garbled text.
        lines_with_bbox = []
        for line_num, line in enumerate(ocr_result.lines):
            words = [WordWithBBox(text=word.text, bbox=word.bbox) for word in line.words]
            annotations = line.get_annotations(width, height, extract_line_bbox)
            line_with_bbox = TextWithBBox(words=words, page_num=page_num, bbox=line.bbox, line_num=line_num, annotations=annotations)
            lines_with_bbox.append(line_with_bbox)

        return lines_with_bbox

    # endregion METHOD___split_image2bboxes
    # region METHOD__filtered_bboxes [DOMAIN(7): DocumentProcessing; CONCEPT(6): Method; TECH(6): Python]
    def _filtered_bboxes(self, bboxes: List[TextWithBBox]) -> Iterable[TextWithBBox]:
        for text_with_bbox in bboxes:
            bbox = text_with_bbox.bbox
            height_width = bbox.height / (bbox.width + 1e-6)
            if 0.01 < height_width < 24:
                yield text_with_bbox
    # endregion METHOD__filtered_bboxes
# endregion CLASS_OCRLineExtractor


# region MODULE_CONTRACT [DOMAIN(8): DocumentProcessing; CONCEPT(7): Reader_ocr_line_extractor; TECH(6): Python, dedoc]
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
## CLASS [8][OCRLineExtractor reader/processor] => OCRLineExtractor
## @usecases
## - [read]: System (Pipeline) → ParseDocument(PDF) → UnstructuredDocument
def _module_contract():
    pass
# endregion MODULE_CONTRACT
# GREP_SUMMARY: ocr_line_extractor, dedoc, reader, OCR, image, txtlayer, columns, orientation, metadata, extraction, line, bbox, OCRLineExtractor, OCREngineAbstract, DI, Strategy
# STRUCTURE: ▶ Init ┌config + engine┐ → [OCRLineExtractor] ○ split_image2lines → __split_image2bboxes → engine.recognize_page() → ⊕ OCRResult → OCRLine.get_annotations() → ∑ TextWithBBox → PageWithBBox
