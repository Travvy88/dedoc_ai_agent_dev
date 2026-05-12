import logging

from dedoc.data_structures.annotation import Annotation

logger = logging.getLogger(__name__)


# region CLASS_SubscriptAnnotation [DOMAIN(4): DocumentProcessing; CONCEPT(5): TextAnnotation, Subscript; TECH(3): DataStructure]
## @purpose Mark subscript text inside the line.
class SubscriptAnnotation(Annotation):
    """
    Subscript text inside the line.
    """
    name = "subscript"
    valid_values = ["True", "False"]

    # region METHOD___init__ [DOMAIN(4): DocumentProcessing; CONCEPT(5): TextAnnotation; TECH(3): DataStructure]
    ## @purpose Initialize subscript annotation with validated boolean value.
    ## @uses Annotation.__init__
    ## @io (int, int, str) -> None
    ## @complexity 3
    def __init__(self, start: int, end: int, value: str) -> None:
        """
        :param start: start of the subscript text
        :param end: end of the subscript text (not included)
        :param value: True if subscript else False (False usually isn't used because you may not use this annotation at all)
        """
        logger.debug(f"[IMP:4][SubscriptAnnotation][INIT] start={start}, end={end}, value={value}")
        try:
            bool(value)
        except ValueError:
            raise ValueError("the value of subscript annotation should be True or False")
        super().__init__(start=start, end=end, name=SubscriptAnnotation.name, value=value)
        logger.debug(f"[IMP:4][SubscriptAnnotation][INIT] SubscriptAnnotation created successfully")
    # endregion METHOD___init__
# endregion CLASS_SubscriptAnnotation

# region MODULE_CONTRACT [DOMAIN(4): DocumentProcessing; CONCEPT(5): TextAnnotation, Subscript; TECH(3): DataStructure, Python]
## @modulecontract
## @purpose Provide subscript text annotation — marks text rendered below the baseline.
## @scope Text annotation for subscript formatting.
## @input Subscript boolean value ("True"/"False").
## @output SubscriptAnnotation instance.
## @links [INHERITS(9): Annotation]
## @invariants
## - value is always "True" or "False"
## @rationale
## Q: Why use string boolean rather than native bool?
## A: Annotation.value is str-typed for uniform serialization across all annotation types.
## @changes
## LAST_CHANGE: [v1.0.0 – Added semantic markup and LDD logging]
## @modulemap
## CLASS 10[Subscript text annotation] => SubscriptAnnotation
## @usecases
## - [SubscriptAnnotation]: Reader → ExtractSubscriptFormatting → SubscriptAnnotationStored
def _module_contract():
    pass
# endregion MODULE_CONTRACT
# GREP_SUMMARY: subscript, annotation, text, formatting, document, font, baseline, boolean
# STRUCTURE: ▶ Init [start, end, value] → ◇ bool(value) check → ⊕ super().__init__(name="subscript") → ⎋ SubscriptAnnotation
