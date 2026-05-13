import logging

import dedoc.data_structures.concrete_annotations as annotations
from .annotation import Annotation
from .attached_file import AttachedFile
from .cell_with_meta import CellWithMeta
from .concrete_annotations import *
from .document_content import DocumentContent
from .document_metadata import DocumentMetadata
from .hierarchy_level import HierarchyLevel
from .line_metadata import LineMetadata
from .line_with_meta import LineWithMeta
from .parsed_document import ParsedDocument
from .serializable import Serializable
from .table import Table
from .table_metadata import TableMetadata
from .tree_node import TreeNode
from .unstructured_document import UnstructuredDocument

logger = logging.getLogger(__name__)

__all__ = ['Annotation', 'AttachedFile', 'DocumentContent', 'DocumentMetadata', 'HierarchyLevel', 'LineMetadata',
           'LineWithMeta', 'ParsedDocument', 'Serializable', 'Table', 'TableMetadata', 'CellWithMeta', 'TreeNode', 'UnstructuredDocument', *annotations.__all__]

logger.debug(f"[IMP:4][data_structures__init__][INIT] Exported {len(__all__)} symbols")

# region MODULE_CONTRACT [DOMAIN(9): DocumentProcessing, DataStructures; CONCEPT(8): ModuleAggregation, Exports; TECH(5): Python, PackageInit]
## @modulecontract
## @purpose Aggregate all document data structure classes and annotations into a single public namespace for use by readers, converters, and structure extractors.
## @scope Re-export of all data structure classes and annotation types.
## @input None (package-level imports).
## @output Unified __all__ list containing all public data structure symbols.
## @links [EXPORTS(10): Annotation, AttachedFile, CellWithMeta, DocumentContent, DocumentMetadata, HierarchyLevel, LineMetadata, LineWithMeta, ParsedDocument, Serializable, Table, TableMetadata, TreeNode, UnstructuredDocument, all_concrete_annotations]
## @invariants
## - __all__ includes all public symbols from submodules
## @rationale
## Q: Why aggregate all symbols here?
## A: Provides a single import point for all data structures, simplifying downstream code.
## @changes
## LAST_CHANGE: [v1.0.0 – Added semantic markup and LDD logging]
## @modulemap
## MODULE 10[Central data structure exports] => __init__
## @usecases
## - [__init__]: DownstreamModule → ImportDataStructures → AllSymbolsAvailable
def _module_contract():
    pass
# endregion MODULE_CONTRACT
# GREP_SUMMARY: data_structures, exports, init, package, Annotation, AttachedFile, CellWithMeta, DocumentContent, DocumentMetadata, HierarchyLevel, LineMetadata, LineWithMeta, ParsedDocument, Serializable, Table, TableMetadata, TreeNode, UnstructuredDocument
# STRUCTURE: ▶ Import ┌all submodules + concrete_annotations┐ → ⊕ __all__ = [all symbols] → ⎋ public namespace
