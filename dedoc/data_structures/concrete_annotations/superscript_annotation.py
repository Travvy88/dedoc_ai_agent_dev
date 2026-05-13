import logging

from dedoc.data_structures.annotation import Annotation

logger = logging.getLogger(__name__)


# region CLASS_SuperscriptAnnotation [DOMAIN(4): DocumentProcessing; CONCEPT(5): TextAnnotation, Superscript; TECH(3): DataStructure]
## @purpose Mark superscript text inside the line.
class SuperscriptAnnotation(Annotation):
    """
    Superscript text inside the line.
    """
    name = "superscript"
    valid_values = ["True", "False"]

    # region METHOD___init__ [DOMAIN(4): DocumentProcessing; CONCEPT(5): TextAnnotation; TECH(3): DataStructure]
    ## @purpose Initialize superscript annotation with validated boolean value.
    ## @uses Annotation.__init__
    ## @io (int, int, str) -> None
    ## @complexity 3
    def __init__(self, start: int, end: int, value: str) -> None:
        """
        :param start: start of the superscript text
        :param end: end of the superscript text (not included)
        :param value: True if superscript else False (False usually isn't used because you may not use this annotation at all)
        """
        logger.debug(f"[IMP:4][SuperscriptAnnotation][INIT] start={start}, end={end}, value={value}")
        try:
            bool(value)
        except ValueError:
            raise ValueError("the value of superscript annotation should be True or False")
        super().__init__(start=start, end=end, name=SuperscriptAnnotation.name, value=value)
        logger.debug(f"[IMP:4][SuperscriptAnnotation][INIT] SuperscriptAnnotation created successfully")
    # endregion METHOD___init__
# endregion CLASS_SuperscriptAnnotation

# region MODULE_CONTRACT [DOMAIN(4): DocumentProcessing; CONCEPT(5): TextAnnotation, Superscript; TECH(3): DataStructure, Python]
## @modulecontract
## @purpose Provide superscript text annotation — marks text rendered above the baseline.
## @scope Text annotation for superscript formatting.
## @input Superscript boolean value ("True"/"False").
## @output SuperscriptAnnotation instance.
## @links [INHERITS(9): Annotation]
## @invariants
## - value is always "True" or "False"
## @rationale
## Q: Why use string boolean rather than native bool?
## A: Annotation.value is str-typed for uniform serialization across all annotation types.
## @changes
## LAST_CHANGE: [v1.0.0 – Added semantic markup and LDD logging]
## @modulemap
## CLASS 10[Superscript text annotation] => SuperscriptAnnotation
## @usecases
## - [SuperscriptAnnotation]: Reader → ExtractSuperscriptFormatting → SuperscriptAnnotationStored
def _module_contract():
    pass
# endregion MODULE_CONTRACT
# GREP_SUMMARY: superscript, annotation, text, formatting, document, font, baseline, boolean
# STRUCTURE: ▶ Init [start, end, value] → ◇ bool(value) check → ⊕ super().__init__(name="superscript") → ⎋ SuperscriptAnnotation
