# region MODULE_CONTRACT [DOMAIN(8): DocumentProcessing; CONCEPT(9): ErrorHandling, Exceptions; TECH(6): PythonInheritance]
## @modulecontract
## @purpose To define BadFileFormatError — raised when an input file cannot be handled by any reader in the dedoc processing pipeline.
## @scope File format rejection error signalling.
## @input Error context (msg, filename, version).
## @output BadFileFormatError with HTTP 415 Unsupported Media Type code.
## @links [USES_API(9): dedoc.common.exceptions.dedoc_error.DedocError]
## @invariants
## - ALWAYS carries HTTP code 415 (Unsupported Media Type).
## - Inherits full DedocError API (msg_api, filename, version, metadata).
## @rationale
## Q: Why hardcode code=415?
## A: Bad file format is semantically "Unsupported Media Type" in HTTP terms — the client sent a file the server cannot process.
## @changes
## LAST_CHANGE: [v1.0.0 — Semantic template markup and LDD logging added.]
## @modulemap
## CLASS 8[Exception for unreadable file formats, always HTTP 415] => BadFileFormatError
## @usecases
## - [BadFileFormatError]: Reader → NoReaderFound → RaiseBadFileFormatError → APIResponds415
def _module_contract():
    pass
# endregion MODULE_CONTRACT
# GREP_SUMMARY: exceptions, BadFileFormatError, 415, file, format, reader, unsupported
# STRUCTURE: ▶ DedocError ──▶ BadFileFormatError ▸ __init__(⟦msg⟧, code=415) ⊕ __str__(→[msg])

import logging
from typing import Optional

from dedoc.common.exceptions.dedoc_error import DedocError

logger = logging.getLogger(__name__)

# region CLASS_BadFileFormatError [DOMAIN(8): DocumentProcessing; CONCEPT(9): ErrorHandling, Exceptions; TECH(6): PythonInheritance]
## @purpose To signal that a given file cannot be processed by any available reader, resulting in an HTTP 415 response.
class BadFileFormatError(DedocError):

    # region METHOD___init__ [DOMAIN(8): DocumentProcessing; CONCEPT(8): ErrorHandling; TECH(6): PythonConstructor]
    ## @purpose To initialize the error with a fixed HTTP 415 code, preserving full DedocError context.
    ## @uses DedocError.__init__
    ## @io (msg: str, msg_api: Optional[str], filename: Optional[str], version: Optional[str]) -> None
    ## @complexity 2
    def __init__(self, msg: str, msg_api: Optional[str] = None, filename: Optional[str] = None, version: Optional[str] = None) -> None:
        logger.debug(f"[IMP:4][BadFileFormatError][INIT] Bad file format: msg='{msg}', filename='{filename}'")
        super(BadFileFormatError, self).__init__(msg_api=msg_api, msg=msg, filename=filename, version=version, code=415)
        logger.info(f"[IMP:7][BadFileFormatError][INIT] BadFileFormatError raised (HTTP 415): {msg}")
    # endregion METHOD___init__

    # region METHOD___str__ [DOMAIN(7): DocumentProcessing; CONCEPT(8): ErrorHandling; TECH(5): PythonStr]
    ## @purpose To provide a human-readable string representation of the error.
    ## @io None -> str
    ## @complexity 1
    def __str__(self) -> str:
        return f"BadFileFormatError({self.msg})"
    # endregion METHOD___str__
# endregion CLASS_BadFileFormatError
