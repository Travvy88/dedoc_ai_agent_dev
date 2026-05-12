import logging

from dedoc.data_structures.annotation import Annotation

logger = logging.getLogger(__name__)


# region CLASS_LinkedTextAnnotation [DOMAIN(4): DocumentProcessing; CONCEPT(5): TextAnnotation, LinkedText; TECH(3): DataStructure]
## @purpose Link some text to a line or its part (e.g. footnote text linked to a reference number).
class LinkedTextAnnotation(Annotation):
    """
    This annotation is used when some text is linked to the line or its part.
    For example, line can contain a number that refers the footnote - the text of this footnote will be the value of this annotation.
    """
    name = "linked_text"

    # region METHOD___init__ [DOMAIN(4): DocumentProcessing; CONCEPT(5): TextAnnotation; TECH(3): DataStructure]
    ## @purpose Initialize linked text annotation with the linked text value.
    ## @uses Annotation.__init__
    ## @io (int, int, str) -> None
    ## @complexity 2
    def __init__(self, start: int, end: int, value: str) -> None:
        """
        :param start: start of the annotated text
        :param end: end of the annotated text (not included)
        :param value: text, linked to given one, for example text of the footnote
        """
        logger.debug(f"[IMP:4][LinkedTextAnnotation][INIT] start={start}, end={end}, value={value[:50]}...")
        super().__init__(start=start, end=end, name=LinkedTextAnnotation.name, value=value, is_mergeable=False)
        logger.debug(f"[IMP:4][LinkedTextAnnotation][INIT] LinkedTextAnnotation created successfully")
    # endregion METHOD___init__
# endregion CLASS_LinkedTextAnnotation

# region MODULE_CONTRACT [DOMAIN(4): DocumentProcessing; CONCEPT(5): TextAnnotation, LinkedText; TECH(3): DataStructure, Python]
## @modulecontract
## @purpose Provide linked text annotation — associates a text reference (e.g. footnote) with a position in the document.
## @scope Text annotation for linked text references.
## @input Linked text string.
## @output LinkedTextAnnotation instance with is_mergeable=False.
## @links [INHERITS(9): Annotation]
## @invariants
## - is_mergeable is always False
## @rationale
## Q: Why is_mergeable=False?
## A: Each linked text reference is unique and should not be merged.
## @changes
## LAST_CHANGE: [v1.0.0 – Added semantic markup and LDD logging]
## @modulemap
## CLASS 10[Linked text annotation] => LinkedTextAnnotation
## @usecases
## - [LinkedTextAnnotation]: Reader → LinkTextToAnnotation → LinkedTextAnnotationStored
def _module_contract():
    pass
# endregion MODULE_CONTRACT
# GREP_SUMMARY: linked, text, annotation, footnote, reference, document, line
# STRUCTURE: ▶ Init [start, end, value] → ⊕ super().__init__(name="linked_text", is_mergeable=False) → ⎋ LinkedTextAnnotation
