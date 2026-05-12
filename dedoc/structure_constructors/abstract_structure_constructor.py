# region MODULE_CONTRACT [DOMAIN(9): DocumentProcessing, StructureConstruction; CONCEPT(8): AbstractFactory, Polymorphism; TECH(5): ABC, abstractmethod]
## @modulecontract
## @purpose Define the abstract interface that all structure constructors must implement, ensuring a uniform contract for transforming unstructured documents into parsed documents.
## @scope Abstract base class for document structure construction.
## @input None (interface definition only).
## @output Abstract class with a single abstract method `construct`.
## @links [USES_API(9): abc.ABC, abc.abstractmethod]
## @links_to_spec REQ-STR-001: All structure constructors must implement construct(UnstructuredDocument) → ParsedDocument.
## @invariants
## - AbstractStructureConstructor is an ABC and cannot be instantiated directly.
## - construct returns ParsedDocument or raises an exception.
## @rationale
## Q: Why ABC instead of protocol?
## A: ABC provides runtime enforcement via `@abstractmethod`, catching missing implementations at import time rather than at call time.
## @changes
## LAST_CHANGE: [v1.0.0 – Semantic template markup and LDD logging added]
## @modulemap
## CLASS 10[Abstract interface for structure constructors] => AbstractStructureConstructor
## METHOD 9[Transforms unstructured document to parsed document] => construct
## @usecases
## - [construct]: StructureExtractor → TransformUnstructuredDocument → ProduceParsedDocument
def _module_contract():
    pass
# endregion MODULE_CONTRACT
# GREP_SUMMARY: AbstractStructureConstructor, ABC, interface, document structure, UnstructuredDocument, ParsedDocument, polymorphic dispatch
# STRUCTURE: ▶ ┌ABC┐ → ◇ define abstract construct(UnstructuredDocument) → ParsedDocument

import logging
from abc import ABC, abstractmethod
from typing import Optional

from dedoc.data_structures.parsed_document import ParsedDocument
from dedoc.data_structures.unstructured_document import UnstructuredDocument

logger = logging.getLogger(__name__)

# region CLASS_AbstractStructureConstructor [DOMAIN(9): DocumentProcessing; CONCEPT(8): AbstractFactory, Polymorphism; TECH(5): ABC, abstractmethod]
## @purpose Define a uniform contract for all structure constructors: given an intermediate document representation, produce a fully structured parsed document.
class AbstractStructureConstructor(ABC):
    """
    This class construct structured representation of the document from unstructured document (list of lines).

    The result class :class:`~dedoc.data_structures.ParsedDocument` contains :class:`~dedoc.data_structures.DocumentContent`
    consisting of tables and the structure itself.
    This structure is formed based on the list of :class:`~dedoc.data_structures.LineWithMeta` with their types and hierarchy levels,
    that are retrieved with the help of some structure extractor.

    The order of the document lines and their hierarchy can be represented in different ways, e.g. standard tree of lines hierarchy.
    Also, some other custom structure can be defined by the specific constructor.
    """

    # region METHOD_construct [DOMAIN(9): DocumentProcessing; CONCEPT(8): PolymorphicDispatch, StructureTransformation; TECH(5): abstractmethod]
    ## @purpose Transform an intermediate UnstructuredDocument into a final ParsedDocument by applying the specific structure construction algorithm.
    ## @uses UnstructuredDocument, ParsedDocument
    ## @io UnstructuredDocument, Optional[dict] -> ParsedDocument
    ## @complexity 10 (dispatched to concrete implementations)
    @abstractmethod
    def construct(self, document: UnstructuredDocument, parameters: Optional[dict] = None) -> ParsedDocument:
        """
        Process unstructured document and build parsed document representation on this basis.

        :param document: intermediate representation of the document received from some structure extractor \
        (there should be filled hierarchy levels for all lines)
        :param parameters: additional parameters for document parsing, see :ref:`structure_type_parameters` for more details
        :return:  the structured representation of the given document
        """
        # LDD-log: boundary call — abstract dispatch
        logger.debug(f"[IMP:7][AbstractStructureConstructor][CONSTRUCT] Abstract dispatch called with parameters={parameters}")
        pass
    # endregion METHOD_construct
# endregion CLASS_AbstractStructureConstructor
