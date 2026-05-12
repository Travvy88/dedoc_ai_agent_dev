# region MODULE_CONTRACT [DOMAIN(9): DocumentProcessing, DocumentContent; CONCEPT(8): ContentStructure, TreeRepresentation; TECH(7): Pydantic, BaseModel]
## @modulecontract
## @purpose Define the DocumentContent schema — the core container for parsed document content: a tree structure of text nodes and a list of tables.
## @scope Document content data model — structure and tables.
## @input None (standalone model, references TreeNode and Table).
## @output Pydantic BaseModel `DocumentContent` with structure (TreeNode) and tables (List[Table]).
## @links [USES_API(7): pydantic.BaseModel; READS_DATA_FROM(8): TreeNode, Table]
## @invariants
## - structure is always a valid TreeNode (root of document tree).
## - tables list may be empty but never None.
## @rationale
## Q: Why separate structure from tables?
## A: Tables have fundamentally different layout (grid vs. tree). Separating them allows specialized rendering and querying.
## @changes
## LAST_CHANGE: [v1.0.0 – Initial creation with semantic markup]
## @modulemap
## CLASS 10[Document content container — tree + tables] => DocumentContent
## @usecases
## - [DocumentContent]: APIResponseBuilder => SerializeContent => ReturnParsedDocumentJSON
def _module_contract():
    pass
# endregion MODULE_CONTRACT
# GREP_SUMMARY: document, content, structure, tree, tables, Pydantic, schema, TreeNode, Table
# STRUCTURE: ▶ Pydantic BaseModel → DocumentContent ┌structure:TreeNode (root), tables:List[Table]┐ → ⎋ JSON

import logging
from typing import List

from pydantic import BaseModel, Field

from dedoc.api.schema.table import Table
from dedoc.api.schema.tree_node import TreeNode

logger = logging.getLogger(__name__)

# region CLASS_DocumentContent [DOMAIN(9): DocumentProcessing; CONCEPT(8): DocumentContent; TECH(7): PydanticBaseModel]
## @purpose Container for the full parsed document content: a hierarchical tree of text nodes and a flat list of tables with their cells.
## @io (structure, tables) -> JSON serializable model
class DocumentContent(BaseModel):
    """
    Content of the document - structured text and tables.

    :ivar tables: list of document tables
    :ivar structure: tree structure of the document nodes with text and additional metadata

    :vartype tables: List[Table]
    :vartype structure: TreeNode
    """
    structure: TreeNode = Field(description="Tree structure where content of the document is organized")
    tables: List[Table] = Field(description="List of document tables")
# endregion CLASS_DocumentContent
