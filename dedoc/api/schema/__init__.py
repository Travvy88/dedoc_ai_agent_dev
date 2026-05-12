# region MODULE_CONTRACT [DOMAIN(8): DocumentProcessing, APISchema; CONCEPT(7): SchemaAggregation, PublicAPI; TECH(6): Pydantic, FastAPI]
## @modulecontract
## @purpose Aggregate and re-export all API schema classes for external consumers, providing a single import point for the dedoc API schema layer.
## @scope Public API schema surface — Pydantic models for document representation.
## @input None (re-exports from sibling modules).
## @output Flat namespace of all schema classes via __all__.
## @links
## @invariants
## - __all__ always contains all public schema class names.
## - All names in __all__ resolve to actual classes via relative imports.
## @rationale
## Q: Why centralize exports?
## A: Provides a stable public API contract. External consumers import from `dedoc.api.schema` without knowing internal module layout.
## @changes
## LAST_CHANGE: [v1.0.0 – Initial creation with semantic markup]
## @modulemap
## EXPORT [Aggregates schema classes for public API] => __all__
## @usecases
## - [__all__]: ExternalConsumer => ImportSchemaNamespace => DiscoverAvailableSchemaClasses
def _module_contract():
    pass
# endregion MODULE_CONTRACT
# GREP_SUMMARY: schema, API, Pydantic, models, exports, __all__, aggregated, public surface
# STRUCTURE: ▶ Imports ┌Annotation,CellWithMeta,DocumentContent,...┐ → ⊕ __all__ list → ⎋ export

from .annotation import Annotation
from .cell_with_meta import CellWithMeta
from .document_content import DocumentContent
from .document_metadata import DocumentMetadata
from .line_metadata import LineMetadata
from .line_with_meta import LineWithMeta
from .parsed_document import ParsedDocument
from .table import Table
from .table_metadata import TableMetadata
from .tree_node import TreeNode

__all__ = ["Annotation", "CellWithMeta", "DocumentContent", "DocumentMetadata", "LineMetadata", "LineWithMeta", "ParsedDocument", "Table", "TableMetadata",
           "TreeNode"]
