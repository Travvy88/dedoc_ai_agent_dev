from typing import Optional

from dedoc.common.exceptions.structure_extractor_error import StructureExtractorError
from dedoc.data_structures.hierarchy_level import HierarchyLevel
from dedoc.data_structures.unstructured_document import UnstructuredDocument
from dedoc.structure_extractors.abstract_structure_extractor import AbstractStructureExtractor
from dedoc.structure_extractors.patterns.abstract_pattern import AbstractPattern
from dedoc.structure_extractors.patterns.pattern_composition import PatternComposition

import logging
logger = logging.getLogger(__name__)


# region CLASS_DefaultStructureExtractor [DOMAIN(DocumentProcessing): ...; CONCEPT(DocumentStructureParser): ...; TECH(Python): ...]
## @purpose DefaultStructureExtractor for document structure extraction pipeline
class DefaultStructureExtractor(AbstractStructureExtractor):
    """
    This class corresponds the basic structure extraction from the documents.

    You can find the description of this type of structure in the section :ref:`other_structure`.
    """
    document_type = "other"

    # region METHOD_extract [DOMAIN(X): ...; CONCEPT(Y): ...; TECH(Z): ...]
    ## @purpose extract method
    ## @io Input -> Output
    ## @complexity 5
    def extract(self, document: UnstructuredDocument, parameters: Optional[dict] = None) -> UnstructuredDocument:
        self.logger.debug(f"[IMP:4][DefaultStructureExtractor][extract_INIT] Starting")
        """
        Extract basic structure from the given document and add additional information to the lines' metadata.
        To get the information about the method's parameters look at the documentation of the class \
        :class:`~dedoc.structure_extractors.AbstractStructureExtractor`.

        ``parameters`` parameter can contain patterns for configuring lines types and their levels in the output document tree ("patterns" key).
        Please see :ref:`dedoc_structure_extractors_patterns` and :ref:`using_patterns` to get information how to use patterns for making your custom structure.
        """
        parameters = {} if parameters is None else parameters
        pattern_composition = self.__get_pattern_composition(parameters)

        for line in document.lines:
            line.metadata.hierarchy_level = pattern_composition.get_hierarchy_level(line=line)
        return document

    # endregion METHOD_extract
    # region METHOD___get_pattern_composition [DOMAIN(X): ...; CONCEPT(Y): ...; TECH(Z): ...]
    ## @purpose __get_pattern_composition method
    ## @io Input -> Output
    ## @complexity 5
    def __get_pattern_composition(self, parameters: dict) -> PatternComposition:
        self.logger.debug(f"[IMP:4][DefaultStructureExtractor][__get_pattern_composition_INIT] Starting")
        patterns = parameters.get("patterns")
        if not patterns:
            from dedoc.structure_extractors.patterns.bracket_list_pattern import BracketListPattern
            from dedoc.structure_extractors.patterns.bullet_list_pattern import BulletListPattern
            from dedoc.structure_extractors.patterns.dotted_list_pattern import DottedListPattern
            from dedoc.structure_extractors.patterns.letter_list_pattern import LetterListPattern
            from dedoc.structure_extractors.patterns.roman_list_pattern import RomanListPattern
            from dedoc.structure_extractors.patterns.tag_header_pattern import TagHeaderPattern
            from dedoc.structure_extractors.patterns.tag_list_pattern import TagListPattern
            from dedoc.structure_extractors.patterns.tag_pattern import TagPattern

            return PatternComposition(
                patterns=[
                    TagHeaderPattern(line_type=HierarchyLevel.header, level_1=1, can_be_multiline=False),
                    TagListPattern(line_type=HierarchyLevel.list_item, default_level_1=2, can_be_multiline=False),
                    DottedListPattern(line_type=HierarchyLevel.list_item, level_1=2, can_be_multiline=False),
                    RomanListPattern(line_type=HierarchyLevel.list_item, level_1=3, level_2=1, can_be_multiline=False),
                    BracketListPattern(line_type=HierarchyLevel.list_item, level_1=4, level_2=1, can_be_multiline=False),
                    LetterListPattern(line_type=HierarchyLevel.list_item, level_1=5, level_2=1, can_be_multiline=False),
                    BulletListPattern(line_type=HierarchyLevel.list_item, level_1=6, level_2=1, can_be_multiline=False),
                    TagPattern(default_line_type=HierarchyLevel.raw_text)
                ]
            )

        import ast
        from dedoc.structure_extractors.patterns.utils import get_pattern

        if isinstance(patterns, str):
            try:
                patterns = ast.literal_eval(patterns)
            except ValueError as e:
                raise StructureExtractorError(msg=f"Bad syntax for patterns: {str(e)}")

        if not isinstance(patterns, list):
            raise StructureExtractorError(msg="Patterns parameter should contain a list of patterns")

        pattern_classes = []
        for pattern in patterns:
            if isinstance(pattern, dict):
                pattern_classes.append(get_pattern(pattern))
            elif isinstance(pattern, AbstractPattern):
                pattern_classes.append(pattern)
            else:
                raise StructureExtractorError(msg="Pattern should be dict or `AbstractPattern`")

        return PatternComposition(patterns=pattern_classes)

    # endregion METHOD___get_pattern_composition
# endregion CLASS_DefaultStructureExtractor
# region MODULE_CONTRACT [DOMAIN(DocumentProcessing): ...; CONCEPT(DocumentStructureParser): ...; TECH(Python): ...]
## @modulecontract
## @purpose Document structure extraction for structure_extractors/concrete_structure_extractors/default_structure_extractor: line classification, hierarchy level assignment, pattern matching.
## @scope Structure extraction pipeline — structure_extractors/concrete_structure_extractors/default_structure_extractor
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
## CLASS [Weight 7][Structure extraction] => DefaultStructureExtractor
## @usecases
## - Extract structure: Reader → StructureExtractor → HierarchyBuilder → AnnotatedDocument
def _module_contract():
    pass
# endregion MODULE_CONTRACT
# GREP_SUMMARY: structure extractors, concrete structure extractors, default structure extractor
# STRUCTURE: ▶ structure_extractors/concrete_structure_extractors/default_structure_extractor → ○ DefaultStructureExtractor.cls → ⎋ result