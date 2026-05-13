# region MODULE_CONTRACT [DOMAIN(8): DocumentProcessing; CONCEPT(9): ErrorHandling, Exceptions; TECH(6): PythonInheritance]
## @modulecontract
## @purpose To define StructureExtractorError — raised when a structure extractor fails to build a structured document from unstructured input.
## @scope Structure extraction failure error signalling.
## @input Error context (msg, filename, version).
## @output StructureExtractorError with default HTTP 400 Bad Request code.
## @links [USES_API(9): dedoc.common.exceptions.dedoc_error.DedocError]
## @invariants
## - Uses default code=400 (structure extraction failure often stems from unparseable document content).
## - Inherits full DedocError API (msg_api, filename, version, metadata).
## @rationale
## Q: Why default code=400 rather than 500?
## A: A document that cannot be parsed structurally often has invalid or unsupported content — a client data issue, not a server bug.
## @changes
## LAST_CHANGE: [v1.0.0 — Semantic template markup and LDD logging added.]
## @modulemap
## CLASS 8[Exception for structure extraction failures] => StructureExtractorError
## @usecases
## - [StructureExtractorError]: StructureExtractor → BuildStructureFailed → RaiseStructureExtractorError → APIResponds400
def _module_contract():
    pass
# endregion MODULE_CONTRACT
# GREP_SUMMARY: exceptions, StructureExtractorError, 400, structure, extraction, parser, unstructured
# STRUCTURE: ▶ DedocError ──▶ StructureExtractorError ▸ __init__(⟦msg⟧, code=400 default) ⊕ __str__(→[msg])

import logging
from typing import Optional

from dedoc.common.exceptions.dedoc_error import DedocError

logger = logging.getLogger(__name__)

# region CLASS_StructureExtractorError [DOMAIN(8): DocumentProcessing; CONCEPT(9): ErrorHandling, Exceptions; TECH(6): PythonInheritance]
## @purpose To signal that structure extraction from an unstructured document has failed, resulting in an HTTP 400 response.
class StructureExtractorError(DedocError):

    # region METHOD___init__ [DOMAIN(8): DocumentProcessing; CONCEPT(8): ErrorHandling; TECH(6): PythonConstructor]
    ## @purpose To initialize the error, using DedocError's default code=400.
    ## @uses DedocError.__init__
    ## @io (msg: str, msg_api: Optional[str], filename: Optional[str], version: Optional[str]) -> None
    ## @complexity 2
    def __init__(self, msg: str, msg_api: Optional[str] = None, filename: Optional[str] = None, version: Optional[str] = None) -> None:
        logger.debug(f"[IMP:4][StructureExtractorError][INIT] Structure extraction error: msg='{msg}', filename='{filename}'")
        super(StructureExtractorError, self).__init__(msg_api=msg_api, msg=msg, filename=filename, version=version)
        logger.info(f"[IMP:7][StructureExtractorError][INIT] StructureExtractorError raised (HTTP 400): {msg}")
    # endregion METHOD___init__

    # region METHOD___str__ [DOMAIN(7): DocumentProcessing; CONCEPT(8): ErrorHandling; TECH(5): PythonStr]
    ## @purpose To provide a human-readable string representation of the error.
    ## @io None -> str
    ## @complexity 1
    def __str__(self) -> str:
        return f"StructureExtractorError({self.msg})"
    # endregion METHOD___str__
# endregion CLASS_StructureExtractorError
