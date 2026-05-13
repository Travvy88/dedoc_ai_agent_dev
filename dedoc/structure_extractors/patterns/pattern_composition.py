from typing import List

from dedoc.data_structures.hierarchy_level import HierarchyLevel
from dedoc.data_structures.line_with_meta import LineWithMeta
from dedoc.structure_extractors.patterns.abstract_pattern import AbstractPattern

import logging
logger = logging.getLogger(__name__)


# region CLASS_PatternComposition [DOMAIN(DocumentProcessing): ...; CONCEPT(PatternMatching): ...; TECH(Regexp): ...]
## @purpose PatternComposition for document structure extraction pipeline
class PatternComposition:
    """
    Class for applying patterns to get line's hierarchy level.

    Example of usage:

    .. code-block:: python

        from dedoc.data_structures.line_with_meta import LineWithMeta
        from dedoc.structure_extractors.patterns import TagListPattern, TagPattern
        from dedoc.structure_extractors.patterns.pattern_composition import PatternComposition


        pattern_composition = PatternComposition(
            patterns=[
                TagListPattern(line_type="list_item", default_level_1=2, can_be_multiline=False),
                TagPattern(default_line_type="raw_text")
            ]
        )
        line = LineWithMeta(line="Some text")
        line.metadata.hierarchy_level = pattern_composition.get_hierarchy_level(line=line)
    """
    # region METHOD___init__ [DOMAIN(X): ...; CONCEPT(Y): ...; TECH(Z): ...]
    ## @purpose __init__ method
    ## @io Input -> Output
    ## @complexity 5
    def __init__(self, patterns: List[AbstractPattern]) -> None:
        self.logger = logging.getLogger(__name__)
        self.logger.debug(f"[IMP:4][PatternComposition][__init___INIT] Starting")
        """
        Set the list of patterns to apply to lines.

        **Note:** the order of the patterns is important. More specific patterns should go first.
        Otherwise, they may be ignored because of the patterns which also are applicable to the given line.

        :param patterns: list of patterns to apply to lines.
        """
        self.patterns = patterns

    # endregion METHOD___init__
    # region METHOD_get_hierarchy_level [DOMAIN(X): ...; CONCEPT(Y): ...; TECH(Z): ...]
    ## @purpose get_hierarchy_level method
    ## @io Input -> Output
    ## @complexity 5
    def get_hierarchy_level(self, line: LineWithMeta) -> HierarchyLevel:
        self.logger.debug(f"[IMP:4][PatternComposition][get_hierarchy_level_INIT] Starting")
        """
        Choose the suitable pattern from the list of patterns for applying to the given line.
        The first applicable pattern will be chosen.
        If no applicable pattern was found, the default ``raw_text`` :class:`~dedoc.data_structures.HierarchyLevel` is used as result.

        :param line: line to get hierarchy level for.
        """
        line_pattern = None

        for pattern in self.patterns:
            if pattern.match(line):
                line_pattern = pattern
                break

        return line_pattern.get_hierarchy_level(line) if line_pattern else HierarchyLevel.create_raw_text()

    # endregion METHOD_get_hierarchy_level
# endregion CLASS_PatternComposition
# region MODULE_CONTRACT [DOMAIN(DocumentProcessing): ...; CONCEPT(PatternMatching): ...; TECH(Regexp): ...]
## @modulecontract
## @purpose Document structure extraction for structure_extractors/patterns/pattern_composition: line classification, hierarchy level assignment, pattern matching.
## @scope Structure extraction pipeline — structure_extractors/patterns/pattern_composition
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
## CLASS [Weight 7][Structure extraction] => PatternComposition
## @usecases
## - Extract structure: Reader → StructureExtractor → HierarchyBuilder → AnnotatedDocument
def _module_contract():
    pass
# endregion MODULE_CONTRACT
# GREP_SUMMARY: structure extractors, patterns, pattern composition
# STRUCTURE: ▶ structure_extractors/patterns/pattern_composition → ○ PatternComposition.cls → ⎋ result