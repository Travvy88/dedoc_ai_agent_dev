from typing import Optional, Tuple

from dedoc.data_structures.hierarchy_level import HierarchyLevel
from dedoc.structure_extractors.hierarchy_level_builders.law_builders.structure_unit.abstract_structure_unit import AbstractStructureUnit

import logging
logger = logging.getLogger(__name__)
from dedoc.structure_extractors.hierarchy_level_builders.utils_reg import regexps_ends_of_number, regexps_foiv_item, regexps_item_with_bracket, \
    regexps_subitem, roman_regexp


# region CLASS_LawStructureUnitBuilder [DOMAIN(DocumentProcessing): ...; CONCEPT(HierarchyBuilding): ...; TECH(Python): ...]
## @purpose LawStructureUnitBuilder for document structure extraction pipeline
class LawStructureUnitBuilder(AbstractStructureUnit):
    document_types = ["law"]
    regexps_item_with_bracket = regexps_item_with_bracket
    regexps_part = regexps_foiv_item
    ends_of_number = regexps_ends_of_number
    regexps_subitem = regexps_subitem
    roman_regexp = roman_regexp

    # region METHOD_structure_unit [DOMAIN(X): ...; CONCEPT(Y): ...; TECH(Z): ...]
    ## @purpose structure_unit method
    ## @io Input -> Output
    ## @complexity 5
    def structure_unit(self, text: str, init_hl_depth: int, previous_hl: Optional[HierarchyLevel]) -> Tuple[HierarchyLevel, Optional[HierarchyLevel]]:
        logger.debug(f"[IMP:4][LawStructureUnitBuilder][structure_unit_INIT] Starting")
        if text.lower().startswith("часть"):
            hl = HierarchyLevel(init_hl_depth + 1, 0, True, "part")  # 3
            return hl, hl
        if text.lower().startswith("раздел"):
            hl = HierarchyLevel(init_hl_depth + 2, 0, True, "section")  # 4
            return hl, hl
        if self.roman_regexp.match(text):  # match roman numbers
            hl = HierarchyLevel(init_hl_depth + 3, 0, True, "subsection")  # 5
            return hl, hl
        if text.lower().startswith("глава"):
            hl = HierarchyLevel(init_hl_depth + 4, 0, True, "chapter")  # 6
            return hl, hl
        if text.lower().startswith("§"):
            hl = HierarchyLevel(init_hl_depth + 5, 0, True, "paragraph")  # 7
            return hl, hl
        if text.lower().startswith("статья"):
            hl = HierarchyLevel(init_hl_depth + 6, 0, True, "article")  # 8
            return hl, hl
        # We should check item before the part case sometimes part does not contain dot
        match_item = self.regexps_item_with_bracket.match(text)
        if match_item:
            return HierarchyLevel(init_hl_depth + 8, 0, False, "item"), None  # 10
        match_part = self.regexps_part.match(text)
        if match_part:
            len(match_part.group().split("."))
            return HierarchyLevel(init_hl_depth + 7, 0, False, "articlePart"), None  # 9
        if self.regexps_subitem.match(text):
            return HierarchyLevel(init_hl_depth + 9, 0, False, "subitem"), None  # 11
        elif previous_hl is not None:
            return previous_hl, previous_hl
        return HierarchyLevel(None, None, False, HierarchyLevel.raw_text), None

    # endregion METHOD_structure_unit
# endregion CLASS_LawStructureUnitBuilder
# region MODULE_CONTRACT [DOMAIN(DocumentProcessing): ...; CONCEPT(HierarchyBuilding): ...; TECH(Python): ...]
## @modulecontract
## @purpose Document structure extraction for structure_extractors/hierarchy_level_builders/law_builders/structure_unit/law_structure_unit: line classification, hierarchy level assignment, pattern matching.
## @scope Structure extraction pipeline — structure_extractors/hierarchy_level_builders/law_builders/structure_unit/law_structure_unit
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
## CLASS [Weight 7][Structure extraction] => LawStructureUnitBuilder
## @usecases
## - Extract structure: Reader → StructureExtractor → HierarchyBuilder → AnnotatedDocument
def _module_contract():
    pass
# endregion MODULE_CONTRACT
# GREP_SUMMARY: structure extractors, hierarchy level builders, law builders, structure unit, law structure unit
# STRUCTURE: ▶ structure_extractors/hierarchy_level_builders/law_builders/structure_unit/law_structure_unit → ○ LawStructureUnitBuilder.cls → ⎋ result