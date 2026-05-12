from typing import List

import numpy as np

import logging

logger = logging.getLogger(__name__)

from dedoc.data_structures.line_with_meta import LineWithMeta
from dedoc.readers.pdf_reader.pdf_auto_reader.txtlayer_classifier.abstract_txtlayer_classifier import AbstractTxtlayerClassifier


# region CLASS_SimpleTxtlayerClassifier [DOMAIN(8): DocumentProcessing; CONCEPT(7): Reader; TECH(6): Python]
class SimpleTxtlayerClassifier(AbstractTxtlayerClassifier):
    """
    Simple textual layer correctness classification.
    The textual layer is considered as a correct if it isn't empty.
    """

    # region METHOD_predict [DOMAIN(7): DocumentProcessing; CONCEPT(6): Method; TECH(6): Python]
    def predict(self, lines: List[List[LineWithMeta]]) -> np.ndarray:
        result = np.array([any(line.line.strip() for line in line_list) for line_list in lines])
# endregion CLASS_SimpleTxtlayerClassifier
        return result

    # endregion METHOD_predict


# region MODULE_CONTRACT [DOMAIN(8): DocumentProcessing; CONCEPT(7): Reader_simple_txtlayer_classifier; TECH(6): Python, dedoc]
## @modulecontract
## @purpose Read and parse PDF documents, extracting lines with metadata, tables, and attachments into UnstructuredDocument.
## @scope Machine learning classification for document layout analysis.
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
## CLASS [2][SimpleTxtlayerClassifier reader/processor] => SimpleTxtlayerClassifier
## @usecases
## - [read]: System (Pipeline) → ParseDocument(PDF) → UnstructuredDocument
def _module_contract():
    pass
# endregion MODULE_CONTRACT
# GREP_SUMMARY: simple_txtlayer_classifier, dedoc, reader, PDF, PdfReader, BaseReader, PDF, pdfminer, tabby, OCR, tables, image, txtlayer, columns, orientation, paragraphs, metadata, extraction, line, bbox, SimpleTxtlayerClassifier
# STRUCTURE: ▶ Init ┌PDF file┐ → [SimpleTxtlayerClassifier] ○ can_read? → ○ read → [predict] → ⊕ UnstructuredDocument(lines, tables, attachments)
