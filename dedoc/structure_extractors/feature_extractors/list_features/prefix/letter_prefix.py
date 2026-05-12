import re

from dedoc.structure_extractors.feature_extractors.list_features.prefix.prefix import LinePrefix

import logging
logger = logging.getLogger(__name__)


# region CLASS_LetterPrefix [DOMAIN(DocumentProcessing): ...; CONCEPT(FeatureEngineering): ...; TECH(Pandas): ...]
## @purpose LetterPrefix for document structure extraction pipeline
class LetterPrefix(LinePrefix):
    """
    for such items as

    a) first letter
    b) second letter

    or for russian
    а) Moskau — fremd und geheimnisvoll
    б) Türme aus rotem Gold
    в) Kalt wie das Eis
    """

    regexp = re.compile(r"^\s*[а-яёa-z]\)")
    name = "letter"

    # region METHOD_order [DOMAIN(X): ...; CONCEPT(Y): ...; TECH(Z): ...]
    ## @purpose order method
    ## @io Input -> Output
    ## @complexity 5
    @property
    def order(self) -> float:
        logger.debug(f"[IMP:4][LetterPrefix][order_INIT] Starting")
        letter = self.prefix[0]
        if letter == "ё":  # ё is between е and ж, but ord("ё") is not between them
            return 0.5 * (ord("е") + ord("ж"))
        elif letter == "Ё":  # Ё is between Е and Ж, but ord("Ё") is not between them
            return 0.5 * (ord("Е") + ord("Ж"))
        else:
            return ord(letter)

    # endregion METHOD_order
    # region METHOD_predecessor [DOMAIN(X): ...; CONCEPT(Y): ...; TECH(Z): ...]
    ## @purpose predecessor method
    ## @io Input -> Output
    ## @complexity 5
    def predecessor(self, other: LinePrefix) -> bool:
        logger.debug(f"[IMP:4][LetterPrefix][predecessor_INIT] Starting")
        return isinstance(other, LetterPrefix) and 1 >= (self.order - other.order) > 0

    # endregion METHOD_predecessor
    # region METHOD_is_valid [DOMAIN(X): ...; CONCEPT(Y): ...; TECH(Z): ...]
    ## @purpose is_valid method
    ## @io Input -> Output
    ## @complexity 5
    @staticmethod
    def is_valid(prefix_str: str) -> bool:
        logger.debug(f"[IMP:4][LetterPrefix][is_valid_INIT] Starting")
        if len(prefix_str) > 1 and not prefix_str.endswith(")"):
            return False
        return len(prefix_str) > 0 and prefix_str[0].isalpha()

    # endregion METHOD_is_valid
# endregion CLASS_LetterPrefix
# region MODULE_CONTRACT [DOMAIN(DocumentProcessing): ...; CONCEPT(FeatureEngineering): ...; TECH(Pandas): ...]
## @modulecontract
## @purpose Document structure extraction for structure_extractors/feature_extractors/list_features/prefix/letter_prefix: line classification, hierarchy level assignment, pattern matching.
## @scope Structure extraction pipeline — structure_extractors/feature_extractors/list_features/prefix/letter_prefix
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
## CLASS [Weight 7][Structure extraction] => LetterPrefix
## @usecases
## - Extract structure: Reader → StructureExtractor → HierarchyBuilder → AnnotatedDocument
def _module_contract():
    pass
# endregion MODULE_CONTRACT
# GREP_SUMMARY: structure extractors, feature extractors, list features, prefix, letter prefix
# STRUCTURE: ▶ structure_extractors/feature_extractors/list_features/prefix/letter_prefix → ○ LetterPrefix.cls → ⎋ result