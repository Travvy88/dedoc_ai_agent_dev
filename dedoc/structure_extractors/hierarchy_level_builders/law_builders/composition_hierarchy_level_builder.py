from typing import List, Optional

from dedoc.structure_extractors.hierarchy_level_builders.abstract_hierarchy_level_builder import AbstractHierarchyLevelBuilder
from dedoc.structure_extractors.hierarchy_level_builders.law_builders.stub_hierarchy_level_builder import StubHierarchyLevelBuilder

import logging
logger = logging.getLogger(__name__)


# region CLASS_HierarchyLevelBuilderComposition [DOMAIN(DocumentProcessing): ...; CONCEPT(HierarchyBuilding): ...; TECH(Python): ...]
## @purpose HierarchyLevelBuilderComposition for document structure extraction pipeline
class HierarchyLevelBuilderComposition(object):

    # region METHOD___init__ [DOMAIN(X): ...; CONCEPT(Y): ...; TECH(Z): ...]
    ## @purpose __init__ method
    ## @io Input -> Output
    ## @complexity 5
    def __init__(self, builders: List[AbstractHierarchyLevelBuilder]) -> None:
        self.logger = logging.getLogger(__name__)
        self.logger.debug(f"[IMP:4][HierarchyLevelBuilderComposition][__init___INIT] Starting")
        self.builders = builders

    # endregion METHOD___init__
    # region METHOD__get_builder [DOMAIN(X): ...; CONCEPT(Y): ...; TECH(Z): ...]
    ## @purpose _get_builder method
    ## @io Input -> Output
    ## @complexity 5
    def _get_builder(self, start_tag: str, document_type: str) -> Optional[AbstractHierarchyLevelBuilder]:
        self.logger.debug(f"[IMP:4][HierarchyLevelBuilderComposition][_get_builder_INIT] Starting")
        for builder in self.builders:
            if builder.can_build(start_tag, document_type):
                return builder

        return None

    # endregion METHOD__get_builder
    # region METHOD__get_builders [DOMAIN(X): ...; CONCEPT(Y): ...; TECH(Z): ...]
    ## @purpose _get_builders method
    ## @io Input -> Output
    ## @complexity 5
    def _get_builders(self, start_tags: List[str], doc_types: str) -> List[AbstractHierarchyLevelBuilder]:
        self.logger.debug(f"[IMP:4][HierarchyLevelBuilderComposition][_get_builders_INIT] Starting")
        builders = []
        for start_tag in start_tags:
            builder = self._get_builder(start_tag, doc_types)
            if builder is not None:
                builders.append(builder)

        return builders if builders else [StubHierarchyLevelBuilder()]

    # endregion METHOD__get_builders
# endregion CLASS_HierarchyLevelBuilderComposition
# region MODULE_CONTRACT [DOMAIN(DocumentProcessing): ...; CONCEPT(HierarchyBuilding): ...; TECH(Python): ...]
## @modulecontract
## @purpose Document structure extraction for structure_extractors/hierarchy_level_builders/law_builders/composition_hierarchy_level_builder: line classification, hierarchy level assignment, pattern matching.
## @scope Structure extraction pipeline — structure_extractors/hierarchy_level_builders/law_builders/composition_hierarchy_level_builder
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
## CLASS [Weight 7][Structure extraction] => HierarchyLevelBuilderComposition
## @usecases
## - Extract structure: Reader → StructureExtractor → HierarchyBuilder → AnnotatedDocument
def _module_contract():
    pass
# endregion MODULE_CONTRACT
# GREP_SUMMARY: structure extractors, hierarchy level builders, law builders, composition hierarchy level builder
# STRUCTURE: ▶ structure_extractors/hierarchy_level_builders/law_builders/composition_hierarchy_level_builder → ○ HierarchyLevelBuilderComposition.cls → ⎋ result