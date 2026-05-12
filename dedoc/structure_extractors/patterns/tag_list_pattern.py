from typing import Optional, Union

from dedoc.data_structures.hierarchy_level import HierarchyLevel
from dedoc.data_structures.line_with_meta import LineWithMeta
from dedoc.structure_extractors.patterns.tag_pattern import TagPattern

import logging
logger = logging.getLogger(__name__)


# region CLASS_TagListPattern [DOMAIN(DocumentProcessing): ...; CONCEPT(PatternMatching): ...; TECH(Regexp): ...]
## @purpose TagListPattern for document structure extraction pipeline
class TagListPattern(TagPattern):
    """
    Pattern for using information about list item lines (list_item) from readers saved in ``line.metadata.tag_hierarchy_level``.
    Also allows to calculate ``level_2`` based on dotted list depth (same as in :class:`~dedoc.structure_extractors.patterns.DottedListPattern`)
    **if level_2, tag_hierarchy_level.level_2, default_level_2 are empty**.

    .. seealso::

        Please see :ref:`readers_line_types` to find out which readers can extract lines with type "list_item".

    Example of library usage:

    .. code-block:: python

        import re
        from dedoc.structure_extractors import DefaultStructureExtractor
        from dedoc.structure_extractors.patterns import TagListPattern

        reader = ...
        structure_extractor = DefaultStructureExtractor()
        patterns = [TagListPattern(line_type="list_item", default_level_1=2, can_be_multiline=False)]
        document = reader.read(file_path=file_path)
        document = structure_extractor.extract(document=document, parameters={"patterns": patterns})

    Example of API usage:

    .. code-block:: python

        import requests

        patterns = [{"name": "tag_list", "line_type": "list_item", "default_level_1": 2, "can_be_multiline": "False"}]
        parameters = {"patterns": str(patterns)}
        with open(file_path, "rb") as file:
            files = {"file": (file_name, file)}
            r = requests.post("http://localhost:1231/upload", files=files, data=parameters)
    """
    _name = "tag_list"

    # region METHOD___init__ [DOMAIN(X): ...; CONCEPT(Y): ...; TECH(Z): ...]
    ## @purpose __init__ method
    ## @io Input -> Output
    ## @complexity 5
    def __init__(self,
                 line_type: Optional[str] = None,
                 level_1: Optional[int] = None,
                 level_2: Optional[int] = None,
                 can_be_multiline: Optional[Union[bool, str]] = None,
                 default_line_type: str = HierarchyLevel.list_item,
                 default_level_1: int = 2,
                 default_level_2: Optional[int] = None) -> None:
        super().__init__(line_type=line_type, level_1=level_1, level_2=level_2, can_be_multiline=can_be_multiline, default_line_type=default_line_type,
                         default_level_1=default_level_1, default_level_2=default_level_2)

        self.logger.debug(f"[IMP:4][TagListPattern][__init___INIT] Starting")
    # endregion METHOD___init__
    # region METHOD_match [DOMAIN(X): ...; CONCEPT(Y): ...; TECH(Z): ...]
    ## @purpose match method
    ## @io Input -> Output
    ## @complexity 5
    def match(self, line: LineWithMeta) -> bool:
        self.logger.debug(f"[IMP:4][TagListPattern][match_INIT] Starting")
        """
        Check if the pattern is suitable for the given line:

        * ``line.metadata.tag_hierarchy_level`` should not be empty;
        * ``line.metadata.tag_hierarchy_level.line_type == "list_item"``

        ``line.metadata.tag_hierarchy_level`` is filled during reading step,
        please see :ref:`readers_line_types` to find out which readers can extract lines with type "list_item".
        """
        return line.metadata.tag_hierarchy_level is not None and line.metadata.tag_hierarchy_level.line_type == HierarchyLevel.list_item

    # endregion METHOD_match
    # region METHOD_get_hierarchy_level [DOMAIN(X): ...; CONCEPT(Y): ...; TECH(Z): ...]
    ## @purpose get_hierarchy_level method
    ## @io Input -> Output
    ## @complexity 5
    def get_hierarchy_level(self, line: LineWithMeta) -> HierarchyLevel:
        self.logger.debug(f"[IMP:4][TagListPattern][get_hierarchy_level_INIT] Starting")
        return HierarchyLevel(
            line_type=self._get_line_type(line),
            level_1=self._get_level_1(line),
            level_2=self._get_regexp_level_2(line),
            can_be_multiline=self._get_can_be_multiline(line)
        )

    # endregion METHOD_get_hierarchy_level
# endregion CLASS_TagListPattern
# region MODULE_CONTRACT [DOMAIN(DocumentProcessing): ...; CONCEPT(PatternMatching): ...; TECH(Regexp): ...]
## @modulecontract
## @purpose Document structure extraction for structure_extractors/patterns/tag_list_pattern: line classification, hierarchy level assignment, pattern matching.
## @scope Structure extraction pipeline — structure_extractors/patterns/tag_list_pattern
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
## CLASS [Weight 7][Structure extraction] => TagListPattern
## @usecases
## - Extract structure: Reader → StructureExtractor → HierarchyBuilder → AnnotatedDocument
def _module_contract():
    pass
# endregion MODULE_CONTRACT
# GREP_SUMMARY: structure extractors, patterns, tag list pattern
# STRUCTURE: ▶ structure_extractors/patterns/tag_list_pattern → ○ TagListPattern.cls → ⎋ result