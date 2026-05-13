from typing import List, Optional, Tuple

from dedoc.data_structures.concrete_annotations.bold_annotation import BoldAnnotation
from dedoc.data_structures.hierarchy_level import HierarchyLevel
from dedoc.data_structures.line_with_meta import LineWithMeta
from dedoc.structure_extractors.feature_extractors.list_features.list_utils import get_dotted_item_depth
from dedoc.structure_extractors.hierarchy_level_builders.abstract_hierarchy_level_builder import AbstractHierarchyLevelBuilder
from dedoc.structure_extractors.hierarchy_level_builders.law_builders.body_builder.abstract_body_hierarchy_level_builder import \
    AbstractBodyHierarchyLevelBuilder
from dedoc.structure_extractors.hierarchy_level_builders.utils_reg import regexps_digits_with_dots
from dedoc.structure_extractors.patterns import BracketListPattern, BulletListPattern, DottedListPattern, LetterListPattern, TagListPattern, TagPattern
from dedoc.structure_extractors.patterns.pattern_composition import PatternComposition

import logging
logger = logging.getLogger(__name__)


# region CLASS_DiplomaBodyBuilder [DOMAIN(DocumentProcessing): ...; CONCEPT(HierarchyBuilding): ...; TECH(Python): ...]
## @purpose DiplomaBodyBuilder for document structure extraction pipeline
class DiplomaBodyBuilder(AbstractHierarchyLevelBuilder):
    named_item_keywords = ("введение", "заключение", "библиографический список", "список литературы", "глава", "приложение", "приложения")

    # region METHOD___init__ [DOMAIN(X): ...; CONCEPT(Y): ...; TECH(Z): ...]
    ## @purpose __init__ method
    ## @io Input -> Output
    ## @complexity 5
    def __init__(self) -> None:
        super().__init__()

        self.logger.debug(f"[IMP:4][DiplomaBodyBuilder][__init___INIT] Starting")
        self.digits_with_dots_regexp = regexps_digits_with_dots
        self.pattern_composition = PatternComposition(
            [
                TagListPattern(line_type=HierarchyLevel.list_item, default_level_1=2, can_be_multiline=False),
                DottedListPattern(line_type=HierarchyLevel.list_item, level_1=2, can_be_multiline=False),
                BracketListPattern(line_type=HierarchyLevel.list_item, level_1=3, level_2=1, can_be_multiline=False),
                LetterListPattern(line_type=HierarchyLevel.list_item, level_1=4, level_2=1, can_be_multiline=False),
                BulletListPattern(line_type=HierarchyLevel.list_item, level_1=5, level_2=1, can_be_multiline=False),
                TagPattern(line_type=HierarchyLevel.raw_text)
            ]
        )

    # endregion METHOD___init__
    # region METHOD_get_lines_with_hierarchy [DOMAIN(X): ...; CONCEPT(Y): ...; TECH(Z): ...]
    ## @purpose get_lines_with_hierarchy method
    ## @io Input -> Output
    ## @complexity 5
    def get_lines_with_hierarchy(self, lines_with_labels: List[Tuple[LineWithMeta, str]], init_hl_depth: int) -> List[LineWithMeta]:
        self.logger.debug(f"[IMP:4][DiplomaBodyBuilder][get_lines_with_hierarchy_INIT] Starting")
        if len(lines_with_labels) > 0:
            line = lines_with_labels[0][0]
            page_id = line.metadata.page_id
            line_id = line.metadata.line_id
            body_line = AbstractBodyHierarchyLevelBuilder.get_body_line(page_id=page_id, line_id=line_id, init_hl_depth=init_hl_depth)
            result = [body_line]
        else:
            result = [AbstractBodyHierarchyLevelBuilder.get_body_line(init_hl_depth=init_hl_depth)]
        previous_named_item_line = None

        for line, prediction in lines_with_labels:
            if prediction == "named_item" or line.metadata.tag_hierarchy_level.line_type == "header":
                line = self.__handle_named_item(init_hl_depth, line, prediction, previous_named_item_line)
                previous_named_item_line = line
            elif prediction == "list_item":
                level = line.metadata.tag_hierarchy_level
                level_1 = previous_named_item_line.metadata.hierarchy_level.level_1 + level.level_1 - 1 if previous_named_item_line else \
                    init_hl_depth + level.level_1 - 1
                line.metadata.hierarchy_level = HierarchyLevel(level_1=level_1, level_2=level.level_2, line_type=prediction, can_be_multiline=True)
            elif prediction == "page_id":
                line.metadata.hierarchy_level = HierarchyLevel(level_1=None, level_2=None, line_type=prediction, can_be_multiline=False)
            elif prediction == "raw_text":
                line = self.__postprocess_raw_text(line, init_hl_depth)
                if not (line.metadata.hierarchy_level is not None and line.metadata.hierarchy_level.line_type == "named_item"):
                    line.metadata.hierarchy_level = self.pattern_composition.get_hierarchy_level(line)
            else:
                line.metadata.hierarchy_level = HierarchyLevel.create_raw_text()
                line.metadata.hierarchy_level.line_type = prediction
            result.append(line)
        return result

    # endregion METHOD_get_lines_with_hierarchy
    # region METHOD___handle_named_item [DOMAIN(X): ...; CONCEPT(Y): ...; TECH(Z): ...]
    ## @purpose __handle_named_item method
    ## @io Input -> Output
    ## @complexity 5
    def __handle_named_item(self, init_hl_depth: int, line: LineWithMeta, prediction: str, previous_named_item_line: Optional[LineWithMeta] = None)\
            -> LineWithMeta:
        self.logger.debug(f"[IMP:4][DiplomaBodyBuilder][__handle_named_item_INIT] Starting")
        text = line.line.strip().lower()
        item_depth = get_dotted_item_depth(text)

        if text.startswith(self.named_item_keywords):
            hierarchy_level = HierarchyLevel(init_hl_depth, 0, True, prediction)
        elif item_depth == -1:
            if previous_named_item_line:
                hierarchy_level = previous_named_item_line.metadata.hierarchy_level
            else:
                hierarchy_level = HierarchyLevel(init_hl_depth, 0, True, prediction)
        else:
            hierarchy_level = HierarchyLevel(init_hl_depth, item_depth - 1, True, prediction)
        line.metadata.hierarchy_level = hierarchy_level
        return line

    # endregion METHOD___handle_named_item
    # region METHOD___postprocess_raw_text [DOMAIN(X): ...; CONCEPT(Y): ...; TECH(Z): ...]
    ## @purpose __postprocess_raw_text method
    ## @io Input -> Output
    ## @complexity 5
    def __postprocess_raw_text(self, line: LineWithMeta, init_hl_depth: int) -> LineWithMeta:
        self.logger.debug(f"[IMP:4][DiplomaBodyBuilder][__postprocess_raw_text_INIT] Starting")
        text = line.line.strip().lower()
        if not text.startswith(self.named_item_keywords):
            return line

        bold = [annotation for annotation in line.annotations if annotation.name == BoldAnnotation.name and annotation.value == "True"]
        if len(bold) == 0:
            return line

        return self.__handle_named_item(init_hl_depth, line, "named_item")

    # endregion METHOD___postprocess_raw_text
# endregion CLASS_DiplomaBodyBuilder
# region MODULE_CONTRACT [DOMAIN(DocumentProcessing): ...; CONCEPT(HierarchyBuilding): ...; TECH(Python): ...]
## @modulecontract
## @purpose Document structure extraction for structure_extractors/hierarchy_level_builders/diploma_builder/body_builder: line classification, hierarchy level assignment, pattern matching.
## @scope Structure extraction pipeline — structure_extractors/hierarchy_level_builders/diploma_builder/body_builder
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
## CLASS [Weight 7][Structure extraction] => DiplomaBodyBuilder
## @usecases
## - Extract structure: Reader → StructureExtractor → HierarchyBuilder → AnnotatedDocument
def _module_contract():
    pass
# endregion MODULE_CONTRACT
# GREP_SUMMARY: structure extractors, hierarchy level builders, diploma builder, body builder
# STRUCTURE: ▶ structure_extractors/hierarchy_level_builders/diploma_builder/body_builder → ○ DiplomaBodyBuilder.cls → ⎋ result