import logging
from typing import List, Optional

from dedoc.api.schema.cell_with_meta import CellWithMeta as ApiCellWithMeta
from dedoc.data_structures.annotation import Annotation
from dedoc.data_structures.line_with_meta import LineWithMeta
from dedoc.data_structures.serializable import Serializable

logger = logging.getLogger(__name__)


# region CLASS_CellWithMeta [DOMAIN(9): DocumentProcessing, DataStructures; CONCEPT(9): Table, Cell; TECH(6): Python, API]
## @purpose Hold information about a table cell: list of text lines, colspan, rowspan, and visibility flag.
class CellWithMeta(Serializable):
    """
    This class holds the information about the cell: list of lines and cell properties (rowspan, colspan, invisible).

    :ivar lines: list of textual lines of the cell
    :ivar colspan: number of columns to span (for cells merged horizontally)
    :ivar rowspan: number of rows to span (for cells merged vertically)
    :ivar invisible: indicator for displaying or hiding cell text - cells that are merged with others are hidden (for HTML display)

    :vartype lines: List[LineWithMeta]
    :vartype colspan: int
    :vartype rowspan: int
    :vartype invisible: bool
    """

    # region METHOD___init__ [DOMAIN(9): DocumentProcessing; CONCEPT(9): Table; TECH(6): Python]
    ## @purpose Initialize cell with optional lines list, colspan, rowspan, and visibility.
    ## @io (Optional[List[LineWithMeta]], int, int, bool) -> None
    ## @complexity 2
    def __init__(self, lines: Optional[List[LineWithMeta]], colspan: int = 1, rowspan: int = 1, invisible: bool = False) -> None:
        """
        :param lines: textual lines of the cell
        :param colspan: number of columns to span like in HTML format
        :param rowspan: number of rows to span like in HTML format
        :param invisible: indicator for displaying or hiding cell text
        """
        logger.debug(f"[IMP:4][CellWithMeta][INIT] colspan={colspan}, rowspan={rowspan}, invisible={invisible}, lines_count={len(lines) if lines else 0}")
        self.lines: List[LineWithMeta] = [] if lines is None else lines
        self.colspan: int = colspan
        self.rowspan: int = rowspan
        self.invisible: bool = invisible
        logger.debug(f"[IMP:4][CellWithMeta][INIT] CellWithMeta created")
    # endregion METHOD___init__

    # region METHOD___repr__ [DOMAIN(9): DocumentProcessing; CONCEPT(5): Display; TECH(5): Python]
    ## @purpose Return repr showing first 65 chars of cell text.
    ## @io None -> str
    ## @complexity 1
    def __repr__(self) -> str:
        return f"CellWithMeta({self.get_text()[:65]})"
    # endregion METHOD___repr__

    # region METHOD_get_text [DOMAIN(9): DocumentProcessing; CONCEPT(8): TextExtraction; TECH(5): Python]
    ## @purpose Get merged text of all cell lines joined by newline.
    ## @io None -> str
    ## @complexity 2
    def get_text(self) -> str:
        """
        Get merged text of all cell lines
        """
        return "\n".join([line.line for line in self.lines])
    # endregion METHOD_get_text

    # region METHOD_get_annotations [DOMAIN(9): DocumentProcessing; CONCEPT(8): AnnotationExtraction; TECH(6): Python]
    ## @purpose Get merged annotations of all cell lines with positions adjusted for the merged text.
    ## @uses LineWithMeta.join
    ## @io None -> List[Annotation]
    ## @complexity 4
    def get_annotations(self) -> List[Annotation]:
        """
        Get merged annotations of all cell lines (start/end of annotations moved according to the merged text)
        """
        logger.debug(f"[IMP:4][CellWithMeta][GET_ANNOTATIONS] Merging annotations from {len(self.lines)} lines")
        result = LineWithMeta.join(lines=self.lines, delimiter="\n").annotations
        logger.debug(f"[IMP:4][CellWithMeta][GET_ANNOTATIONS] Got {len(result)} merged annotations")
        return result
    # endregion METHOD_get_annotations

    # region METHOD___str__ [DOMAIN(9): DocumentProcessing; CONCEPT(5): Display; TECH(5): Python]
    ## @purpose Return string representation with colspan, rowspan, and text.
    ## @io None -> str
    ## @complexity 1
    def __str__(self) -> str:
        return f"CellWithMeta(cs={self.colspan}, rs={self.rowspan}, {self.get_text()})"
    # endregion METHOD___str__

    # region METHOD_to_api_schema [DOMAIN(9): DocumentProcessing; CONCEPT(8): Serialization; TECH(6): API]
    ## @purpose Convert cell to API schema, serializing lines and ensuring numpy int types.
    ## @uses ApiCellWithMeta, numpy
    ## @io None -> ApiCellWithMeta
    ## @complexity 4
    def to_api_schema(self) -> ApiCellWithMeta:
        import numpy as np

        logger.debug(f"[IMP:4][CellWithMeta][TO_API] Converting cell to API schema")
        lines = [line.to_api_schema() for line in self.lines]
        return ApiCellWithMeta(lines=lines, colspan=int(np.int8(self.colspan)), rowspan=int(np.int8(self.rowspan)), invisible=self.invisible)
    # endregion METHOD_to_api_schema
# endregion CLASS_CellWithMeta

# region MODULE_CONTRACT [DOMAIN(9): DocumentProcessing, DataStructures; CONCEPT(9): Table, Cell; TECH(6): Python, API]
## @modulecontract
## @purpose Define the CellWithMeta data structure — represents a single table cell with text lines, merge spans, and visibility.
## @scope Table cell data: lines, colspan, rowspan, annotations, serialization.
## @input Lines list, colspan, rowspan, invisible flag.
## @output CellWithMeta instance convertible to API schema.
## @links [INHERITS(5): Serializable, USES_API(8): ApiCellWithMeta, READS_DATA_FROM(9): LineWithMeta]
## @invariants
## - lines is never None (defaults to empty list)
## - colspan >= 1, rowspan >= 1
## @rationale
## Q: Why use colspan/rowspan rather than pre-expanded cells?
## A: This preserves the original table structure information, allowing the consumer to decide how to flatten/display.
## @changes
## LAST_CHANGE: [v1.0.0 – Added semantic markup and LDD logging]
## @modulemap
## CLASS 10[Table cell with metadata] => CellWithMeta
## METHOD 6[Get merged text] => get_text
## METHOD 7[Merge annotations] => get_annotations
## METHOD 8[API schema conversion] => to_api_schema
## @usecases
## - [CellWithMeta]: TableReader → CreateCell → CellWithMetaStoredInTable
def _module_contract():
    pass
# endregion MODULE_CONTRACT
# GREP_SUMMARY: CellWithMeta, cell, table, colspan, rowspan, invisible, lines, annotations, LineWithMeta, API
# STRUCTURE: ▶ CellWithMeta ┌lines?, colspan, rowspan, invisible┐ → ⊕ get_text (join lines) → ⊕ get_annotations (LineWithMeta.join) → ⊕ to_api_schema → ⎋ ApiCellWithMeta
