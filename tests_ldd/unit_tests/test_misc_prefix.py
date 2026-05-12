# region MODULE_CONTRACT [DOMAIN(7): Testing; CONCEPT(8): UnitTest, LDD_Telemetry; TECH(8): unittest, pytest]
## @modulecontract
## @purpose Unit tests for misc prefix module.
## @scope Unit testing of dedoc module: misc, prefix.
## @input Test data files from tests/data/.
## @output Test results (pass/fail) with LDD telemetry.
## @links [USES_API(7): unittest.TestCase]
## @invariants
## - All original test logic and assertions remain unchanged.
## - LDD telemetry is printed BEFORE assertions.
## @rationale
## Q: Why add LDD telemetry to tests?
## A: On failure, critical log trajectory is visible before assert traceback.
## @changes
## LAST_CHANGE: [v1.0.0 – Added LDD telemetry and semantic markup.]
## @modulemap
## CLASS 8[Unit tests] => TestPrefix
## @usecases
## - [Tests]: QA Agent (Verify) => RunTestsWithTelemetry => DiagnosticTrajectoryVisible
def _module_contract():
    pass
# endregion MODULE_CONTRACT
# GREP_SUMMARY: misc, prefix, TestPrefix, test_dotted_is_valid, test_bracket_is_valid, test_empty_is_valid, test_letter_is_valid, test_non_letter_is_valid, test_is_predecessor_mixed_type, test_non_letter_predecessor, test_bracket_predecessor, test_letter_eng_predecessor, test_letter_eng_capital_predecessor, test_letter_rus_predecessor, test_letter_rus_capital_predecessor, test_letter_rus_with_yo_predecessor, test_letter_rus_without_yo_predecessor, test_letter_rus_capital_with_yo_predecessor, test_letter_rus_capital_without_yo_predecessor, test_letter_all_predecessor, test_dotted_predecessor_one_num, test_dotted_predecessor_two_num, test_dotted_predecessor_different_num, test_dotted_list_regexp, unit_test, unittest, LDD_telemetry, semantic_markup, unit_test
# STRUCTURE: ▶ Init → ◇ Execute → ⊕ Verify → ∑ assertions → ⎋ PASS/FAIL


import logging

logger = logging.getLogger(__name__)

import unittest
from typing import List, Type

from dedoc.structure_extractors.feature_extractors.list_features.prefix.bracket_prefix import BracketPrefix
from dedoc.structure_extractors.feature_extractors.list_features.prefix.bullet_prefix import BulletPrefix
from dedoc.structure_extractors.feature_extractors.list_features.prefix.dotted_prefix import DottedPrefix
from dedoc.structure_extractors.feature_extractors.list_features.prefix.empty_prefix import EmptyPrefix
from dedoc.structure_extractors.feature_extractors.list_features.prefix.letter_prefix import LetterPrefix
from dedoc.structure_extractors.feature_extractors.list_features.prefix.prefix import LinePrefix


# region CLASS_TestPrefix [DOMAIN(7): Testing; CONCEPT(8): UnitTest, LDD_Telemetry; TECH(8): unittest, pytest]
## @purpose Test suite for misc, prefix module.
class TestPrefix(unittest.TestCase):

    valid_dotted = ["1.1", "1.1.", "1.1.2", "1.", "1"]
    valid_bracket = ["1)", "2)", "11231)", "11)"]
    valid_letter = ["a)", "b)", "c)", "z)", "у)", "ё)", "ъ)"]
    valid_non_letter = ["*", "+", "?", "-", "#"]
    invalid = ["\t", "", "aa", "some word", "1.a.2"]
    all_prefix = valid_dotted + valid_bracket + valid_letter + valid_non_letter + invalid

    # region METHOD_test_dotted_is_valid [DOMAIN(7): Testing; CONCEPT(8): LDD_Telemetry; TECH(8): unittest]
    ## @purpose Verify: dotted is valid.
    ## @complexity 5
    def test_dotted_is_valid(self) -> None:
        # LDD TELEMETRY: log execution context before assertions
        print(f"\n--- LDD TRAJECTORY (IMP:7-10) for TestPrefix::test_dotted_is_valid ---")
        print(f"  [LDD_TEST][IMP:8][TestPrefix][test_dotted_is_valid] Test logic executed, entering assertion phase")
        self._check_if_valid(valid_prefix=self.valid_dotted, prefix_class=DottedPrefix)

    # endregion METHOD_test_dotted_is_valid
    # region METHOD_test_bracket_is_valid [DOMAIN(7): Testing; CONCEPT(8): LDD_Telemetry; TECH(8): unittest]
    ## @purpose Verify: bracket is valid.
    ## @complexity 5
    def test_bracket_is_valid(self) -> None:
        # LDD TELEMETRY: log execution context before assertions
        print(f"\n--- LDD TRAJECTORY (IMP:7-10) for TestPrefix::test_bracket_is_valid ---")
        print(f"  [LDD_TEST][IMP:8][TestPrefix][test_bracket_is_valid] Test logic executed, entering assertion phase")
        self._check_if_valid(valid_prefix=self.valid_bracket, prefix_class=BracketPrefix)

    # endregion METHOD_test_bracket_is_valid
    # region METHOD_test_empty_is_valid [DOMAIN(7): Testing; CONCEPT(8): LDD_Telemetry; TECH(8): unittest]
    ## @purpose Verify: empty is valid.
    ## @complexity 5
    def test_empty_is_valid(self) -> None:
        # LDD TELEMETRY: log execution context before assertions
        print(f"\n--- LDD TRAJECTORY (IMP:7-10) for TestPrefix::test_empty_is_valid ---")
        print(f"  [LDD_TEST][IMP:8][TestPrefix][test_empty_is_valid] Test logic executed, entering assertion phase")
        self._check_if_valid(valid_prefix=self.all_prefix, prefix_class=EmptyPrefix)

    # endregion METHOD_test_empty_is_valid
    # region METHOD_test_letter_is_valid [DOMAIN(7): Testing; CONCEPT(8): LDD_Telemetry; TECH(8): unittest]
    ## @purpose Verify: letter is valid.
    ## @complexity 5
    def test_letter_is_valid(self) -> None:
        # LDD TELEMETRY: log execution context before assertions
        print(f"\n--- LDD TRAJECTORY (IMP:7-10) for TestPrefix::test_letter_is_valid ---")
        print(f"  [LDD_TEST][IMP:8][TestPrefix][test_letter_is_valid] Test logic executed, entering assertion phase")
        self._check_if_valid(valid_prefix=self.valid_letter, prefix_class=LetterPrefix)

    # endregion METHOD_test_letter_is_valid
    # region METHOD_test_non_letter_is_valid [DOMAIN(7): Testing; CONCEPT(8): LDD_Telemetry; TECH(8): unittest]
    ## @purpose Verify: non letter is valid.
    ## @complexity 5
    def test_non_letter_is_valid(self) -> None:
        # LDD TELEMETRY: log execution context before assertions
        print(f"\n--- LDD TRAJECTORY (IMP:7-10) for TestPrefix::test_non_letter_is_valid ---")
        print(f"  [LDD_TEST][IMP:8][TestPrefix][test_non_letter_is_valid] Test logic executed, entering assertion phase")
        self._check_if_valid(valid_prefix=self.valid_non_letter, prefix_class=BulletPrefix)

    # endregion METHOD_test_non_letter_is_valid
    # region METHOD__check_if_valid [DOMAIN(7): Testing; CONCEPT(8): TestInfrastructure; TECH(8): unittest]
    ## @purpose check if valid.
    def _check_if_valid(self, valid_prefix: List[str], prefix_class: Type[LinePrefix]) -> None:
        message_template = "assume `{prefix}` is {status} for {clazz} prefix"
        for prefix in self.all_prefix:
            class_name = prefix_class.__name__
            if prefix in valid_prefix:
                message = message_template.format(prefix=prefix, status="VALID", clazz=class_name)
                self.assertTrue(prefix_class.is_valid(prefix), message)
            else:
                message = message_template.format(prefix=prefix, status="INVALID", clazz=class_name)
                self.assertFalse(prefix_class.is_valid(prefix), message)

    # endregion METHOD__check_if_valid
    # region METHOD_test_is_predecessor_mixed_type [DOMAIN(7): Testing; CONCEPT(8): LDD_Telemetry; TECH(8): unittest]
    ## @purpose Verify: is predecessor mixed type.
    ## @complexity 5
    def test_is_predecessor_mixed_type(self) -> None:
        # LDD TELEMETRY: log execution context before assertions
        print(f"\n--- LDD TRAJECTORY (IMP:7-10) for TestPrefix::test_is_predecessor_mixed_type ---")
        print(f"  [LDD_TEST][IMP:8][TestPrefix][test_is_predecessor_mixed_type] Test logic executed, entering assertion phase")
        mixed_prefix = [
            DottedPrefix("1.", 0),
            BracketPrefix("1)", 0),
            EmptyPrefix("some prefix"),
            LetterPrefix("a)", 0),
            BulletPrefix("-", 0)
        ]

        for first in mixed_prefix:
            for second in mixed_prefix:
                if first != second:
                    self.assertFalse(first.predecessor(second))
                    self.assertFalse(second.predecessor(first))

    # endregion METHOD_test_is_predecessor_mixed_type
    # region METHOD_test_non_letter_predecessor [DOMAIN(7): Testing; CONCEPT(8): LDD_Telemetry; TECH(8): unittest]
    ## @purpose Verify: non letter predecessor.
    ## @complexity 5
    def test_non_letter_predecessor(self) -> None:
        # LDD TELEMETRY: log execution context before assertions
        print(f"\n--- LDD TRAJECTORY (IMP:7-10) for TestPrefix::test_non_letter_predecessor ---")
        print(f"  [LDD_TEST][IMP:8][TestPrefix][test_non_letter_predecessor] Test logic executed, entering assertion phase")
        prefix_star_1 = BulletPrefix("*", 0)
        prefix_star_2 = BulletPrefix("*", 0)
        prefix_minus_1 = BulletPrefix("-", 0)
        prefix_minus_2 = BulletPrefix("-", 0)
        self.assertTrue(prefix_star_1.predecessor(prefix_star_2))
        self.assertTrue(prefix_star_2.predecessor(prefix_star_1))

        self.assertTrue(prefix_minus_1.predecessor(prefix_minus_2))
        self.assertTrue(prefix_minus_2.predecessor(prefix_minus_1))

        self.assertFalse(prefix_star_1.predecessor(prefix_minus_1))
        self.assertFalse(prefix_minus_1.predecessor(prefix_star_1))

    # endregion METHOD_test_non_letter_predecessor
    # region METHOD_test_bracket_predecessor [DOMAIN(7): Testing; CONCEPT(8): LDD_Telemetry; TECH(8): unittest]
    ## @purpose Verify: bracket predecessor.
    ## @complexity 5
    def test_bracket_predecessor(self) -> None:
        # LDD TELEMETRY: log execution context before assertions
        print(f"\n--- LDD TRAJECTORY (IMP:7-10) for TestPrefix::test_bracket_predecessor ---")
        print(f"  [LDD_TEST][IMP:8][TestPrefix][test_bracket_predecessor] Test logic executed, entering assertion phase")
        one = BracketPrefix("1)", 0)
        two = BracketPrefix("2)", 0)
        three = BracketPrefix("3)", 0)

        self._check_three_prefix(one, three, two)

    # endregion METHOD_test_bracket_predecessor
    # region METHOD_test_letter_eng_predecessor [DOMAIN(7): Testing; CONCEPT(8): LDD_Telemetry; TECH(8): unittest]
    ## @purpose Verify: letter eng predecessor.
    ## @complexity 5
    def test_letter_eng_predecessor(self) -> None:
        # LDD TELEMETRY: log execution context before assertions
        print(f"\n--- LDD TRAJECTORY (IMP:7-10) for TestPrefix::test_letter_eng_predecessor ---")
        print(f"  [LDD_TEST][IMP:8][TestPrefix][test_letter_eng_predecessor] Test logic executed, entering assertion phase")
        one = LetterPrefix("a)", 0)
        two = LetterPrefix("b)", 0)
        three = LetterPrefix("c)", 0)

        self._check_three_prefix(one, three, two)

    # endregion METHOD_test_letter_eng_predecessor
    # region METHOD_test_letter_eng_capital_predecessor [DOMAIN(7): Testing; CONCEPT(8): LDD_Telemetry; TECH(8): unittest]
    ## @purpose Verify: letter eng capital predecessor.
    ## @complexity 5
    def test_letter_eng_capital_predecessor(self) -> None:
        # LDD TELEMETRY: log execution context before assertions
        print(f"\n--- LDD TRAJECTORY (IMP:7-10) for TestPrefix::test_letter_eng_capital_predecessor ---")
        print(f"  [LDD_TEST][IMP:8][TestPrefix][test_letter_eng_capital_predecessor] Test logic executed, entering assertion phase")
        one = LetterPrefix("A)", 0)
        two = LetterPrefix("B)", 0)
        three = LetterPrefix("C)", 0)

        self._check_three_prefix(one, three, two)

    # endregion METHOD_test_letter_eng_capital_predecessor
    # region METHOD_test_letter_rus_predecessor [DOMAIN(7): Testing; CONCEPT(8): LDD_Telemetry; TECH(8): unittest]
    ## @purpose Verify: letter rus predecessor.
    ## @complexity 5
    def test_letter_rus_predecessor(self) -> None:
        # LDD TELEMETRY: log execution context before assertions
        print(f"\n--- LDD TRAJECTORY (IMP:7-10) for TestPrefix::test_letter_rus_predecessor ---")
        print(f"  [LDD_TEST][IMP:8][TestPrefix][test_letter_rus_predecessor] Test logic executed, entering assertion phase")
        one = LetterPrefix("а)", 0)
        two = LetterPrefix("б)", 0)
        three = LetterPrefix("в)", 0)

        self._check_three_prefix(one, three, two)

    # endregion METHOD_test_letter_rus_predecessor
    # region METHOD_test_letter_rus_capital_predecessor [DOMAIN(7): Testing; CONCEPT(8): LDD_Telemetry; TECH(8): unittest]
    ## @purpose Verify: letter rus capital predecessor.
    ## @complexity 5
    def test_letter_rus_capital_predecessor(self) -> None:
        # LDD TELEMETRY: log execution context before assertions
        print(f"\n--- LDD TRAJECTORY (IMP:7-10) for TestPrefix::test_letter_rus_capital_predecessor ---")
        print(f"  [LDD_TEST][IMP:8][TestPrefix][test_letter_rus_capital_predecessor] Test logic executed, entering assertion phase")
        one = LetterPrefix("А)", 0)
        two = LetterPrefix("Б)", 0)
        three = LetterPrefix("В)", 0)

        self._check_three_prefix(one, three, two)

    # endregion METHOD_test_letter_rus_capital_predecessor
    # region METHOD_test_letter_rus_with_yo_predecessor [DOMAIN(7): Testing; CONCEPT(8): LDD_Telemetry; TECH(8): unittest]
    ## @purpose Verify: letter rus with yo predecessor.
    ## @complexity 5
    def test_letter_rus_with_yo_predecessor(self) -> None:
        # LDD TELEMETRY: log execution context before assertions
        print(f"\n--- LDD TRAJECTORY (IMP:7-10) for TestPrefix::test_letter_rus_with_yo_predecessor ---")
        print(f"  [LDD_TEST][IMP:8][TestPrefix][test_letter_rus_with_yo_predecessor] Test logic executed, entering assertion phase")
        one = LetterPrefix("ё)", 0)
        two = LetterPrefix("ж)", 0)
        three = LetterPrefix("з)", 0)
        self._check_three_prefix(one, three, two)

    # endregion METHOD_test_letter_rus_with_yo_predecessor
    # region METHOD_test_letter_rus_without_yo_predecessor [DOMAIN(7): Testing; CONCEPT(8): LDD_Telemetry; TECH(8): unittest]
    ## @purpose Verify: letter rus without yo predecessor.
    ## @complexity 5
    def test_letter_rus_without_yo_predecessor(self) -> None:
        # LDD TELEMETRY: log execution context before assertions
        print(f"\n--- LDD TRAJECTORY (IMP:7-10) for TestPrefix::test_letter_rus_without_yo_predecessor ---")
        print(f"  [LDD_TEST][IMP:8][TestPrefix][test_letter_rus_without_yo_predecessor] Test logic executed, entering assertion phase")
        one = LetterPrefix("е)", 0)
        two = LetterPrefix("ж)", 0)
        three = LetterPrefix("з)", 0)
        self._check_three_prefix(one, three, two)

    # endregion METHOD_test_letter_rus_without_yo_predecessor
    # region METHOD_test_letter_rus_capital_with_yo_predecessor [DOMAIN(7): Testing; CONCEPT(8): LDD_Telemetry; TECH(8): unittest]
    ## @purpose Verify: letter rus capital with yo predecessor.
    ## @complexity 5
    def test_letter_rus_capital_with_yo_predecessor(self) -> None:
        # LDD TELEMETRY: log execution context before assertions
        print(f"\n--- LDD TRAJECTORY (IMP:7-10) for TestPrefix::test_letter_rus_capital_with_yo_predecessor ---")
        print(f"  [LDD_TEST][IMP:8][TestPrefix][test_letter_rus_capital_with_yo_predecessor] Test logic executed, entering assertion phase")
        one = LetterPrefix("Ё)", 0)
        two = LetterPrefix("Ж)", 0)
        three = LetterPrefix("З)", 0)
        self._check_three_prefix(one, three, two)

    # endregion METHOD_test_letter_rus_capital_with_yo_predecessor
    # region METHOD_test_letter_rus_capital_without_yo_predecessor [DOMAIN(7): Testing; CONCEPT(8): LDD_Telemetry; TECH(8): unittest]
    ## @purpose Verify: letter rus capital without yo predecessor.
    ## @complexity 5
    def test_letter_rus_capital_without_yo_predecessor(self) -> None:
        # LDD TELEMETRY: log execution context before assertions
        print(f"\n--- LDD TRAJECTORY (IMP:7-10) for TestPrefix::test_letter_rus_capital_without_yo_predecessor ---")
        print(f"  [LDD_TEST][IMP:8][TestPrefix][test_letter_rus_capital_without_yo_predecessor] Test logic executed, entering assertion phase")
        one = LetterPrefix("Е)", 0)
        two = LetterPrefix("Ж)", 0)
        three = LetterPrefix("З)", 0)
        self._check_three_prefix(one, three, two)

    # endregion METHOD_test_letter_rus_capital_without_yo_predecessor
    # region METHOD_test_letter_all_predecessor [DOMAIN(7): Testing; CONCEPT(8): LDD_Telemetry; TECH(8): unittest]
    ## @purpose Verify: letter all predecessor.
    ## @complexity 5
    def test_letter_all_predecessor(self) -> None:
        # LDD TELEMETRY: log execution context before assertions
        print(f"\n--- LDD TRAJECTORY (IMP:7-10) for TestPrefix::test_letter_all_predecessor ---")
        print(f"  [LDD_TEST][IMP:8][TestPrefix][test_letter_all_predecessor] Test logic executed, entering assertion phase")
        letters_lower_rus = "абвгдеёжзийклмнопрстуфхцчшщъыьэюя"
        letters_upper_rus = letters_lower_rus.upper()

        letters_lower_eng = "abcdefghijklmnopqrstuvwxyz"
        letters_upper_eng = "abcdefghijklmnopqrstuvwxyz"

        for letters in (letters_lower_rus, letters_upper_rus, letters_lower_eng, letters_upper_eng):
            for first, second in zip(letters[:-1], letters[1:]):
                first = LetterPrefix(first, 0)
                second = LetterPrefix(second, 0)
                self.assertTrue(second.predecessor(first), f"{first} should be predecessor of {second}")
                self.assertFalse(first.predecessor(second), f"{first} should not be predecessor of {second}")

    # endregion METHOD_test_letter_all_predecessor
    # region METHOD__check_three_prefix [DOMAIN(7): Testing; CONCEPT(8): TestInfrastructure; TECH(8): unittest]
    ## @purpose check three prefix.
    def _check_three_prefix(self, one: LinePrefix, three: LinePrefix, two: LinePrefix) -> None:
        self.assertTrue(two.predecessor(one))
        self.assertTrue(three.predecessor(two))
        self.assertFalse(one.predecessor(one))
        self.assertFalse(one.predecessor(two))
        self.assertFalse(one.predecessor(three))
        self.assertFalse(three.predecessor(one), f"{three} {one}")

    # endregion METHOD__check_three_prefix
    # region METHOD_test_dotted_predecessor_one_num [DOMAIN(7): Testing; CONCEPT(8): LDD_Telemetry; TECH(8): unittest]
    ## @purpose Verify: dotted predecessor one num.
    ## @complexity 5
    def test_dotted_predecessor_one_num(self) -> None:
        # LDD TELEMETRY: log execution context before assertions
        print(f"\n--- LDD TRAJECTORY (IMP:7-10) for TestPrefix::test_dotted_predecessor_one_num ---")
        print(f"  [LDD_TEST][IMP:8][TestPrefix][test_dotted_predecessor_one_num] Test logic executed, entering assertion phase")
        one = DottedPrefix("1.", 0)
        two = DottedPrefix("2.", 0)
        self.assertTrue(two.predecessor(one))
        self.assertFalse(one.predecessor(two))

        one = DottedPrefix("1.", 0)
        two = DottedPrefix("3.", 0)
        self.assertFalse(two.predecessor(one))
        self.assertFalse(one.predecessor(two))

    # endregion METHOD_test_dotted_predecessor_one_num
    # region METHOD_test_dotted_predecessor_two_num [DOMAIN(7): Testing; CONCEPT(8): LDD_Telemetry; TECH(8): unittest]
    ## @purpose Verify: dotted predecessor two num.
    ## @complexity 5
    def test_dotted_predecessor_two_num(self) -> None:
        # LDD TELEMETRY: log execution context before assertions
        print(f"\n--- LDD TRAJECTORY (IMP:7-10) for TestPrefix::test_dotted_predecessor_two_num ---")
        print(f"  [LDD_TEST][IMP:8][TestPrefix][test_dotted_predecessor_two_num] Test logic executed, entering assertion phase")
        one = DottedPrefix("1.1.", 0)
        two = DottedPrefix("1.2.", 0)
        self.assertTrue(two.predecessor(one))
        self.assertFalse(one.predecessor(two))

        one = DottedPrefix("1.1.", 0)
        two = DottedPrefix("1.3.", 0)
        self.assertFalse(two.predecessor(one))
        self.assertFalse(one.predecessor(two))

        one = DottedPrefix("1.1.", 0)
        two = DottedPrefix("1.1.", 0)
        self.assertFalse(two.predecessor(one))
        self.assertFalse(one.predecessor(two))

    # endregion METHOD_test_dotted_predecessor_two_num
    # region METHOD_test_dotted_predecessor_different_num [DOMAIN(7): Testing; CONCEPT(8): LDD_Telemetry; TECH(8): unittest]
    ## @purpose Verify: dotted predecessor different num.
    ## @complexity 5
    def test_dotted_predecessor_different_num(self) -> None:
        # LDD TELEMETRY: log execution context before assertions
        print(f"\n--- LDD TRAJECTORY (IMP:7-10) for TestPrefix::test_dotted_predecessor_different_num ---")
        print(f"  [LDD_TEST][IMP:8][TestPrefix][test_dotted_predecessor_different_num] Test logic executed, entering assertion phase")
        one = DottedPrefix("1.", 0)
        two = DottedPrefix("1.1.", 0)
        self.assertTrue(two.predecessor(one))
        self.assertFalse(one.predecessor(two))

        one = DottedPrefix("1.", 0)
        two = DottedPrefix("1.2.", 0)
        self.assertFalse(two.predecessor(one))
        self.assertFalse(one.predecessor(two))

        one = DottedPrefix("1.1.1", 0)
        two = DottedPrefix("1.2.", 0)
        self.assertTrue(two.predecessor(one))
        self.assertFalse(one.predecessor(two))

        one = DottedPrefix("1.1.2.1.2.1", 0)
        two = DottedPrefix("1.2.", 0)
        self.assertTrue(two.predecessor(one))
        self.assertFalse(one.predecessor(two))

        one = DottedPrefix("1.2.1.", 0)
        two = DottedPrefix("1.2.1.1.1.", 0)
        self.assertFalse(two.predecessor(one))
        self.assertFalse(one.predecessor(two))

    # endregion METHOD_test_dotted_predecessor_different_num
    # region METHOD_test_dotted_list_regexp [DOMAIN(7): Testing; CONCEPT(8): LDD_Telemetry; TECH(8): unittest]
    ## @purpose Verify: dotted list regexp.
    ## @complexity 5
    def test_dotted_list_regexp(self) -> None:
        # LDD TELEMETRY: log execution context before assertions
        print(f"\n--- LDD TRAJECTORY (IMP:7-10) for TestPrefix::test_dotted_list_regexp ---")
        print(f"  [LDD_TEST][IMP:8][TestPrefix][test_dotted_list_regexp] Test logic executed, entering assertion phase")
        self.assertTrue(BulletPrefix.regexp.fullmatch(" -"))
        self.assertTrue(BulletPrefix.regexp.fullmatch("*"))
        self.assertTrue(BulletPrefix.regexp.fullmatch("     ©"))
        self.assertTrue(BulletPrefix.regexp.fullmatch("     ©   ") is None)

    # endregion METHOD_test_dotted_list_regexp
# endregion CLASS_TestPrefix