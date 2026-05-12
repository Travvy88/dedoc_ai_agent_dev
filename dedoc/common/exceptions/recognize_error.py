# region MODULE_CONTRACT [DOMAIN(8): DocumentProcessing; CONCEPT(9): ErrorHandling, Exceptions; TECH(6): PythonInheritance]
## @modulecontract
## @purpose To define RecognizeError — raised when document recognition (OCR, layout analysis, text extraction) fails.
## @scope Recognition failure error signalling.
## @input Error context (msg, filename, version).
## @output RecognizeError with HTTP 500 Internal Server Error code.
## @links [USES_API(9): dedoc.common.exceptions.dedoc_error.DedocError]
## @invariants
## - ALWAYS carries HTTP code 500 (recognition failure is a server-side processing error).
## - Inherits full DedocError API (msg_api, filename, version, metadata).
## @rationale
## Q: Why code=500?
## A: Recognition failure typically stems from model crashes or internal processing errors — not a client mistake.
## @changes
## LAST_CHANGE: [v1.0.0 — Semantic template markup and LDD logging added.]
## @modulemap
## CLASS 8[Exception for recognition failures, always HTTP 500] => RecognizeError
## @usecases
## - [RecognizeError]: Recognizer → OCRFailed → RaiseRecognizeError → APIResponds500
def _module_contract():
    pass
# endregion MODULE_CONTRACT
# GREP_SUMMARY: exceptions, RecognizeError, 500, recognition, OCR, processing, failure
# STRUCTURE: ▶ DedocError ──▶ RecognizeError ▸ __init__(⟦msg⟧, code=500) ⊕ __str__(→[msg])

import logging
from typing import Optional

from dedoc.common.exceptions.dedoc_error import DedocError

logger = logging.getLogger(__name__)

# region CLASS_RecognizeError [DOMAIN(8): DocumentProcessing; CONCEPT(9): ErrorHandling, Exceptions; TECH(6): PythonInheritance]
## @purpose To signal that document recognition has failed, resulting in an HTTP 500 response.
class RecognizeError(DedocError):

    # region METHOD___init__ [DOMAIN(8): DocumentProcessing; CONCEPT(8): ErrorHandling; TECH(6): PythonConstructor]
    ## @purpose To initialize the error with a fixed HTTP 500 code, preserving full DedocError context.
    ## @uses DedocError.__init__
    ## @io (msg: str, msg_api: Optional[str], filename: Optional[str], version: Optional[str]) -> None
    ## @complexity 2
    def __init__(self, msg: str, msg_api: Optional[str] = None, filename: Optional[str] = None, version: Optional[str] = None) -> None:
        logger.debug(f"[IMP:4][RecognizeError][INIT] Recognition error: msg='{msg}', filename='{filename}'")
        super(RecognizeError, self).__init__(msg_api=msg_api, msg=msg, filename=filename, version=version, code=500)
        logger.info(f"[IMP:7][RecognizeError][INIT] RecognizeError raised (HTTP 500): {msg}")
    # endregion METHOD___init__

    # region METHOD___str__ [DOMAIN(7): DocumentProcessing; CONCEPT(8): ErrorHandling; TECH(5): PythonStr]
    ## @purpose To provide a human-readable string representation of the error.
    ## @io None -> str
    ## @complexity 1
    def __str__(self) -> str:
        return f"RecognizeError({self.msg})"
    # endregion METHOD___str__
# endregion CLASS_RecognizeError
