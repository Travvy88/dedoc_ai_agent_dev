import logging

from dedoc.data_structures.annotation import Annotation

logger = logging.getLogger(__name__)


# region CLASS_ItalicAnnotation [DOMAIN(4): DocumentProcessing; CONCEPT(5): TextAnnotation, Italic; TECH(3): DataStructure]
## @purpose Mark italic text inside the line.
class ItalicAnnotation(Annotation):
    """
    Text written in italic inside the line.
    """
    name = "italic"
    valid_values = ["True", "False"]

    # region METHOD___init__ [DOMAIN(4): DocumentProcessing; CONCEPT(5): TextAnnotation; TECH(3): DataStructure]
    ## @purpose Initialize italic annotation with validated boolean value.
    ## @uses Annotation.__init__
    ## @io (int, int, str) -> None
    ## @complexity 3
    def __init__(self, start: int, end: int, value: str) -> None:
        """
        :param start: start of the italic text
        :param end: end of the italic text (not included)
        :param value: True if italic else False (False usually isn't used because you may not use this annotation at all)
        """
        logger.debug(f"[IMP:4][ItalicAnnotation][INIT] start={start}, end={end}, value={value}")
        try:
            bool(value)
        except ValueError:
            raise ValueError("the value of italic annotation should be True or False")
        super().__init__(start=start, end=end, name=ItalicAnnotation.name, value=value)
        logger.debug(f"[IMP:4][ItalicAnnotation][INIT] ItalicAnnotation created successfully")
    # endregion METHOD___init__
# endregion CLASS_ItalicAnnotation

# region MODULE_CONTRACT [DOMAIN(4): DocumentProcessing; CONCEPT(5): TextAnnotation, Italic; TECH(3): DataStructure, Python]
## @modulecontract
## @purpose Provide italic text annotation — marks which portion of text is rendered in italic.
## @scope Text annotation for italic formatting.
## @input Italic boolean value ("True"/"False").
## @output ItalicAnnotation instance.
## @links [INHERITS(9): Annotation]
## @invariants
## - value is always "True" or "False"
## @rationale
## Q: Why use string boolean rather than native bool?
## A: Annotation.value is str-typed for uniform serialization across all annotation types.
## @changes
## LAST_CHANGE: [v1.0.0 – Added semantic markup and LDD logging]
## @modulemap
## CLASS 10[Italic text annotation] => ItalicAnnotation
## @usecases
## - [ItalicAnnotation]: Reader → ExtractItalicFormatting → ItalicAnnotationStored
def _module_contract():
    pass
# endregion MODULE_CONTRACT
# GREP_SUMMARY: italic, annotation, text, formatting, document, font, boolean
# STRUCTURE: ▶ Init [start, end, value] → ◇ bool(value) check → ⊕ super().__init__(name="italic") → ⎋ ItalicAnnotation
