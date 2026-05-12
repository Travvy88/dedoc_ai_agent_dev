import logging

from dedoc.data_structures.annotation import Annotation

logger = logging.getLogger(__name__)


# region CLASS_UnderlinedAnnotation [DOMAIN(4): DocumentProcessing; CONCEPT(5): TextAnnotation, Underlined; TECH(3): DataStructure]
## @purpose Mark underlined text inside the line.
class UnderlinedAnnotation(Annotation):
    """
    Underlined text inside the line.
    """
    name = "underlined"
    valid_values = ["True", "False"]

    # region METHOD___init__ [DOMAIN(4): DocumentProcessing; CONCEPT(5): TextAnnotation; TECH(3): DataStructure]
    ## @purpose Initialize underlined annotation with validated boolean value.
    ## @uses Annotation.__init__
    ## @io (int, int, str) -> None
    ## @complexity 3
    def __init__(self, start: int, end: int, value: str) -> None:
        """
        :param start: start of the underlined text
        :param end: end of the underlined text (not included)
        :param value: True if underlined else False (False usually isn't used because you may not use this annotation at all)
        """
        logger.debug(f"[IMP:4][UnderlinedAnnotation][INIT] start={start}, end={end}, value={value}")
        try:
            bool(value)
        except ValueError:
            raise ValueError("the value of underlined annotation should be True or False")
        super().__init__(start=start, end=end, name=UnderlinedAnnotation.name, value=value)
        logger.debug(f"[IMP:4][UnderlinedAnnotation][INIT] UnderlinedAnnotation created successfully")
    # endregion METHOD___init__
# endregion CLASS_UnderlinedAnnotation

# region MODULE_CONTRACT [DOMAIN(4): DocumentProcessing; CONCEPT(5): TextAnnotation, Underlined; TECH(3): DataStructure, Python]
## @modulecontract
## @purpose Provide underlined text annotation — marks which portion of text is rendered with an underline.
## @scope Text annotation for underlined formatting.
## @input Underlined boolean value ("True"/"False").
## @output UnderlinedAnnotation instance.
## @links [INHERITS(9): Annotation]
## @invariants
## - value is always "True" or "False"
## @rationale
## Q: Why use string boolean rather than native bool?
## A: Annotation.value is str-typed for uniform serialization across all annotation types.
## @changes
## LAST_CHANGE: [v1.0.0 – Added semantic markup and LDD logging]
## @modulemap
## CLASS 10[Underlined text annotation] => UnderlinedAnnotation
## @usecases
## - [UnderlinedAnnotation]: Reader → ExtractUnderlinedFormatting → UnderlinedAnnotationStored
def _module_contract():
    pass
# endregion MODULE_CONTRACT
# GREP_SUMMARY: underlined, underline, annotation, text, formatting, document, font, boolean
# STRUCTURE: ▶ Init [start, end, value] → ◇ bool(value) check → ⊕ super().__init__(name="underlined") → ⎋ UnderlinedAnnotation
