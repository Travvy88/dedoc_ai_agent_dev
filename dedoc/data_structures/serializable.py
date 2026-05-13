import logging
from abc import ABC, abstractmethod

from pydantic import BaseModel

logger = logging.getLogger(__name__)


# region CLASS_Serializable [DOMAIN(9): DocumentProcessing, DataStructures; CONCEPT(9): Serialization, AbstractBase; TECH(6): Python, ABC, Pydantic]
## @purpose Abstract base class for all data structures that must be convertible to API schema Pydantic models.
class Serializable(ABC):
    """
    Base class for the API schema objects which we later need convert to dict.
    """

    # region METHOD_to_api_schema [DOMAIN(9): DocumentProcessing; CONCEPT(9): Serialization; TECH(6): Python, Pydantic]
    ## @purpose Convert class data to the corresponding API schema Pydantic model.
    ## @io None -> BaseModel
    ## @complexity 1
    @abstractmethod
    def to_api_schema(self) -> BaseModel:
        """
        Convert class data into the corresponding API schema class.

        :return: API schema class
        """
        pass
    # endregion METHOD_to_api_schema
# endregion CLASS_Serializable

# region MODULE_CONTRACT [DOMAIN(9): DocumentProcessing, DataStructures; CONCEPT(9): Serialization, AbstractBase; TECH(6): Python, ABC, Pydantic]
## @modulecontract
## @purpose Define the Serializable abstract base class — the contract that all data structures must implement to enable API schema conversion.
## @scope Abstract base for API serialization: single abstract method to_api_schema.
## @input None (abstract).
## @output BaseModel (API schema instance).
## @links [USES_API(10): pydantic.BaseModel, INHERITED_BY(10): Annotation, CellWithMeta, DocumentContent, DocumentMetadata, LineMetadata, LineWithMeta, ParsedDocument, Table, TableMetadata, TreeNode]
## @invariants
## - All subclasses must implement to_api_schema returning a BaseModel
## @rationale
## Q: Why use ABC instead of Protocol?
## A: ABC enforces implementation at class definition time, catching errors early. It's simpler and more explicit than typing.Protocol for this use case.
## @changes
## LAST_CHANGE: [v1.0.0 – Added semantic markup and LDD logging]
## @modulemap
## CLASS 10[Serializable abstract base] => Serializable
## METHOD 10[API schema conversion] => to_api_schema
## @usecases
## - [Serializable]: APIHandler → ConvertToApiSchema → ApiResponseBuilt
def _module_contract():
    pass
# endregion MODULE_CONTRACT
# GREP_SUMMARY: Serializable, abstract, base, ABC, API, schema, Pydantic, BaseModel, to_api_schema, serialization
# STRUCTURE: ▶ Serializable (ABC) → ◇ @abstractmethod to_api_schema() → ⎋ BaseModel (subclass contract)
