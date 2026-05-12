from typing import List, Tuple

from dedoc.data_structures.hierarchy_level import HierarchyLevel
from dedoc.data_structures.line_metadata import LineMetadata
from dedoc.data_structures.line_with_meta import LineWithMeta
from dedoc.structure_extractors.feature_extractors.toc_feature_extractor import TOCFeatureExtractor
from dedoc.structure_extractors.hierarchy_level_builders.abstract_hierarchy_level_builder import AbstractHierarchyLevelBuilder

import logging
logger = logging.getLogger(__name__)


# region CLASS_TocBuilder [DOMAIN(DocumentProcessing): ...; CONCEPT(HierarchyBuilding): ...; TECH(Python): ...]
## @purpose TocBuilder for document structure extraction pipeline
class TocBuilder(AbstractHierarchyLevelBuilder):
    # region METHOD_get_lines_with_hierarchy [DOMAIN(X): ...; CONCEPT(Y): ...; TECH(Z): ...]
    ## @purpose get_lines_with_hierarchy method
    ## @io Input -> Output
    ## @complexity 5
    def get_lines_with_hierarchy(self, lines_with_labels: List[Tuple[LineWithMeta, str]], init_hl_depth: int) -> List[LineWithMeta]:
        self.logger.debug(f"[IMP:4][TocBuilder][get_lines_with_hierarchy_INIT] Starting")
        # TODO add analyse toc if tag 'toc' and 'toc_item' exist
        result = []
        is_toc_begun = False
        for line, _ in lines_with_labels:
            if line.line.lower().strip() in TOCFeatureExtractor.titles:  # set line as toc
                line.metadata.hierarchy_level = HierarchyLevel(init_hl_depth + 0, 0, False, "toc")
                result.append(line)
                is_toc_begun = True
                continue
            elif not is_toc_begun:
                result.append(self.__get_toc_line(line, init_hl_depth=init_hl_depth))
            is_toc_begun = True
            line.metadata.hierarchy_level = HierarchyLevel(init_hl_depth + 1, 0, False, "toc_item")
            result.append(line)
        return result

    # endregion METHOD_get_lines_with_hierarchy
    # region METHOD___get_toc_line [DOMAIN(X): ...; CONCEPT(Y): ...; TECH(Z): ...]
    ## @purpose __get_toc_line method
    ## @io Input -> Output
    ## @complexity 5
    def __get_toc_line(self, line: LineWithMeta, init_hl_depth: int) -> LineWithMeta:
        self.logger.debug(f"[IMP:4][TocBuilder][__get_toc_line_INIT] Starting")
        return LineWithMeta(line="",
                            metadata=LineMetadata(hierarchy_level=HierarchyLevel(init_hl_depth + 0, 0, False, "toc"),
                                                  page_id=line.metadata.page_id,
                                                  line_id=line.metadata.line_id),
                            annotations=[],
                            uid=line.uid + "_toc")

    # endregion METHOD___get_toc_line
# endregion CLASS_TocBuilder
# region MODULE_CONTRACT [DOMAIN(DocumentProcessing): ...; CONCEPT(HierarchyBuilding): ...; TECH(Python): ...]
## @modulecontract
## @purpose Document structure extraction for structure_extractors/hierarchy_level_builders/toc_builder/toc_builder: line classification, hierarchy level assignment, pattern matching.
## @scope Structure extraction pipeline — structure_extractors/hierarchy_level_builders/toc_builder/toc_builder
## @input Document lines with reader metadata.
## @output Lines annotated with hierarchy levels and line type labels.
## @links [USES_API(8): dedoc.data_structures; READS_DATA_FROM(8): readers]
## @invariants
## - Output lines preserve input order.
## @rationale
## Q: Why semantic region markup and LDD logging?
## A: Enables agent navigation via grep/Doxygen XML and runtime trace analysis.
## @changes
## LAST_CHANGE: [v1.0.0 – Added semantic template markup and LDD logging]
## @modulemap
## CLASS [Weight 7][Structure extraction] => TocBuilder
## @usecases
## - Extract structure: Reader → StructureExtractor → HierarchyBuilder → AnnotatedDocument
def _module_contract():
    pass
# endregion MODULE_CONTRACT
# GREP_SUMMARY: structure extractors, hierarchy level builders, toc builder, toc builder
# STRUCTURE: ▶ structure_extractors/hierarchy_level_builders/toc_builder/toc_builder → ○ TocBuilder.cls → ⎋ result