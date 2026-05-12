# region MODULE_CONTRACT [DOMAIN(9): DocumentProcessing, TreeStructure; CONCEPT(8): HierarchicalContent, DocumentTree; TECH(7): Pydantic, BaseModel]
## @modulecontract
## @purpose Define the TreeNode schema — a recursive Pydantic model for document hierarchical structure: each node has text, annotations, metadata, and child nodes.
## @scope Document tree structure model — recursive node hierarchy.
## @input None (standalone model, references Annotation, LineMetadata).
## @output Pydantic BaseModel `TreeNode` with node_id, text, annotations, metadata, subparagraphs.
## @links [USES_API(7): pydantic.BaseModel; READS_DATA_FROM(8): Annotation, LineMetadata]
## @invariants
## - node_id is unique within the document tree (dot-separated path like "0.2.1").
## - subparagraphs is always a list (empty for leaf nodes).
## - The tree forms a valid DAG (no cycles).
## @rationale
## Q: Why recursive TreeNode instead of flat list with parent references?
## A: Recursive structure mirrors document structure naturally and simplifies JSON serialization. Tree traversal is idiomatic in API consumers.
## @changes
## LAST_CHANGE: [v1.0.0 – Initial creation with semantic markup]
## @modulemap
## CLASS 10[Recursive tree node for document hierarchy] => TreeNode
## @usecases
## - [TreeNode]: StructureConstructor => BuildDocumentTree => SerializeAsJSON
def _module_contract():
    pass
# endregion MODULE_CONTRACT
# GREP_SUMMARY: tree, node, recursive, hierarchy, subparagraphs, document, structure, Pydantic, schema, TreeNode
# STRUCTURE: ▶ Pydantic BaseModel → TreeNode ┌node_id:str, text:str, annotations:List[Annotation], metadata:LineMetadata, subparagraphs:List[TreeNode]┐ → ⎋ JSON

import logging
from typing import List

from pydantic import BaseModel, Field

from dedoc.api.schema.annotation import Annotation
from dedoc.api.schema.line_metadata import LineMetadata

logger = logging.getLogger(__name__)

# region CLASS_TreeNode [DOMAIN(9): DocumentProcessing; CONCEPT(8): DocumentTree; TECH(7): PydanticBaseModel]
## @purpose Recursive tree node representing document hierarchical structure: each node holds text, annotations, metadata, and children for nested sections.
## @io (node_id, text, annotations, metadata, subparagraphs) -> JSON serializable model
class TreeNode(BaseModel):
    """
    Helps to represent document as recursive tree structure.
    It has list of children `TreeNode` nodes (empty list for a leaf node).

    :ivar node_id: unique node identifier
    :ivar text: text of the node (may contain several lines)
    :ivar annotations: some metadata related to the part of the text (as font size)
    :ivar metadata: metadata refers to entire node (as node type)
    :ivar subparagraphs: list of child of this node

    :vartype node_id: str
    :vartype text: str
    :vartype annotations: List[Annotation]
    :vartype metadata: LineMetadata
    :vartype subparagraphs: List[TreeNode]
    """
    node_id: str = Field(description="Document element identifier. It is unique within a document content tree. "
                                     "The identifier consists of numbers separated by dots where each number "
                                     "means node's number among nodes with the same level in the document hierarchy.)", example="0.2.1")
    text: str = Field(description="Text of the node", example="Some text")
    annotations: List[Annotation] = Field(description="Some metadata related to the part of the text (as font size)")
    metadata: LineMetadata = Field(description="Metadata for the entire node (as node type)")
    subparagraphs: List["TreeNode"] = Field(description="List of children of this node, each child is `TreeNode`")
# endregion CLASS_TreeNode
