import logging
from functools import total_ordering
from typing import Optional

logger = logging.getLogger(__name__)


# region CLASS_HierarchyLevel [DOMAIN(9): DocumentProcessing, DataStructures; CONCEPT(10): Hierarchy, LineLevel; TECH(6): Python, TotalOrdering]
## @purpose Define the hierarchical level of a document line — encodes primary (level_1) and secondary (level_2) importance with line type.
@total_ordering
class HierarchyLevel:
    """
    This class defines the level of the document line.
    The lower is its value, the more important the line is.

    The level of the line consists of two parts:
        - level_1 defines primary importance (e.g. root - level_1=0, header - level_1=1, etc.);
        - level_2 defines the level inside lines of equal type (e.g. for list items - "1." - level_2=1, "1.1." - level_2=2, etc.).

    For the least important lines (line_type=raw_text) both levels are None.

    Look to the :ref:`hierarchy level description <add_structure_type_hierarchy_level>` to get more details.

    :ivar level_1: value of a line's primary importance
    :ivar level_2: level of the line inside specific class
    :ivar can_be_multiline: is used to unify lines inside tree node, if line can be multiline, it can be joined with another line
    :ivar line_type: type of the line, e.g. raw text, list item, header, etc.

    :vartype level_1: Optional[int]
    :vartype level_2: Optional[int]
    :vartype can_be_multiline: bool
    :vartype line_type: str
    """
    root = "root"
    toc = "toc"
    header = "header"
    toc_item = "toc_item"
    list = "list"  # noqa
    list_item = "list_item"
    bullet_list_item = "bullet_list_item"
    raw_text = "raw_text"
    footer = "footer"
    page_id = "page_id"
    unknown = "unknown"

    # region METHOD___init__ [DOMAIN(9): DocumentProcessing; CONCEPT(10): Hierarchy; TECH(6): Python]
    ## @purpose Initialize hierarchy level with validated level_1, level_2, multiline flag, and line type.
    ## @io (Optional[int], Optional[int], bool, str) -> None
    ## @complexity 3
    def __init__(self, level_1: Optional[int], level_2: Optional[int], can_be_multiline: bool, line_type: str) -> None:
        """
        :param level_1: value of a line's primary importance
        :param level_2: level of the line inside specific class
        :param can_be_multiline: is used to unify lines inside tree node, if line can be multiline, it can be joined with another line
        :param line_type: type of the line
        """
        logger.debug(f"[IMP:4][HierarchyLevel][INIT] level_1={level_1}, level_2={level_2}, can_be_multiline={can_be_multiline}, line_type={line_type}")
        assert level_1 is None or level_1 >= 0
        assert level_2 is None or level_2 >= 0
        self.level_1: Optional[int] = level_1
        self.level_2: Optional[int] = level_2
        self.can_be_multiline: bool = can_be_multiline
        self.line_type: str = line_type
        logger.debug(f"[IMP:4][HierarchyLevel][INIT] HierarchyLevel created: type={line_type}")
    # endregion METHOD___init__

    # region METHOD___is_defined [DOMAIN(9): DocumentProcessing; CONCEPT(8): Comparison; TECH(5): Python]
    ## @purpose Check if both self and other have defined (non-None) level_1 and level_2.
    ## @io (HierarchyLevel) -> bool
    ## @complexity 2
    def __is_defined(self, other: "HierarchyLevel") -> bool:
        return self.level_1 is not None and self.level_2 is not None and other.level_1 is not None and other.level_2 is not None
    # endregion METHOD___is_defined

    # region METHOD___eq__ [DOMAIN(9): DocumentProcessing; CONCEPT(8): Equality; TECH(5): Python]
    ## @purpose Compare two hierarchy levels — None values are treated as +inf for equality.
    ## @uses __to_number
    ## @io (HierarchyLevel) -> bool
    ## @complexity 3
    def __eq__(self, other: "HierarchyLevel") -> bool:
        """
        Defines the equality of two hierarchy levels:
            - two lines with equal level_1, level_2 are equal.
            - if some of the levels is None, its value is considered as +inf (infinities have equal value)

        :param other: other hierarchy level
        :return: whether current hierarchy level == other hierarchy level
        """
        if not isinstance(other, HierarchyLevel):
            return False

        level_1, level_2 = self.__to_number(self.level_1), self.__to_number(self.level_2)
        other_level_1, other_level_2 = self.__to_number(other.level_1), self.__to_number(other.level_2)
        return (level_1, level_2) == (other_level_1, other_level_2)
    # endregion METHOD___eq__

    # region METHOD___lt__ [DOMAIN(9): DocumentProcessing; CONCEPT(8): Ordering; TECH(5): Python]
    ## @purpose Compare two hierarchy levels for ordering — lower level_1/level_2 means more important.
    ## @uses __is_defined, __to_number
    ## @io (HierarchyLevel) -> bool
    ## @complexity 5
    def __lt__(self, other: "HierarchyLevel") -> bool:
        """
        Defines the comparison of hierarchy levels:
            - current level < other level if (level_1, level_2) < other (level_1, level_2);
            - if some of the levels is None, its value is considered as +inf (infinities have equal value)

        :param other: other hierarchy level
        :return: whether current hierarchy level < other hierarchy level
        """
        # all not None
        if self.__is_defined(other):
            return (self.level_1, self.level_2) < (other.level_1, other.level_2)

        # all None
        if self.level_1 is None and self.level_2 is None and other.level_1 is None and other.level_2 is None:
            return False

        level_1, level_2 = self.__to_number(self.level_1), self.__to_number(self.level_2)
        other_level_1, other_level_2 = self.__to_number(other.level_1), self.__to_number(other.level_2)

        return (level_1, level_2) < (other_level_1, other_level_2)
    # endregion METHOD___lt__

    # region METHOD___str__ [DOMAIN(9): DocumentProcessing; CONCEPT(5): Display; TECH(5): Python]
    ## @purpose Return string representation of the hierarchy level.
    ## @io None -> str
    ## @complexity 1
    def __str__(self) -> str:
        return f"HierarchyLevel(level_1={self.level_1}, level_2={self.level_2}, can_be_multiline={self.can_be_multiline}, line_type={self.line_type})"
    # endregion METHOD___str__

    # region METHOD___to_number [DOMAIN(9): DocumentProcessing; CONCEPT(5): Comparison; TECH(5): Python, numpy]
    ## @purpose Convert Optional[int] to number, mapping None to +inf for comparison purposes.
    ## @uses numpy
    ## @io Optional[int] -> int
    ## @complexity 2
    def __to_number(self, x: Optional[int]) -> int:
        import numpy as np

        return np.inf if x is None else x
    # endregion METHOD___to_number

    # region METHOD_is_raw_text [DOMAIN(9): DocumentProcessing; CONCEPT(6): LineType; TECH(5): Python]
    ## @purpose Check if the line is raw text.
    ## @io None -> bool
    ## @complexity 1
    def is_raw_text(self) -> bool:
        """
        Check if the line is raw text.
        """
        return self.line_type == HierarchyLevel.raw_text
    # endregion METHOD_is_raw_text

    # region METHOD_is_unknown [DOMAIN(9): DocumentProcessing; CONCEPT(6): LineType; TECH(5): Python]
    ## @purpose Check if the line type is unknown (only for levels from readers).
    ## @io None -> bool
    ## @complexity 1
    def is_unknown(self) -> bool:
        """
        Check if the type of the line is unknown (only for levels from readers).
        """
        return self.line_type == HierarchyLevel.unknown
    # endregion METHOD_is_unknown

    # region METHOD_is_list_item [DOMAIN(9): DocumentProcessing; CONCEPT(6): LineType; TECH(5): Python]
    ## @purpose Check if the line is a list item.
    ## @io None -> bool
    ## @complexity 1
    def is_list_item(self) -> bool:
        """
        Check if the line is a list item.
        """
        return self.line_type == HierarchyLevel.list_item
    # endregion METHOD_is_list_item

    # region METHOD_create_raw_text [DOMAIN(9): DocumentProcessing; CONCEPT(8): Factory; TECH(5): Python]
    ## @purpose Create hierarchy level for a raw textual line (both levels None).
    ## @io None -> HierarchyLevel
    ## @complexity 1
    @staticmethod
    def create_raw_text() -> "HierarchyLevel":
        """
        Create hierarchy level for a raw textual line.
        """
        return HierarchyLevel(level_1=None, level_2=None, can_be_multiline=True, line_type=HierarchyLevel.raw_text)
    # endregion METHOD_create_raw_text

    # region METHOD_create_unknown [DOMAIN(9): DocumentProcessing; CONCEPT(8): Factory; TECH(5): Python]
    ## @purpose Create hierarchy level for a line with unknown type.
    ## @io None -> HierarchyLevel
    ## @complexity 1
    @staticmethod
    def create_unknown() -> "HierarchyLevel":
        """
        Create hierarchy level for a line with unknown type.
        """
        return HierarchyLevel(level_1=None, level_2=None, can_be_multiline=True, line_type=HierarchyLevel.unknown)
    # endregion METHOD_create_unknown

    # region METHOD_create_root [DOMAIN(9): DocumentProcessing; CONCEPT(8): Factory; TECH(5): Python]
    ## @purpose Create hierarchy level for the document root (level_1=0, level_2=0).
    ## @io None -> HierarchyLevel
    ## @complexity 1
    @staticmethod
    def create_root() -> "HierarchyLevel":
        """
        Create hierarchy level for the document root.
        """
        return HierarchyLevel(level_1=0, level_2=0, can_be_multiline=True, line_type=HierarchyLevel.root)
    # endregion METHOD_create_root
# endregion CLASS_HierarchyLevel

# region MODULE_CONTRACT [DOMAIN(9): DocumentProcessing, DataStructures; CONCEPT(10): Hierarchy, LineLevel; TECH(6): Python, TotalOrdering]
## @modulecontract
## @purpose Define the HierarchyLevel data structure — two-dimensional importance levels (level_1, level_2) with total ordering for document tree construction.
## @scope Hierarchy levels: comparison operators, factory methods for known line types.
## @input Level_1, level_2 (Optional[int]), multiline flag, line type string.
## @output HierarchyLevel instances with total ordering support.
## @links [USED_BY(9): LineMetadata, TreeNode]
## @invariants
## - level_1 is either None or >= 0
## - level_2 is either None or >= 0
## - None levels are treated as +inf in comparisons
## @rationale
## Q: Why two-level hierarchy (level_1 and level_2)?
## A: Documents have both primary importance (root > header > list > raw_text) and secondary ordering within the same type (list item numbering). Two-dimensional model captures both aspects.
## @changes
## LAST_CHANGE: [v1.0.0 – Added semantic markup and LDD logging]
## @modulemap
## CLASS 10[Document line hierarchy level] => HierarchyLevel
## METHOD 6[Constructor] => __init__
## METHOD 8[Comparison less] => __lt__
## METHOD 7[Equality] => __eq__
## METHOD 5[Type check: raw] => is_raw_text
## METHOD 5[Type check: unknown] => is_unknown
## METHOD 5[Type check: list] => is_list_item
## METHOD 5[Factory: raw_text] => create_raw_text
## METHOD 5[Factory: unknown] => create_unknown
## METHOD 5[Factory: root] => create_root
## @usecases
## - [HierarchyLevel]: StructureExtractor → AssignHierarchyLevel → HierarchyLevelInstantiated
## - [HierarchyLevel]: TreeNode → CompareLevels → TreeBuilt
def _module_contract():
    pass
# endregion MODULE_CONTRACT
# GREP_SUMMARY: HierarchyLevel, hierarchy, level, document, line, ordering, root, header, list_item, raw_text, can_be_multiline, total_ordering
# STRUCTURE: ▶ HierarchyLevel ┌level_1?, level_2?, can_be_multiline, line_type┐ → ◇ [total_ordering] __eq__(None→inf) + __lt__ → ⊕ is_raw_text/is_unknown/is_list_item → ⊕ factory: create_raw_text/create_unknown/create_root → ⎋ Level
