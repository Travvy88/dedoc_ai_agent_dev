import numpy as np
import pytesseract

import logging

logger = logging.getLogger(__name__)

from dedoc.readers.pdf_reader.pdf_image_reader.ocr.ocr_page.ocr_page import OcrPage


def get_text_with_bbox_from_document_page_one_column(image: np.ndarray, language: str, ocr_conf_threshold: float) -> OcrPage:
    """
    Extract text from image with Tesseract OCR.
    :param image: document image (assume that it is black and white text)
    :param language: document language as rus, eng or rus+eng
    :param ocr_conf_threshold: minimal confidence value
    :return:
    """
    config = "--psm 4"
    rec_dict = pytesseract.image_to_data(image, lang=language, output_type=pytesseract.Output.DICT, config=config)

    return OcrPage.from_dict(rec_dict, ocr_conf_threshold)


def get_text_with_bbox_from_document_page(image: np.ndarray, language: str, ocr_conf_threshold: float = -1.0) -> OcrPage:
    """
    Extract text from image with Tesseract OCR.
    :param image: document image (assume that it is black and white text)
    :param language: document language as rus, eng or rus+eng
    :param ocr_conf_threshold: minimal confidence value
    :return:
    """
    config = "--psm 3"
    rec_dict = pytesseract.image_to_data(image, lang=language, output_type=pytesseract.Output.DICT, config=config)

    return OcrPage.from_dict(rec_dict, ocr_conf_threshold)


def get_text_with_bbox_from_cells(image: np.ndarray, language: str, ocr_conf_threshold: float = -1.0) -> OcrPage:
    """
    Extract text from image with Tesseract OCR.
    :param image: document image (assume that it is black and white text)
    :param language: document language as rus, eng or rus+eng
    :param ocr_conf_threshold: minimal confidence value
    :return:
    """
    config = "--psm 6"
    rec_dict = pytesseract.image_to_data(image, lang=language, output_type=pytesseract.Output.DICT, config=config)

    return OcrPage.from_dict(rec_dict, ocr_conf_threshold)


# region MODULE_CONTRACT [DOMAIN(8): DocumentProcessing; CONCEPT(7): Reader_ocr_utils; TECH(6): Python, dedoc]
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
## FUNC [5][get_text_with_bbox_from_document_page_one_column utility/helper] => get_text_with_bbox_from_document_page_one_column
## FUNC [5][get_text_with_bbox_from_document_page utility/helper] => get_text_with_bbox_from_document_page
## FUNC [5][get_text_with_bbox_from_cells utility/helper] => get_text_with_bbox_from_cells
## @usecases
## - [read]: System (Pipeline) → ParseDocument(PDF) → UnstructuredDocument
def _module_contract():
    pass
# endregion MODULE_CONTRACT
# GREP_SUMMARY: ocr_utils, dedoc, reader, PDF, PdfReader, BaseReader, PDF, pdfminer, tabby, OCR, tables, image, txtlayer, columns, orientation, paragraphs, metadata, extraction, line, bbox, get_text_with_bbox_from_document_page_one_column, get_text_with_bbox_from_document_page, get_text_with_bbox_from_cells
# STRUCTURE: ▶ Input → ○ get_text_with_bbox_from_document_page_one_column → get_text_with_bbox_from_document_page → get_text_with_bbox_from_cells → ⊕ result
