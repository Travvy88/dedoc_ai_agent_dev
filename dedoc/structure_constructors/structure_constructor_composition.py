# region MODULE_CONTRACT [DOMAIN(9): DocumentProcessing, StructureConstruction; CONCEPT(8): CompositePattern, StrategyDispatch; TECH(7): RuntimeDispatch, Mapping]
## @modulecontract
## @purpose Implement the Composite pattern for structure constructors: route a document to the correct constructor based on the `structure_type` parameter, with a fallback to a default constructor.
## @scope Structure-type-based dispatch, composition of multiple structure constructors.
## @input Dict[str, AbstractStructureConstructor] (constructor registry), default AbstractStructureConstructor.
## @output ParsedDocument via the selected concrete constructor.
## @links [USES_API(9): AbstractStructureConstructor]
## @links_to_spec REQ-STR-002: Multiple structure types must be supported via runtime dispatch.
## @invariants
## - If structure_type is empty/None, the default_constructor is ALWAYS used.
## - If structure_type is unknown, StructureExtractorError is ALWAYS raised.
## - constructors dictionary keys are the valid structure_type values.
## @rationale
## Q: Why a composition class instead of inheritance?
## A: This pattern allows adding new structure types at runtime without modifying the constructor hierarchy — new constructors are simply registered in the dict.
## @changes
## LAST_CHANGE: [v1.0.0 – Semantic template markup and LDD logging added]
## @modulemap
## CLASS 9[Composite dispatcher for structure constructors] => StructureConstructorComposition
## METHOD 6[Constructor with registry injection] => __init__
## METHOD 9[Dispatch to correct constructor by structure_type] => construct
## @usecases
## - [construct]: DedocManager (ParseRequest) → ResolveStructureType → DispatchToConstructor → ProduceParsedDocument
def _module_contract():
    pass
# endregion MODULE_CONTRACT
# GREP_SUMMARY: StructureConstructorComposition, composite, dispatch, structure_type, strategy, runtime routing, fallback
# STRUCTURE: ▶ ┌constructors_dict, default_constructor┐ → ◇ structure_type ? ⚡ dispatch to match → ParsedDocument ⎋ or StructureExtractorError

import logging
from typing import Dict, Optional

from dedoc.common.exceptions.structure_extractor_error import StructureExtractorError
from dedoc.data_structures.parsed_document import ParsedDocument
from dedoc.data_structures.unstructured_document import UnstructuredDocument
from dedoc.structure_constructors.abstract_structure_constructor import AbstractStructureConstructor

logger = logging.getLogger(__name__)

# region CLASS_StructureConstructorComposition [DOMAIN(9): DocumentProcessing; CONCEPT(8): CompositePattern, StrategyDispatch; TECH(7): RuntimeDispatch, Mapping]
## @purpose Route a document to the correct structure constructor based on the `structure_type` parameter, enabling runtime selection of document structure representations.
class StructureConstructorComposition(AbstractStructureConstructor):
    """
    This class allows to construct structure from any document according to the available list of structure constructors.
    The list of structure constructors and names of structure types for them is set via the class constructor.
    Each structure type defines some specific document representation, which is retrieved via the corresponding structure constructor.
    """
    # region METHOD___init__ [DOMAIN(5): DocumentProcessing; CONCEPT(6): DependencyInjection; TECH(5): Constructor, Mapping]
    ## @purpose Initialize the composition with a registry of named constructors and a fallback default constructor.
    ## @io Dict[str, AbstractStructureConstructor], AbstractStructureConstructor -> None
    ## @complexity 2
    def __init__(self, constructors: Dict[str, AbstractStructureConstructor], default_constructor: AbstractStructureConstructor) -> None:
        """
        :param constructors: mapping structure_type -> structure constructor, defined for certain structure representations
        :param default_constructor: the structure constructor, that will be used by default if the empty structure type is given
        """
        self.constructors = constructors
        self.default_constructor = default_constructor
        # LDD-log: initialization
        logger.debug(f"[IMP:4][StructureConstructorComposition][INIT] Registered constructors: {list(constructors.keys())}, default: {type(default_constructor).__name__}")
    # endregion METHOD___init__

    # region METHOD_construct [DOMAIN(9): DocumentProcessing; CONCEPT(8): StrategyDispatch; TECH(7): RuntimeRouting, ErrorHandling]
    ## @purpose Dispatch the document to the matching constructor by structure_type; raise StructureExtractorError if the type is unknown.
    ## @uses AbstractStructureConstructor, StructureExtractorError
    ## @io UnstructuredDocument, Optional[dict] -> ParsedDocument
    ## @complexity 5
    def construct(self, document: UnstructuredDocument, parameters: Optional[dict] = None) -> ParsedDocument:
        """
        Construct the result document structure according to the `structure_type` parameter.
        If `structure_type` is empty string or None the default constructor will be used.
        To get the information about the parameters look at the documentation of :class:`~dedoc.structure_constructors.AbstractStructureConstructor`.
        """
        structure_type = parameters.get("structure_type") if parameters else None
        # LDD-log: dispatch decision
        logger.info(f"[IMP:8][StructureConstructorComposition][DISPATCH] structure_type={structure_type}, available={list(self.constructors.keys())}")

        if structure_type in self.constructors:
            # LDD-log: matched constructor
            logger.debug(f"[IMP:5][StructureConstructorComposition][MATCH] Routing to {structure_type}")
            return self.constructors[structure_type].construct(document)

        if structure_type is None or structure_type == "":
            # LDD-log: fallback to default
            logger.info(f"[IMP:7][StructureConstructorComposition][FALLBACK] No structure_type, using default: {type(self.default_constructor).__name__}")
            return self.default_constructor.construct(document)

        # LDD-log: error — unknown type
        logger.critical(f"[IMP:10][StructureConstructorComposition][ERROR] Bad structure_type={structure_type}, valid: {list(self.constructors.keys())}")
        raise StructureExtractorError(f"Bad structure type {structure_type}, available structure types is: {' '.join(self.constructors.keys())}")
    # endregion METHOD_construct
# endregion CLASS_StructureConstructorComposition
