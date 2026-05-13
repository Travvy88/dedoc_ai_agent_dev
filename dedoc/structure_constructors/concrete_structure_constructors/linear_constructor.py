# region MODULE_CONTRACT [DOMAIN(9): DocumentProcessing, StructureConstruction; CONCEPT(7): FlatStructure, LinearRepresentation; TECH(6): TreeNode, DocumentAssembly]
## @modulecontract
## @purpose Build a flat, linear document structure where all lines are direct children of an empty root node — the simplest possible document representation.
## @scope Flat structure construction, TreeNode assembly, metadata propagation.
## @input UnstructuredDocument (lines + tables + metadata).
## @output ParsedDocument with a flat line tree.
## @links [USES_API(8): AbstractStructureConstructor, TreeNode, DocumentContent, DocumentMetadata]
## @links_to_spec REQ-STR-003: A linear (flat) structure must be available as the simplest document representation.
## @invariants
## - Root node ALWAYS has the empty lines list.
## - All document lines become direct children of the root.
## - Metadata is copied from the UnstructuredDocument.
## @rationale
## Q: Why an empty root node instead of making the first line the root?
## A: A uniform root with empty lines ensures all constructors produce the same TreeNode shape, simplifying downstream consumers.
## @changes
## LAST_CHANGE: [v1.0.0 – Semantic template markup and LDD logging added]
## @modulemap
## CLASS 8[Flat linear structure constructor] => LinearConstructor
## METHOD 9[Assemble flat document tree from lines] => construct
## @usecases
## - [construct]: StructureExtractor → AssembleFlatTree → ProduceLinearParsedDocument
def _module_contract():
    pass
# endregion MODULE_CONTRACT
# GREP_SUMMARY: LinearConstructor, flat structure, linear, TreeNode, document assembly, simplest representation
# STRUCTURE: ▶ ┌lines┐ → ⚡ TreeNode.create(lines=[]) → ○ Loop ∋line: add_child(line) → merge_annotations → ⊕ DocumentContent + DocumentMetadata → ⟦ParsedDocument⟧

import logging
from typing import Optional

from dedoc.data_structures.parsed_document import ParsedDocument
from dedoc.data_structures.unstructured_document import UnstructuredDocument
from dedoc.structure_constructors.abstract_structure_constructor import AbstractStructureConstructor

logger = logging.getLogger(__name__)

# region CLASS_LinearConstructor [DOMAIN(9): DocumentProcessing; CONCEPT(7): FlatStructure, LinearRepresentation; TECH(6): TreeNode, DocumentAssembly]
## @purpose Produce a flat linear document structure where every line is a direct child of the root node — the fallback/simplest representation.
class LinearConstructor(AbstractStructureConstructor):
    """
    This class is used to form a simple basic document structure representation as a list of document lines.
    The result contains the empty root node with the consecutive list of all document lines as its children.
    """

    # region METHOD_construct [DOMAIN(9): DocumentProcessing; CONCEPT(8): TreeAssembly, DocumentConstruction; TECH(6): TreeNode, LazyImport]
    ## @purpose Build a flat tree representation: create root node, append all lines as children, merge annotations, and return the parsed document.
    ## @uses TreeNode, DocumentContent, DocumentMetadata
    ## @io UnstructuredDocument, Optional[dict] -> ParsedDocument
    ## @complexity 4
    def construct(self, document: UnstructuredDocument, parameters: Optional[dict] = None) -> ParsedDocument:
        """
        Build the linear structure representation for the given document intermediate representation.
        To get the information about the parameters look at the documentation of :class:`~dedoc.structure_constructors.AbstractStructureConstructor`.
        """
        from dedoc.data_structures.document_content import DocumentContent
        from dedoc.data_structures.document_metadata import DocumentMetadata
        from dedoc.data_structures.tree_node import TreeNode

        lines = document.lines
        # LDD-log: flow start
        logger.debug(f"[IMP:4][LinearConstructor][INIT] Building linear structure for {len(lines)} lines")
        tree = TreeNode.create(lines=[])
        for line in lines:
            tree.add_child(line)
            logger.debug(f"[IMP:3][LinearConstructor][ADD_CHILD] Added line id={line.metadata.line_id} hierarchy={line.metadata.hierarchy_level}")
        tree.merge_annotations()
        document_content = DocumentContent(tables=document.tables, structure=tree)
        metadata = DocumentMetadata(**document.metadata)
        result = ParsedDocument(content=document_content, metadata=metadata, warnings=document.warnings)
        # LDD-log: business result
        logger.info(f"[IMP:9][LinearConstructor][RESULT] Linear structure built: {len(lines)} lines in flat tree")
        return result
    # endregion METHOD_construct
# endregion CLASS_LinearConstructor
