import logging

from dedoc.data_structures.annotation import Annotation

logger = logging.getLogger(__name__)


# region CLASS_StrikeAnnotation [DOMAIN(4): DocumentProcessing; CONCEPT(5): TextAnnotation, Strikethrough; TECH(3): DataStructure]
## @purpose Mark strikethrough text inside the line.
class StrikeAnnotation(Annotation):
    """
    Strikethrough of some text inside the line.
    """
    name = "strike"
    valid_values = ["True", "False"]

    # region METHOD___init__ [DOMAIN(4): DocumentProcessing; CONCEPT(5): TextAnnotation; TECH(3): DataStructure]
    ## @purpose Initialize strikethrough annotation with validated boolean value.
    ## @uses Annotation.__init__
    ## @io (int, int, str) -> None
    ## @complexity 3
    def __init__(self, start: int, end: int, value: str) -> None:
        """
        :param start: start of the strikethrough text
        :param end: end of the strikethrough text (not included)
        :param value: True if strikethrough else False (False usually isn't used because you may not use this annotation at all)
        """
        logger.debug(f"[IMP:4][StrikeAnnotation][INIT] start={start}, end={end}, value={value}")
        try:
            bool(value)
        except ValueError:
            raise ValueError("the value of strike annotation should be True or False")
        super().__init__(start=start, end=end, name=StrikeAnnotation.name, value=value)
        logger.debug(f"[IMP:4][StrikeAnnotation][INIT] StrikeAnnotation created successfully")
    # endregion METHOD___init__
# endregion CLASS_StrikeAnnotation

# region MODULE_CONTRACT [DOMAIN(4): DocumentProcessing; CONCEPT(5): TextAnnotation, Strikethrough; TECH(3): DataStructure, Python]
## @modulecontract
## @purpose Provide strikethrough text annotation — marks text rendered with a line through it.
## @scope Text annotation for strikethrough formatting.
## @input Strikethrough boolean value ("True"/"False").
## @output StrikeAnnotation instance.
## @links [INHERITS(9): Annotation]
## @invariants
## - value is always "True" or "False"
## @rationale
## Q: Why use string boolean rather than native bool?
## A: Annotation.value is str-typed for uniform serialization across all annotation types.
## @changes
## LAST_CHANGE: [v1.0.0 – Added semantic markup and LDD logging]
## @modulemap
## CLASS 10[Strikethrough text annotation] => StrikeAnnotation
## @usecases
## - [StrikeAnnotation]: Reader → ExtractStrikethroughFormatting → StrikeAnnotationStored
def _module_contract():
    pass
# endregion MODULE_CONTRACT
# GREP_SUMMARY: strike, strikethrough, annotation, text, formatting, document, font, boolean
# STRUCTURE: ▶ Init [start, end, value] → ◇ bool(value) check → ⊕ super().__init__(name="strike") → ⎋ StrikeAnnotation
