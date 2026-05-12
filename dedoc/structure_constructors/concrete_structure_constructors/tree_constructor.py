# region MODULE_CONTRACT [DOMAIN(10): DocumentProcessing, StructureConstruction; CONCEPT(9): HierarchicalTree, StructureAssembly; TECH(8): TreeNode, LexicographicCompare, ListInsertion]
## @modulecontract
## @purpose Build a hierarchical (tree) document structure from lines with hierarchy levels — the primary structure representation that mirrors the document's logical sections.
## @scope Tree construction from lines with hierarchy levels, list-item merging, multi-line header handling, metadata propagation.
## @input UnstructuredDocument (lines with hierarchy levels, tables, metadata).
## @output ParsedDocument with a tree structure rooted at the document title line(s).
## @links [USES_API(9): AbstractStructureConstructor, TreeNode, DocumentContent, DocumentMetadata, LineWithMeta, HierarchyLevel]
## @links_to_spec REQ-STR-004: A hierarchical tree structure must represent the document's logical sections.
## @invariants
## - Lines with hierarchy level (0, 0) are merged into the root node.
## - Lines with line_type "list_item" get an auxiliary "list" parent line inserted above them.
## - Tree node insertion follows lexicographic comparison of hierarchy levels.
## - Multi-line headers with equal hierarchy levels are merged via add_text.
## @rationale
## Q: Why insert auxiliary list lines instead of grouping list items directly?
## A: Auxiliary list nodes ensure the tree structure remains regular — all children of a "list" node are naturally list items, simplifying traversal and rendering.
## @changes
## LAST_CHANGE: [v1.0.0 – Semantic template markup and LDD logging added]
## @modulemap
## CLASS 10[Hierarchical tree structure constructor] => TreeConstructor
## METHOD 10[Assemble tree from document lines] => construct
## METHOD 6[Separate document name lines (0,0) from content lines] => __get_document_name
## METHOD 7[Insert auxiliary list nodes for list items] => __add_lists
## METHOD 5[Create auxiliary list line with adjusted hierarchy] => __create_list_line
## @usecases
## - [construct]: StructureExtractor → BuildHierarchicalTree → ProduceTreeParsedDocument
def _module_contract():
    pass
# endregion MODULE_CONTRACT
# GREP_SUMMARY: TreeConstructor, hierarchical tree, hierarchy levels, lexicographic, list items, multi-line headers, TreeNode, document structure
# STRUCTURE: ▶ ┌lines┐ → ◇ __get_document_name: split (0,0) vs rest → __add_lists: insert aux list nodes → ○ Loop ∋line: 〈can_be_multiline ∧ hl_equal ? add_text : move_up + add_child〉 → merge_annotations → ⟦ParsedDocument⟧

import logging
from typing import List, Optional, Tuple

from dedoc.data_structures.line_with_meta import LineWithMeta
from dedoc.data_structures.parsed_document import ParsedDocument
from dedoc.data_structures.unstructured_document import UnstructuredDocument
from dedoc.structure_constructors.abstract_structure_constructor import AbstractStructureConstructor

logger = logging.getLogger(__name__)

# region CLASS_TreeConstructor [DOMAIN(10): DocumentProcessing; CONCEPT(9): HierarchicalTree, StructureAssembly; TECH(8): TreeNode, LexicographicCompare, ListInsertion]
## @purpose Build the primary hierarchical document structure: construct a tree from lines with hierarchy levels, merging headers, and inserting auxiliary list nodes.
class TreeConstructor(AbstractStructureConstructor):
    """
    This class is used to form a basic hierarchical document structure representation as a tree.

    The structure is built according to the lines' hierarchy levels and their types:
        - lines with hierarchy level (0, 0) are merged and become a root of the document;
        - lines with a type `list_item` become children of a new empty auxiliary node `list`;
        - each line is added as a separate tree node in the document hierarchy according to its hierarchy level:
            - if the level of the current line is less then the previous line level, the current line becomes its child;
            - else the line becomes a child of the first line which have less hierarchy level that the current line has.

    Hierarchy levels of the lines are compared lexicographically.

    **Example:**
        - **root line (0, 0)**
            - **first child line (1, 0)**
                - **line (2, 0)**
                    - **line (2, 1)**
                - **line (2, 0)**
            - **second child line (1, 0)**
    """

    # region METHOD_construct [DOMAIN(10): DocumentProcessing; CONCEPT(9): HierarchicalTree, StructureAssembly; TECH(8): TreeNode, LazyImport, TreeInsertion]
    ## @purpose Build the full hierarchical tree: extract document name, insert list auxiliary nodes, add lines with hierarchy-aware positioning, merge root.
    ## @uses TreeNode, DocumentContent, DocumentMetadata, __get_document_name, __add_lists
    ## @io UnstructuredDocument, Optional[dict] -> ParsedDocument
    ## @complexity 8
    def construct(self, document: UnstructuredDocument, parameters: Optional[dict] = None) -> ParsedDocument:
        """
        Build the tree structure representation for the given document intermediate representation.
        To get the information about the parameters look at the documentation of :class:`~dedoc.structure_constructors.AbstractStructureConstructor`.
        """
        from dedoc.data_structures.document_content import DocumentContent
        from dedoc.data_structures.document_metadata import DocumentMetadata

        from dedoc.data_structures.tree_node import TreeNode

        # LDD-log: flow start
        logger.info(f"[IMP:7][TreeConstructor][INIT] Building tree structure for {len(document.lines)} lines")

        document_name, not_document_name = self.__get_document_name(document.lines)
        # LDD-log: split result
        logger.debug(f"[IMP:4][TreeConstructor][SPLIT] document_name_lines={len(document_name)}, content_lines={len(not_document_name)}")

        not_document_name = self.__add_lists(not_document_name)
        tree = TreeNode.create(lines=document_name)

        for line in not_document_name:
            hl_equal = line.metadata.hierarchy_level == tree.metadata.hierarchy_level
            line_type_equal = line.metadata.hierarchy_level.line_type == tree.metadata.hierarchy_level.line_type

            if line.metadata.hierarchy_level.can_be_multiline and hl_equal and line_type_equal:
                # LDD-log: multi-line header merge
                logger.debug(f"[IMP:4][TreeConstructor][MULTILINE] Merging line id={line.metadata.line_id} into current node")
                tree.add_text(line)
            else:
                while tree.metadata.hierarchy_level >= line.metadata.hierarchy_level:
                    tree = tree.parent
                tree = tree.add_child(line=line)
                logger.debug(f"[IMP:3][TreeConstructor][ADD_CHILD] Added line id={line.metadata.line_id} hl={line.metadata.hierarchy_level}")

        tree = tree.get_root()
        tree.merge_annotations()
        document_content = DocumentContent(tables=document.tables, structure=tree)
        metadata = DocumentMetadata(**document.metadata)
        result = ParsedDocument(content=document_content, metadata=metadata, warnings=document.warnings)

        # LDD-log: business result
        logger.info(f"[IMP:9][TreeConstructor][RESULT] Tree structure built: root_node={tree.node_id}")
        return result
    # endregion METHOD_construct

    # region METHOD___get_document_name [DOMAIN(6): DocumentProcessing; CONCEPT(6): LineClassification; TECH(4): ListFiltering]
    ## @purpose Separate lines with hierarchy level (0, 0) (document title/name) from all other content lines.
    ## @uses LineWithMeta
    ## @io List[LineWithMeta] -> Tuple[List[LineWithMeta], List[LineWithMeta]]
    ## @complexity 3
    def __get_document_name(self, lines: List[LineWithMeta]) -> Tuple[List[LineWithMeta], List[LineWithMeta]]:
        document_name = []
        other_lines = []
        for line in lines:
            if line.metadata.hierarchy_level.level_1 == 0 and line.metadata.hierarchy_level.level_2 == 0:
                document_name.append(line)
            else:
                other_lines.append(line)
        # LDD-log: classification result
        logger.debug(f"[IMP:4][TreeConstructor][GET_DOC_NAME] doc_name={len(document_name)}, other={len(other_lines)}")
        return document_name, other_lines
    # endregion METHOD___get_document_name

    # region METHOD___add_lists [DOMAIN(7): DocumentProcessing; CONCEPT(7): ListDetection, AuxiliaryNodeInsertion; TECH(6): StackTracking, HierarchyCompare]
    ## @purpose Insert auxiliary "list" nodes before consecutive list-item lines that share the same hierarchy level.
    ## @uses LineWithMeta, __create_list_line, HierarchyLevel.is_list_item
    ## @io List[LineWithMeta] -> List[LineWithMeta]
    ## @complexity 6
    def __add_lists(self, not_document_name: List[LineWithMeta]) -> List[LineWithMeta]:
        previous_hierarchy_levels = []
        res = []
        for line in not_document_name:
            if line.metadata.hierarchy_level.is_list_item():
                while len(previous_hierarchy_levels) > 0 and previous_hierarchy_levels[-1] > line.metadata.hierarchy_level:
                    previous_hierarchy_levels.pop()
                if previous_hierarchy_levels == [] or previous_hierarchy_levels[-1] < line.metadata.hierarchy_level:
                    list_line = self.__create_list_line(line)
                    res.append(list_line)
                    previous_hierarchy_levels.append(line.metadata.hierarchy_level)
                    # LDD-log: list node inserted
                    logger.debug(f"[IMP:5][TreeConstructor][ADD_LIST] Inserted auxiliary list node for hl={line.metadata.hierarchy_level}")
            elif not line.metadata.hierarchy_level.is_raw_text():
                previous_hierarchy_levels = []
            res.append(line)
        return res
    # endregion METHOD___add_lists

    # region METHOD___create_list_line [DOMAIN(5): DocumentProcessing; CONCEPT(5): AuxiliaryNodeFactory; TECH(5): HierarchyLevel, LineWithMeta]
    ## @purpose Create an auxiliary "list" line with adjusted hierarchy level (level_2 -= 0.5) to serve as a container for list-item children.
    ## @uses HierarchyLevel, LineMetadata, LineWithMeta
    ## @io LineWithMeta -> LineWithMeta
    ## @complexity 3
    @staticmethod
    def __create_list_line(line: LineWithMeta) -> LineWithMeta:
        from dedoc.data_structures.hierarchy_level import HierarchyLevel
        from dedoc.data_structures.line_metadata import LineMetadata

        hierarchy_level = HierarchyLevel(
            level_1=line.metadata.hierarchy_level.level_1,
            level_2=line.metadata.hierarchy_level.level_2 - 0.5,
            line_type="list",
            can_be_multiline=False
        )
        return LineWithMeta(line="",
                            metadata=LineMetadata(hierarchy_level=hierarchy_level, page_id=line.metadata.page_id, line_id=line.metadata.line_id),
                            annotations=[])
    # endregion METHOD___create_list_line
# endregion CLASS_TreeConstructor
