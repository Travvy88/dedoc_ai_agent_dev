import logging

from dedoc.data_structures.annotation import Annotation

logger = logging.getLogger(__name__)


# region CLASS_IndentationAnnotation [DOMAIN(4): DocumentProcessing; CONCEPT(5): TextAnnotation, Indentation; TECH(3): DataStructure]
## @purpose Store indentation of the entire line in twentieths of a point (1/1440 of an inch).
class IndentationAnnotation(Annotation):
    """
    This annotation contains the indentation of the entire line in twentieths of a point (1/1440 of an inch).
    These units of measurement are taken from the standard Office Open XML File Formats.
    """
    name = "indentation"

    # region METHOD___init__ [DOMAIN(4): DocumentProcessing; CONCEPT(5): TextAnnotation; TECH(3): DataStructure]
    ## @purpose Initialize indentation annotation with validated numeric value.
    ## @uses Annotation.__init__
    ## @io (int, int, str) -> None
    ## @complexity 3
    def __init__(self, start: int, end: int, value: str) -> None:
        """
        :param start: start of the annotated text (usually zero)
        :param end: end of the annotated text (usually end of the line)
        :param value: text indentation in twentieths of a point (1/1440 of an inch) how it's defined in DOCX format
        """
        logger.debug(f"[IMP:4][IndentationAnnotation][INIT] start={start}, end={end}, value={value}")
        try:
            float(value)
        except ValueError:
            raise ValueError("the value of indentation annotation should be a number")
        super().__init__(start=start, end=end, name=IndentationAnnotation.name, value=value)
        logger.debug(f"[IMP:4][IndentationAnnotation][INIT] IndentationAnnotation created successfully")
    # endregion METHOD___init__
# endregion CLASS_IndentationAnnotation

# region MODULE_CONTRACT [DOMAIN(4): DocumentProcessing; CONCEPT(5): TextAnnotation, Indentation; TECH(3): DataStructure, Python, DOCX]
## @modulecontract
## @purpose Provide line indentation annotation — stores text indentation in twentieths of a point (DOCX standard).
## @scope Text annotation for paragraph indentation.
## @input Indentation value as string (numeric, twentieths of a point).
## @output IndentationAnnotation instance.
## @links [INHERITS(9): Annotation, READS_DATA_FROM(8): DOCX_format]
## @invariants
## - value is parseable as float
## @rationale
## Q: Why store indentation in twentieths of a point?
## A: This is the standard DOCX measurement unit, preserving precision without conversion.
## @changes
## LAST_CHANGE: [v1.0.0 – Added semantic markup and LDD logging]
## @modulemap
## CLASS 10[Indentation text annotation] => IndentationAnnotation
## @usecases
## - [IndentationAnnotation]: DOCX_Reader → ExtractLineIndentation → IndentationAnnotationStored
def _module_contract():
    pass
# endregion MODULE_CONTRACT
# GREP_SUMMARY: indentation, annotation, text, document, line, DOCX, twentieths, point
# STRUCTURE: ▶ Init [start, end, value] → ◇ float(value) check → ⊕ super().__init__(name="indentation") → ⎋ IndentationAnnotation
