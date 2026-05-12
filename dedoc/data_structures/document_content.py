import logging
from typing import List, Optional

from dedoc.api.schema.document_content import DocumentContent as ApiDocumentContent
from dedoc.data_structures.serializable import Serializable
from dedoc.data_structures.table import Table
from dedoc.data_structures.tree_node import TreeNode

logger = logging.getLogger(__name__)


# region CLASS_DocumentContent [DOMAIN(9): DocumentProcessing, DataStructures; CONCEPT(10): Document, Content; TECH(6): Python, API]
## @purpose Hold the structured document content — tree-structured text (TreeNode) and list of tables, plus warnings.
class DocumentContent(Serializable):
    """
    This class holds the document content - structured text and tables.

    :ivar tables: list of document tables
    :ivar structure: tree structure of the document nodes with text and additional metadata
    :ivar warnings: list of warnings, obtained in the process of the document parsing

    :vartype tables: List[Table]
    :vartype structure: TreeNode
    :vartype warnings: List[str]
    """

    # region METHOD___init__ [DOMAIN(9): DocumentProcessing; CONCEPT(10): Document; TECH(6): Python]
    ## @purpose Initialize document content with tables, tree structure, and optional warnings.
    ## @io (List[Table], TreeNode, Optional[List[str]]) -> None
    ## @complexity 2
    def __init__(self, tables: List[Table], structure: TreeNode, warnings: Optional[List[str]] = None) -> None:
        """
        :param tables: list of document tables
        :param structure: tree structure in which content of the document is organized
        :param warnings: list of warnings
        """
        logger.debug(f"[IMP:4][DocumentContent][INIT] tables_count={len(tables)}, warnings_count={len(warnings) if warnings else 0}")
        self.tables: List[Table] = tables
        self.structure: TreeNode = structure
        self.warnings: List[str] = warnings if warnings is not None else []
        logger.info(f"[IMP:9][DocumentContent][RESULT] DocumentContent initialized with {len(self.tables)} tables and {len(self.warnings)} warnings")
    # endregion METHOD___init__

    # region METHOD_to_api_schema [DOMAIN(9): DocumentProcessing; CONCEPT(8): Serialization; TECH(6): API]
    ## @purpose Convert document content to API schema, serializing structure and tables recursively.
    ## @uses ApiDocumentContent
    ## @io None -> ApiDocumentContent
    ## @complexity 4
    def to_api_schema(self) -> ApiDocumentContent:
        logger.debug(f"[IMP:4][DocumentContent][TO_API] Converting to API schema")
        structure = self.structure.to_api_schema()
        tables = [table.to_api_schema() for table in self.tables]
        return ApiDocumentContent(structure=structure, tables=tables)
    # endregion METHOD_to_api_schema
# endregion CLASS_DocumentContent

# region MODULE_CONTRACT [DOMAIN(9): DocumentProcessing, DataStructures; CONCEPT(10): Document, Content; TECH(6): Python, API]
## @modulecontract
## @purpose Define the DocumentContent data structure — the primary container for a document's parsed text (as a tree) and tables.
## @scope Structured document content: text tree, tables, warnings.
## @input Tables list, TreeNode root, optional warnings.
## @output DocumentContent instance convertible to API schema.
## @links [INHERITS(5): Serializable, USES_API(8): ApiDocumentContent, READS_DATA_FROM(9): Table, TreeNode]
## @invariants
## - warnings is never None (defaults to empty list)
## @rationale
## Q: Why separate tables from the text tree structure?
## A: Tables have a fundamentally different data model (grid vs tree), and keeping them separate simplifies both storage and API representation.
## @changes
## LAST_CHANGE: [v1.0.0 – Added semantic markup and LDD logging]
## @modulemap
## CLASS 10[Document content container] => DocumentContent
## METHOD 6[Constructor] => __init__
## METHOD 8[API schema conversion] => to_api_schema
## @usecases
## - [DocumentContent]: StructureConstructor → BuildDocumentContent → DocumentContentReturned
def _module_contract():
    pass
# endregion MODULE_CONTRACT
# GREP_SUMMARY: DocumentContent, document, content, structure, tables, TreeNode, tree, warnings, API, serializable
# STRUCTURE: ▶ DocumentContent ┌tables[], TreeNode, warnings[]┐ → ⊕ to_api_schema (recursive: structure + tables) → ⎋ ApiDocumentContent
