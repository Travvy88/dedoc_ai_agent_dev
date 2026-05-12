import logging

from dedoc.data_structures.annotation import Annotation

logger = logging.getLogger(__name__)


# region CLASS_AlignmentAnnotation [DOMAIN(4): DocumentProcessing; CONCEPT(5): TextAnnotation, Alignment; TECH(3): DataStructure]
## @purpose Define the alignment of the entire line in the document: left, right, both sides, or center.
class AlignmentAnnotation(Annotation):
    """
    This annotation defines the alignment of the entire line in the document: left, right, to the both sides of the page or in the center.
    """
    name = "alignment"
    valid_values = ["left", "right", "both", "center"]

    # region METHOD___init__ [DOMAIN(4): DocumentProcessing; CONCEPT(5): TextAnnotation; TECH(3): DataStructure]
    ## @purpose Initialize alignment annotation with validated value.
    ## @uses Annotation.__init__
    ## @io (int, int, str) -> None
    ## @complexity 3
    def __init__(self, start: int, end: int, value: str) -> None:
        """
        :param start: start of the annotated text (usually zero)
        :param end: end of the annotated text (usually end of the line)
        :param value: kind of the line alignment: left, right, both of center
        """
        logger.debug(f"[IMP:4][AlignmentAnnotation][INIT] start={start}, end={end}, value={value}")
        if value not in ["left", "right", "both", "center"]:
            raise ValueError("the value of alignment annotation should be left, right, both, or center")
        super().__init__(start=start, end=end, name=AlignmentAnnotation.name, value=value)
        logger.debug(f"[IMP:4][AlignmentAnnotation][INIT] AlignmentAnnotation created successfully")
    # endregion METHOD___init__
# endregion CLASS_AlignmentAnnotation

# region MODULE_CONTRACT [DOMAIN(4): DocumentProcessing; CONCEPT(5): TextAnnotation, Alignment; TECH(3): DataStructure, Python]
## @modulecontract
## @purpose Provide alignment annotation for document lines — describes horizontal text alignment (left, right, both, center).
## @scope Text annotation data structure for line alignment.
## @input Alignment value string (left/right/both/center).
## @output AlignmentAnnotation instance.
## @links [INHERITS(9): Annotation]
## @invariants
## - value is always one of ["left", "right", "both", "center"]
## @rationale
## Q: Why validate value in __init__ rather than at serialization time?
## A: Fail-fast validation prevents downstream errors in structure extraction.
## @changes
## LAST_CHANGE: [v1.0.0 – Added semantic markup and LDD logging]
## @modulemap
## CLASS 10[Alignment text annotation] => AlignmentAnnotation
## @usecases
## - [AlignmentAnnotation]: Reader → ExtractLineAlignment → AlignmentAnnotationStored
def _module_contract():
    pass
# endregion MODULE_CONTRACT
# GREP_SUMMARY: alignment, annotation, text, left, right, center, both, document, line
# STRUCTURE: ▶ Init [start, end, value] → ◇ validate value ∋ ["left","right","both","center"] → ⊕ super().__init__(name="alignment") → ⎋ AlignmentAnnotation
