import abc
from typing import List, Optional, Tuple

from dedoc.data_structures.hierarchy_level import HierarchyLevel
from dedoc.data_structures.line_with_meta import LineWithMeta
from dedoc.structure_extractors.hierarchy_level_builders.utils_reg import roman_regexp

import logging
logger = logging.getLogger(__name__)


# region CLASS_AbstractHierarchyLevelBuilder [DOMAIN(DocumentProcessing): ...; CONCEPT(HierarchyBuilding): ...; TECH(Python): ...]
## @purpose AbstractHierarchyLevelBuilder for document structure extraction pipeline
class AbstractHierarchyLevelBuilder(abc.ABC):
    starting_line_types = [""]
    document_types = [""]
    """
    Class is extracted hierarchy level for each line of the input chunk.
    Where the chunk is list of LineWithMeta with their predicted labels from the classifier.
    The chunk is a block from the document.
    self.starting_line_type - is a predicted type of start line from classifier. It is a type of the first line of the chunk.
    You must set:
    1 - self.starting_line_type as the type of the first line of input chunk.
    2 - write function get_lines_with_hierarchy(...)
    """

    # region METHOD___init__ [DOMAIN(X): ...; CONCEPT(Y): ...; TECH(Z): ...]
    ## @purpose Initialize base hierarchy level builder with logger
    ## @io Optional[dict] -> None
    ## @complexity 1
    def __init__(self, *, config: Optional[dict] = None) -> None:
        self.logger = (config or {}).get("logger", logging.getLogger(__name__)) if config else logging.getLogger(__name__)
    # endregion METHOD___init__

    # region METHOD_can_build [DOMAIN(X): ...; CONCEPT(Y): ...; TECH(Z): ...]
    ## @purpose can_build method
    ## @io Input -> Output
    ## @complexity 5
    def can_build(self, tag: str, document_type: str) -> bool:
        self.logger.debug(f"[IMP:4][AbstractHierarchyLevelBuilder][can_build_INIT] Starting")
        """
        if the first line type of the chunk equals starting_line_type, then this is the right builder
        @param tag: the first line type of the input chunk
        @return: can or can't work with this builder
        """

        return tag in self.starting_line_types and document_type in self.document_types

    # endregion METHOD_can_build
    # region METHOD_get_lines_with_hierarchy [DOMAIN(X): ...; CONCEPT(Y): ...; TECH(Z): ...]
    ## @purpose get_lines_with_hierarchy method
    ## @io Input -> Output
    ## @complexity 5
    @abc.abstractmethod
    def get_lines_with_hierarchy(self, lines_with_labels: List[Tuple[LineWithMeta, str]], init_hl_depth: int) -> List[LineWithMeta]:
        self.logger.debug(f"[IMP:4][AbstractHierarchyLevelBuilder][get_lines_with_hierarchy_INIT] Starting")
        """
        is a major function for extraction hierarchy level
        for each LineWithMeta with label (predicted class from classifier)
        @param lines_with_labels - lines of input chunk (a block from document)
        """
        pass

    # endregion METHOD_get_lines_with_hierarchy
    # region METHOD__postprocess_roman [DOMAIN(X): ...; CONCEPT(Y): ...; TECH(Z): ...]
    ## @purpose _postprocess_roman method
    ## @io Input -> Output
    ## @complexity 5
    @staticmethod
    def _postprocess_roman(hierarchy_level: HierarchyLevel, line: LineWithMeta) -> LineWithMeta:
        logger.debug(f"[IMP:4][AbstractHierarchyLevelBuilder][_postprocess_roman_INIT] Starting")
        # BUG_FIX_CONTEXT: self.logger недоступен в @staticmethod; заменён на модульный logger
        if hierarchy_level.line_type == "subsection" and roman_regexp.match(line.line):
            match = roman_regexp.match(line.line)
            prefix = line.line[match.start(): match.end()]
            suffix = line.line[match.end():]
            symbols = [("T", "I"), ("Т", "I"), ("У", "V"), ("П", "II"), ("Ш", "III"), ("Г", "I")]
            for symbol_from, symbol_to in symbols:
                prefix = prefix.replace(symbol_from, symbol_to)
            line.set_line(prefix + suffix)
        return line

    # endregion METHOD__postprocess_roman
# endregion CLASS_AbstractHierarchyLevelBuilder
# region MODULE_CONTRACT [DOMAIN(DocumentProcessing): ...; CONCEPT(HierarchyBuilding): ...; TECH(Python): ...]
## @modulecontract
## @purpose Document structure extraction for structure_extractors/hierarchy_level_builders/abstract_hierarchy_level_builder: line classification, hierarchy level assignment, pattern matching.
## @scope Structure extraction pipeline — structure_extractors/hierarchy_level_builders/abstract_hierarchy_level_builder
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
## CLASS [Weight 7][Structure extraction] => AbstractHierarchyLevelBuilder
## @usecases
## - Extract structure: Reader → StructureExtractor → HierarchyBuilder → AnnotatedDocument
def _module_contract():
    pass
# endregion MODULE_CONTRACT
# GREP_SUMMARY: structure extractors, hierarchy level builders, abstract hierarchy level builder
# STRUCTURE: ▶ structure_extractors/hierarchy_level_builders/abstract_hierarchy_level_builder → ○ AbstractHierarchyLevelBuilder.cls → ⎋ result