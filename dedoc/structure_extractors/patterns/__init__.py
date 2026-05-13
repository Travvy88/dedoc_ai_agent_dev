from dedoc.structure_extractors.patterns.bracket_list_pattern import BracketListPattern
from dedoc.structure_extractors.patterns.bracket_roman_list_pattern import BracketRomanListPattern
from dedoc.structure_extractors.patterns.bullet_list_pattern import BulletListPattern
from dedoc.structure_extractors.patterns.dotted_list_pattern import DottedListPattern
from dedoc.structure_extractors.patterns.letter_list_pattern import LetterListPattern
from dedoc.structure_extractors.patterns.regexp_pattern import RegexpPattern
from dedoc.structure_extractors.patterns.roman_list_pattern import RomanListPattern
from dedoc.structure_extractors.patterns.start_word_pattern import StartWordPattern
from dedoc.structure_extractors.patterns.tag_header_pattern import TagHeaderPattern
from dedoc.structure_extractors.patterns.tag_list_pattern import TagListPattern
from dedoc.structure_extractors.patterns.tag_pattern import TagPattern

import logging
logger = logging.getLogger(__name__)

__all__ = [BracketListPattern, BracketRomanListPattern, BulletListPattern, DottedListPattern, LetterListPattern, RegexpPattern, RomanListPattern,
           StartWordPattern, TagHeaderPattern, TagListPattern, TagPattern]

# region MODULE_CONTRACT [DOMAIN(DocumentProcessing): ...; CONCEPT(PatternMatching): ...; TECH(Regexp): ...]
## @modulecontract
## @purpose Document structure extraction for structure_extractors/patterns/__init__: line classification, hierarchy level assignment, pattern matching.
## @scope Structure extraction pipeline — structure_extractors/patterns/__init__
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
## @usecases
## - Extract structure: Reader → StructureExtractor → HierarchyBuilder → AnnotatedDocument
def _module_contract():
    pass
# endregion MODULE_CONTRACT
# GREP_SUMMARY: structure extractors, patterns
# STRUCTURE: ▶ structure_extractors/patterns/__init__ → ○ module → ⎋ result