from typing import Optional, Union

from dedoc.data_structures.hierarchy_level import HierarchyLevel
from dedoc.data_structures.line_with_meta import LineWithMeta
from dedoc.structure_extractors.patterns.abstract_pattern import AbstractPattern

import logging
logger = logging.getLogger(__name__)


# region CLASS_TagPattern [DOMAIN(DocumentProcessing): ...; CONCEPT(PatternMatching): ...; TECH(Regexp): ...]
## @purpose TagPattern for document structure extraction pipeline
class TagPattern(AbstractPattern):
    """
    Pattern for using information from readers saved in ``line.metadata.tag_hierarchy_level``.
    Can be useful for paragraph extraction in PDF documents and images,
    because PDF and image readers save information about paragraphs in ``line.metadata.tag_hierarchy_level.can_be_multiline``.

    .. seealso::

        Please see :ref:`readers_line_types` if you need information, which line types can be extracted by each reader.

    Example of library usage:

    .. code-block:: python

        import re
        from dedoc.structure_extractors import DefaultStructureExtractor
        from dedoc.structure_extractors.patterns import TagPattern

        reader = ...
        structure_extractor = DefaultStructureExtractor()
        patterns = [TagPattern(default_line_type="raw_text")]
        document = reader.read(file_path=file_path)
        document = structure_extractor.extract(document=document, parameters={"patterns": patterns})

    Example of API usage:

    .. code-block:: python

        import requests

        patterns = [{"name": "tag", "default_line_type": "raw_text"}]
        parameters = {"patterns": str(patterns)}
        with open(file_path, "rb") as file:
            files = {"file": (file_name, file)}
            r = requests.post("http://localhost:1231/upload", files=files, data=parameters)
    """
    _name = "tag"

    # region METHOD___init__ [DOMAIN(X): ...; CONCEPT(Y): ...; TECH(Z): ...]
    ## @purpose __init__ method
    ## @io Input -> Output
    ## @complexity 5
    def __init__(self,
                 line_type: Optional[str] = None,
                 level_1: Optional[int] = None,
                 level_2: Optional[int] = None,
                 can_be_multiline: Optional[Union[bool, str]] = None,
                 default_line_type: str = HierarchyLevel.raw_text,
                 default_level_1: Optional[int] = None,
                 default_level_2: Optional[int] = None) -> None:
        """
        Initialize pattern for configuring values of :class:`~dedoc.data_structures.HierarchyLevel` attributes.
        It is recommended to configure ``default_*`` values in case ``line.metadata.tag_hierarchy_level`` miss some values.
        If you want to use values from ``line.metadata.tag_hierarchy_level``, it is recommended to leave
        ``line_type``, ``level_1``, ``level_2``, ``can_be_multiline`` empty.

        ``can_be_multiline`` is filled in PDF and images readers during paragraph detection, so if you want to extract paragraphs,
        you shouldn't set ``can_be_multiline`` during pattern initialization.

        :param line_type: type of the line, replaces line_type from tag_hierarchy_level if non-empty.
        :param level_1: value of a line primary importance, replaces level_1 from tag_hierarchy_level if non-empty.
        :param level_2: level of the line inside specific class, replaces level_2 from tag_hierarchy_level if non-empty.
        :param can_be_multiline: is used to unify lines inside tree node by :class:`~dedoc.structure_constructors.TreeConstructor`,
            if line can be multiline, it can be joined with another line. If not None, replaces can_be_multiline from tag_hierarchy_level.
        :param default_line_type: type of the line, is used when tag_hierarchy_level.line_type == "unknown".
        :param default_level_1: value of a line primary importance, is used when tag_hierarchy_level.level_1 is None.
        :param default_level_2: level of the line inside specific class, is used when tag_hierarchy_level.level_2 is None.
        """
        super().__init__(line_type=line_type, level_1=level_1, level_2=level_2, can_be_multiline=can_be_multiline)

        self.logger.debug(f"[IMP:4][TagPattern][__init___INIT] Starting")
        self._can_be_multiline_none = can_be_multiline is None
        self._default_line_type = default_line_type
        self._default_level_1 = default_level_1
        self._default_level_2 = default_level_2

    # endregion METHOD___init__
    # region METHOD_match [DOMAIN(X): ...; CONCEPT(Y): ...; TECH(Z): ...]
    ## @purpose match method
    ## @io Input -> Output
    ## @complexity 5
    def match(self, line: LineWithMeta) -> bool:
        self.logger.debug(f"[IMP:4][TagPattern][match_INIT] Starting")
        """
        Check if the pattern is suitable for the given line: ``line.metadata.tag_hierarchy_level`` should not be empty.
        ``line.metadata.tag_hierarchy_level`` is filled during reading step, some readers can skip ``tag_hierarchy_level`` initialisation.
        """
        return line.metadata.tag_hierarchy_level is not None

    # endregion METHOD_match
    # region METHOD_get_hierarchy_level [DOMAIN(X): ...; CONCEPT(Y): ...; TECH(Z): ...]
    ## @purpose get_hierarchy_level method
    ## @io Input -> Output
    ## @complexity 5
    def get_hierarchy_level(self, line: LineWithMeta) -> HierarchyLevel:
        self.logger.debug(f"[IMP:4][TagPattern][get_hierarchy_level_INIT] Starting")
        """
        This method should be applied only when :meth:`~dedoc.structure_extractors.patterns.TagPattern.match`
        returned ``True`` for the given line.

        Return :class:`~dedoc.data_structures.HierarchyLevel` for initialising ``line.metadata.hierarchy_level``.
        The attribute ``line_type`` is initialized according to the following rules:

        * if non-empty ``line_type`` is given during pattern initialisation, then its value is used in the result;
        * if ``line_type`` is not given (or ``None`` is given) and ``line.metadata.tag_hierarchy_level`` is not ``unknown``, \
            the ``line_type`` value from ``line.metadata.tag_hierarchy_level`` is used in the result;
        * otherwise (``line_type`` is empty and ``line.metadata.tag_hierarchy_level`` is ``unknown``) ``default_line_type`` value is used in the result.

        Similar rules work for ``level_1`` and ``level_2`` with comparing with ``None`` instead of ``unknown``.

        The ``can_be_multiline`` attribute is initialized according to the following rules:

        * if non-empty ``can_be_multiline`` is given during pattern initialisation, then its value is used in the result;
        * otherwise ``can_be_multiline`` value from ``line.metadata.tag_hierarchy_level`` is used in the result.
        """
        return HierarchyLevel(
            line_type=self._get_line_type(line),
            level_1=self._get_level_1(line),
            level_2=self._get_level_2(line),
            can_be_multiline=self._get_can_be_multiline(line)
        )

    # endregion METHOD_get_hierarchy_level
    # region METHOD__get_line_type [DOMAIN(X): ...; CONCEPT(Y): ...; TECH(Z): ...]
    ## @purpose _get_line_type method
    ## @io Input -> Output
    ## @complexity 5
    def _get_line_type(self, line: LineWithMeta) -> str:
        self.logger.debug(f"[IMP:4][TagPattern][_get_line_type_INIT] Starting")
        if self._line_type is not None:
            return self._line_type

        return self._default_line_type if line.metadata.tag_hierarchy_level.is_unknown() else line.metadata.tag_hierarchy_level.line_type

    # endregion METHOD__get_line_type
    # region METHOD__get_level_1 [DOMAIN(X): ...; CONCEPT(Y): ...; TECH(Z): ...]
    ## @purpose _get_level_1 method
    ## @io Input -> Output
    ## @complexity 5
    def _get_level_1(self, line: LineWithMeta) -> Optional[int]:
        self.logger.debug(f"[IMP:4][TagPattern][_get_level_1_INIT] Starting")
        if self._level_1 is not None:
            return self._level_1

        return self._default_level_1 if line.metadata.tag_hierarchy_level.level_1 is None else line.metadata.tag_hierarchy_level.level_1

    # endregion METHOD__get_level_1
    # region METHOD__get_level_2 [DOMAIN(X): ...; CONCEPT(Y): ...; TECH(Z): ...]
    ## @purpose _get_level_2 method
    ## @io Input -> Output
    ## @complexity 5
    def _get_level_2(self, line: LineWithMeta) -> Optional[int]:
        self.logger.debug(f"[IMP:4][TagPattern][_get_level_2_INIT] Starting")
        if self._level_2 is not None:
            return self._level_2

        return self._default_level_2 if line.metadata.tag_hierarchy_level.level_2 is None else line.metadata.tag_hierarchy_level.level_2

    # endregion METHOD__get_level_2
    # region METHOD__get_regexp_level_2 [DOMAIN(X): ...; CONCEPT(Y): ...; TECH(Z): ...]
    ## @purpose _get_regexp_level_2 method
    ## @io Input -> Output
    ## @complexity 5
    def _get_regexp_level_2(self, line: LineWithMeta) -> int:
        self.logger.debug(f"[IMP:4][TagPattern][_get_regexp_level_2_INIT] Starting")
        if self._level_2 is not None:
            return self._level_2
        elif line.metadata.tag_hierarchy_level.level_2 is not None:
            return line.metadata.tag_hierarchy_level.level_2
        elif self._default_level_2 is not None:
            return self._default_level_2

        from dedoc.structure_extractors.feature_extractors.list_features.list_utils import get_dotted_item_depth
        depth = get_dotted_item_depth(line.line.strip())
        return depth if depth > 0 else 1

    # endregion METHOD__get_regexp_level_2
    # region METHOD__get_can_be_multiline [DOMAIN(X): ...; CONCEPT(Y): ...; TECH(Z): ...]
    ## @purpose _get_can_be_multiline method
    ## @io Input -> Output
    ## @complexity 5
    def _get_can_be_multiline(self, line: LineWithMeta) -> bool:
        self.logger.debug(f"[IMP:4][TagPattern][_get_can_be_multiline_INIT] Starting")
        return line.metadata.tag_hierarchy_level.can_be_multiline if self._can_be_multiline_none else self._can_be_multiline

    # endregion METHOD__get_can_be_multiline
# endregion CLASS_TagPattern
# region MODULE_CONTRACT [DOMAIN(DocumentProcessing): ...; CONCEPT(PatternMatching): ...; TECH(Regexp): ...]
## @modulecontract
## @purpose Document structure extraction for structure_extractors/patterns/tag_pattern: line classification, hierarchy level assignment, pattern matching.
## @scope Structure extraction pipeline — structure_extractors/patterns/tag_pattern
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
## CLASS [Weight 7][Structure extraction] => TagPattern
## @usecases
## - Extract structure: Reader → StructureExtractor → HierarchyBuilder → AnnotatedDocument
def _module_contract():
    pass
# endregion MODULE_CONTRACT
# GREP_SUMMARY: structure extractors, patterns, tag pattern
# STRUCTURE: ▶ structure_extractors/patterns/tag_pattern → ○ TagPattern.cls → ⎋ result