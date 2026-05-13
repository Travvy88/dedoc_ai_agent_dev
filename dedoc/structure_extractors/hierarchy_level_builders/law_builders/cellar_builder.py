from copy import deepcopy
from typing import List, Tuple

from dedoc.data_structures.hierarchy_level import HierarchyLevel
from dedoc.data_structures.line_with_meta import LineWithMeta
from dedoc.structure_extractors.hierarchy_level_builders.abstract_hierarchy_level_builder import AbstractHierarchyLevelBuilder

import logging
logger = logging.getLogger(__name__)


# region CLASS_CellarHierarchyLevelBuilder [DOMAIN(DocumentProcessing): ...; CONCEPT(HierarchyBuilding): ...; TECH(Python): ...]
## @purpose CellarHierarchyLevelBuilder for document structure extraction pipeline
class CellarHierarchyLevelBuilder(AbstractHierarchyLevelBuilder):
    document_types = ["foiv", "law"]
    starting_line_types = ["cellar"]

    # region METHOD_get_lines_with_hierarchy [DOMAIN(X): ...; CONCEPT(Y): ...; TECH(Z): ...]
    ## @purpose get_lines_with_hierarchy method
    ## @io Input -> Output
    ## @complexity 5
    def get_lines_with_hierarchy(self, lines_with_labels: List[Tuple[LineWithMeta, str]], init_hl_depth: int = 2) -> List[LineWithMeta]:
        self.logger.debug(f"[IMP:4][CellarHierarchyLevelBuilder][get_lines_with_hierarchy_INIT] Starting")
        result = []
        # detect begin of body
        hierarchy_level = HierarchyLevel(level_1=init_hl_depth, level_2=0, can_be_multiline=True, line_type="cellar")

        for line, _ in lines_with_labels:
            # postprocessing of others units
            metadata = deepcopy(line.metadata)
            metadata.hierarchy_level = hierarchy_level
            line = LineWithMeta(line=line.line, metadata=metadata, annotations=line.annotations, uid=line.uid)
            result.append(line)
        return result

    # endregion METHOD_get_lines_with_hierarchy
# endregion CLASS_CellarHierarchyLevelBuilder
# region MODULE_CONTRACT [DOMAIN(DocumentProcessing): ...; CONCEPT(HierarchyBuilding): ...; TECH(Python): ...]
## @modulecontract
## @purpose Document structure extraction for structure_extractors/hierarchy_level_builders/law_builders/cellar_builder: line classification, hierarchy level assignment, pattern matching.
## @scope Structure extraction pipeline — structure_extractors/hierarchy_level_builders/law_builders/cellar_builder
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
## CLASS [Weight 7][Structure extraction] => CellarHierarchyLevelBuilder
## @usecases
## - Extract structure: Reader → StructureExtractor → HierarchyBuilder → AnnotatedDocument
def _module_contract():
    pass
# endregion MODULE_CONTRACT
# GREP_SUMMARY: structure extractors, hierarchy level builders, law builders, cellar builder
# STRUCTURE: ▶ structure_extractors/hierarchy_level_builders/law_builders/cellar_builder → ○ CellarHierarchyLevelBuilder.cls → ⎋ result