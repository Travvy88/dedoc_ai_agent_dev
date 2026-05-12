import abc
from copy import deepcopy
from typing import List, Optional, Tuple
from uuid import uuid1

from dedoc.data_structures.hierarchy_level import HierarchyLevel
from dedoc.data_structures.line_metadata import LineMetadata
from dedoc.data_structures.line_with_meta import LineWithMeta
from dedoc.structure_extractors.hierarchy_level_builders.abstract_hierarchy_level_builder import AbstractHierarchyLevelBuilder
from dedoc.structure_extractors.hierarchy_level_builders.law_builders.structure_unit.abstract_structure_unit import AbstractStructureUnit

import logging
logger = logging.getLogger(__name__)
from dedoc.structure_extractors.hierarchy_level_builders.utils_reg import regexps_ends_of_number, regexps_item_with_bracket, regexps_number, \
    regexps_subitem, roman_regexp


# region CLASS_AbstractBodyHierarchyLevelBuilder [DOMAIN(DocumentProcessing): ...; CONCEPT(HierarchyBuilding): ...; TECH(Python): ...]
## @purpose AbstractBodyHierarchyLevelBuilder for document structure extraction pipeline
class AbstractBodyHierarchyLevelBuilder(AbstractHierarchyLevelBuilder, abc.ABC):
    starting_line_types = ["body"]
    regexps_item = regexps_item_with_bracket
    regexps_part = regexps_number
    ends_of_number = regexps_ends_of_number
    regexps_subitem = regexps_subitem
    roman_regexp = roman_regexp

    # region METHOD_structure_unit_builder [DOMAIN(X): ...; CONCEPT(Y): ...; TECH(Z): ...]
    ## @purpose structure_unit_builder method
    ## @io Input -> Output
    ## @complexity 5
    @property
    @abc.abstractmethod
    def structure_unit_builder(self) -> AbstractStructureUnit:
        self.logger.debug(f"[IMP:4][AbstractBodyHierarchyLevelBuilder][structure_unit_builder_INIT] Starting")
        pass

    # endregion METHOD_structure_unit_builder
    # region METHOD_get_body_line [DOMAIN(X): ...; CONCEPT(Y): ...; TECH(Z): ...]
    ## @purpose get_body_line method
    ## @io Input -> Output
    ## @complexity 5
    @staticmethod
    def get_body_line(page_id: int = 0, line_id: int = 0, init_hl_depth: int = 1) -> LineWithMeta:
        self.logger.debug(f"[IMP:4][AbstractBodyHierarchyLevelBuilder][get_body_line_INIT] Starting")
        # if line_with_label is None:
        line_uid = str(uuid1()) + "_body"
        page_id = page_id
        line_id = line_id
        return LineWithMeta(line="",
                            metadata=LineMetadata(hierarchy_level=HierarchyLevel(init_hl_depth, 0, False, "body"), page_id=page_id, line_id=line_id),
                            annotations=[],
                            uid=line_uid)

    # endregion METHOD_get_body_line
    # region METHOD_get_lines_with_hierarchy [DOMAIN(X): ...; CONCEPT(Y): ...; TECH(Z): ...]
    ## @purpose get_lines_with_hierarchy method
    ## @io Input -> Output
    ## @complexity 5
    def get_lines_with_hierarchy(self, lines_with_labels: List[Tuple[LineWithMeta, str]], init_hl_depth: int = 2) -> List[LineWithMeta]:
        self.logger.debug(f"[IMP:4][AbstractBodyHierarchyLevelBuilder][get_lines_with_hierarchy_INIT] Starting")
        result = []
        # detect begin of body
        is_body_begun = False
        previous_hl = HierarchyLevel.create_root()

        for line, label in lines_with_labels:

            # postprocessing of others units
            hierarchy_level, previous_hl = self._line_2level(text=line.line, label=label, init_hl_depth=init_hl_depth, previous_hl=previous_hl)
            self._postprocess_roman(hierarchy_level, line)

            hierarchy_level = deepcopy(hierarchy_level)
            if len(line.line.strip()) == 0:
                hierarchy_level.can_be_multiline = True
            metadata = deepcopy(line.metadata)
            metadata.hierarchy_level = hierarchy_level

            if hierarchy_level.line_type != HierarchyLevel.root and not is_body_begun:
                result.append(self.get_body_line(init_hl_depth=init_hl_depth))
                is_body_begun = True

            line = LineWithMeta(line=line.line, metadata=metadata, annotations=line.annotations, uid=line.uid)
            result.append(line)
        if not is_body_begun:
            result.append(self.get_body_line(init_hl_depth=init_hl_depth))
        return result

    # endregion METHOD_get_lines_with_hierarchy
    # region METHOD__line_2level [DOMAIN(X): ...; CONCEPT(Y): ...; TECH(Z): ...]
    ## @purpose _line_2level method
    ## @io Input -> Output
    ## @complexity 5
    def _line_2level(self, text: str, label: str, init_hl_depth: int, previous_hl: HierarchyLevel = None) -> Tuple[HierarchyLevel, Optional[HierarchyLevel]]:
        self.logger.debug(f"[IMP:4][AbstractBodyHierarchyLevelBuilder][_line_2level_INIT] Starting")
        text = text.strip()
        if label == "header":
            label = "raw_text"

        if (label in ("application", "raw_text", "cellar")) and self.roman_regexp.match(text):
            label = "structure_unit"

        if label == "structure_unit":
            return self.structure_unit_builder.structure_unit(text=text, init_hl_depth=init_hl_depth, previous_hl=previous_hl)
        if label == "footer":
            return HierarchyLevel(None, None, False, HierarchyLevel.raw_text), None
        if label == "raw_text":
            if previous_hl is not None:
                if previous_hl.line_type in ["application", "chapter"]:
                    return previous_hl, previous_hl
            return HierarchyLevel(None, None, False, HierarchyLevel.raw_text), None

        if label == "Other":
            return HierarchyLevel(1, 1, False, "Other"), None

        if label == "application":
            return HierarchyLevel(None, None, False, HierarchyLevel.raw_text), None
        else:
            raise Exception(f"{text} {label}")

    # endregion METHOD__line_2level
# endregion CLASS_AbstractBodyHierarchyLevelBuilder
# region MODULE_CONTRACT [DOMAIN(DocumentProcessing): ...; CONCEPT(HierarchyBuilding): ...; TECH(Python): ...]
## @modulecontract
## @purpose Document structure extraction for structure_extractors/hierarchy_level_builders/law_builders/body_builder/abstract_body_hierarchy_level_builder: line classification, hierarchy level assignment, pattern matching.
## @scope Structure extraction pipeline — structure_extractors/hierarchy_level_builders/law_builders/body_builder/abstract_body_hierarchy_level_builder
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
## CLASS [Weight 7][Structure extraction] => AbstractBodyHierarchyLevelBuilder
## @usecases
## - Extract structure: Reader → StructureExtractor → HierarchyBuilder → AnnotatedDocument
def _module_contract():
    pass
# endregion MODULE_CONTRACT
# GREP_SUMMARY: structure extractors, hierarchy level builders, law builders, body builder, abstract body hierarchy level builder
# STRUCTURE: ▶ structure_extractors/hierarchy_level_builders/law_builders/body_builder/abstract_body_hierarchy_level_builder → ○ AbstractBodyHierarchyLevelBuilder.cls → ⎋ result