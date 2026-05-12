import logging

from dedoc.data_structures.annotation import Annotation

logger = logging.getLogger(__name__)


# region CLASS_TableAnnotation [DOMAIN(4): DocumentProcessing; CONCEPT(5): TextAnnotation, Table; TECH(3): DataStructure]
## @purpose Indicate the place of the table in the original document. The line containing this annotation is placed directly before the referred table.
class TableAnnotation(Annotation):
    """
    This annotation indicate the place of the table in the original document.
    The line containing this annotation is placed directly before the referred table.
    """
    name = "table"

    # region METHOD___init__ [DOMAIN(4): DocumentProcessing; CONCEPT(5): TextAnnotation; TECH(3): DataStructure]
    ## @purpose Initialize table annotation with table UID reference.
    ## @uses Annotation.__init__
    ## @io (str, int, int) -> None
    ## @complexity 2
    def __init__(self, value: str, start: int, end: int) -> None:
        """
        :param value: unique identifier of the table which is referenced inside this annotation
        :param start: start of the annotated text (usually zero)
        :param end: end of the annotated text (usually end of the line)
        """
        logger.debug(f"[IMP:4][TableAnnotation][INIT] value={value}, start={start}, end={end}")
        super().__init__(start=start, end=end, name=TableAnnotation.name, value=value, is_mergeable=False)
        logger.debug(f"[IMP:4][TableAnnotation][INIT] TableAnnotation created successfully")
    # endregion METHOD___init__
# endregion CLASS_TableAnnotation

# region MODULE_CONTRACT [DOMAIN(4): DocumentProcessing; CONCEPT(5): TextAnnotation, Table; TECH(3): DataStructure, Python]
## @modulecontract
## @purpose Provide table reference annotation — marks where a table is placed in the document via its UID.
## @scope Text annotation for table placement references.
## @input Table UID string.
## @output TableAnnotation instance with is_mergeable=False.
## @links [INHERITS(9): Annotation]
## @invariants
## - is_mergeable is always False
## @rationale
## Q: Why is_mergeable=False?
## A: Each table reference is unique and should not be merged with others.
## @changes
## LAST_CHANGE: [v1.0.0 – Added semantic markup and LDD logging]
## @modulemap
## CLASS 10[Table reference annotation] => TableAnnotation
## @usecases
## - [TableAnnotation]: Reader → MarkTablePlacement → TableAnnotationStored
def _module_contract():
    pass
# endregion MODULE_CONTRACT
# GREP_SUMMARY: table, annotation, text, document, reference, uid, placement
# STRUCTURE: ▶ Init [value, start, end] → ⊕ super().__init__(name="table", is_mergeable=False) → ⎋ TableAnnotation
