# region MODULE_CONTRACT [DOMAIN(7): DocumentProcessing, StructureConstruction; CONCEPT(9): OrderedList, HierarchyNumbering; TECH(5): CustomComparators, LexicographicOrder]
## @modulecontract
## @purpose Define the ListItem data class that models multi-level list numbering (e.g., "1.2.3)" or "1.2.3.") and provides ordering logic for tree construction.
## @scope List item identity, parent computation, lexicographic comparison.
## @input List[int] (hierarchy levels), str (end delimiter).
## @output ListItem objects with comparison and parent navigation capabilities.
## @links [USES_API(4): builtins]
## @invariants
## - ListItem ALWAYS stores end_type as either LIST_ITEM_POINT_END_TYPE or LIST_ITEM_BRACKET_END_TYPE.
## - get_parent returns a ListItem with the last element decremented; empty if last becomes <=0.
## - __lt__ returns False if end_types differ.
## @rationale
## Q: Why a custom class instead of a plain tuple?
## A: Multi-level list comparison requires lexicographic logic that plain tuples don't handle correctly when lists have different lengths.
## @changes
## LAST_CHANGE: [v1.0.0 – Semantic template markup and LDD logging added]
## @modulemap
## CONST 3[Point end delimiter constant] => LIST_ITEM_POINT_END_TYPE
## CONST 3[Bracket end delimiter constant] => LIST_ITEM_BRACKET_END_TYPE
## CLASS 8[List item with multi-level numbering and comparison] => ListItem
## METHOD 5[Initialize item from level list and end type] => __init__
## METHOD 6[Compute parent item in hierarchy] => get_parent
## METHOD 7[Lexicographic comparison] => __lt__
## METHOD 5[Equality check] => __eq__
## METHOD 5[Inequality check] => __ne__
## METHOD 4[Check if this is the first item (level [1])] => is_first_item
## METHOD 4[String representation "1.2.3."] => __str__
## @usecases
## - [ListItem]: TreeConstructor → CompareListItems → DetermineHierarchyPosition
def _module_contract():
    pass
# endregion MODULE_CONTRACT
# GREP_SUMMARY: ListItem, list numbering, hierarchy, lexicographic, comparison, multi-level, parent, ordering, tree construction
# STRUCTURE: ▶ ┌item:[int], end:str┐ → ◇ end_type: '.' | ')' → ⊕ get_parent() = item[:-1] with last-- → ⟦ListItem┘ ⟦ListItem┘ ⇔ __lt__ lexicographic

import logging
from typing import List

logger = logging.getLogger(__name__)


LIST_ITEM_POINT_END_TYPE = "."
LIST_ITEM_BRACKET_END_TYPE = ")"

# region CLASS_ListItem [DOMAIN(7): DocumentProcessing; CONCEPT(9): OrderedList, HierarchyNumbering; TECH(5): CustomComparators, LexicographicOrder]
## @purpose Model a multi-level list item (e.g., "1.2.3." or "1.2.3)") with hierarchy navigation and lexicographic comparison for tree structure construction.
class ListItem:
    # region METHOD___init__ [DOMAIN(5): DocumentProcessing; CONCEPT(6): DataInitialization; TECH(4): Constructor]
    ## @purpose Initialize a ListItem from a level list and end delimiter string.
    ## @io List[int], str -> None
    ## @complexity 2
    def __init__(self, item: List[int], end: str) -> None:
        self.item = item
        self.end_type = LIST_ITEM_BRACKET_END_TYPE if end == ")" else LIST_ITEM_POINT_END_TYPE
        # LDD-log: initialization
        logger.debug(f"[IMP:3][ListItem][INIT] Created ListItem item={item}, end_type={self.end_type}")
    # endregion METHOD___init__

    # region METHOD_get_parent [DOMAIN(6): DocumentProcessing; CONCEPT(7): HierarchyNavigation; TECH(5): ListManipulation]
    ## @purpose Compute the parent ListItem by decrementing the last level; remove trailing zero levels.
    ## @io None (uses self) -> ListItem
    ## @complexity 4
    def get_parent(self) -> "ListItem":
        parent_item = [item for item in self.item]
        parent_item[-1] -= 1

        if parent_item[-1] <= 0:
            parent_item.pop()

        # LDD-log: parent computation
        logger.debug(f"[IMP:3][ListItem][GET_PARENT] item={self.item} -> parent={parent_item}")
        return ListItem(parent_item, self.end_type)
    # endregion METHOD_get_parent

    # region METHOD___lt__ [DOMAIN(7): DocumentProcessing; CONCEPT(8): OrderedList, LexicographicOrder; TECH(5): CustomComparator]
    ## @purpose Compare two ListItems lexicographically by their level lists; return False if end_types differ.
    ## @io ListItem -> bool
    ## @complexity 5
    def __lt__(self, item: "ListItem") -> bool:
        if self.end_type != item.end_type:
            return False

        max_len = max(len(self.item), len(item.item))

        for i in range(max_len):
            d1 = self.item[i] if i < len(self.item) else 0
            d2 = item.item[i] if i < len(item.item) else 0

            if d1 != d2:
                return d1 < d2

        return False
    # endregion METHOD___lt__

    # region METHOD___eq__ [DOMAIN(5): DocumentProcessing; CONCEPT(5): EqualityCheck; TECH(4): BuiltinOverride]
    ## @purpose Check equality: same level list and same end_type.
    ## @io ListItem -> bool
    ## @complexity 2
    def __eq__(self, item: "ListItem") -> bool:
        return self.item == item.item and self.end_type == item.end_type
    # endregion METHOD___eq__

    # region METHOD___ne__ [DOMAIN(5): DocumentProcessing; CONCEPT(5): InequalityCheck; TECH(4): BuiltinOverride]
    ## @purpose Check inequality: different level list or different end_type.
    ## @io ListItem -> bool
    ## @complexity 2
    def __ne__(self, item: "ListItem") -> bool:
        return self.item != item.item or self.end_type != item.end_type
    # endregion METHOD___ne__

    # region METHOD_is_first_item [DOMAIN(5): DocumentProcessing; CONCEPT(6): HierarchyCheck; TECH(3): IdentityCheck]
    ## @purpose Determine if this item is the root of a list hierarchy (level [1]).
    ## @io None -> bool
    ## @complexity 2
    def is_first_item(self) -> bool:
        return self.item == [1]
    # endregion METHOD_is_first_item

    # region METHOD___str__ [DOMAIN(4): DocumentProcessing; CONCEPT(4): StringRepresentation; TECH(3): Joins]
    ## @purpose Produce a human-readable string representation: "1.2.3." or "1.2.3)".
    ## @io None -> str
    ## @complexity 2
    def __str__(self) -> str:
        return ".".join([str(item) for item in self.item]) + self.end_type
    # endregion METHOD___str__
# endregion CLASS_ListItem
