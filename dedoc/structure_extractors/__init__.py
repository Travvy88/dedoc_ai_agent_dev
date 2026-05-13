from .abstract_structure_extractor import AbstractStructureExtractor
from .concrete_structure_extractors.default_structure_extractor import DefaultStructureExtractor
from .concrete_structure_extractors.abstract_law_structure_extractor import AbstractLawStructureExtractor
from .concrete_structure_extractors.article_structure_extractor import ArticleStructureExtractor
from .concrete_structure_extractors.classifying_law_structure_extractor import ClassifyingLawStructureExtractor
from .concrete_structure_extractors.diploma_structure_extractor import DiplomaStructureExtractor
from .concrete_structure_extractors.fintoc_structure_extractor import FintocStructureExtractor
from .concrete_structure_extractors.foiv_law_structure_extractor import FoivLawStructureExtractor
from .concrete_structure_extractors.law_structure_excractor import LawStructureExtractor
from .concrete_structure_extractors.tz_structure_extractor import TzStructureExtractor
from .structure_extractor_composition import StructureExtractorComposition

import logging
logger = logging.getLogger(__name__)

__all__ = ['AbstractStructureExtractor', 'AbstractLawStructureExtractor', 'ArticleStructureExtractor', 'ClassifyingLawStructureExtractor',
           'DefaultStructureExtractor', 'DiplomaStructureExtractor', 'FintocStructureExtractor', 'FoivLawStructureExtractor', 'LawStructureExtractor',
           'TzStructureExtractor', 'StructureExtractorComposition']

# region MODULE_CONTRACT [DOMAIN(DocumentProcessing): ...; CONCEPT(StructureExtraction): ...; TECH(Python): ...]
## @modulecontract
## @purpose Document structure extraction for structure_extractors/__init__: line classification, hierarchy level assignment, pattern matching.
## @scope Structure extraction pipeline — structure_extractors/__init__
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
# GREP_SUMMARY: structure extractors
# STRUCTURE: ▶ structure_extractors/__init__ → ○ module → ⎋ result