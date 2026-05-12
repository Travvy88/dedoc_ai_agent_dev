from typing import Iterable, List

import numpy as np

import logging

logger = logging.getLogger(__name__)

from dedoc.readers.pdf_reader.data_classes.page_with_bboxes import PageWithBBox
from dedoc.readers.pdf_reader.data_classes.text_with_bbox import TextWithBBox
from dedoc.readers.pdf_reader.data_classes.word_with_bbox import WordWithBBox
from dedoc.readers.pdf_reader.pdf_image_reader.ocr.ocr_utils import get_text_with_bbox_from_document_page, get_text_with_bbox_from_document_page_one_column


# region CLASS_OCRLineExtractor [DOMAIN(8): DocumentProcessing; CONCEPT(7): Reader; TECH(6): Python]
class OCRLineExtractor:

    # region METHOD___init__ [DOMAIN(7): DocumentProcessing; CONCEPT(6): Method; TECH(6): Python]
    def __init__(self, *, config: dict) -> None:
        self.config = config

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
        ocr_conf_threshold = self.config.get("ocr_conf_threshold", -1)
        if is_one_column_document:
            output_dict = get_text_with_bbox_from_document_page_one_column(image, language, ocr_conf_threshold)
        else:
            output_dict = get_text_with_bbox_from_document_page(image, language, ocr_conf_threshold)

        height, width = image.shape[:2]
        extract_line_bbox = self.config.get("labeling_mode", False)

        lines_with_bbox = []
        for line_num, line in enumerate(output_dict.lines):
            words = [WordWithBBox(text=word.text, bbox=word.bbox) for word in line.words]
            annotations = line.get_annotations(width, height, extract_line_bbox)
            line_with_bbox = TextWithBBox(words=words, page_num=page_num, bbox=line.bbox, line_num=line_num, annotations=annotations)
            lines_with_bbox.append(line_with_bbox)

        return lines_with_bbox

    # region METHOD__filtered_bboxes [DOMAIN(7): DocumentProcessing; CONCEPT(6): Method; TECH(6): Python]
    # endregion METHOD___split_image2bboxes
    def _filtered_bboxes(self, bboxes: List[TextWithBBox]) -> Iterable[TextWithBBox]:
        for text_with_bbox in bboxes:
            bbox = text_with_bbox.bbox
            height_width = bbox.height / (bbox.width + 1e-6)
            if 0.01 < height_width < 24:
# endregion CLASS_OCRLineExtractor
                yield text_with_bbox

    # endregion METHOD__filtered_bboxes


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
# GREP_SUMMARY: ocr_line_extractor, dedoc, reader, PDF, PdfReader, BaseReader, PDF, pdfminer, tabby, OCR, tables, image, txtlayer, columns, orientation, paragraphs, metadata, extraction, line, bbox, OCRLineExtractor
# STRUCTURE: ▶ Init ┌PDF file┐ → [OCRLineExtractor] ○ can_read? → ○ read → [__init__ → split_image2lines → __split_image2bboxes] → ⊕ UnstructuredDocument(lines, tables, attachments)
