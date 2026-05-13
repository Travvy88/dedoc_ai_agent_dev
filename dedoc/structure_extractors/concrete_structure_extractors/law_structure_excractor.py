from typing import List, Optional

from dedoc.data_structures.line_with_meta import LineWithMeta
from dedoc.structure_extractors.concrete_structure_extractors.abstract_law_structure_extractor import AbstractLawStructureExtractor

import logging
logger = logging.getLogger(__name__)


# region CLASS_LawStructureExtractor [DOMAIN(DocumentProcessing): ...; CONCEPT(DocumentStructureParser): ...; TECH(Python): ...]
## @purpose LawStructureExtractor for document structure extraction pipeline
class LawStructureExtractor(AbstractLawStructureExtractor):
    """
    This class is used for extraction structure from common laws.

    You can find the description of this type of structure in the section :ref:`simple_law_structure`.
    """
    document_type = "law"

    # region METHOD___init__ [DOMAIN(X): ...; CONCEPT(Y): ...; TECH(Z): ...]
    ## @purpose __init__ method
    ## @io Input -> Output
    ## @complexity 5
    def __init__(self, *, config: Optional[dict] = None) -> None:
        super().__init__(config=config)

        self.logger.debug(f"[IMP:4][LawStructureExtractor][__init___INIT] Starting")
        import re
        from dedoc.structure_extractors.hierarchy_level_builders.utils_reg import regexps_ends_of_number, regexps_number
        from dedoc.structure_extractors.hierarchy_level_builders.header_builder.header_hierarchy_level_builder import HeaderHierarchyLevelBuilder
        from dedoc.structure_extractors.hierarchy_level_builders.law_builders.application_builder.application_law_hierarchy_level_builder import \
            ApplicationLawHierarchyLevelBuilder
        from dedoc.structure_extractors.hierarchy_level_builders.law_builders.body_builder.body_law_hierarchy_level_builder import BodyLawHierarchyLevelBuilder
        from dedoc.structure_extractors.hierarchy_level_builders.law_builders.cellar_builder import CellarHierarchyLevelBuilder

        self.hierarchy_level_builders = [
            HeaderHierarchyLevelBuilder(),
            BodyLawHierarchyLevelBuilder(),
            CellarHierarchyLevelBuilder(),
            ApplicationLawHierarchyLevelBuilder()
        ]
        self.regexps_item = re.compile(r"^\s*(\d*\.)*\d+[\)|\}]")
        self.regexps_part = regexps_number
        self.regexps_subitem = re.compile(r"^\s*[а-яё]\)")
        self.regexps_ends_of_number = regexps_ends_of_number
        self.init_hl_depth = 2
        self.hl_type = "law"

    # endregion METHOD___init__
    # region METHOD__postprocess_lines [DOMAIN(X): ...; CONCEPT(Y): ...; TECH(Z): ...]
    ## @purpose _postprocess_lines method
    ## @io Input -> Output
    ## @complexity 5
    def _postprocess_lines(self, lines: List[LineWithMeta]) -> List[LineWithMeta]:
        self.logger.debug(f"[IMP:4][LawStructureExtractor][_postprocess_lines_INIT] Starting")
        return self._postprocess(lines=lines,
                                 paragraph_type=["item", "articlePart", "subitem"],
                                 regexps=[self.regexps_item, self.regexps_part, self.regexps_subitem],
                                 excluding_regexps=[None, self.regexps_ends_of_number, self.regexps_ends_of_number])

    # endregion METHOD__postprocess_lines
# endregion CLASS_LawStructureExtractor
# region MODULE_CONTRACT [DOMAIN(DocumentProcessing): ...; CONCEPT(DocumentStructureParser): ...; TECH(Python): ...]
## @modulecontract
## @purpose Document structure extraction for structure_extractors/concrete_structure_extractors/law_structure_excractor: line classification, hierarchy level assignment, pattern matching.
## @scope Structure extraction pipeline — structure_extractors/concrete_structure_extractors/law_structure_excractor
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
## CLASS [Weight 7][Structure extraction] => LawStructureExtractor
## @usecases
## - Extract structure: Reader → StructureExtractor → HierarchyBuilder → AnnotatedDocument
def _module_contract():
    pass
# endregion MODULE_CONTRACT
# GREP_SUMMARY: structure extractors, concrete structure extractors, law structure excractor
# STRUCTURE: ▶ structure_extractors/concrete_structure_extractors/law_structure_excractor → ○ LawStructureExtractor.cls → ⎋ result