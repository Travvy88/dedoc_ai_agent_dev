# region MODULE_CONTRACT [DOMAIN(7): Testing; CONCEPT(8): UnitTest, LDD_Telemetry; TECH(8): unittest, pytest]
## @modulecontract
## @purpose Unit tests for misc list feature extractor module.
## @scope Unit testing of dedoc module: misc, list, feature, extractor.
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
## CLASS 8[Unit tests] => TestListFeatures
## @usecases
## - [Tests]: QA Agent (Verify) => RunTestsWithTelemetry => DiagnosticTrajectoryVisible
def _module_contract():
    pass
# endregion MODULE_CONTRACT
# GREP_SUMMARY: misc, list, feature, extractor, TestListFeatures, test_bracket, test_dotted, test_letter, test_non_letter_prefix, test_empty_prefix, test_get_window, unit_test, unittest, LDD_telemetry, semantic_markup, unit_test
# STRUCTURE: ▶ Init → ◇ Execute → ⊕ Verify → ∑ assertions → ⎋ PASS/FAIL


import logging

logger = logging.getLogger(__name__)

from unittest import TestCase

import numpy as np

from dedoc.data_structures.concrete_annotations.indentation_annotation import IndentationAnnotation
from dedoc.data_structures.line_metadata import LineMetadata
from dedoc.data_structures.line_with_meta import LineWithMeta
from dedoc.structure_extractors.feature_extractors.list_features.list_features_extractor import ListFeaturesExtractor
from dedoc.structure_extractors.feature_extractors.list_features.prefix.bracket_prefix import BracketPrefix
from dedoc.structure_extractors.feature_extractors.list_features.prefix.bullet_prefix import BulletPrefix
from dedoc.structure_extractors.feature_extractors.list_features.prefix.dotted_prefix import DottedPrefix
from dedoc.structure_extractors.feature_extractors.list_features.prefix.empty_prefix import EmptyPrefix
from dedoc.structure_extractors.feature_extractors.list_features.prefix.letter_prefix import LetterPrefix


# region CLASS_TestListFeatures [DOMAIN(7): Testing; CONCEPT(8): UnitTest, LDD_Telemetry; TECH(8): unittest, pytest]
## @purpose Test suite for misc, list, feature, extractor module.
class TestListFeatures(TestCase):
    feature_extractor = ListFeaturesExtractor()

    # region METHOD__get_line_with_meta [DOMAIN(7): Testing; CONCEPT(8): TestInfrastructure; TECH(8): unittest]
    ## @purpose get line with meta.
    def _get_line_with_meta(self, text: str, indentation: int = 10) -> LineWithMeta:
        annotations = [IndentationAnnotation(0, len(text), str(indentation))]
        return LineWithMeta(line=text, metadata=LineMetadata(page_id=0, line_id=0), annotations=annotations)

    # endregion METHOD__get_line_with_meta
    # region METHOD_test_bracket [DOMAIN(7): Testing; CONCEPT(8): LDD_Telemetry; TECH(8): unittest]
    ## @purpose Verify: bracket.
    ## @complexity 5
    def test_bracket(self) -> None:
        # LDD TELEMETRY: log execution context before assertions
        print(f"\n--- LDD TRAJECTORY (IMP:7-10) for TestListFeatures::test_bracket ---")
        print(f"  [LDD_TEST][IMP:8][TestListFeatures][test_bracket] Test logic executed, entering assertion phase")
        line = self._get_line_with_meta("1) some text")
        self.assertEqual(BracketPrefix("1)", 10), self.feature_extractor._get_prefix(line))

        line = self._get_line_with_meta("2) some text")
        self.assertEqual(BracketPrefix("2)", 10), self.feature_extractor._get_prefix(line))

        line = self._get_line_with_meta("   3) some text")
        self.assertEqual(BracketPrefix("3)", 10), self.feature_extractor._get_prefix(line))

        line = self._get_line_with_meta("\t3) some text")
        self.assertEqual(BracketPrefix("3)", 10), self.feature_extractor._get_prefix(line))

        line = self._get_line_with_meta("   3) some text")
        self.assertEqual(BracketPrefix("3)", 10), self.feature_extractor._get_prefix(line))

    # endregion METHOD_test_bracket
    # region METHOD_test_dotted [DOMAIN(7): Testing; CONCEPT(8): LDD_Telemetry; TECH(8): unittest]
    ## @purpose Verify: dotted.
    ## @complexity 5
    def test_dotted(self) -> None:
        # LDD TELEMETRY: log execution context before assertions
        print(f"\n--- LDD TRAJECTORY (IMP:7-10) for TestListFeatures::test_dotted ---")
        print(f"  [LDD_TEST][IMP:8][TestListFeatures][test_dotted] Test logic executed, entering assertion phase")
        line = self._get_line_with_meta("1 some text")
        self.assertEqual(EmptyPrefix(indent=10), self.feature_extractor._get_prefix(line))

        line = self._get_line_with_meta("1. some text")
        self.assertEqual(DottedPrefix("1.", 10), self.feature_extractor._get_prefix(line))

        line = self._get_line_with_meta("   3. some text")
        self.assertEqual(DottedPrefix("3.", 10), self.feature_extractor._get_prefix(line))

        line = self._get_line_with_meta("   1.3. some text")
        self.assertEqual(DottedPrefix("1.3.", 10), self.feature_extractor._get_prefix(line))

        line = self._get_line_with_meta("\t1.3. some text")
        self.assertEqual(DottedPrefix("1.3.", 10), self.feature_extractor._get_prefix(line))

        line = self._get_line_with_meta("\n1.3. some text")
        self.assertEqual(DottedPrefix("1.3.", 10), self.feature_extractor._get_prefix(line))

        line = self._get_line_with_meta("   1.2.3. some text")
        self.assertEqual(DottedPrefix("1.2.3.", 10), self.feature_extractor._get_prefix(line))

        line = self._get_line_with_meta("   1.2.3 some text")
        self.assertEqual(DottedPrefix("1.2.3", 10), self.feature_extractor._get_prefix(line))

    # endregion METHOD_test_dotted
    # region METHOD_test_letter [DOMAIN(7): Testing; CONCEPT(8): LDD_Telemetry; TECH(8): unittest]
    ## @purpose Verify: letter.
    ## @complexity 5
    def test_letter(self) -> None:
        # LDD TELEMETRY: log execution context before assertions
        print(f"\n--- LDD TRAJECTORY (IMP:7-10) for TestListFeatures::test_letter ---")
        print(f"  [LDD_TEST][IMP:8][TestListFeatures][test_letter] Test logic executed, entering assertion phase")
        line = self._get_line_with_meta("a) some text")
        self.assertEqual(LetterPrefix("a)", 10), self.feature_extractor._get_prefix(line))

        line = self._get_line_with_meta("b) some text")
        self.assertEqual(LetterPrefix("b)", 10), self.feature_extractor._get_prefix(line))

        line = self._get_line_with_meta(" c) some text")
        self.assertEqual(LetterPrefix("c)", 10), self.feature_extractor._get_prefix(line))

        line = self._get_line_with_meta("\td) some text")
        self.assertEqual(LetterPrefix("d)", 10), self.feature_extractor._get_prefix(line))

        line = self._get_line_with_meta("\tа) some text")
        self.assertEqual(LetterPrefix("а)", 10), self.feature_extractor._get_prefix(line))

        line = self._get_line_with_meta("\tё) some text")
        self.assertEqual(LetterPrefix("ё)", 10), self.feature_extractor._get_prefix(line))

    # endregion METHOD_test_letter
    # region METHOD_test_non_letter_prefix [DOMAIN(7): Testing; CONCEPT(8): LDD_Telemetry; TECH(8): unittest]
    ## @purpose Verify: non letter prefix.
    ## @complexity 5
    def test_non_letter_prefix(self) -> None:
        # LDD TELEMETRY: log execution context before assertions
        print(f"\n--- LDD TRAJECTORY (IMP:7-10) for TestListFeatures::test_non_letter_prefix ---")
        print(f"  [LDD_TEST][IMP:8][TestListFeatures][test_non_letter_prefix] Test logic executed, entering assertion phase")
        line = self._get_line_with_meta("- some text")
        self.assertEqual(BulletPrefix("-", 10), self.feature_extractor._get_prefix(line))

        line = self._get_line_with_meta("* some text")
        self.assertEqual(BulletPrefix("*", 10), self.feature_extractor._get_prefix(line))

        line = self._get_line_with_meta("+ some text")
        self.assertEqual(BulletPrefix("+", 10), self.feature_extractor._get_prefix(line))

    # endregion METHOD_test_non_letter_prefix
    # region METHOD_test_empty_prefix [DOMAIN(7): Testing; CONCEPT(8): LDD_Telemetry; TECH(8): unittest]
    ## @purpose Verify: empty prefix.
    ## @complexity 5
    def test_empty_prefix(self) -> None:
        # LDD TELEMETRY: log execution context before assertions
        print(f"\n--- LDD TRAJECTORY (IMP:7-10) for TestListFeatures::test_empty_prefix ---")
        print(f"  [LDD_TEST][IMP:8][TestListFeatures][test_empty_prefix] Test logic executed, entering assertion phase")
        line = self._get_line_with_meta("some text")
        self.assertEqual(EmptyPrefix(indent=10), self.feature_extractor._get_prefix(line))

        line = self._get_line_with_meta("\tsome text")
        self.assertEqual(EmptyPrefix(indent=10), self.feature_extractor._get_prefix(line))

        line = self._get_line_with_meta(" some text")
        self.assertEqual(EmptyPrefix(indent=10), self.feature_extractor._get_prefix(line))

        line = self._get_line_with_meta("\nsome text")
        self.assertEqual(EmptyPrefix(indent=10), self.feature_extractor._get_prefix(line))

    # endregion METHOD_test_empty_prefix
    # region METHOD_test_get_window [DOMAIN(7): Testing; CONCEPT(8): LDD_Telemetry; TECH(8): unittest]
    ## @purpose Verify: get window.
    ## @complexity 5
    def test_get_window(self) -> None:
        # LDD TELEMETRY: log execution context before assertions
        print(f"\n--- LDD TRAJECTORY (IMP:7-10) for TestListFeatures::test_get_window ---")
        print(f"  [LDD_TEST][IMP:8][TestListFeatures][test_get_window] Test logic executed, entering assertion phase")
        prefixes = [BracketPrefix(f"{i})", 1.01 * i) for i in range(0, 300)]
        doc_size = len(prefixes)
        assert doc_size == 300
        indents = np.array([prefix.indent for prefix in prefixes])
        window_0 = self.feature_extractor._get_window(indents=indents, prefixes=prefixes, line_id=0, doc_size=doc_size)
        self.assertEqual(0, len(window_0.prefix_before))
        self.assertNotIn("0)", [prefix.prefix for prefix in window_0.prefix_after])
        self.assertIn("2)", [prefix.prefix for prefix in window_0.prefix_after])

        window_12 = self.feature_extractor._get_window(indents=indents, prefixes=prefixes, line_id=12, doc_size=doc_size)
        self.assertEqual(12, len(window_12.prefix_before))
        self.assertEqual(prefixes[12].prefix, "12)")
        self.assertNotIn("12)", [prefix.prefix for prefix in window_12.prefix_after])
        self.assertIn("13)", [prefix.prefix for prefix in window_12.prefix_after])

        window_299 = self.feature_extractor._get_window(indents=indents, prefixes=prefixes, line_id=299, doc_size=doc_size)
        self.assertEqual(0, len(window_299.prefix_after))
        self.assertNotIn("299)", [prefix.prefix for prefix in window_12.prefix_after])

    # endregion METHOD_test_get_window
# endregion CLASS_TestListFeatures