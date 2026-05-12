from abc import ABC, abstractmethod
from typing import Optional, Union

from dedoc.data_structures.hierarchy_level import HierarchyLevel
from dedoc.data_structures.line_with_meta import LineWithMeta

import logging
logger = logging.getLogger(__name__)


# region CLASS_AbstractPattern [DOMAIN(DocumentProcessing): ...; CONCEPT(PatternMatching): ...; TECH(Regexp): ...]
## @purpose AbstractPattern for document structure extraction pipeline
class AbstractPattern(ABC):
    """
    Base class for all patterns to configure structure extraction by :class:`~dedoc.structure_extractors.DefaultStructureExtractor`.
    """
    _name = ""

    # region METHOD___init__ [DOMAIN(X): ...; CONCEPT(Y): ...; TECH(Z): ...]
    ## @purpose __init__ method
    ## @io Input -> Output
    ## @complexity 5
    def __init__(self, line_type: Optional[str], level_1: Optional[int], level_2: Optional[int], can_be_multiline: Optional[Union[bool, str]]) -> None:
        self.logger = logging.getLogger(__name__)
        self.logger.debug(f"[IMP:4][AbstractPattern][__init___INIT] Starting")
        """
        Initialize pattern with default values of :class:`~dedoc.data_structures.HierarchyLevel` attributes.
        They can be used in :meth:`~dedoc.structure_extractors.patterns.abstract_pattern.AbstractPattern.get_hierarchy_level`
        according to specific pattern logic.

        :param line_type: type of the line, e.g. "header", "bullet_list_item", "chapter", etc.
        :param level_1: value of a line primary importance
        :param level_2: level of the line inside specific class
        :param can_be_multiline: is used to unify lines inside tree node by :class:`~dedoc.structure_constructors.TreeConstructor`,
            if line can be multiline, it can be joined with another line. If ``None`` is given, can_be_multiline is set to ``True``.
        """
        from dedoc.utils.parameter_utils import get_bool_value

        self._line_type = line_type
        self._level_1 = level_1
        self._level_2 = level_2
        self._can_be_multiline = get_bool_value(can_be_multiline, default_value=True)

    # endregion METHOD___init__
    # region METHOD_name [DOMAIN(X): ...; CONCEPT(Y): ...; TECH(Z): ...]
    ## @purpose name method
    ## @io Input -> Output
    ## @complexity 5
    @classmethod
    def name(cls: "AbstractPattern") -> str:
        # BUG_FIX_CONTEXT: self.logger не существует в @classmethod — заменён на модульный logger.
        logger.debug(f"[IMP:4][AbstractPattern][name_INIT] Starting")
        """
        Returns ``_name`` attribute, is used in parameters configuration to choose a specific pattern.
        Each pattern has a unique non-empty name.
        """
        return cls._name

    # endregion METHOD_name
    # region METHOD_match [DOMAIN(X): ...; CONCEPT(Y): ...; TECH(Z): ...]
    ## @purpose match method
    ## @io Input -> Output
    ## @complexity 5
    @abstractmethod
    def match(self, line: LineWithMeta) -> bool:
        self.logger.debug(f"[IMP:4][AbstractPattern][match_INIT] Starting")
        """
        Check if the given line satisfies to the pattern requirements.
        Line text, annotations or metadata (``metadata.tag_hierarchy_level``) can be used to decide, if the line matches the pattern or not.
        """
        pass

    # endregion METHOD_match
    # region METHOD_get_hierarchy_level [DOMAIN(X): ...; CONCEPT(Y): ...; TECH(Z): ...]
    ## @purpose get_hierarchy_level method
    ## @io Input -> Output
    ## @complexity 5
    @abstractmethod
    def get_hierarchy_level(self, line: LineWithMeta) -> HierarchyLevel:
        self.logger.debug(f"[IMP:4][AbstractPattern][get_hierarchy_level_INIT] Starting")
        """
        This method should be applied only when :meth:`~dedoc.structure_extractors.patterns.abstract_pattern.AbstractPattern.match`
        returned ``True`` for the given line.

        Get :class:`~dedoc.data_structures.HierarchyLevel` for initialising ``line.metadata.hierarchy_level`` attribute.
        Please see :ref:`add_structure_type_hierarchy_level` to get more information about :class:`~dedoc.data_structures.HierarchyLevel`.
        """
        pass

    # endregion METHOD_get_hierarchy_level
# endregion CLASS_AbstractPattern
# region MODULE_CONTRACT [DOMAIN(DocumentProcessing): ...; CONCEPT(PatternMatching): ...; TECH(Regexp): ...]
## @modulecontract
## @purpose Document structure extraction for structure_extractors/patterns/abstract_pattern: line classification, hierarchy level assignment, pattern matching.
## @scope Structure extraction pipeline — structure_extractors/patterns/abstract_pattern
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
## CLASS [Weight 7][Structure extraction] => AbstractPattern
## @usecases
## - Extract structure: Reader → StructureExtractor → HierarchyBuilder → AnnotatedDocument
def _module_contract():
    pass
# endregion MODULE_CONTRACT
# GREP_SUMMARY: structure extractors, patterns, abstract pattern
# STRUCTURE: ▶ structure_extractors/patterns/abstract_pattern → ○ AbstractPattern.cls → ⎋ result