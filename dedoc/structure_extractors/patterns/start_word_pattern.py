from typing import Optional, Union

from dedoc.data_structures.hierarchy_level import HierarchyLevel
from dedoc.data_structures.line_with_meta import LineWithMeta
from dedoc.structure_extractors.patterns.abstract_pattern import AbstractPattern

import logging
logger = logging.getLogger(__name__)


# region CLASS_StartWordPattern [DOMAIN(DocumentProcessing): ...; CONCEPT(PatternMatching): ...; TECH(Regexp): ...]
## @purpose StartWordPattern for document structure extraction pipeline
class StartWordPattern(AbstractPattern):
    """
    Pattern for lines that begin with some specific text (e.g. Introduction, Chapter, etc.).

    .. note::

        The pattern is case-insensitive (lower and upper letters are not differed).
        Before matching, the line text is stripped (space symbols are deleted from both sides).
        Start word for marching is also stripped and made lowercase.

    Example of library usage:

    .. code-block:: python

        import re
        from dedoc.structure_extractors import DefaultStructureExtractor
        from dedoc.structure_extractors.patterns import StartWordPattern

        reader = ...
        structure_extractor = DefaultStructureExtractor()
        patterns = [StartWordPattern(start_word="chapter", line_type="chapter", level_1=1, can_be_multiline=False)]
        document = reader.read(file_path=file_path)
        document = structure_extractor.extract(document=document, parameters={"patterns": patterns})

    Example of API usage:

    .. code-block:: python

        import requests

        patterns = [{"name": "start_word", "start_word": "chapter", "line_type": "chapter", "level_1": 1, "can_be_multiline": "false"}]
        parameters = {"patterns": str(patterns)}
        with open(file_path, "rb") as file:
            files = {"file": (file_name, file)}
            r = requests.post("http://localhost:1231/upload", files=files, data=parameters)
    """
    _name = "start_word"

    # region METHOD___init__ [DOMAIN(X): ...; CONCEPT(Y): ...; TECH(Z): ...]
    ## @purpose __init__ method
    ## @io Input -> Output
    ## @complexity 5
    def __init__(self,
                 start_word: str,
                 line_type: str,
                 level_1: Optional[int] = None,
                 level_2: Optional[int] = None,
                 can_be_multiline: Optional[Union[bool, str]] = None) -> None:
        """
        Initialize pattern with default values of :class:`~dedoc.data_structures.HierarchyLevel` attributes.

        :param start_word: string for checking of line text beginning.
            Note that start_word will be stripped and made lowercase, and will be used on the lowercase and stripped line.
        :param line_type: type of the line, e.g. "header", "bullet_list_item", "chapter", etc.
        :param level_1: value of a line primary importance
        :param level_2: level of the line inside specific class
        :param can_be_multiline: is used to unify lines inside tree node by :class:`~dedoc.structure_constructors.TreeConstructor`,
            if line can be multiline, it can be joined with another line. If ``None`` is given, can_be_multiline is set to ``True``.
        """
        super().__init__(line_type=line_type, level_1=level_1, level_2=level_2, can_be_multiline=can_be_multiline)

        self.logger.debug(f"[IMP:4][StartWordPattern][__init___INIT] Starting")
        self.__start_word = start_word.strip().lower()

    # endregion METHOD___init__
    # region METHOD_match [DOMAIN(X): ...; CONCEPT(Y): ...; TECH(Z): ...]
    ## @purpose match method
    ## @io Input -> Output
    ## @complexity 5
    def match(self, line: LineWithMeta) -> bool:
        self.logger.debug(f"[IMP:4][StartWordPattern][match_INIT] Starting")
        """
        Check if the pattern is suitable for the given line.
        Line text is checked if it starts with the given ``start_word``, text is stripped and made lowercase beforehand.
        """
        text = line.line.strip().lower()
        return text.startswith(self.__start_word)

    # endregion METHOD_match
    # region METHOD_get_hierarchy_level [DOMAIN(X): ...; CONCEPT(Y): ...; TECH(Z): ...]
    ## @purpose get_hierarchy_level method
    ## @io Input -> Output
    ## @complexity 5
    def get_hierarchy_level(self, line: LineWithMeta) -> HierarchyLevel:
        self.logger.debug(f"[IMP:4][StartWordPattern][get_hierarchy_level_INIT] Starting")
        """
        This method should be applied only when :meth:`~dedoc.structure_extractors.patterns.StartWordPattern.match`
        returned ``True`` for the given line.

        Return :class:`~dedoc.data_structures.HierarchyLevel` for initialising ``line.metadata.hierarchy_level``.
        The attributes ``line_type``, ``level_1``, ``level_2``, ``can_be_multiline`` are equal to values given during class initialisation.
        """
        return HierarchyLevel(line_type=self._line_type, level_1=self._level_1, level_2=self._level_2, can_be_multiline=self._can_be_multiline)

    # endregion METHOD_get_hierarchy_level
# endregion CLASS_StartWordPattern
# region MODULE_CONTRACT [DOMAIN(DocumentProcessing): ...; CONCEPT(PatternMatching): ...; TECH(Regexp): ...]
## @modulecontract
## @purpose Document structure extraction for structure_extractors/patterns/start_word_pattern: line classification, hierarchy level assignment, pattern matching.
## @scope Structure extraction pipeline — structure_extractors/patterns/start_word_pattern
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
## CLASS [Weight 7][Structure extraction] => StartWordPattern
## @usecases
## - Extract structure: Reader → StructureExtractor → HierarchyBuilder → AnnotatedDocument
def _module_contract():
    pass
# endregion MODULE_CONTRACT
# GREP_SUMMARY: structure extractors, patterns, start word pattern
# STRUCTURE: ▶ structure_extractors/patterns/start_word_pattern → ○ StartWordPattern.cls → ⎋ result