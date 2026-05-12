import logging
from typing import Dict, Optional, Union

from dedoc.api.schema.line_metadata import LineMetadata as ApiLineMetadata
from dedoc.data_structures.hierarchy_level import HierarchyLevel
from dedoc.data_structures.serializable import Serializable

logger = logging.getLogger(__name__)


# region CLASS_LineMetadata [DOMAIN(9): DocumentProcessing, DataStructures; CONCEPT(9): Line, Metadata; TECH(6): Python, API]
## @purpose Hold line-level metadata: page number, line ID, tag hierarchy level (from reader), result hierarchy level (from structure extractor), and extensible attributes.
class LineMetadata(Serializable):
    """
    This class holds information about document node (and document line) metadata, such as page number or line level in a document hierarchy.

    :ivar tag_hierarchy_level: the hierarchy level of the line with its type directly extracted by some of the readers
        (usually information got from tags e.g. in docx or html readers)
    :ivar hierarchy_level: the hierarchy level of the line extracted by some of the structure extractors - the result type and level of the line.
        The lower the level of the hierarchy, the closer it is to the root, it's used to construct document tree.
    :ivar page_id: page number where paragraph starts, the numeration starts from page 0
    :ivar line_id: line number inside the entire document, the numeration starts from line 0

    :vartype tag_hierarchy_level: HierarchyLevel
    :vartype hierarchy_level: Optional[HierarchyLevel]
    :vartype page_id: int
    :vartype line_id: Optional[int]

    Additional variables may be added with other line metadata.
    """

    # region METHOD___init__ [DOMAIN(9): DocumentProcessing; CONCEPT(9): Line; TECH(6): Python]
    ## @purpose Initialize line metadata with page/line IDs, hierarchy levels, and extra kwargs.
    ## @io (int, Optional[int], Optional[HierarchyLevel], Optional[HierarchyLevel], **kwargs) -> None
    ## @complexity 3
    def __init__(self,
                 page_id: int,
                 line_id: Optional[int],
                 tag_hierarchy_level: Optional[HierarchyLevel] = None,
                 hierarchy_level: Optional[HierarchyLevel] = None,
                 **kwargs: Dict[str, Union[str, int, float]]) -> None:
        """
        :param page_id: page number where paragraph starts, the numeration starts from page 0
        :param line_id: line number inside the entire document, the numeration starts from line 0
        :param tag_hierarchy_level: the hierarchy level of the line with its type directly extracted by some of the readers
        :param hierarchy_level: the hierarchy level of the line extracted by some of the structure extractors - the result type and level of the line.
        """
        logger.debug(f"[IMP:4][LineMetadata][INIT] page_id={page_id}, line_id={line_id}, tag_hl={tag_hierarchy_level}, hl={hierarchy_level}")
        self.tag_hierarchy_level: HierarchyLevel = HierarchyLevel.create_unknown() if tag_hierarchy_level is None else tag_hierarchy_level
        self.hierarchy_level: Optional[HierarchyLevel] = hierarchy_level
        self.page_id: int = page_id
        self.line_id: Optional[int] = line_id
        for key, value in kwargs.items():
            setattr(self, key, value)
        logger.debug(f"[IMP:4][LineMetadata][INIT] LineMetadata created: page_id={self.page_id}, line_id={self.line_id}")
    # endregion METHOD___init__

    # region METHOD_to_api_schema [DOMAIN(9): DocumentProcessing; CONCEPT(8): Serialization; TECH(6): API]
    ## @purpose Convert line metadata to API schema, mapping hierarchy level to paragraph type.
    ## @uses ApiLineMetadata
    ## @io None -> ApiLineMetadata
    ## @complexity 3
    def to_api_schema(self) -> ApiLineMetadata:
        logger.debug(f"[IMP:4][LineMetadata][TO_API] Converting to API schema")
        paragraph_type = self.hierarchy_level.line_type if self.hierarchy_level is not None else HierarchyLevel.raw_text
        api_line_metadata = ApiLineMetadata(page_id=self.page_id, line_id=self.line_id, paragraph_type=paragraph_type)
        for key, value in vars(self).items():
            if not hasattr(api_line_metadata, key) and key not in ("tag_hierarchy_level", "hierarchy_level"):
                setattr(api_line_metadata, key, value)
        return api_line_metadata
    # endregion METHOD_to_api_schema
# endregion CLASS_LineMetadata

# region MODULE_CONTRACT [DOMAIN(9): DocumentProcessing, DataStructures; CONCEPT(9): Line, Metadata; TECH(6): Python, API]
## @modulecontract
## @purpose Define the LineMetadata data structure — holds per-line metadata: position IDs, dual hierarchy levels, and extensible attributes.
## @scope Line metadata: page/line IDs, tag hierarchy (reader-origin), result hierarchy (structure extractor), dynamic attributes.
## @input Page ID, line ID, optional tag hierarchy level, optional result hierarchy level, extra kwargs.
## @output LineMetadata instance convertible to API schema.
## @links [INHERITS(5): Serializable, USES_API(8): ApiLineMetadata, READS_DATA_FROM(9): HierarchyLevel]
## @invariants
## - tag_hierarchy_level is never None (defaults to create_unknown())
## @rationale
## Q: Why two separate hierarchy levels (tag vs result)?
## A: Readers extract format-specific tags (tag_hierarchy_level) while structure extractors compute the final hierarchy (hierarchy_level). Preserving both enables debugging and fallback.
## @changes
## LAST_CHANGE: [v1.0.0 – Added semantic markup and LDD logging]
## @modulemap
## CLASS 10[Line metadata container] => LineMetadata
## METHOD 6[Constructor] => __init__
## METHOD 8[API schema conversion] => to_api_schema
## @usecases
## - [LineMetadata]: Reader → CreateLineMetadata → LineMetadataStored
## - [LineMetadata]: StructureExtractor → AssignResultHierarchy → hierarchy_levelSet
def _module_contract():
    pass
# endregion MODULE_CONTRACT
# GREP_SUMMARY: LineMetadata, metadata, line, document, page_id, line_id, hierarchy_level, tag_hierarchy_level, API, serializable
# STRUCTURE: ▶ LineMetadata ┌page_id, line_id?, tag_hierarchy_level?, hierarchy_level?, **kwargs┐ → ◇ tag_hl default → ⊕ setattr kwargs → ⊕ to_api_schema (paragraph_type + dynamic attrs) → ⎋ ApiLineMetadata
