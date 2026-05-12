from copy import deepcopy

from dedoc.common.exceptions.structure_extractor_error import StructureExtractorError
from dedoc.structure_extractors.patterns.abstract_pattern import AbstractPattern

import logging
logger = logging.getLogger(__name__)


# region FUNC_get_pattern [DOMAIN(DocumentProcessing): ...; CONCEPT(PatternMatching): ...; TECH(Regexp): ...]
## @purpose get_pattern utility function
## @io Input -> Output
## @complexity 3
def get_pattern(pattern_parameters: dict) -> AbstractPattern:
    logger.debug("[IMP:4][get_pattern][INIT]")
    import dedoc.structure_extractors.patterns as patterns_module

    if "name" not in pattern_parameters:
        raise StructureExtractorError(msg="Pattern parameter missing 'name'")

    supported_patterns = {pattern.name(): pattern for pattern in patterns_module.__all__}
    pattern_class = supported_patterns.get(pattern_parameters["name"])

    if pattern_class is None:
        raise StructureExtractorError(msg=f"Pattern {pattern_parameters['name']} is not found in supported patterns: {supported_patterns.keys()}")

    pattern_parameters_copy = deepcopy(pattern_parameters)
    pattern_parameters_copy.pop("name")
    try:
        pattern = pattern_class(**pattern_parameters_copy)
    except TypeError as e:
        raise StructureExtractorError(msg=str(e))
    return pattern

# endregion FUNC_get_pattern
# region MODULE_CONTRACT [DOMAIN(DocumentProcessing): ...; CONCEPT(PatternMatching): ...; TECH(Regexp): ...]
## @modulecontract
## @purpose Document structure extraction for structure_extractors/patterns/utils: line classification, hierarchy level assignment, pattern matching.
## @scope Structure extraction pipeline — structure_extractors/patterns/utils
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
## FUNC [Weight 5][Utility] => get_pattern
## @usecases
## - Extract structure: Reader → StructureExtractor → HierarchyBuilder → AnnotatedDocument
def _module_contract():
    pass
# endregion MODULE_CONTRACT
# GREP_SUMMARY: structure extractors, patterns, utils
# STRUCTURE: ▶ structure_extractors/patterns/utils → ○ get_pattern.func → ⎋ result