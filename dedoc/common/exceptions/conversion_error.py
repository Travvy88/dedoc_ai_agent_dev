# region MODULE_CONTRACT [DOMAIN(8): DocumentProcessing; CONCEPT(9): ErrorHandling, Exceptions; TECH(6): PythonInheritance]
## @modulecontract
## @purpose To define ConversionError — raised when document conversion fails (e.g., converter crash, timeout, malformed output).
## @scope Conversion failure error signalling.
## @input Error context (msg, filename, version).
## @output ConversionError with HTTP 415 Unsupported Media Type code.
## @links [USES_API(9): dedoc.common.exceptions.dedoc_error.DedocError]
## @invariants
## - ALWAYS carries HTTP code 415 (conversion failure means the file type cannot be served).
## - Inherits full DedocError API (msg_api, filename, version, metadata).
## @rationale
## Q: Why code=415 for conversion error?
## A: If conversion fails, the server cannot produce a representation of the requested format — semantically "Unsupported Media Type."
## @changes
## LAST_CHANGE: [v1.0.0 — Semantic template markup and LDD logging added.]
## @modulemap
## CLASS 8[Exception for conversion failures, always HTTP 415] => ConversionError
## @usecases
## - [ConversionError]: Converter → ConversionFailed → RaiseConversionError → APIResponds415
def _module_contract():
    pass
# endregion MODULE_CONTRACT
# GREP_SUMMARY: exceptions, ConversionError, 415, conversion, converter, failure
# STRUCTURE: ▶ DedocError ──▶ ConversionError ▸ __init__(⟦msg⟧, code=415) ⊕ __str__(→[msg])

import logging
from typing import Optional

from dedoc.common.exceptions.dedoc_error import DedocError

logger = logging.getLogger(__name__)

# region CLASS_ConversionError [DOMAIN(8): DocumentProcessing; CONCEPT(9): ErrorHandling, Exceptions; TECH(6): PythonInheritance]
## @purpose To signal that document conversion has failed or been terminated, resulting in an HTTP 415 response.
class ConversionError(DedocError):

    # region METHOD___init__ [DOMAIN(8): DocumentProcessing; CONCEPT(8): ErrorHandling; TECH(6): PythonConstructor]
    ## @purpose To initialize the error with a fixed HTTP 415 code, preserving full DedocError context.
    ## @uses DedocError.__init__
    ## @io (msg: str, msg_api: Optional[str], filename: Optional[str], version: Optional[str]) -> None
    ## @complexity 2
    def __init__(self, msg: str, msg_api: Optional[str] = None, filename: Optional[str] = None, version: Optional[str] = None) -> None:
        logger.debug(f"[IMP:4][ConversionError][INIT] Conversion error: msg='{msg}', filename='{filename}'")
        super(ConversionError, self).__init__(msg_api=msg_api, msg=msg, filename=filename, version=version, code=415)
        logger.info(f"[IMP:7][ConversionError][INIT] ConversionError raised (HTTP 415): {msg}")
    # endregion METHOD___init__

    # region METHOD___str__ [DOMAIN(7): DocumentProcessing; CONCEPT(8): ErrorHandling; TECH(5): PythonStr]
    ## @purpose To provide a human-readable string representation of the error.
    ## @io None -> str
    ## @complexity 1
    def __str__(self) -> str:
        return f"ConversionError({self.msg})"
    # endregion METHOD___str__
# endregion CLASS_ConversionError
