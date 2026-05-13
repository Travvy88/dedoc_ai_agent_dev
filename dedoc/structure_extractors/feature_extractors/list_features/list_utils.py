from typing import List

from dedoc.data_structures.line_with_meta import LineWithMeta
from dedoc.structure_extractors.feature_extractors.abstract_extractor import AbstractFeatureExtractor
from dedoc.structure_extractors.feature_extractors.list_features.prefix.dotted_prefix import DottedPrefix
from dedoc.structure_extractors.feature_extractors.list_features.prefix.empty_prefix import EmptyPrefix
from dedoc.structure_extractors.feature_extractors.list_features.prefix.prefix import LinePrefix

import logging
logger = logging.getLogger(__name__)


# region FUNC_get_dotted_item_depth [DOMAIN(DocumentProcessing): ...; CONCEPT(FeatureEngineering): ...; TECH(Pandas): ...]
## @purpose get_dotted_item_depth utility function
## @io Input -> Output
## @complexity 3
def get_dotted_item_depth(text: str) -> int:
    logger.debug("[IMP:4][get_dotted_item_depth][INIT]")
    match = DottedPrefix.regexp.match(text)
    if match:
        prefix = DottedPrefix(match.group().strip(), indent=0)
        return len(prefix.numbers)
    else:
        return -1


# endregion FUNC_get_dotted_item_depth
# region FUNC_get_prefix [DOMAIN(DocumentProcessing): ...; CONCEPT(FeatureEngineering): ...; TECH(Pandas): ...]
## @purpose get_prefix utility function
## @io Input -> Output
## @complexity 3
def get_prefix(prefix_list: List[LinePrefix], line: LineWithMeta) -> LinePrefix:
    logger.debug("[IMP:4][get_prefix][INIT]")
    text = line.line.strip().lower()
    indent = AbstractFeatureExtractor._get_indentation(line)

    for prefix in prefix_list:
        match = prefix.regexp.match(text)
        if match:
            return prefix(match.group().strip(), indent=indent)
    return EmptyPrefix(indent=indent)

# endregion FUNC_get_prefix
# region MODULE_CONTRACT [DOMAIN(DocumentProcessing): ...; CONCEPT(FeatureEngineering): ...; TECH(Pandas): ...]
## @modulecontract
## @purpose Document structure extraction for structure_extractors/feature_extractors/list_features/list_utils: line classification, hierarchy level assignment, pattern matching.
## @scope Structure extraction pipeline — structure_extractors/feature_extractors/list_features/list_utils
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
## FUNC [Weight 5][Utility] => get_dotted_item_depth
## FUNC [Weight 5][Utility] => get_prefix
## @usecases
## - Extract structure: Reader → StructureExtractor → HierarchyBuilder → AnnotatedDocument
def _module_contract():
    pass
# endregion MODULE_CONTRACT
# GREP_SUMMARY: structure extractors, feature extractors, list features, list utils
# STRUCTURE: ▶ structure_extractors/feature_extractors/list_features/list_utils → ○ get_dotted_item_depth.func ⊕ get_prefix.func → ⎋ result