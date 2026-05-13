# region MODULE_CONTRACT [DOMAIN(8): DocumentProcessing; CONCEPT(9): ErrorHandling, Exceptions; TECH(6): PythonInheritance]
## @modulecontract
## @purpose To define BadParametersError — raised when API request parameters are invalid or cannot be processed (e.g., wrong type, missing required field).
## @scope Parameter validation error signalling.
## @input Error context (msg, filename, version).
## @output BadParametersError with default HTTP 400 Bad Request code.
## @links [USES_API(9): dedoc.common.exceptions.dedoc_error.DedocError]
## @invariants
## - Inherits full DedocError API (msg_api, filename, version, metadata).
## - Uses default code=400 from DedocError base class.
## @rationale
## Q: Why no explicit code override?
## A: DedocError defaults to code=400, which is semantically correct for bad parameters.
## @changes
## LAST_CHANGE: [v1.0.0 — Semantic template markup and LDD logging added.]
## @modulemap
## CLASS 8[Exception for invalid API parameters] => BadParametersError
## @usecases
## - [BadParametersError]: APIHandler → ValidateParameters → ParametersInvalid → RaiseBadParametersError → APIResponds400
def _module_contract():
    pass
# endregion MODULE_CONTRACT
# GREP_SUMMARY: exceptions, BadParametersError, 400, parameters, validation, API
# STRUCTURE: ▶ DedocError ──▶ BadParametersError ▸ __init__(⟦msg⟧, code=400 default) ⊕ __str__(→[msg])

import logging
from typing import Optional

from dedoc.common.exceptions.dedoc_error import DedocError

logger = logging.getLogger(__name__)

# region CLASS_BadParametersError [DOMAIN(8): DocumentProcessing; CONCEPT(9): ErrorHandling, Exceptions; TECH(6): PythonInheritance]
## @purpose To signal that provided API parameters are invalid or malformed, resulting in an HTTP 400 response.
class BadParametersError(DedocError):

    # region METHOD___init__ [DOMAIN(8): DocumentProcessing; CONCEPT(8): ErrorHandling; TECH(6): PythonConstructor]
    ## @purpose To initialize the error, using DedocError's default code=400 for bad requests.
    ## @uses DedocError.__init__
    ## @io (msg: str, msg_api: Optional[str], filename: Optional[str], version: Optional[str]) -> None
    ## @complexity 2
    def __init__(self, msg: str, msg_api: Optional[str] = None, filename: Optional[str] = None, version: Optional[str] = None) -> None:
        logger.debug(f"[IMP:4][BadParametersError][INIT] Bad parameters: msg='{msg}', filename='{filename}'")
        super(BadParametersError, self).__init__(msg_api=msg_api, msg=msg, filename=filename, version=version)
        logger.info(f"[IMP:7][BadParametersError][INIT] BadParametersError raised (HTTP 400): {msg}")
    # endregion METHOD___init__

    # region METHOD___str__ [DOMAIN(7): DocumentProcessing; CONCEPT(8): ErrorHandling; TECH(5): PythonStr]
    ## @purpose To provide a human-readable string representation of the error.
    ## @io None -> str
    ## @complexity 1
    def __str__(self) -> str:
        return f"BadParametersError({self.msg})"
    # endregion METHOD___str__
# endregion CLASS_BadParametersError
