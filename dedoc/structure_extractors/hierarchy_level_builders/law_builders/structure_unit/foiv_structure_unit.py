from typing import Optional, Tuple

from dedoc.data_structures.hierarchy_level import HierarchyLevel
from dedoc.structure_extractors.hierarchy_level_builders.law_builders.structure_unit.abstract_structure_unit import AbstractStructureUnit
from dedoc.structure_extractors.hierarchy_level_builders.utils_reg import regexps_foiv_item, regexps_item_with_bracket, regexps_subitem, roman_regexp

import logging
logger = logging.getLogger(__name__)


# region CLASS_FoivStructureUnitBuilder [DOMAIN(DocumentProcessing): ...; CONCEPT(HierarchyBuilding): ...; TECH(Python): ...]
## @purpose FoivStructureUnitBuilder for document structure extraction pipeline
class FoivStructureUnitBuilder(AbstractStructureUnit):
    document_types = ["foiv"]
    regexps_item = regexps_foiv_item
    regexps_subitem_with_char = regexps_subitem
    regexps_subitem_with_number = regexps_item_with_bracket

    # region METHOD_structure_unit [DOMAIN(X): ...; CONCEPT(Y): ...; TECH(Z): ...]
    ## @purpose structure_unit method
    ## @io Input -> Output
    ## @complexity 5
    def structure_unit(self, text: str, init_hl_depth: int, previous_hl: Optional[HierarchyLevel]) -> Tuple[HierarchyLevel, Optional[HierarchyLevel]]:
        self.logger.debug(f"[IMP:4][FoivStructureUnitBuilder][structure_unit_INIT] Starting")
        if text.lower().startswith("глава") or roman_regexp.match(text):
            hl = HierarchyLevel(init_hl_depth + 4, 0, True, "chapter")
            return hl, hl

        match_subitem = self.regexps_subitem_with_number.match(text)
        if match_subitem:
            nodes = [i for i in text[match_subitem.start(): match_subitem.end()].split(".") if len(i.strip()) > 0]
            hl = HierarchyLevel(init_hl_depth + 9, len(nodes), False, "subitem")
            return hl, hl
        match_subitem = self.regexps_subitem_with_char.match(text)
        if match_subitem:
            nodes = [i for i in text[match_subitem.start(): match_subitem.end()].split(".") if len(i.strip()) > 0]
            hl = HierarchyLevel(init_hl_depth + 10, len(nodes), False, "subitem")
            return hl, hl
        match_item = self.regexps_item.match(text)
        if match_item:
            nodes = [i for i in text[match_item.start(): match_item.end()].split(".") if len(i.strip()) > 0]
            hl = HierarchyLevel(init_hl_depth + 8, len(nodes), False, "item")
            return hl, hl
        elif previous_hl is not None:
            return previous_hl, previous_hl

        return HierarchyLevel(None, None, False, HierarchyLevel.raw_text), None

    # endregion METHOD_structure_unit
# endregion CLASS_FoivStructureUnitBuilder
# region MODULE_CONTRACT [DOMAIN(DocumentProcessing): ...; CONCEPT(HierarchyBuilding): ...; TECH(Python): ...]
## @modulecontract
## @purpose Document structure extraction for structure_extractors/hierarchy_level_builders/law_builders/structure_unit/foiv_structure_unit: line classification, hierarchy level assignment, pattern matching.
## @scope Structure extraction pipeline — structure_extractors/hierarchy_level_builders/law_builders/structure_unit/foiv_structure_unit
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
## CLASS [Weight 7][Structure extraction] => FoivStructureUnitBuilder
## @usecases
## - Extract structure: Reader → StructureExtractor → HierarchyBuilder → AnnotatedDocument
def _module_contract():
    pass
# endregion MODULE_CONTRACT
# GREP_SUMMARY: structure extractors, hierarchy level builders, law builders, structure unit, foiv structure unit
# STRUCTURE: ▶ structure_extractors/hierarchy_level_builders/law_builders/structure_unit/foiv_structure_unit → ○ FoivStructureUnitBuilder.cls → ⎋ result