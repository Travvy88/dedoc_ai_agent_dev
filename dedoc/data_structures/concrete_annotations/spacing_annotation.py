import logging

from dedoc.data_structures.annotation import Annotation

logger = logging.getLogger(__name__)


# region CLASS_SpacingAnnotation [DOMAIN(4): DocumentProcessing; CONCEPT(5): TextAnnotation, Spacing; TECH(3): DataStructure]
## @purpose Store spacing between the current line and the previous one in twentieths of a point.
class SpacingAnnotation(Annotation):
    """
    This annotation contains spacing between the current line and the previous one.
    It's measured in twentieths of a point or one hundredths of a line according to the standard Office Open XML File Formats.
    """
    name = "spacing"

    # region METHOD___init__ [DOMAIN(4): DocumentProcessing; CONCEPT(5): TextAnnotation; TECH(3): DataStructure]
    ## @purpose Initialize spacing annotation with validated integer value.
    ## @uses Annotation.__init__
    ## @io (int, int, str) -> None
    ## @complexity 3
    def __init__(self, start: int, end: int, value: str) -> None:
        """
        :param start: start of the annotated text (usually zero)
        :param end: end of the annotated text (usually end of the line)
        :param value: spacing between the current line and the previous one how it's defined in DOCX format (integer value)
        """
        logger.debug(f"[IMP:4][SpacingAnnotation][INIT] start={start}, end={end}, value={value}")
        try:
            int(value)
        except ValueError:
            raise ValueError(f"the value of spacing annotation should be a number, get {value}")
        super().__init__(start=start, end=end, name=SpacingAnnotation.name, value=value)
        logger.debug(f"[IMP:4][SpacingAnnotation][INIT] SpacingAnnotation created successfully")
    # endregion METHOD___init__
# endregion CLASS_SpacingAnnotation

# region MODULE_CONTRACT [DOMAIN(4): DocumentProcessing; CONCEPT(5): TextAnnotation, Spacing; TECH(3): DataStructure, Python, DOCX]
## @modulecontract
## @purpose Provide line spacing annotation — stores inter-line spacing in twentieths of a point (DOCX standard).
## @scope Text annotation for line spacing.
## @input Spacing value as string (integer, twentieths of a point).
## @output SpacingAnnotation instance.
## @links [INHERITS(9): Annotation, READS_DATA_FROM(8): DOCX_format]
## @invariants
## - value is parseable as int
## @rationale
## Q: Why use int validation instead of float?
## A: DOCX spacing values are always integers in twentieths of a point.
## @changes
## LAST_CHANGE: [v1.0.0 – Added semantic markup and LDD logging]
## @modulemap
## CLASS 10[Line spacing annotation] => SpacingAnnotation
## @usecases
## - [SpacingAnnotation]: DOCX_Reader → ExtractLineSpacing → SpacingAnnotationStored
def _module_contract():
    pass
# endregion MODULE_CONTRACT
# GREP_SUMMARY: spacing, annotation, text, document, line, DOCX, twentieths, point, inter-line
# STRUCTURE: ▶ Init [start, end, value] → ◇ int(value) check → ⊕ super().__init__(name="spacing") → ⎋ SpacingAnnotation
