from typing import List

import numpy as np

import logging

logger = logging.getLogger(__name__)

from dedoc.data_structures.line_with_meta import LineWithMeta
from dedoc.readers.pdf_reader.pdf_auto_reader.txtlayer_classifier.abstract_txtlayer_classifier import AbstractTxtlayerClassifier


# region CLASS_LetterTxtlayerClassifier [DOMAIN(8): DocumentProcessing; CONCEPT(7): Reader; TECH(6): Python]
class LetterTxtlayerClassifier(AbstractTxtlayerClassifier):
    """
    Simple multilingual textual layer correctness classification.
    Textual layer is considered as correct if percent of letters in the text > 50%.
    """
    # region METHOD___init__ [DOMAIN(7): DocumentProcessing; CONCEPT(6): Method; TECH(6): Python]
    def __init__(self, *, config: dict) -> None:
        super().__init__(config=config)
        self.__symbol_threshold = 0.5

    # region METHOD_predict [DOMAIN(7): DocumentProcessing; CONCEPT(6): Method; TECH(6): Python]
    # endregion METHOD___init__
    def predict(self, lines: List[List[LineWithMeta]]) -> np.ndarray:
        texts = np.array(["".join(line.line for line in line_list) for line_list in lines])
        result = np.array([bool(text.strip()) for text in texts])
        ids_for_pred = np.where(result)[0]

        for idx in ids_for_pred:
            text = texts[idx].replace(".", "").replace("…", "")
            letters_number = sum(1 for symbol in text if symbol.isalpha())
            result[idx] = letters_number / max(len(text), 1) > self.__symbol_threshold

# endregion CLASS_LetterTxtlayerClassifier
        return result

    # endregion METHOD_predict


# region MODULE_CONTRACT [DOMAIN(8): DocumentProcessing; CONCEPT(7): Reader_letter_txtlayer_classifier; TECH(6): Python, dedoc]
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
## CLASS [4][LetterTxtlayerClassifier reader/processor] => LetterTxtlayerClassifier
## @usecases
## - [read]: System (Pipeline) → ParseDocument(PDF) → UnstructuredDocument
def _module_contract():
    pass
# endregion MODULE_CONTRACT
# GREP_SUMMARY: letter_txtlayer_classifier, dedoc, reader, PDF, PdfReader, BaseReader, PDF, pdfminer, tabby, OCR, tables, image, txtlayer, columns, orientation, paragraphs, metadata, extraction, line, bbox, LetterTxtlayerClassifier
# STRUCTURE: ▶ Init ┌PDF file┐ → [LetterTxtlayerClassifier] ○ can_read? → ○ read → [__init__ → predict] → ⊕ UnstructuredDocument(lines, tables, attachments)
