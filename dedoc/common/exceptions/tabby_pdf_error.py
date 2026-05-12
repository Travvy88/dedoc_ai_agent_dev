# region MODULE_CONTRACT [DOMAIN(8): DocumentProcessing; CONCEPT(9): ErrorHandling, Exceptions; TECH(6): PythonInheritance]
## @modulecontract
## @purpose To define TabbyPdfError — raised when the TabbyPDF external processing tool returns an error.
## @scope TabbyPDF processing error signalling.
## @input Error context (msg, filename, version).
## @output TabbyPdfError with HTTP 500 Internal Server Error code.
## @links [USES_API(9): dedoc.common.exceptions.dedoc_error.DedocError]
## @invariants
## - ALWAYS carries HTTP code 500 (external tool failure is a server-side dependency error).
## - Inherits full DedocError API (msg_api, filename, version, metadata).
## @rationale
## Q: Why code=500?
## A: TabbyPDF is a server-side dependency — its failures are infrastructure errors, not client mistakes.
## @changes
## LAST_CHANGE: [v1.0.0 — Semantic template markup and LDD logging added.]
## @modulemap
## CLASS 8[Exception for TabbyPDF external tool errors, always HTTP 500] => TabbyPdfError
## @usecases
## - [TabbyPdfError]: PDFProcessor → CallTabbyPDF → TabbyPDFFails → RaiseTabbyPdfError → APIResponds500
def _module_contract():
    pass
# endregion MODULE_CONTRACT
# GREP_SUMMARY: exceptions, TabbyPdfError, 500, TabbyPDF, PDF, external, tool, processing
# STRUCTURE: ▶ DedocError ──▶ TabbyPdfError ▸ __init__(⟦msg⟧, code=500) ⊕ __str__(→[msg])

import logging
from typing import Optional

from dedoc.common.exceptions.dedoc_error import DedocError

logger = logging.getLogger(__name__)

# region CLASS_TabbyPdfError [DOMAIN(8): DocumentProcessing; CONCEPT(9): ErrorHandling, Exceptions; TECH(6): PythonInheritance]
## @purpose To signal that the TabbyPDF external tool has failed, resulting in an HTTP 500 response.
class TabbyPdfError(DedocError):

    # region METHOD___init__ [DOMAIN(8): DocumentProcessing; CONCEPT(8): ErrorHandling; TECH(6): PythonConstructor]
    ## @purpose To initialize the error with a fixed HTTP 500 code, preserving full DedocError context.
    ## @uses DedocError.__init__
    ## @io (msg: str, msg_api: Optional[str], filename: Optional[str], version: Optional[str]) -> None
    ## @complexity 2
    def __init__(self, msg: str, msg_api: Optional[str] = None, filename: Optional[str] = None, version: Optional[str] = None) -> None:
        logger.debug(f"[IMP:4][TabbyPdfError][INIT] TabbyPDF error: msg='{msg}', filename='{filename}'")
        super(TabbyPdfError, self).__init__(msg_api=msg_api, msg=msg, filename=filename, version=version, code=500)
        logger.info(f"[IMP:7][TabbyPdfError][INIT] TabbyPdfError raised (HTTP 500): {msg}")
    # endregion METHOD___init__

    # region METHOD___str__ [DOMAIN(7): DocumentProcessing; CONCEPT(8): ErrorHandling; TECH(5): PythonStr]
    ## @purpose To provide a human-readable string representation of the error.
    ## @io None -> str
    ## @complexity 1
    def __str__(self) -> str:
        return f"TabbyPdfError({self.msg})"
    # endregion METHOD___str__
# endregion CLASS_TabbyPdfError
