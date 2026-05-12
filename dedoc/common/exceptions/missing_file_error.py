# region MODULE_CONTRACT [DOMAIN(8): DocumentProcessing; CONCEPT(9): ErrorHandling, Exceptions; TECH(6): PythonInheritance]
## @modulecontract
## @purpose To define MissingFileError — raised when no file is provided in the POST request body.
## @scope Missing file error signalling for API handlers.
## @input Error context (msg, filename, version).
## @output MissingFileError with default HTTP 400 Bad Request code.
## @links [USES_API(9): dedoc.common.exceptions.dedoc_error.DedocError]
## @invariants
## - Uses default code=400 (missing file is a client error).
## - Inherits full DedocError API (msg_api, filename, version, metadata).
## @rationale
## Q: Why no explicit code override?
## A: DedocError defaults to code=400 — client failed to attach a file, a Bad Request scenario.
## @changes
## LAST_CHANGE: [v1.0.0 — Semantic template markup and LDD logging added.]
## @modulemap
## CLASS 8[Exception for missing file in request] => MissingFileError
## @usecases
## - [MissingFileError]: APIHandler → ValidateFileAttached → NoFileFound → RaiseMissingFileError → APIResponds400
def _module_contract():
    pass
# endregion MODULE_CONTRACT
# GREP_SUMMARY: exceptions, MissingFileError, 400, file, missing, request, API
# STRUCTURE: ▶ DedocError ──▶ MissingFileError ▸ __init__(⟦msg⟧, code=400 default) ⊕ __str__(→[msg])

import logging
from typing import Optional

from dedoc.common.exceptions.dedoc_error import DedocError

logger = logging.getLogger(__name__)

# region CLASS_MissingFileError [DOMAIN(8): DocumentProcessing; CONCEPT(9): ErrorHandling, Exceptions; TECH(6): PythonInheritance]
## @purpose To signal that no file was provided in the API request, resulting in an HTTP 400 response.
class MissingFileError(DedocError):

    # region METHOD___init__ [DOMAIN(8): DocumentProcessing; CONCEPT(8): ErrorHandling; TECH(6): PythonConstructor]
    ## @purpose To initialize the error, using DedocError's default code=400 for bad requests.
    ## @uses DedocError.__init__
    ## @io (msg: str, msg_api: Optional[str], filename: Optional[str], version: Optional[str]) -> None
    ## @complexity 2
    def __init__(self, msg: str, msg_api: Optional[str] = None, filename: Optional[str] = None, version: Optional[str] = None) -> None:
        logger.debug(f"[IMP:4][MissingFileError][INIT] Missing file: msg='{msg}', filename='{filename}'")
        super(MissingFileError, self).__init__(msg_api=msg_api, msg=msg, filename=filename, version=version)
        logger.info(f"[IMP:7][MissingFileError][INIT] MissingFileError raised (HTTP 400): {msg}")
    # endregion METHOD___init__

    # region METHOD___str__ [DOMAIN(7): DocumentProcessing; CONCEPT(8): ErrorHandling; TECH(5): PythonStr]
    ## @purpose To provide a human-readable string representation of the error.
    ## @io None -> str
    ## @complexity 1
    def __str__(self) -> str:
        return f"MissingFileError({self.msg})"
    # endregion METHOD___str__
# endregion CLASS_MissingFileError
