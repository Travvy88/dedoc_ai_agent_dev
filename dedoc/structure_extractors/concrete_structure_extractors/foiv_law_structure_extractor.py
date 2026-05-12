from typing import List, Optional

from dedoc.data_structures.line_with_meta import LineWithMeta
from dedoc.structure_extractors.concrete_structure_extractors.abstract_law_structure_extractor import AbstractLawStructureExtractor

import logging
logger = logging.getLogger(__name__)


# region CLASS_FoivLawStructureExtractor [DOMAIN(DocumentProcessing): ...; CONCEPT(DocumentStructureParser): ...; TECH(Python): ...]
## @purpose FoivLawStructureExtractor for document structure extraction pipeline
class FoivLawStructureExtractor(AbstractLawStructureExtractor):
    """
    This class is used for extraction structure from foiv type of law.

    You can find the description of this type of structure in the section :ref:`foiv_law_structure`.
    """
    document_type = "foiv_law"

    # region METHOD___init__ [DOMAIN(X): ...; CONCEPT(Y): ...; TECH(Z): ...]
    ## @purpose __init__ method
    ## @io Input -> Output
    ## @complexity 5
    def __init__(self, *, config: Optional[dict] = None) -> None:
        from dedoc.structure_extractors.hierarchy_level_builders.utils_reg import regexps_ends_of_number
        super().__init__(config=config)

        self.logger.debug(f"[IMP:4][FoivLawStructureExtractor][__init___INIT] Starting")
        from dedoc.structure_extractors.hierarchy_level_builders.header_builder.header_hierarchy_level_builder import HeaderHierarchyLevelBuilder
        from dedoc.structure_extractors.hierarchy_level_builders.law_builders.application_builder.application_foiv_hierarchy_level_builder import \
            ApplicationFoivHierarchyLevelBuilder
        from dedoc.structure_extractors.hierarchy_level_builders.law_builders.body_builder.body_foiv_hierarchy_level_builder import \
            BodyFoivHierarchyLevelBuilder
        from dedoc.structure_extractors.hierarchy_level_builders.law_builders.cellar_builder import CellarHierarchyLevelBuilder

        self.hierarchy_level_builders = [
            HeaderHierarchyLevelBuilder(),
            BodyFoivHierarchyLevelBuilder(),
            CellarHierarchyLevelBuilder(),
            ApplicationFoivHierarchyLevelBuilder()
        ]
        self.regexps_subitem_with_number = BodyFoivHierarchyLevelBuilder.regexps_subitem_with_number
        self.regexps_subitem_with_char = BodyFoivHierarchyLevelBuilder.regexps_subitem_with_char
        self.regexps_ends_of_number = regexps_ends_of_number
        self.init_hl_depth = 2
        self.hl_type = "foiv"

    # endregion METHOD___init__
    # region METHOD__postprocess_lines [DOMAIN(X): ...; CONCEPT(Y): ...; TECH(Z): ...]
    ## @purpose _postprocess_lines method
    ## @io Input -> Output
    ## @complexity 5
    def _postprocess_lines(self, lines: List[LineWithMeta]) -> List[LineWithMeta]:
        self.logger.debug(f"[IMP:4][FoivLawStructureExtractor][_postprocess_lines_INIT] Starting")
        from dedoc.structure_extractors.hierarchy_level_builders.utils_reg import regexps_foiv_item
        return self._postprocess(lines=lines,
                                 paragraph_type=["item", "subitem", "subitem"],
                                 regexps=[regexps_foiv_item, self.regexps_subitem_with_number, self.regexps_subitem_with_char],
                                 excluding_regexps=[None, self.regexps_ends_of_number, None])

    # endregion METHOD__postprocess_lines
# endregion CLASS_FoivLawStructureExtractor
# region MODULE_CONTRACT [DOMAIN(DocumentProcessing): ...; CONCEPT(DocumentStructureParser): ...; TECH(Python): ...]
## @modulecontract
## @purpose Document structure extraction for structure_extractors/concrete_structure_extractors/foiv_law_structure_extractor: line classification, hierarchy level assignment, pattern matching.
## @scope Structure extraction pipeline — structure_extractors/concrete_structure_extractors/foiv_law_structure_extractor
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
## CLASS [Weight 7][Structure extraction] => FoivLawStructureExtractor
## @usecases
## - Extract structure: Reader → StructureExtractor → HierarchyBuilder → AnnotatedDocument
def _module_contract():
    pass
# endregion MODULE_CONTRACT
# GREP_SUMMARY: structure extractors, concrete structure extractors, foiv law structure extractor
# STRUCTURE: ▶ structure_extractors/concrete_structure_extractors/foiv_law_structure_extractor → ○ FoivLawStructureExtractor.cls → ⎋ result