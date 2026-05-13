from typing import Dict

from .abstract_txtlayer_classifier import AbstractTxtlayerClassifier
from .letter_txtlayer_classifier import LetterTxtlayerClassifier
from .ml_txtlayer_classifier import MlTxtlayerClassifier
from .simple_txtlayer_classifier import SimpleTxtlayerClassifier

import logging

logger = logging.getLogger(__name__)


def get_classifiers(config: dict) -> Dict[str, AbstractTxtlayerClassifier]:
    return {
        "ml": MlTxtlayerClassifier(config=config),
        "simple": SimpleTxtlayerClassifier(config=config),
        "letter": LetterTxtlayerClassifier(config=config)
    }


# region MODULE_CONTRACT [DOMAIN(8): DocumentProcessing; CONCEPT(7): Reader___init__; TECH(6): Python, dedoc]
## @modulecontract
## @purpose Re-export symbols for the txtlayer_classifier reader subpackage of dedoc/readers/.
## @scope Symbol re-export.
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
## FUNC [5][get_classifiers utility/helper] => get_classifiers
## @usecases
## - [read]: System (Pipeline) → ParseDocument(PDF) → UnstructuredDocument
def _module_contract():
    pass
# endregion MODULE_CONTRACT
# GREP_SUMMARY: __init__, dedoc, reader, PDF, PdfReader, BaseReader, PDF, pdfminer, tabby, OCR, tables, image, txtlayer, columns, orientation, paragraphs, metadata, extraction, line, bbox, get_classifiers
# STRUCTURE: ▶ Input → ○ get_classifiers → ⊕ result
