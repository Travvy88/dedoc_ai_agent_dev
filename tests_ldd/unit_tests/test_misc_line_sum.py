# region MODULE_CONTRACT [DOMAIN(7): Testing; CONCEPT(8): UnitTest, LDD_Telemetry; TECH(8): unittest, pytest]
## @modulecontract
## @purpose Unit tests for misc line sum module.
## @scope Unit testing of dedoc module: misc, line, sum.
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
## CLASS 8[Unit tests] => TestLineSum
## @usecases
## - [Tests]: QA Agent (Verify) => RunTestsWithTelemetry => DiagnosticTrajectoryVisible
def _module_contract():
    pass
# endregion MODULE_CONTRACT
# GREP_SUMMARY: misc, line, sum, TestLineSum, test_empty_plus_empty, test_empty_nonempty, test_sum_with_str, test_line_plus_line, unit_test, unittest, LDD_telemetry, semantic_markup, unit_test
# STRUCTURE: ▶ Init → ◇ Execute → ⊕ Verify → ∑ assertions → ⎋ PASS/FAIL


import logging

logger = logging.getLogger(__name__)

import unittest
from typing import List

from dedoc.data_structures.annotation import Annotation
from dedoc.data_structures.concrete_annotations.bold_annotation import BoldAnnotation
from dedoc.data_structures.concrete_annotations.italic_annotation import ItalicAnnotation
from dedoc.data_structures.concrete_annotations.size_annotation import SizeAnnotation
from dedoc.data_structures.line_metadata import LineMetadata
from dedoc.data_structures.line_with_meta import LineWithMeta


def _make_line(line: str, annotations: List[Annotation]) -> LineWithMeta:
    line = LineWithMeta(line=line, metadata=LineMetadata(page_id=0, line_id=0), annotations=annotations)
    return line


# region CLASS_TestLineSum [DOMAIN(7): Testing; CONCEPT(8): UnitTest, LDD_Telemetry; TECH(8): unittest, pytest]
## @purpose Test suite for misc, line, sum module.
class TestLineSum(unittest.TestCase):

    empty = _make_line("", [])
    italic_line = _make_line("italic", [ItalicAnnotation(0, 6, "True")])
    bold_line = _make_line("bold", [BoldAnnotation(0, 4, "True")])
    sized_line = _make_line("SmallBig", [SizeAnnotation(0, 5, "8"), SizeAnnotation(5, 8, "14")])
    lines = [empty, italic_line, sized_line, bold_line]

    # region METHOD_assert_annotations_equal [DOMAIN(7): Testing; CONCEPT(8): TestInfrastructure; TECH(8): unittest]
    ## @purpose assert annotations equal.
    def assert_annotations_equal(self, expected: List[Annotation], result: List[Annotation]) -> None:
        self.assertEqual(len(expected), len(result))
        for annotation in result:
            self.assertIn(annotation, expected)

    # endregion METHOD_assert_annotations_equal
    # region METHOD_test_empty_plus_empty [DOMAIN(7): Testing; CONCEPT(8): LDD_Telemetry; TECH(8): unittest]
    ## @purpose Verify: empty plus empty.
    ## @complexity 5
    def test_empty_plus_empty(self) -> None:
        # LDD TELEMETRY: log execution context before assertions
        print(f"\n--- LDD TRAJECTORY (IMP:7-10) for TestLineSum::test_empty_plus_empty ---")
        print(f"  [LDD_TEST][IMP:8][TestLineSum][test_empty_plus_empty] Test logic executed, entering assertion phase")
        result = self.empty + self.empty
        self.assertEqual("", result.line)

    # endregion METHOD_test_empty_plus_empty
    # region METHOD_test_empty_nonempty [DOMAIN(7): Testing; CONCEPT(8): LDD_Telemetry; TECH(8): unittest]
    ## @purpose Verify: empty nonempty.
    ## @complexity 5
    def test_empty_nonempty(self) -> None:
        # LDD TELEMETRY: log execution context before assertions
        print(f"\n--- LDD TRAJECTORY (IMP:7-10) for TestLineSum::test_empty_nonempty ---")
        print(f"  [LDD_TEST][IMP:8][TestLineSum][test_empty_nonempty] Test logic executed, entering assertion phase")
        for non_empty in self.lines:
            for result in (self.empty + non_empty, non_empty + self.empty):
                self.assertEqual(non_empty.line, result.line)
                self.assert_annotations_equal(non_empty.annotations, result.annotations)

    # endregion METHOD_test_empty_nonempty
    # region METHOD_test_sum_with_str [DOMAIN(7): Testing; CONCEPT(8): LDD_Telemetry; TECH(8): unittest]
    ## @purpose Verify: sum with str.
    ## @complexity 5
    def test_sum_with_str(self) -> None:
        # LDD TELEMETRY: log execution context before assertions
        print(f"\n--- LDD TRAJECTORY (IMP:7-10) for TestLineSum::test_sum_with_str ---")
        print(f"  [LDD_TEST][IMP:8][TestLineSum][test_sum_with_str] Test logic executed, entering assertion phase")
        text = "some text"
        for line in self.lines:
            result = line + text
            self.assertEqual(line.line + text, result.line)
            self.assert_annotations_equal(line.annotations, result.annotations)

    # endregion METHOD_test_sum_with_str
    # region METHOD_test_line_plus_line [DOMAIN(7): Testing; CONCEPT(8): LDD_Telemetry; TECH(8): unittest]
    ## @purpose Verify: line plus line.
    ## @complexity 5
    def test_line_plus_line(self) -> None:
        # LDD TELEMETRY: log execution context before assertions
        print(f"\n--- LDD TRAJECTORY (IMP:7-10) for TestLineSum::test_line_plus_line ---")
        print(f"  [LDD_TEST][IMP:8][TestLineSum][test_line_plus_line] Test logic executed, entering assertion phase")
        for first in self.lines:
            for second in self.lines:
                result = first + second
                self.assertEqual(first.line + second.line, result.line)

        result = self.bold_line + self.bold_line
        self.assertEqual([BoldAnnotation(0, len(result.line), "True")], result.annotations)

        result = self.bold_line + self.italic_line
        expected = [BoldAnnotation(0, len(self.bold_line.line), "True"), ItalicAnnotation(4, 10, "True")]
        self.assert_annotations_equal(expected, result.annotations)

    # endregion METHOD_test_line_plus_line
# endregion CLASS_TestLineSum