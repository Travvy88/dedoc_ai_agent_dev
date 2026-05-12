import abc
import copy
from copy import deepcopy
from typing import List, Optional, Tuple

from dedoc.data_structures.hierarchy_level import HierarchyLevel
from dedoc.data_structures.line_with_meta import LineWithMeta
from dedoc.structure_extractors.feature_extractors.law_text_features import LawTextFeatures
from dedoc.structure_extractors.hierarchy_level_builders.abstract_hierarchy_level_builder import AbstractHierarchyLevelBuilder
from dedoc.structure_extractors.hierarchy_level_builders.law_builders.structure_unit.abstract_structure_unit import AbstractStructureUnit
from dedoc.structure_extractors.hierarchy_level_builders.utils_reg import regexps_item_with_bracket, regexps_number, roman_regexp

import logging
logger = logging.getLogger(__name__)


# region CLASS_AbstractApplicationHierarchyLevelBuilder [DOMAIN(DocumentProcessing): ...; CONCEPT(HierarchyBuilding): ...; TECH(Python): ...]
## @purpose AbstractApplicationHierarchyLevelBuilder for document structure extraction pipeline
class AbstractApplicationHierarchyLevelBuilder(AbstractHierarchyLevelBuilder, abc.ABC):
    starting_line_types = ["application"]
    regexps_item = regexps_item_with_bracket
    regexps_part = regexps_number
    regexp_application_begin = LawTextFeatures.regexp_application_begin
    roman_regexp = roman_regexp

    # region METHOD_structure_unit_builder [DOMAIN(X): ...; CONCEPT(Y): ...; TECH(Z): ...]
    ## @purpose structure_unit_builder method
    ## @io Input -> Output
    ## @complexity 5
    @property
    @abc.abstractmethod
    def structure_unit_builder(self) -> AbstractStructureUnit:
        self.logger.debug(f"[IMP:4][AbstractApplicationHierarchyLevelBuilder][structure_unit_builder_INIT] Starting")
        pass

    # endregion METHOD_structure_unit_builder
    # region METHOD_get_lines_with_hierarchy [DOMAIN(X): ...; CONCEPT(Y): ...; TECH(Z): ...]
    ## @purpose get_lines_with_hierarchy method
    ## @io Input -> Output
    ## @complexity 5
    def get_lines_with_hierarchy(self, lines_with_labels: List[Tuple[LineWithMeta, str]], init_hl_depth: int) -> List[LineWithMeta]:
        self.logger.debug(f"[IMP:4][AbstractApplicationHierarchyLevelBuilder][get_lines_with_hierarchy_INIT] Starting")
        if len(lines_with_labels) == 0:
            return []
        result = []
        # detect begin of body
        previous_hl = HierarchyLevel(level_1=init_hl_depth, level_2=0, can_be_multiline=True, line_type="application")

        lines_with_labels[0] = lines_with_labels[0][0], "application"
        previous_line_start_of_application = False
        for line_id, (line, label) in enumerate(lines_with_labels):
            # postprocessing of others units
            hierarchy_level, previous_hl = self._line_2level(text=line.line, label=label, init_hl_depth=init_hl_depth, previous_hl=previous_hl)
            assert previous_hl is None or hierarchy_level == previous_hl

            # postprocess multiple applications
            if self.regexp_application_begin.match(line.line.strip().lower()):
                hierarchy_level.can_be_multiline = previous_line_start_of_application
                previous_line_start_of_application = True
            elif line.line.strip() != "":
                previous_line_start_of_application = False

            self._postprocess_roman(hierarchy_level, line)

            metadata = deepcopy(line.metadata)
            hierarchy_level = copy.deepcopy(hierarchy_level)
            if line_id == 0:
                hierarchy_level.can_be_multiline = False
            metadata.hierarchy_level = hierarchy_level
            line = LineWithMeta(line=line.line, metadata=metadata, annotations=line.annotations, uid=line.uid)
            result.append(line)

        return result

    # endregion METHOD_get_lines_with_hierarchy
    # region METHOD__line_2level [DOMAIN(X): ...; CONCEPT(Y): ...; TECH(Z): ...]
    ## @purpose _line_2level method
    ## @io Input -> Output
    ## @complexity 5
    def _line_2level(self, text: str, label: str, init_hl_depth: int, previous_hl: HierarchyLevel = None) -> Tuple[HierarchyLevel, Optional[HierarchyLevel]]:
        self.logger.debug(f"[IMP:4][AbstractApplicationHierarchyLevelBuilder][_line_2level_INIT] Starting")
        text = text.strip()
        if len(text) == 0:
            label = HierarchyLevel.raw_text
        if label in ("header", "cellar"):
            label = "application"
        if label == "raw_text" and LawTextFeatures.regexp_application_begin.match(text):
            label = "application"
        if (label == "application" or label == "raw_text") and roman_regexp.match(text):
            label = "structure_unit"

        if label == "structure_unit":
            return self.structure_unit_builder.structure_unit(text=text, init_hl_depth=init_hl_depth, previous_hl=previous_hl)
        elif label == "footer":
            return HierarchyLevel(None, None, False, HierarchyLevel.raw_text), None
        elif label == "raw_text" and previous_hl is not None and previous_hl.line_type == "chapter":
            return previous_hl, previous_hl

        elif label == "raw_text" and previous_hl is None:
            return HierarchyLevel.create_raw_text(), None

        elif label == "Other":
            return HierarchyLevel(1, 1, False, "Other"), None

        elif label in ("application", "header", "raw_text"):
            application_continue = label == "raw_text" and previous_hl is not None and previous_hl.line_type == "application"
            if label == "application" or application_continue:
                hl = HierarchyLevel(init_hl_depth, 0, True, "application")
                return hl, hl
            else:
                return HierarchyLevel.create_raw_text(), None
        else:
            raise Exception(f"{text} {label}")

    # endregion METHOD__line_2level
# endregion CLASS_AbstractApplicationHierarchyLevelBuilder
# region MODULE_CONTRACT [DOMAIN(DocumentProcessing): ...; CONCEPT(HierarchyBuilding): ...; TECH(Python): ...]
## @modulecontract
## @purpose Document structure extraction for structure_extractors/hierarchy_level_builders/law_builders/application_builder/abstract_application_hierarchy_level_builder: line classification, hierarchy level assignment, pattern matching.
## @scope Structure extraction pipeline — structure_extractors/hierarchy_level_builders/law_builders/application_builder/abstract_application_hierarchy_level_builder
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
## CLASS [Weight 7][Structure extraction] => AbstractApplicationHierarchyLevelBuilder
## @usecases
## - Extract structure: Reader → StructureExtractor → HierarchyBuilder → AnnotatedDocument
def _module_contract():
    pass
# endregion MODULE_CONTRACT
# GREP_SUMMARY: structure extractors, hierarchy level builders, law builders, application builder, abstract application hierarchy level builder
# STRUCTURE: ▶ structure_extractors/hierarchy_level_builders/law_builders/application_builder/abstract_application_hierarchy_level_builder → ○ AbstractApplicationHierarchyLevelBuilder.cls → ⎋ result