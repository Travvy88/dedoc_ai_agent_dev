import re

from dedoc.structure_extractors.feature_extractors.list_features.prefix.prefix import LinePrefix

import logging
logger = logging.getLogger(__name__)


# region CLASS_DottedPrefix [DOMAIN(DocumentProcessing): ...; CONCEPT(FeatureEngineering): ...; TECH(Pandas): ...]
## @purpose DottedPrefix for document structure extraction pipeline
class DottedPrefix(LinePrefix):

    regexp = re.compile(r"^\s*(\d+\.)+(\d+)?\s*")
    name = "dotted"

    # region METHOD___init__ [DOMAIN(X): ...; CONCEPT(Y): ...; TECH(Z): ...]
    ## @purpose __init__ method
    ## @io Input -> Output
    ## @complexity 5
    def __init__(self, prefix: str, indent: float) -> None:
        logger.debug(f"[IMP:4][DottedPrefix][__init___INIT] Starting")
        super().__init__(prefix, indent=indent)
        self.numbers = [int(n) for n in self.prefix.split(".") if len(n) > 0]

    # endregion METHOD___init__
    # region METHOD_predecessor [DOMAIN(X): ...; CONCEPT(Y): ...; TECH(Z): ...]
    ## @purpose predecessor method
    ## @io Input -> Output
    ## @complexity 5
    def predecessor(self, other: "DottedPrefix") -> bool:
        logger.debug(f"[IMP:4][DottedPrefix][predecessor_INIT] Starting")
        if not isinstance(other, DottedPrefix):
            return False
        if len(self.numbers) == len(other.numbers):
            for n1, n2 in zip(self.numbers[:-1], other.numbers[:-1]):
                if n1 != n2:
                    return False
            n1, n2 = self.numbers[-1], other.numbers[-1]
            return n1 - n2 == 1
        if len(self.numbers) == 1 + len(other.numbers):
            for n1, n2 in zip(self.numbers, other.numbers):
                if n1 != n2:
                    return False
            return self.numbers[-1] == 1
        if len(other.numbers) > len(self.numbers):
            for n1, n2 in zip(self.numbers[:-1], other.numbers[:-1]):
                if n1 != n2:
                    return False
            return self.numbers[-1] == other.numbers[len(self.numbers) - 1] + 1
        return False

    # endregion METHOD_predecessor
    # region METHOD_is_valid [DOMAIN(X): ...; CONCEPT(Y): ...; TECH(Z): ...]
    ## @purpose is_valid method
    ## @io Input -> Output
    ## @complexity 5
    @staticmethod
    def is_valid(prefix_str: str) -> bool:
        logger.debug(f"[IMP:4][DottedPrefix][is_valid_INIT] Starting")
        return len(prefix_str) > 0 and all(_.isdigit() for _ in prefix_str.split(".") if _)

    # endregion METHOD_is_valid
# endregion CLASS_DottedPrefix
# region MODULE_CONTRACT [DOMAIN(DocumentProcessing): ...; CONCEPT(FeatureEngineering): ...; TECH(Pandas): ...]
## @modulecontract
## @purpose Document structure extraction for structure_extractors/feature_extractors/list_features/prefix/dotted_prefix: line classification, hierarchy level assignment, pattern matching.
## @scope Structure extraction pipeline — structure_extractors/feature_extractors/list_features/prefix/dotted_prefix
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
## CLASS [Weight 7][Structure extraction] => DottedPrefix
## @usecases
## - Extract structure: Reader → StructureExtractor → HierarchyBuilder → AnnotatedDocument
def _module_contract():
    pass
# endregion MODULE_CONTRACT
# GREP_SUMMARY: structure extractors, feature extractors, list features, prefix, dotted prefix
# STRUCTURE: ▶ structure_extractors/feature_extractors/list_features/prefix/dotted_prefix → ○ DottedPrefix.cls → ⎋ result