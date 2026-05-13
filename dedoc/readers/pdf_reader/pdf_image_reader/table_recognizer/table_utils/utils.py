from typing import List, Tuple

import numpy as np

import logging

logger = logging.getLogger(__name__)

from dedoc.readers.pdf_reader.data_classes.tables.cell import Cell


def equal_with_eps(x: int, y: int, eps: int = 10) -> bool:
    return y + eps >= x >= y - eps


def get_highest_pixel_frequency(image: np.ndarray) -> int:
    unique, counts = np.unique(image.reshape(-1, 1), axis=0, return_counts=True)
    if len(counts) == 0:
        return np.uint8(255)
    color = unique[np.argmax(counts)][0]
    if color == 0:
        color = np.uint8(255)

    return color


def similarity(s1: str, s2: str) -> float:
    """string similarity"""
    import difflib

    normalized1 = s1.lower()
    normalized2 = s2.lower()
    matcher = difflib.SequenceMatcher(None, normalized1, normalized2)
    return matcher.ratio()


def get_statistic_values(cells: List[List[Cell]]) -> Tuple[int, int, int, int]:

    cnt_rows = len(cells)
    cnt_columns = len(cells[0]) if cnt_rows else 0
    cnt_cell = cnt_columns * cnt_rows
    cnt_attr_cell = len([cell for row in cells for cell in row if cell.is_attribute])

    return cnt_attr_cell, cnt_cell, cnt_columns, cnt_rows


# region MODULE_CONTRACT [DOMAIN(8): DocumentProcessing; CONCEPT(7): Reader_utils; TECH(6): Python, dedoc]
## @modulecontract
## @purpose Read and parse PDF documents, extracting lines with metadata, tables, and attachments into UnstructuredDocument.
## @scope Table recognition and extraction from document images.
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
## FUNC [5][equal_with_eps utility/helper] => equal_with_eps
## FUNC [5][get_highest_pixel_frequency utility/helper] => get_highest_pixel_frequency
## FUNC [5][similarity utility/helper] => similarity
## FUNC [5][get_statistic_values utility/helper] => get_statistic_values
## @usecases
## - [read]: System (Pipeline) → ParseDocument(PDF) → UnstructuredDocument
def _module_contract():
    pass
# endregion MODULE_CONTRACT
# GREP_SUMMARY: utils, dedoc, reader, PDF, PdfReader, BaseReader, PDF, pdfminer, tabby, OCR, tables, image, txtlayer, columns, orientation, paragraphs, metadata, extraction, line, bbox, equal_with_eps, get_highest_pixel_frequency, similarity, get_statistic_values
# STRUCTURE: ▶ Input → ○ equal_with_eps → get_highest_pixel_frequency → similarity → ⊕ result
