import logging
from typing import List

from dedoc.api.schema.table import Table as ApiTable
from dedoc.data_structures.cell_with_meta import CellWithMeta
from dedoc.data_structures.serializable import Serializable
from dedoc.data_structures.table_metadata import TableMetadata

logger = logging.getLogger(__name__)


# region CLASS_Table [DOMAIN(9): DocumentProcessing, DataStructures; CONCEPT(10): Table; TECH(6): Python, API]
## @purpose Hold a complete table — row-based list of cells and table-level metadata. Assumes rectangular form with colspan/rowspan for merges.
class Table(Serializable):
    """
    This class holds information about tables in the document.
    We assume that a table has rectangle form (has the same number of columns in each row).
    If some cells are merged, they are duplicated and information about merge is stored in rowspan and colspan.
    Table representation is row-based i.e. external list contains list of rows.

    :ivar metadata: a list of lists of table cells (cell has text lines, colspan and rowspan attributes)
    :ivar cells: table metadata as location, title and so on

    :vartype metadata: TableMetadata
    :vartype cells: List[List[CellWithMeta]]
    """

    # region METHOD___init__ [DOMAIN(9): DocumentProcessing; CONCEPT(10): Table; TECH(6): Python]
    ## @purpose Initialize table with cells (list of cell rows) and table metadata.
    ## @io (List[List[CellWithMeta]], TableMetadata) -> None
    ## @complexity 2
    def __init__(self, cells: List[List[CellWithMeta]], metadata: TableMetadata) -> None:
        """
        :param cells: a list of lists of cells
        :param metadata: table metadata
        """
        logger.debug(f"[IMP:4][Table][INIT] rows={len(cells)}, uid={metadata.uid}")
        self.metadata: TableMetadata = metadata
        self.cells: List[List[CellWithMeta]] = cells
        logger.debug(f"[IMP:4][Table][INIT] Table created: {len(cells)} rows")
    # endregion METHOD___init__

    # region METHOD_to_api_schema [DOMAIN(9): DocumentProcessing; CONCEPT(8): Serialization; TECH(6): API]
    ## @purpose Convert table to API schema, serializing all cells recursively.
    ## @uses ApiTable
    ## @io None -> ApiTable
    ## @complexity 3
    def to_api_schema(self) -> ApiTable:
        logger.debug(f"[IMP:4][Table][TO_API] Converting table with {len(self.cells)} rows to API schema")
        cells = [[cell.to_api_schema() for cell in row] for row in self.cells]
        return ApiTable(cells=cells, metadata=self.metadata.to_api_schema())
    # endregion METHOD_to_api_schema
# endregion CLASS_Table

# region MODULE_CONTRACT [DOMAIN(9): DocumentProcessing, DataStructures; CONCEPT(10): Table; TECH(6): Python, API]
## @modulecontract
## @purpose Define the Table data structure — row-based table representation with cells, merge spans, and metadata.
## @scope Table with row-major cell grid and table-level metadata.
## @input 2D cell list and TableMetadata.
## @output Table instance convertible to API schema.
## @links [INHERITS(5): Serializable, USES_API(8): ApiTable, READS_DATA_FROM(9): CellWithMeta, TableMetadata]
## @invariants
## - All rows have the same number of columns (rectangle assumption)
## @rationale
## Q: Why row-based representation?
## A: Row ordering is semantically important for tables; row-based access matches document flow direction.
## @changes
## LAST_CHANGE: [v1.0.0 – Added semantic markup and LDD logging]
## @modulemap
## CLASS 10[Table container] => Table
## METHOD 6[Constructor] => __init__
## METHOD 8[API schema conversion] => to_api_schema
## @usecases
## - [Table]: Reader → ExtractTable → TableStored
## - [Table]: DocumentContent → AssembleContent → TableIncludedInOutput
def _module_contract():
    pass
# endregion MODULE_CONTRACT
# GREP_SUMMARY: Table, table, cells, metadata, row, column, CellWithMeta, TableMetadata, API, serializable
# STRUCTURE: ▶ Table ┌cells[][CellWithMeta], TableMetadata┐ → ⊕ to_api_schema (recursive: cells + metadata) → ⎋ ApiTable
