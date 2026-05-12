import logging

from dedoc.data_structures.annotation import Annotation

logger = logging.getLogger(__name__)


# region CLASS_BoldAnnotation [DOMAIN(4): DocumentProcessing; CONCEPT(5): TextAnnotation, Bold; TECH(3): DataStructure]
## @purpose Mark boldness of some text inside the line.
class BoldAnnotation(Annotation):
    """
    Boldness of some text inside the line.
    """
    name = "bold"
    valid_values = ["True", "False"]

    # region METHOD___init__ [DOMAIN(4): DocumentProcessing; CONCEPT(5): TextAnnotation; TECH(3): DataStructure]
    ## @purpose Initialize bold annotation with validated boolean value.
    ## @uses Annotation.__init__
    ## @io (int, int, str) -> None
    ## @complexity 3
    def __init__(self, start: int, end: int, value: str) -> None:
        """
        :param start: start of the bold text
        :param end: end of the bold text (not included)
        :param value: True if bold else False (False usually isn't used because you may not use this annotation at all)
        """
        logger.debug(f"[IMP:4][BoldAnnotation][INIT] start={start}, end={end}, value={value}")
        try:
            bool(value)
        except ValueError:
            raise ValueError("the value of bold annotation should be True or False")
        super().__init__(start=start, end=end, name=BoldAnnotation.name, value=value)
        logger.debug(f"[IMP:4][BoldAnnotation][INIT] BoldAnnotation created successfully")
    # endregion METHOD___init__
# endregion CLASS_BoldAnnotation

# region MODULE_CONTRACT [DOMAIN(4): DocumentProcessing; CONCEPT(5): TextAnnotation, Bold; TECH(3): DataStructure, Python]
## @modulecontract
## @purpose Provide bold text annotation — marks which portion of text is rendered in bold.
## @scope Text annotation for bold formatting.
## @input Bold boolean value ("True"/"False").
## @output BoldAnnotation instance.
## @links [INHERITS(9): Annotation]
## @invariants
## - value is always "True" or "False"
## @rationale
## Q: Why use string boolean rather than native bool?
## A: Annotation.value is str-typed to support uniform serialization across all annotation types.
## @changes
## LAST_CHANGE: [v1.0.0 – Added semantic markup and LDD logging]
## @modulemap
## CLASS 10[Bold text annotation] => BoldAnnotation
## @usecases
## - [BoldAnnotation]: Reader → ExtractBoldFormatting → BoldAnnotationStored
def _module_contract():
    pass
# endregion MODULE_CONTRACT
# GREP_SUMMARY: bold, annotation, text, formatting, document, font, boolean
# STRUCTURE: ▶ Init [start, end, value] → ◇ bool(value) check → ⊕ super().__init__(name="bold") → ⎋ BoldAnnotation
