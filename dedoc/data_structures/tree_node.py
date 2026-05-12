import logging
from typing import List, Optional

from dedoc.api.schema.tree_node import TreeNode as ApiTreeNode
from dedoc.data_structures.annotation import Annotation
from dedoc.data_structures.hierarchy_level import HierarchyLevel
from dedoc.data_structures.line_metadata import LineMetadata
from dedoc.data_structures.line_with_meta import LineWithMeta
from dedoc.data_structures.serializable import Serializable

logger = logging.getLogger(__name__)


# region CLASS_TreeNode [DOMAIN(9): DocumentProcessing, DataStructures; CONCEPT(10): Tree, DocumentStructure; TECH(7): Python, API, AnnotationMerger]
## @purpose Represent document as a recursive tree structure — each node has an ID, text, annotations, metadata, children, and a parent reference.
class TreeNode(Serializable):
    """
    TreeNode helps to represent document as recursive tree structure.
    It has parent node (None for root ot the tree) and list of children nodes (empty list for list node).

    :ivar node_id: unique node identifier
    :ivar text: text of the node (may contain several lines)
    :ivar annotations: some metadata related to the part of the text (as font size)
    :ivar metadata: metadata refers to entire node (as node type)
    :ivar subparagraphs: list of child of this node
    :ivar parent: parent node (None for root, not none for other nodes)

    :vartype node_id: str
    :vartype text: str
    :vartype annotations: List[Annotation]
    :vartype metadata: LineMetadata
    :vartype subparagraphs: List[TreeNode]
    :vartype parent: TreeNode
    """

    # region METHOD___init__ [DOMAIN(9): DocumentProcessing; CONCEPT(10): Tree; TECH(7): Python]
    ## @purpose Initialize tree node with ID, text, annotations, metadata, children, and parent.
    ## @io (str, str, List[Annotation], LineMetadata, List[TreeNode], Optional[TreeNode]) -> None
    ## @complexity 2
    def __init__(self,
                 node_id: str,
                 text: str,
                 annotations: List[Annotation],
                 metadata: LineMetadata,
                 subparagraphs: List["TreeNode"],
                 parent: Optional["TreeNode"]) -> None:
        """
        :param node_id: node id is unique in one document
        :param text: text of the node
        :param annotations: metadata related to the part of the text
        :param metadata: metadata refers to entire node
        :param subparagraphs: list of child of this node
        :param parent: parent node
        """
        logger.debug(f"[IMP:4][TreeNode][INIT] node_id={node_id}, text_len={len(text)}, annotations_count={len(annotations)}, children={len(subparagraphs)}")
        self.node_id: str = node_id
        self.text: str = text
        self.annotations: List[Annotation] = annotations
        self.metadata: LineMetadata = metadata
        self.subparagraphs: List["TreeNode"] = subparagraphs
        self.parent: "TreeNode" = parent
        logger.debug(f"[IMP:4][TreeNode][INIT] TreeNode created: id={self.node_id}")
    # endregion METHOD___init__

    # region METHOD_to_api_schema [DOMAIN(9): DocumentProcessing; CONCEPT(8): Serialization; TECH(6): API]
    ## @purpose Convert tree node to API schema, recursively serializing annotations, metadata, and children.
    ## @uses ApiTreeNode
    ## @io None -> ApiTreeNode
    ## @complexity 3
    def to_api_schema(self) -> ApiTreeNode:
        logger.debug(f"[IMP:4][TreeNode][TO_API] Converting node id={self.node_id} to API schema")
        annotations = [annotation.to_api_schema() for annotation in self.annotations]
        metadata = self.metadata.to_api_schema()
        subparagraphs = [node.to_api_schema() for node in self.subparagraphs]
        return ApiTreeNode(node_id=self.node_id, text=self.text, annotations=annotations, metadata=metadata, subparagraphs=subparagraphs)
    # endregion METHOD_to_api_schema

    # region METHOD_create [DOMAIN(9): DocumentProcessing; CONCEPT(9): Factory; TECH(7): Python]
    ## @purpose Create a root TreeNode from a list of LineWithMeta lines, merging annotations across lines.
    ## @uses LineMetadata, HierarchyLevel, __shift_annotations, __add_additional_page_id
    ## @io List[LineWithMeta] -> TreeNode
    ## @complexity 5
    @staticmethod
    def create(lines: List[LineWithMeta] = None) -> "TreeNode":
        """
        Creates a root node with given text.

        :param lines: this lines should be the title of the document (or should be empty for documents without title)
        :return: root of the document tree
        """
        logger.debug(f"[IMP:4][TreeNode][CREATE] Creating root node from {len(lines) if lines else 0} lines")
        page_id = 0 if len(lines) == 0 else min((line.metadata.page_id for line in lines))
        line_id = 0 if len(lines) == 0 else min((line.metadata.line_id for line in lines))
        metadata = LineMetadata(page_id=page_id, line_id=line_id, hierarchy_level=HierarchyLevel.create_root())

        texts = (line.line for line in lines)
        annotations = []
        text_length = 0
        for line in lines:
            annotations.extend(TreeNode.__shift_annotations(line=line, text_length=text_length))
            TreeNode.__add_additional_page_id(start=text_length, metadata=metadata, other_line=line)

            text_length += len(line.line)
        text = "".join(texts)
        root_node = TreeNode("0", text, annotations=annotations, metadata=metadata, subparagraphs=[], parent=None)
        logger.info(f"[IMP:9][TreeNode][CREATE] Root TreeNode created: id=0, text_len={len(text)}")
        return root_node
    # endregion METHOD_create

    # region METHOD_add_child [DOMAIN(9): DocumentProcessing; CONCEPT(9): TreeManipulation; TECH(6): Python]
    ## @purpose Create a new child TreeNode from a LineWithMeta and append it as a subparagraph.
    ## @io LineWithMeta -> TreeNode
    ## @complexity 3
    def add_child(self, line: LineWithMeta) -> "TreeNode":
        """
        Create a new tree node - children of the given node from given line. Return newly created node.

        :param line: Line with meta, new node will be built from this line
        :return: return created node (child of the self)
        """
        logger.debug(f"[IMP:4][TreeNode][ADD_CHILD] Adding child to node_id={self.node_id}, child_count={len(self.subparagraphs)}")
        new_node = TreeNode(
            node_id=f"{self.node_id}.{len(self.subparagraphs)}",
            text=line.line,
            annotations=line.annotations,
            metadata=line.metadata,
            subparagraphs=[],
            parent=self
        )
        self.subparagraphs.append(new_node)
        logger.debug(f"[IMP:4][TreeNode][ADD_CHILD] Child node created: id={new_node.node_id}")
        return new_node
    # endregion METHOD_add_child

    # region METHOD_add_text [DOMAIN(9): DocumentProcessing; CONCEPT(8): TreeManipulation; TECH(6): Python]
    ## @purpose Append text and annotations from a line to the current node.
    ## @uses __shift_annotations, __add_additional_page_id
    ## @io LineWithMeta -> None
    ## @complexity 3
    def add_text(self, line: LineWithMeta) -> None:
        """
        Add the text and annotations from given line, text is separated with aa len line symbol.

        :param line: line with text to add
        """
        logger.debug(f"[IMP:4][TreeNode][ADD_TEXT] Adding text len={len(line.line)} to node_id={self.node_id}")
        text_length = len(self.text)
        new_annotations = self.__shift_annotations(line, text_length)

        self.__add_additional_page_id(start=len(self.text), metadata=self.metadata, other_line=line)
        self.text += line.line
        self.annotations.extend(new_annotations)
        logger.debug(f"[IMP:4][TreeNode][ADD_TEXT] Node text now len={len(self.text)}")
    # endregion METHOD_add_text

    # region METHOD___shift_annotations [DOMAIN(9): DocumentProcessing; CONCEPT(7): AnnotationShift; TECH(6): Python]
    ## @purpose Shift annotation start/end positions by text_length offset.
    ## @io (LineWithMeta, int) -> List[Annotation]
    ## @complexity 3
    @staticmethod
    def __shift_annotations(line: LineWithMeta, text_length: int) -> List[Annotation]:
        new_annotations = []
        for annotation in line.annotations:
            new_annotation = Annotation(start=annotation.start + text_length, end=annotation.end + text_length, name=annotation.name, value=annotation.value)
            new_annotations.append(new_annotation)
        return new_annotations
    # endregion METHOD___shift_annotations

    # region METHOD_get_root [DOMAIN(9): DocumentProcessing; CONCEPT(6): TreeNavigation; TECH(5): Python]
    ## @purpose Traverse parents up to return the root of the tree.
    ## @io None -> TreeNode
    ## @complexity 2
    def get_root(self) -> "TreeNode":
        """
        :return: root of the tree
        """
        node = self
        while node.parent is not None:
            node = node.parent
        return node
    # endregion METHOD_get_root

    # region METHOD_merge_annotations [DOMAIN(9): DocumentProcessing; CONCEPT(8): AnnotationMerging; TECH(7): Python, AnnotationMerger]
    ## @purpose Merge annotations on all nodes in the tree using DFS traversal and AnnotationMerger.
    ## @uses AnnotationMerger
    ## @io None -> None
    ## @complexity 5
    def merge_annotations(self) -> None:
        from dedoc.utils.annotation_merger import AnnotationMerger

        logger.debug(f"[IMP:4][TreeNode][MERGE_ANNOTATIONS] Starting annotation merge from tree root")
        root = self.get_root()
        stack = [root]
        merger = AnnotationMerger()
        while len(stack) > 0:
            node = stack.pop()
            node.annotations = merger.merge_annotations(node.annotations, node.text)
            for sub_node in node.subparagraphs:
                stack.append(sub_node)
        logger.info(f"[IMP:9][TreeNode][MERGE_ANNOTATIONS] Annotations merged across all tree nodes")
    # endregion METHOD_merge_annotations

    # region METHOD___add_additional_page_id [DOMAIN(9): DocumentProcessing; CONCEPT(8): MultiPageHandling; TECH(6): Python]
    ## @purpose Add additional page ID metadata for multi-page nodes — tracks which parts of node text belong to which pages.
    ## @io (int, LineMetadata, LineWithMeta) -> None
    ## @complexity 5
    @staticmethod
    def __add_additional_page_id(start: int, metadata: LineMetadata, other_line: LineWithMeta) -> None:
        """
        Adds additional page_id metadata for multi-page nodes.

        If node is located on several pages, its metadata will contain "additional_page_id" attribute with list of dicts:
            {
                start: start index of the text on the next page,
                end: end index (not included),
                page_id: page id, where this textual part (node_text[start:end]) is located
            }
        """
        if metadata.page_id == other_line.metadata.page_id:
            return

        if hasattr(metadata, "additional_page_ids"):
            last_page_id = metadata.additional_page_ids[-1]["page_id"]
            if last_page_id == other_line.metadata.page_id:
                metadata.additional_page_ids[-1]["end"] = start + len(other_line.line)
                return

        additional_page_id = {"start": start, "end": start + len(other_line.line), "page_id": other_line.metadata.page_id}
        if hasattr(metadata, "additional_page_ids"):
            metadata.additional_page_ids.append(additional_page_id)
        else:
            metadata.additional_page_ids = [additional_page_id]
    # endregion METHOD___add_additional_page_id
# endregion CLASS_TreeNode

# region MODULE_CONTRACT [DOMAIN(9): DocumentProcessing, DataStructures; CONCEPT(10): Tree, DocumentStructure; TECH(7): Python, API, AnnotationMerger]
## @modulecontract
## @purpose Define the TreeNode data structure — recursive tree representation of document structure with annotation-aware construction, merging, and multi-page tracking.
## @scope Document tree: nodes with text, annotations, hierarchy metadata, parent/child links, tree construction from lines, annotation merging.
## @input Node ID, text, annotations, metadata, children list, parent reference.
## @output TreeNode instances forming a complete document tree.
## @links [INHERITS(5): Serializable, USES_API(8): ApiTreeNode, READS_DATA_FROM(9): LineWithMeta, LineMetadata, HierarchyLevel, Annotation, AnnotationMerger]
## @invariants
## - Root node has parent=None and node_id="0"
## - Children IDs follow pattern "parent_id.child_index"
## @rationale
## Q: Why a tree rather than a flat list?
## A: Documents have inherent hierarchical structure (sections, subsections, lists). A tree preserves this structure, enabling semantic navigation and table-of-contents generation.
## @changes
## LAST_CHANGE: [v1.0.0 – Added semantic markup and LDD logging]
## @modulemap
## CLASS 10[Document tree node] => TreeNode
## METHOD 8[Create root from lines] => create
## METHOD 7[Add child node] => add_child
## METHOD 7[Append text to node] => add_text
## METHOD 6[Get tree root] => get_root
## METHOD 8[Merge all annotations] => merge_annotations
## METHOD 8[API schema conversion] => to_api_schema
## @usecases
## - [TreeNode]: StructureConstructor → BuildDocumentTree → TreeReturned
## - [TreeNode]: AnnotationMerger → MergeTreeAnnotations → AnnotationsConsolidated
def _module_contract():
    pass
# endregion MODULE_CONTRACT
# GREP_SUMMARY: TreeNode, tree, document, structure, node, parent, child, subparagraphs, annotations, hierarchy, recursive, root, merger, multi-page, API
# STRUCTURE: ▶ TreeNode ┌node_id, text, annotations[], metadata, subparagraphs[], parent?┐ → ◇ create (merge lines→root) → ⊕ add_child (new node by line) → ⊕ add_text (append annotations) → ⊕ get_root (traverse up) → ⊕ merge_annotations (DFS + AnnotationMerger) → ⊕ to_api_schema (recursive) → ⎋ ApiTreeNode
