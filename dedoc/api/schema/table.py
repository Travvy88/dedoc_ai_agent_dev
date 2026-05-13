# region MODULE_CONTRACT [DOMAIN(9): DocumentProcessing, TableModel; CONCEPT(8): TableStructure, GridData; TECH(7): Pydantic, BaseModel]
## @modulecontract
## @purpose Define the Table schema — a Pydantic model for a document table with row-based cell grid and table-level metadata.
## @scope Document table data model.
## @input None (standalone model, references CellWithMeta, TableMetadata).
## @output Pydantic BaseModel `Table` with cells (List[List[CellWithMeta]]) and metadata (TableMetadata).
## @links [USES_API(7): pydantic.BaseModel; READS_DATA_FROM(8): CellWithMeta, TableMetadata]
## @invariants
## - cells grid is rectangular (all rows have equal column count).
## - metadata.uid uniquely identifies the table within the document.
## @rationale
## Q: Why row-based cell storage?
## A: Matches natural document table layout and simplifies HTML rendering (iterate rows, then cells).
## @changes
## LAST_CHANGE: [v1.0.0 – Initial creation with semantic markup]
## @modulemap
## CLASS 9[Document table with cell grid and metadata] => Table
## @usecases
## - [Table]: TableExtractor => PopulateCellGrid => RenderOrQueryTable
def _module_contract():
    pass
# endregion MODULE_CONTRACT
# GREP_SUMMARY: table, cells, grid, metadata, colspan, rowspan, Pydantic, schema, document, CellWithMeta
# STRUCTURE: ▶ Pydantic BaseModel → Table ┌cells:List[List[CellWithMeta]], metadata:TableMetadata┐ → ⎋ JSON

import logging
from typing import List

from pydantic import BaseModel, Field

from dedoc.api.schema.cell_with_meta import CellWithMeta
from dedoc.api.schema.table_metadata import TableMetadata

logger = logging.getLogger(__name__)

# region CLASS_Table [DOMAIN(9): DocumentProcessing; CONCEPT(8): TableStructure; TECH(7): PydanticBaseModel]
## @purpose Represent a document table as a rectangular grid of cells (row-based) with associated table-level metadata (UID, title, page).
## @io (cells, metadata) -> JSON serializable model
class Table(BaseModel):
    """
    Holds information about tables in the document.
    We assume that a table has rectangle form (has the same number of columns in each row).
    Table representation is row-based i.e. external list contains list of rows.

    :ivar metadata: a list of lists of table cells (cell has text lines, colspan and rowspan attributes)
    :ivar cells: table metadata as location, title and so on

    :vartype metadata: TableMetadata
    :vartype cells: List[List[CellWithMeta]]
    """
    cells: List[List[CellWithMeta]] = Field(description="List of lists of table cells (cell has text, colspan and rowspan attributes)")
    metadata: TableMetadata = Field(description="Table meta information")
# endregion CLASS_Table
