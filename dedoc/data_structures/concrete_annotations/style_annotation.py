import logging

from dedoc.data_structures.annotation import Annotation

logger = logging.getLogger(__name__)


# region CLASS_StyleAnnotation [DOMAIN(4): DocumentProcessing; CONCEPT(5): TextAnnotation, Style; TECH(3): DataStructure]
## @purpose Store style information about the line (e.g. Heading styles in DOCX documents).
class StyleAnnotation(Annotation):
    """
    This annotation contains the information about style of the line in the document.
    For example, in docx documents lines can be highlighted using Heading styles.
    """
    name = "style"

    # region METHOD___init__ [DOMAIN(4): DocumentProcessing; CONCEPT(5): TextAnnotation; TECH(3): DataStructure]
    ## @purpose Initialize style annotation with style name value.
    ## @uses Annotation.__init__
    ## @io (int, int, str) -> None
    ## @complexity 2
    def __init__(self, start: int, end: int, value: str) -> None:
        """
        :param start: start of the annotated text
        :param end: end of the annotated text (not included)
        :param value: style name of the text procured from the document formatting if exist (e.g. Heading 1)
        """
        logger.debug(f"[IMP:4][StyleAnnotation][INIT] start={start}, end={end}, value={value}")
        super().__init__(start=start, end=end, name=StyleAnnotation.name, value=value)
        logger.debug(f"[IMP:4][StyleAnnotation][INIT] StyleAnnotation created successfully")
    # endregion METHOD___init__
# endregion CLASS_StyleAnnotation

# region MODULE_CONTRACT [DOMAIN(4): DocumentProcessing; CONCEPT(5): TextAnnotation, Style; TECH(3): DataStructure, Python, DOCX]
## @modulecontract
## @purpose Provide style annotation — stores named style of document lines (e.g. "Heading 1").
## @scope Text annotation for document styles.
## @input Style name string.
## @output StyleAnnotation instance.
## @links [INHERITS(9): Annotation, READS_DATA_FROM(8): DOCX_format]
## @invariants
## - value is the style name as extracted from document formatting
## @rationale
## Q: Why not validate style names against a fixed set?
## A: Different document formats define different style names; validation is format-specific.
## @changes
## LAST_CHANGE: [v1.0.0 – Added semantic markup and LDD logging]
## @modulemap
## CLASS 10[Style text annotation] => StyleAnnotation
## @usecases
## - [StyleAnnotation]: DOCX_Reader → ExtractLineStyle → StyleAnnotationStored
def _module_contract():
    pass
# endregion MODULE_CONTRACT
# GREP_SUMMARY: style, annotation, text, document, line, DOCX, heading, formatting
# STRUCTURE: ▶ Init [start, end, value] → ⊕ super().__init__(name="style") → ⎋ StyleAnnotation
