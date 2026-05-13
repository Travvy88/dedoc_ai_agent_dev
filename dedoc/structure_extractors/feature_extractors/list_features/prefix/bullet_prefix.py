import re

from dedoc.structure_extractors.feature_extractors.list_features.prefix.prefix import LinePrefix

import logging
logger = logging.getLogger(__name__)


# region CLASS_BulletPrefix [DOMAIN(DocumentProcessing): ...; CONCEPT(FeatureEngineering): ...; TECH(Pandas): ...]
## @purpose BulletPrefix for document structure extraction pipeline
class BulletPrefix(LinePrefix):
    """
    Prefix for all kind of dotted lists:

    * first letter
    * second letter

    - first item
    - second item

    and so on
    """
    name = "non_letter"

    regexp = re.compile(r"^\s*(-|—|−|–|®|\.|•|\,|‚|©|⎯|°|\*|>|\| -|●|♣|①|▪|\*|\+)")

    # region METHOD_predecessor [DOMAIN(X): ...; CONCEPT(Y): ...; TECH(Z): ...]
    ## @purpose predecessor method
    ## @io Input -> Output
    ## @complexity 5
    def predecessor(self, other: LinePrefix) -> bool:
        logger.debug(f"[IMP:4][BulletPrefix][predecessor_INIT] Starting")
        return isinstance(other, BulletPrefix) and self.prefix == other.prefix

    # endregion METHOD_predecessor
    # region METHOD_is_valid [DOMAIN(X): ...; CONCEPT(Y): ...; TECH(Z): ...]
    ## @purpose is_valid method
    ## @io Input -> Output
    ## @complexity 5
    @staticmethod
    def is_valid(prefix_str: str) -> bool:
        logger.debug(f"[IMP:4][BulletPrefix][is_valid_INIT] Starting")
        if BulletPrefix.regexp.fullmatch(prefix_str):
            return True
        return len(prefix_str) == 1 and not prefix_str.isalnum() and not prefix_str.isspace()

    # endregion METHOD_is_valid
# endregion CLASS_BulletPrefix
# region MODULE_CONTRACT [DOMAIN(DocumentProcessing): ...; CONCEPT(FeatureEngineering): ...; TECH(Pandas): ...]
## @modulecontract
## @purpose Document structure extraction for structure_extractors/feature_extractors/list_features/prefix/bullet_prefix: line classification, hierarchy level assignment, pattern matching.
## @scope Structure extraction pipeline — structure_extractors/feature_extractors/list_features/prefix/bullet_prefix
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
## CLASS [Weight 7][Structure extraction] => BulletPrefix
## @usecases
## - Extract structure: Reader → StructureExtractor → HierarchyBuilder → AnnotatedDocument
def _module_contract():
    pass
# endregion MODULE_CONTRACT
# GREP_SUMMARY: structure extractors, feature extractors, list features, prefix, bullet prefix
# STRUCTURE: ▶ structure_extractors/feature_extractors/list_features/prefix/bullet_prefix → ○ BulletPrefix.cls → ⎋ result