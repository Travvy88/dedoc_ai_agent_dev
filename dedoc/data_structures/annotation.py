import logging

from dedoc.api.schema.annotation import Annotation as ApiAnnotation
from dedoc.data_structures.serializable import Serializable

logger = logging.getLogger(__name__)


# region CLASS_Annotation [DOMAIN(9): DocumentProcessing, DataStructures; CONCEPT(10): TextAnnotation, BaseClass; TECH(5): Python, Inheritance]
## @purpose Base class for all text annotations — holds start/end positions, name, value, and mergeability flag for text region metadata.
class Annotation(Serializable):
    """
    Base class for text annotations of all kinds.
    Annotation is the piece of information about the text line: it's appearance or links to another document object.
    Look to the concrete kind of annotations to get mode examples.

    :ivar start: start of the annotated text
    :ivar end: end of the annotated text (end isn't included)
    :ivar name: annotation's name, specific for each type of annotation
    :ivar value: information about annotated text, depends on the type of annotation, e.g. "True"/"False", "10.0", etc.
    :ivar is_mergeable: is it possible to merge annotations with the same value

    :vartype start: int
    :vartype end: int
    :vartype name: str
    :vartype value: str
    :vartype is_mergeable: bool
    """

    # region METHOD___init__ [DOMAIN(9): DocumentProcessing; CONCEPT(10): TextAnnotation; TECH(5): DataStructure]
    ## @purpose Initialize annotation with position, name, value, and mergeability flag.
    ## @uses Serializable
    ## @io (int, int, str, str, bool) -> None
    ## @complexity 2
    def __init__(self, start: int, end: int, name: str, value: str, is_mergeable: bool = True) -> None:
        """
        Some kind of text information about symbols between start and end.
        For example Annotation(1, 13, "italic", "True") says that text between 1st and 13th symbol was writen in italic.

        :param start: start of the annotated text
        :param end: end of the annotated text (end isn't included)
        :param name: annotation's name
        :param value: information about annotated text
        :param is_mergeable: is it possible to merge annotations with the same value
        """
        logger.debug(f"[IMP:4][Annotation][INIT] name={name}, start={start}, end={end}, value={value}, is_mergeable={is_mergeable}")
        self.start: int = start
        self.end: int = end
        self.name: str = name
        self.value: str = value
        self.is_mergeable: bool = is_mergeable
        logger.debug(f"[IMP:4][Annotation][INIT] Annotation instance created for name={name}")
    # endregion METHOD___init__

    # region METHOD___eq__ [DOMAIN(9): DocumentProcessing; CONCEPT(8): Equality; TECH(5): Python]
    ## @purpose Compare two annotations for equality by name, value, start, and end.
    ## @io (object) -> bool
    ## @complexity 2
    def __eq__(self, o: object) -> bool:
        if not isinstance(o, Annotation):
            return False
        return self.name == o.name and self.value == o.value and self.start == o.start and self.end == o.end
    # endregion METHOD___eq__

    # region METHOD___str__ [DOMAIN(9): DocumentProcessing; CONCEPT(5): Display; TECH(5): Python]
    ## @purpose Return human-readable string representation of the annotation.
    ## @io None -> str
    ## @complexity 1
    def __str__(self) -> str:
        return f"{self.name.capitalize()}({self.start}:{self.end}, {self.value})"
    # endregion METHOD___str__

    # region METHOD___repr__ [DOMAIN(9): DocumentProcessing; CONCEPT(5): Display; TECH(5): Python]
    ## @purpose Return repr of the annotation (delegates to __str__).
    ## @io None -> str
    ## @complexity 1
    def __repr__(self) -> str:
        return self.__str__()
    # endregion METHOD___repr__

    # region METHOD_to_api_schema [DOMAIN(9): DocumentProcessing; CONCEPT(8): Serialization; TECH(6): API]
    ## @purpose Convert annotation to API schema representation.
    ## @uses ApiAnnotation
    ## @io None -> ApiAnnotation
    ## @complexity 2
    def to_api_schema(self) -> ApiAnnotation:
        logger.debug(f"[IMP:4][Annotation][TO_API] Converting annotation name={self.name} to API schema")
        return ApiAnnotation(start=self.start, end=self.end, name=self.name, value=self.value)
    # endregion METHOD_to_api_schema
# endregion CLASS_Annotation

# region MODULE_CONTRACT [DOMAIN(9): DocumentProcessing, DataStructures; CONCEPT(10): TextAnnotation, BaseClass; TECH(5): Python, API]
## @modulecontract
## @purpose Define the base Annotation class — the root of the annotation hierarchy for all text-level metadata in the document processing pipeline.
## @scope Base annotation class with position, value, equality, serialization.
## @input Start/end positions, annotation name, value string.
## @output Annotation base instances consumed by all annotation subclasses.
## @links [EXPORTS(10): Annotation, INHERITS(4): Serializable, USES_API(8): ApiAnnotation]
## @invariants
## - start <= end (not enforced but expected by convention)
## - name is a non-empty string unique per annotation type
## - is_mergeable defaults to True
## @rationale
## Q: Why inherit from Serializable?
## A: All annotations must be convertible to API schemas for HTTP responses.
## @changes
## LAST_CHANGE: [v1.0.0 – Added semantic markup and LDD logging]
## @modulemap
## CLASS 10[Base annotation class] => Annotation
## METHOD 8[Constructor] => __init__
## METHOD 6[Equality check] => __eq__
## METHOD 4[String representation] => __str__
## METHOD 4[Repr] => __repr__
## METHOD 8[API schema conversion] => to_api_schema
## @usecases
## - [Annotation]: Reader → CreateAnnotation → AnnotationStored
## - [Annotation]: Converter → SerializeToAPI → ApiAnnotationReturned
def _module_contract():
    pass
# endregion MODULE_CONTRACT
# GREP_SUMMARY: Annotation, base, text, document, metadata, start, end, name, value, is_mergeable, serializable, API
# STRUCTURE: ▶ Annotation ┌start, end, name, value, is_mergeable┐ → ⊕ __str__/__eq__/__repr__ → ⊕ to_api_schema → ⎋ ApiAnnotation
