# region MODULE_CONTRACT [DOMAIN(8): DocumentProcessing; CONCEPT(9): ErrorHandling, Exceptions; TECH(6): PythonInheritance]
## @modulecontract
## @purpose To define the base DedocError exception class — the root of the entire dedoc error hierarchy. All specific error types inherit from this class, ensuring consistent error serialization and API representation.
## @scope Base exception definition, error serialization (from_dict), version tracking.
## @input Error context data (msg, filename, version, metadata, code).
## @output Unified DedocError exception instances with API-friendly payloads.
## @links [READS_DATA_FROM(7): dedoc.version]
## @invariants
## - All DedocError subclasses inherit __init__ signature and __str__ pattern.
## - Every DedocError carries msg, msg_api, filename, version, metadata, code.
## - from_dict ALWAYS returns a valid DedocError instance (never None).
## @rationale
## Q: Why a rich error base class with msg_api, version, metadata instead of simple Exception?
## A: The dedoc API serves external clients — errors must be serializable to JSON with machine-readable fields (code, msg_api) for proper HTTP error responses.
## @changes
## LAST_CHANGE: [v1.0.0 — Semantic template markup and LDD logging added.]
## @modulemap
## CLASS 10[Root exception class for the entire dedoc error hierarchy] => DedocError
## @usecases
## - [DedocError]: AnyReader → ProcessingFailed → RaiseDedocError → APIRespondsWithErrorJSON
## - [from_dict]: APIHandler → DeserializeErrorFromJSON → ReconstructDedocError → LoggingOrResponse
def _module_contract():
    pass
# endregion MODULE_CONTRACT
# GREP_SUMMARY: exceptions, DedocError, base class, error hierarchy, serialization, from_dict, msg_api, metadata, version
# STRUCTURE: ▶ ┌dedoc.version┐ → CLASS DedocError ▸ __init__(⟦fields⟧, code=400) ⊕ __str__(→[msg]) ⊕ @static from_dict(⟦dict⟧ → DedocError)

import logging
from typing import Optional

import dedoc.version

logger = logging.getLogger(__name__)

# region CLASS_DedocError [DOMAIN(8): DocumentProcessing; CONCEPT(9): ErrorHandling, Exceptions; TECH(7): PythonInheritance, Serialization]
## @purpose To provide a unified, serializable error base class that all dedoc-specific exceptions inherit from, enabling consistent API error responses with rich metadata.
class DedocError(Exception):
    # region METHOD___init__ [DOMAIN(8): DocumentProcessing; CONCEPT(8): ErrorHandling; TECH(6): PythonConstructor]
    ## @purpose To initialize a DedocError with full error context — message, API message, filename, version, metadata, and HTTP status code.
    ## @uses dedoc.version
    ## @io (msg: str, msg_api: Optional[str], filename: Optional[str], version: Optional[str], metadata: Optional[dict], code: Optional[int]) -> None
    ## @complexity 4
    def __init__(self,
                 msg: str,
                 msg_api: Optional[str] = None,
                 filename: Optional[str] = None,
                 version: Optional[str] = None,
                 metadata: Optional[dict] = None,
                 code: Optional[int] = None) -> None:
        logger.debug(f"[IMP:4][DedocError][INIT] Creating error: msg='{msg}', filename='{filename}', code={code}")
        super(DedocError, self).__init__()
        self.msg = msg
        self.msg_api = msg if msg_api is None else msg_api
        self.filename = filename
        self.version = version if version is not None else dedoc.version.__version__
        self.metadata = metadata
        self.code = 400 if code is None else code
        logger.info(f"[IMP:8][DedocError][INIT] Error instance ready: code={self.code}, version={self.version}")
    # endregion METHOD___init__

    # region METHOD___str__ [DOMAIN(7): DocumentProcessing; CONCEPT(8): ErrorHandling; TECH(5): PythonStr]
    ## @purpose To provide a human-readable string representation of the error for logging and debugging.
    ## @io None -> str
    ## @complexity 1
    def __str__(self) -> str:
        return f"DedocError({self.msg})"
    # endregion METHOD___str__

    # region METHOD_from_dict [DOMAIN(8): DocumentProcessing; CONCEPT(9): ErrorHandling, Serialization; TECH(7): PythonStaticMethod, DictDeserialization]
    ## @purpose To reconstruct a DedocError instance from a dictionary, enabling error deserialization from JSON responses or stored error records.
    ## @uses dedoc.version
    ## @io dict -> DedocError
    ## @complexity 4
    @staticmethod
    def from_dict(error_dict: dict) -> "DedocError":
        logger.debug(f"[IMP:4][DedocError][FROM_DICT] Deserializing error from dict: {error_dict}")
        result = DedocError(
            msg=error_dict.get("msg", ""),
            msg_api=error_dict.get("msg_api", ""),
            filename=error_dict.get("filename", ""),
            version=error_dict.get("version", dedoc.version.__version__),
            metadata=error_dict.get("metadata", {}),
            code=error_dict.get("code", 500)
        )
        logger.info(f"[IMP:8][DedocError][FROM_DICT] Error deserialized: code={result.code}, msg='{result.msg}'")
        return result
    # endregion METHOD_from_dict
# endregion CLASS_DedocError
