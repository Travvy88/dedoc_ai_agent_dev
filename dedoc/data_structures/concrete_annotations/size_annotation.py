import logging

from dedoc.data_structures.annotation import Annotation

logger = logging.getLogger(__name__)


# region CLASS_SizeAnnotation [DOMAIN(4): DocumentProcessing; CONCEPT(5): TextAnnotation, FontSize; TECH(3): DataStructure]
## @purpose Store font size of some part of the line in points (1/72 of an inch).
class SizeAnnotation(Annotation):
    """
    This annotation contains the font size of some part of the line in points (1/72 of an inch).
    These units of measurement are taken from the standard Office Open XML File Formats.
    """
    name = "size"

    # region METHOD___init__ [DOMAIN(4): DocumentProcessing; CONCEPT(5): TextAnnotation; TECH(3): DataStructure]
    ## @purpose Initialize size annotation with validated numeric value.
    ## @uses Annotation.__init__
    ## @io (int, int, str) -> None
    ## @complexity 3
    def __init__(self, start: int, end: int, value: str) -> None:
        """
        :param start: start of the annotated text
        :param end: end of the annotated text (not included)
        :param value: font size in points (1/72 of an inch) how it's defined in DOCX format
        """
        logger.debug(f"[IMP:4][SizeAnnotation][INIT] start={start}, end={end}, value={value}")
        try:
            float(value)
        except ValueError:
            raise ValueError("the value of size annotation should be a number")
        super().__init__(start=start, end=end, name=SizeAnnotation.name, value=value)
        logger.debug(f"[IMP:4][SizeAnnotation][INIT] SizeAnnotation created successfully")
    # endregion METHOD___init__
# endregion CLASS_SizeAnnotation

# region MODULE_CONTRACT [DOMAIN(4): DocumentProcessing; CONCEPT(5): TextAnnotation, FontSize; TECH(3): DataStructure, Python, DOCX]
## @modulecontract
## @purpose Provide font size annotation — stores font size in points (DOCX standard).
## @scope Text annotation for font size formatting.
## @input Font size value as string (numeric, points).
## @output SizeAnnotation instance.
## @links [INHERITS(9): Annotation, READS_DATA_FROM(8): DOCX_format]
## @invariants
## - value is parseable as float
## @rationale
## Q: Why store font size in points?
## A: Points (1/72 inch) is the standard DOCX font size unit, preserving precision.
## @changes
## LAST_CHANGE: [v1.0.0 – Added semantic markup and LDD logging]
## @modulemap
## CLASS 10[Font size text annotation] => SizeAnnotation
## @usecases
## - [SizeAnnotation]: Reader → ExtractFontSize → SizeAnnotationStored
def _module_contract():
    pass
# endregion MODULE_CONTRACT
# GREP_SUMMARY: size, font, annotation, text, document, points, DOCX, formatting
# STRUCTURE: ▶ Init [start, end, value] → ◇ float(value) check → ⊕ super().__init__(name="size") → ⎋ SizeAnnotation
