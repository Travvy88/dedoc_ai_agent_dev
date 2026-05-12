# region MODULE_CONTRACT [DOMAIN(9): DocumentProcessing, TableCell; CONCEPT(7): CellMetadata, TableStructure; TECH(7): Pydantic, BaseModel]
## @modulecontract
## @purpose Define the CellWithMeta schema — a Pydantic model for a single table cell containing text lines and HTML-like cell properties (colspan, rowspan).
## @scope Table cell data model for document tables.
## @input None (standalone model, references LineWithMeta).
## @output Pydantic BaseModel `CellWithMeta` with lines, colspan, rowspan, invisible fields.
## @links [USES_API(7): pydantic.BaseModel; READS_DATA_FROM(8): LineWithMeta]
## @invariants
## - colspan >= 1, rowspan >= 1.
## - lines is never empty for visible cells (invisible=False).
## @rationale
## Q: Why model cells as having multiple LineWithMeta lines?
## A: A single table cell can contain multiple lines of text with individual annotations, mirroring real document structure.
## @changes
## LAST_CHANGE: [v1.0.0 – Initial creation with semantic markup]
## @modulemap
## CLASS 9[Table cell with text lines and span attributes] => CellWithMeta
## @usecases
## - [CellWithMeta]: TableRenderer => IterateCells => RenderHTMLTableCell
def _module_contract():
    pass
# endregion MODULE_CONTRACT
# GREP_SUMMARY: cell, table, colspan, rowspan, invisible, lines, Pydantic, schema, HTML
# STRUCTURE: ▶ Pydantic BaseModel → CellWithMeta ┌lines:List[LineWithMeta], rowspan:int, colspan:int, invisible:bool┐ → ⎋ JSON

import logging
from typing import List

from pydantic import BaseModel, Field

from dedoc.api.schema.line_with_meta import LineWithMeta

logger = logging.getLogger(__name__)

# region CLASS_CellWithMeta [DOMAIN(9): DocumentProcessing; CONCEPT(7): TableCell; TECH(7): PydanticBaseModel]
## @purpose Represent a single table cell with its text lines and HTML-like spanning properties for correct table rendering.
## @io (lines, rowspan, colspan, invisible) -> JSON serializable model
class CellWithMeta(BaseModel):
    """
    Holds the information about the cell: list of lines and cell properties (rowspan, colspan, invisible).

    :ivar lines: list of textual lines of the cell
    :ivar colspan: number of columns to span (for cells merged horizontally)
    :ivar rowspan: number of rows to span (for cells merged vertically)
    :ivar invisible: indicator for displaying or hiding cell text - cells that are merged with others are hidden (for HTML display)

    :vartype lines: List[LineWithMeta]
    :vartype colspan: int
    :vartype rowspan: int
    :vartype invisible: bool
    """
    lines: List[LineWithMeta] = Field(description="Textual lines of the cell with annotations")
    rowspan: int = Field(description="Number of rows to span like in HTML format", example=1)
    colspan: int = Field(description="Number of columns to span like in HTML format", example=2)
    invisible: bool = Field(description="Indicator for displaying or hiding cell text", example=False)
# endregion CLASS_CellWithMeta
