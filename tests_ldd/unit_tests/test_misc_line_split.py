# region MODULE_CONTRACT [DOMAIN(7): Testing; CONCEPT(8): UnitTest, LDD_Telemetry; TECH(8): unittest, pytest]
## @modulecontract
## @purpose Unit tests for misc line split module.
## @scope Unit testing of dedoc module: misc, line, split.
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
## CLASS 8[Unit tests] => TestLineSplit
## @usecases
## - [Tests]: QA Agent (Verify) => RunTestsWithTelemetry => DiagnosticTrajectoryVisible
def _module_contract():
    pass
# endregion MODULE_CONTRACT
# GREP_SUMMARY: misc, line, split, TestLineSplit, test_empty_line_slice, test_line_slice_one_index, test_line_slice_one_negative_index, test_line_slice_border_left, test_line_slice_border_right, test_line_slice_intersection, test_line_slice_type_error, test_line_slice_out_of_range, test_line_slice_border, test_not_implemented_slice, test_line_slice_out_of_border, test_split_empty_line, test_split_empty_separator, test_one_element, test_end_with_sep, test_two_sep_in_a_row, test_two_symbols_sep, test_two_sep, test_by_regexp_sep, test_no_sep, test_split_line_with_two_intersecting_annotations, test_line_with_two_annotations_no_intersection, test_two_annotations_no_intersection_by_sep, test_split_of_one_annotation_ending_close_to_sep, unit_test, unittest, LDD_telemetry, semantic_markup, unit_test
# STRUCTURE: ▶ Init → ◇ Execute → ⊕ Verify → ∑ assertions → ⎋ PASS/FAIL


import logging

logger = logging.getLogger(__name__)

import unittest
from typing import List

from dedoc.data_structures.annotation import Annotation
from dedoc.data_structures.concrete_annotations.bold_annotation import BoldAnnotation
from dedoc.data_structures.concrete_annotations.size_annotation import SizeAnnotation
from dedoc.data_structures.hierarchy_level import HierarchyLevel
from dedoc.data_structures.line_metadata import LineMetadata
from dedoc.data_structures.line_with_meta import LineWithMeta


# region CLASS_TestLineSplit [DOMAIN(7): Testing; CONCEPT(8): UnitTest, LDD_Telemetry; TECH(8): unittest, pytest]
## @purpose Test suite for misc, line, split module.
class TestLineSplit(unittest.TestCase):

    # region METHOD_test_empty_line_slice [DOMAIN(7): Testing; CONCEPT(8): LDD_Telemetry; TECH(8): unittest]
    ## @purpose Verify: empty line slice.
    ## @complexity 5
    def test_empty_line_slice(self) -> None:
        # LDD TELEMETRY: log execution context before assertions
        print(f"\n--- LDD TRAJECTORY (IMP:7-10) for TestLineSplit::test_empty_line_slice ---")
        print(f"  [LDD_TEST][IMP:8][TestLineSplit][test_empty_line_slice] Test logic executed, entering assertion phase")
        line = self._get_line("", [])
        with self.assertRaises(IndexError):
            _ = line[0]
        line_slice = line[0:]
        self.assertNotEqual(id(line_slice), id(line))
        self.assertEqual(line_slice.line, line.line)
        self.assertEqual(line_slice.annotations, line.annotations)

    # endregion METHOD_test_empty_line_slice
    # region METHOD_test_line_slice_one_index [DOMAIN(7): Testing; CONCEPT(8): LDD_Telemetry; TECH(8): unittest]
    ## @purpose Verify: line slice one index.
    ## @complexity 5
    def test_line_slice_one_index(self) -> None:
        # LDD TELEMETRY: log execution context before assertions
        print(f"\n--- LDD TRAJECTORY (IMP:7-10) for TestLineSplit::test_line_slice_one_index ---")
        print(f"  [LDD_TEST][IMP:8][TestLineSplit][test_line_slice_one_index] Test logic executed, entering assertion phase")
        line = self._get_line_for_slice()
        line_slice = line[7]
        self.assertEqual("t", line_slice.line)
        self.assertEqual(2, len(line_slice.annotations))
        self.assertIn(BoldAnnotation(0, 1, "False"), line_slice.annotations)
        self.assertIn(SizeAnnotation(0, 1, "10"), line_slice.annotations)

    # endregion METHOD_test_line_slice_one_index
    # region METHOD_test_line_slice_one_negative_index [DOMAIN(7): Testing; CONCEPT(8): LDD_Telemetry; TECH(8): unittest]
    ## @purpose Verify: line slice one negative index.
    ## @complexity 5
    def test_line_slice_one_negative_index(self) -> None:
        # LDD TELEMETRY: log execution context before assertions
        print(f"\n--- LDD TRAJECTORY (IMP:7-10) for TestLineSplit::test_line_slice_one_negative_index ---")
        print(f"  [LDD_TEST][IMP:8][TestLineSplit][test_line_slice_one_negative_index] Test logic executed, entering assertion phase")
        line = self._get_line_for_slice()
        line_slice = line[-5]
        self.assertEqual(1, len(line_slice))
        self.assertEqual("E", line_slice.line)
        self.assertEqual(2, len(line_slice.annotations))
        self.assertIn(BoldAnnotation(0, 1, "False"), line_slice.annotations)
        self.assertIn(SizeAnnotation(0, 1, "14"), line_slice.annotations)
        with self.assertRaises(IndexError):
            _ = line[-9]
        with self.assertRaises(IndexError):
            _ = line[-10]
        for index in range(-len(line), len(line)):
            slice_left = line[index]
            slice_right = line[index % len(line)]
            self.assertEqual(slice_left.line, slice_right.line)

    # endregion METHOD_test_line_slice_one_negative_index
    # region METHOD_test_line_slice_border_left [DOMAIN(7): Testing; CONCEPT(8): LDD_Telemetry; TECH(8): unittest]
    ## @purpose Verify: line slice border left.
    ## @complexity 5
    def test_line_slice_border_left(self) -> None:
        # LDD TELEMETRY: log execution context before assertions
        print(f"\n--- LDD TRAJECTORY (IMP:7-10) for TestLineSplit::test_line_slice_border_left ---")
        print(f"  [LDD_TEST][IMP:8][TestLineSplit][test_line_slice_border_left] Test logic executed, entering assertion phase")
        line = self._get_line_for_slice()
        line_slice = line[0:4]
        self.assertEqual("SOME", line_slice.line)
        self.assertEqual(2, len(line_slice.annotations), line_slice.annotations)
        self.assertIn(SizeAnnotation(0, 4, "14"), line_slice.annotations)
        self.assertIn(BoldAnnotation(0, 4, "False"), line_slice.annotations)

    # endregion METHOD_test_line_slice_border_left
    # region METHOD_test_line_slice_border_right [DOMAIN(7): Testing; CONCEPT(8): LDD_Telemetry; TECH(8): unittest]
    ## @purpose Verify: line slice border right.
    ## @complexity 5
    def test_line_slice_border_right(self) -> None:
        # LDD TELEMETRY: log execution context before assertions
        print(f"\n--- LDD TRAJECTORY (IMP:7-10) for TestLineSplit::test_line_slice_border_right ---")
        print(f"  [LDD_TEST][IMP:8][TestLineSplit][test_line_slice_border_right] Test logic executed, entering assertion phase")
        line = self._get_line_for_slice()
        line_slice = line[4:8]
        self.assertEqual("text", line_slice.line)
        self.assertEqual(2, len(line_slice.annotations), line_slice.annotations)
        self.assertIn(SizeAnnotation(0, 4, "10"), line_slice.annotations)
        self.assertIn(BoldAnnotation(0, 4, "False"), line_slice.annotations)

    # endregion METHOD_test_line_slice_border_right
    # region METHOD_test_line_slice_intersection [DOMAIN(7): Testing; CONCEPT(8): LDD_Telemetry; TECH(8): unittest]
    ## @purpose Verify: line slice intersection.
    ## @complexity 5
    def test_line_slice_intersection(self) -> None:
        # LDD TELEMETRY: log execution context before assertions
        print(f"\n--- LDD TRAJECTORY (IMP:7-10) for TestLineSplit::test_line_slice_intersection ---")
        print(f"  [LDD_TEST][IMP:8][TestLineSplit][test_line_slice_intersection] Test logic executed, entering assertion phase")
        line = self._get_line_for_slice()
        line_slice = line[3:8]
        self.assertEqual("Etext", line_slice.line)
        self.assertEqual(3, len(line_slice.annotations), line_slice.annotations)
        self.assertIn(SizeAnnotation(1, 5, "10"), line_slice.annotations)
        self.assertIn(SizeAnnotation(0, 1, "14"), line_slice.annotations)
        self.assertIn(BoldAnnotation(0, 5, "False"), line_slice.annotations)

    # endregion METHOD_test_line_slice_intersection
    # region METHOD_test_line_slice_type_error [DOMAIN(7): Testing; CONCEPT(8): LDD_Telemetry; TECH(8): unittest]
    ## @purpose Verify: line slice type error.
    ## @complexity 5
    def test_line_slice_type_error(self) -> None:
        # LDD TELEMETRY: log execution context before assertions
        print(f"\n--- LDD TRAJECTORY (IMP:7-10) for TestLineSplit::test_line_slice_type_error ---")
        print(f"  [LDD_TEST][IMP:8][TestLineSplit][test_line_slice_type_error] Test logic executed, entering assertion phase")
        line = self._get_line_for_slice()
        for index in ["f", None, 1.3]:
            with self.assertRaises(TypeError):
                _ = line[index]

    # endregion METHOD_test_line_slice_type_error
    # region METHOD_test_line_slice_out_of_range [DOMAIN(7): Testing; CONCEPT(8): LDD_Telemetry; TECH(8): unittest]
    ## @purpose Verify: line slice out of range.
    ## @complexity 5
    def test_line_slice_out_of_range(self) -> None:
        # LDD TELEMETRY: log execution context before assertions
        print(f"\n--- LDD TRAJECTORY (IMP:7-10) for TestLineSplit::test_line_slice_out_of_range ---")
        print(f"  [LDD_TEST][IMP:8][TestLineSplit][test_line_slice_out_of_range] Test logic executed, entering assertion phase")
        line = self._get_line_for_slice()
        with self.assertRaises(IndexError):
            _ = line[9]
        with self.assertRaises(IndexError):
            _ = line[8]
        with self.assertRaises(IndexError):
            _ = line[8:]
        with self.assertRaises(IndexError):
            _ = line[9:]

    # endregion METHOD_test_line_slice_out_of_range
    # region METHOD_test_line_slice_border [DOMAIN(7): Testing; CONCEPT(8): LDD_Telemetry; TECH(8): unittest]
    ## @purpose Verify: line slice border.
    ## @complexity 5
    def test_line_slice_border(self) -> None:
        # LDD TELEMETRY: log execution context before assertions
        print(f"\n--- LDD TRAJECTORY (IMP:7-10) for TestLineSplit::test_line_slice_border ---")
        print(f"  [LDD_TEST][IMP:8][TestLineSplit][test_line_slice_border] Test logic executed, entering assertion phase")
        line = self._get_line_for_slice()
        line_slice = line[4:8]
        self.assertIn(BoldAnnotation(0, 4, "False"), line_slice.annotations)
        self.assertIn(SizeAnnotation(0, 4, "10"), line_slice.annotations)
        self.assertEqual(2, len(line_slice.annotations))

    # endregion METHOD_test_line_slice_border
    # region METHOD_test_not_implemented_slice [DOMAIN(7): Testing; CONCEPT(8): LDD_Telemetry; TECH(8): unittest]
    ## @purpose Verify: not implemented slice.
    ## @complexity 5
    def test_not_implemented_slice(self) -> None:
        # LDD TELEMETRY: log execution context before assertions
        print(f"\n--- LDD TRAJECTORY (IMP:7-10) for TestLineSplit::test_not_implemented_slice ---")
        print(f"  [LDD_TEST][IMP:8][TestLineSplit][test_not_implemented_slice] Test logic executed, entering assertion phase")
        line = self._get_line_for_slice()
        with self.assertRaises(NotImplementedError):
            _ = line[1:2:3]
        with self.assertRaises(NotImplementedError):
            _ = line[-2:-1]
        with self.assertRaises(NotImplementedError):
            _ = line[1:2:-1]
        with self.assertRaises(NotImplementedError):
            _ = line[-2:-1:2]

    # endregion METHOD_test_not_implemented_slice
    # region METHOD_test_line_slice_out_of_border [DOMAIN(7): Testing; CONCEPT(8): LDD_Telemetry; TECH(8): unittest]
    ## @purpose Verify: line slice out of border.
    ## @complexity 5
    def test_line_slice_out_of_border(self) -> None:
        # LDD TELEMETRY: log execution context before assertions
        print(f"\n--- LDD TRAJECTORY (IMP:7-10) for TestLineSplit::test_line_slice_out_of_border ---")
        print(f"  [LDD_TEST][IMP:8][TestLineSplit][test_line_slice_out_of_border] Test logic executed, entering assertion phase")
        line = self._get_line_for_slice()
        line_slice = line[3:10]
        self.assertIn(BoldAnnotation(0, 5, "False"), line_slice.annotations)
        self.assertIn(SizeAnnotation(1, 5, "10"), line_slice.annotations)
        self.assertIn(SizeAnnotation(0, 1, "14"), line_slice.annotations)
        self.assertEqual(3, len(line_slice.annotations))

    # endregion METHOD_test_line_slice_out_of_border
    # region METHOD_test_split_empty_line [DOMAIN(7): Testing; CONCEPT(8): LDD_Telemetry; TECH(8): unittest]
    ## @purpose Verify: split empty line.
    ## @complexity 5
    def test_split_empty_line(self) -> None:
        # LDD TELEMETRY: log execution context before assertions
        print(f"\n--- LDD TRAJECTORY (IMP:7-10) for TestLineSplit::test_split_empty_line ---")
        print(f"  [LDD_TEST][IMP:8][TestLineSplit][test_split_empty_line] Test logic executed, entering assertion phase")
        line = self._get_line("", [])
        split = line.split("\n")
        self.assertListEqual([line], split)

    # endregion METHOD_test_split_empty_line
    # region METHOD_test_split_empty_separator [DOMAIN(7): Testing; CONCEPT(8): LDD_Telemetry; TECH(8): unittest]
    ## @purpose Verify: split empty separator.
    ## @complexity 5
    def test_split_empty_separator(self) -> None:
        # LDD TELEMETRY: log execution context before assertions
        print(f"\n--- LDD TRAJECTORY (IMP:7-10) for TestLineSplit::test_split_empty_separator ---")
        print(f"  [LDD_TEST][IMP:8][TestLineSplit][test_split_empty_separator] Test logic executed, entering assertion phase")
        line = self._get_line("some text", [BoldAnnotation(0, 3, "True")])
        with self.assertRaises(ValueError):
            line.split("")

    # endregion METHOD_test_split_empty_separator
    # region METHOD_test_one_element [DOMAIN(7): Testing; CONCEPT(8): LDD_Telemetry; TECH(8): unittest]
    ## @purpose Verify: one element.
    ## @complexity 5
    def test_one_element(self) -> None:
        # LDD TELEMETRY: log execution context before assertions
        print(f"\n--- LDD TRAJECTORY (IMP:7-10) for TestLineSplit::test_one_element ---")
        print(f"  [LDD_TEST][IMP:8][TestLineSplit][test_one_element] Test logic executed, entering assertion phase")
        line = self._get_line("\n", [])
        split = line.split("\n")
        self.assertListEqual([line], split)

    # endregion METHOD_test_one_element
    # region METHOD_test_end_with_sep [DOMAIN(7): Testing; CONCEPT(8): LDD_Telemetry; TECH(8): unittest]
    ## @purpose Verify: end with sep.
    ## @complexity 5
    def test_end_with_sep(self) -> None:
        # LDD TELEMETRY: log execution context before assertions
        print(f"\n--- LDD TRAJECTORY (IMP:7-10) for TestLineSplit::test_end_with_sep ---")
        print(f"  [LDD_TEST][IMP:8][TestLineSplit][test_end_with_sep] Test logic executed, entering assertion phase")
        line = self._get_line("some text\n", [])
        split = line.split("\n")
        self.assertListEqual([line], split)

    # endregion METHOD_test_end_with_sep
    # region METHOD_test_two_sep_in_a_row [DOMAIN(7): Testing; CONCEPT(8): LDD_Telemetry; TECH(8): unittest]
    ## @purpose Verify: two sep in a row.
    ## @complexity 5
    def test_two_sep_in_a_row(self) -> None:
        # LDD TELEMETRY: log execution context before assertions
        print(f"\n--- LDD TRAJECTORY (IMP:7-10) for TestLineSplit::test_two_sep_in_a_row ---")
        print(f"  [LDD_TEST][IMP:8][TestLineSplit][test_two_sep_in_a_row] Test logic executed, entering assertion phase")
        line = self._get_line("some\n\ntext\n", [BoldAnnotation(0, 11, "True")])
        split = line.split("\n")
        self.assertEqual(3, len(split))
        left, middle, right = split
        self.assertEqual("some\n", left.line)

        self.assertEqual("\n", middle.line)

        self.assertEqual("text\n", right.line)

        self.__annotation_all_line(split)

    # endregion METHOD_test_two_sep_in_a_row
    # region METHOD_test_two_symbols_sep [DOMAIN(7): Testing; CONCEPT(8): LDD_Telemetry; TECH(8): unittest]
    ## @purpose Verify: two symbols sep.
    ## @complexity 5
    def test_two_symbols_sep(self) -> None:
        # LDD TELEMETRY: log execution context before assertions
        print(f"\n--- LDD TRAJECTORY (IMP:7-10) for TestLineSplit::test_two_symbols_sep ---")
        print(f"  [LDD_TEST][IMP:8][TestLineSplit][test_two_symbols_sep] Test logic executed, entering assertion phase")
        line = self._get_line("some--text\n", [BoldAnnotation(0, 11, "True")])
        split = line.split("--")
        self.assertEqual(2, len(split))
        left, right = split
        self.assertEqual("some--", left.line)

        self.assertEqual("text\n", right.line)
        self.assertEqual("text\n", right.line)

        self.__annotation_all_line(split)

    # endregion METHOD_test_two_symbols_sep
    # region METHOD_test_two_sep [DOMAIN(7): Testing; CONCEPT(8): LDD_Telemetry; TECH(8): unittest]
    ## @purpose Verify: two sep.
    ## @complexity 5
    def test_two_sep(self) -> None:
        # LDD TELEMETRY: log execution context before assertions
        print(f"\n--- LDD TRAJECTORY (IMP:7-10) for TestLineSplit::test_two_sep ---")
        print(f"  [LDD_TEST][IMP:8][TestLineSplit][test_two_sep] Test logic executed, entering assertion phase")
        line = self._get_line("some\nmore\ntext", [BoldAnnotation(0, 14, "True")])
        split = line.split("\n")
        self.assertEqual(3, len(split))
        left, middle, right = split
        self.assertEqual("some\n", left.line)

        self.assertEqual("more\n", middle.line)
        self.assertEqual("text", right.line)

        self.__annotation_all_line(split)

    # endregion METHOD_test_two_sep
    # region METHOD_test_by_regexp_sep [DOMAIN(7): Testing; CONCEPT(8): LDD_Telemetry; TECH(8): unittest]
    ## @purpose Verify: by regexp sep.
    ## @complexity 5
    def test_by_regexp_sep(self) -> None:
        # LDD TELEMETRY: log execution context before assertions
        print(f"\n--- LDD TRAJECTORY (IMP:7-10) for TestLineSplit::test_by_regexp_sep ---")
        print(f"  [LDD_TEST][IMP:8][TestLineSplit][test_by_regexp_sep] Test logic executed, entering assertion phase")
        line = self._get_line("some more  text\twith\nspaces \t\n", [BoldAnnotation(0, 30, "True")])
        split = line.split(r"\s+")
        self.assertEqual(5, len(split))
        one, two, three, four, five = split
        self.assertEqual("some ", one.line)
        self.assertEqual("more  ", two.line)
        self.assertEqual("text\t", three.line)
        self.assertEqual("with\n", four.line)
        self.assertEqual("spaces \t\n", five.line)

        self.__annotation_all_line(split)

    # endregion METHOD_test_by_regexp_sep
    # region METHOD_test_no_sep [DOMAIN(7): Testing; CONCEPT(8): LDD_Telemetry; TECH(8): unittest]
    ## @purpose Verify: no sep.
    ## @complexity 5
    def test_no_sep(self) -> None:
        # LDD TELEMETRY: log execution context before assertions
        print(f"\n--- LDD TRAJECTORY (IMP:7-10) for TestLineSplit::test_no_sep ---")
        print(f"  [LDD_TEST][IMP:8][TestLineSplit][test_no_sep] Test logic executed, entering assertion phase")
        line = self._get_line("some more text", [BoldAnnotation(0, 14, "True")])
        split = line.split("\n")
        self.assertListEqual([line], split)

    # endregion METHOD_test_no_sep
    # region METHOD_test_split_line_with_two_intersecting_annotations [DOMAIN(7): Testing; CONCEPT(8): LDD_Telemetry; TECH(8): unittest]
    ## @purpose Verify: split line with two intersecting annotations.
    ## @complexity 5
    def test_split_line_with_two_intersecting_annotations(self) -> None:
        # LDD TELEMETRY: log execution context before assertions
        print(f"\n--- LDD TRAJECTORY (IMP:7-10) for TestLineSplit::test_split_line_with_two_intersecting_annotations ---")
        print(f"  [LDD_TEST][IMP:8][TestLineSplit][test_split_line_with_two_intersecting_annotations] Test logic executed, entering assertion phase")
        line = self._get_line("some\ntext", [SizeAnnotation(0, 9, "14"), BoldAnnotation(0, 9, "True")])
        split = line.split("\n")
        self.assertEqual(2, len(split))
        for line in split:
            annotation_bold, annotation_size = sorted(line.annotations, key=lambda a: a.name)
            self.assertEqual(BoldAnnotation.name, annotation_bold.name)
            self.assertEqual("True", annotation_bold.value)
            self.assertEqual(0, annotation_bold.start)
            self.assertEqual(len(line.line), annotation_bold.end)

            self.assertEqual(SizeAnnotation.name, annotation_size.name)
            self.assertEqual("14", annotation_size.value)
            self.assertEqual(0, annotation_size.start)
            self.assertEqual(len(line.line), annotation_size.end)

    # endregion METHOD_test_split_line_with_two_intersecting_annotations
    # region METHOD_test_line_with_two_annotations_no_intersection [DOMAIN(7): Testing; CONCEPT(8): LDD_Telemetry; TECH(8): unittest]
    ## @purpose Verify: line with two annotations no intersection.
    ## @complexity 5
    def test_line_with_two_annotations_no_intersection(self) -> None:
        # LDD TELEMETRY: log execution context before assertions
        print(f"\n--- LDD TRAJECTORY (IMP:7-10) for TestLineSplit::test_line_with_two_annotations_no_intersection ---")
        print(f"  [LDD_TEST][IMP:8][TestLineSplit][test_line_with_two_annotations_no_intersection] Test logic executed, entering assertion phase")
        line = self._get_line("some\ntext", [SizeAnnotation(0, 5, "14"), SizeAnnotation(5, 9, "10")])
        split = line.split("\n")
        self.assertEqual(2, len(split))
        for size, line in zip(("14", "10"), split):
            self.assertEqual(1, len(line.annotations))
            annotation_size = line.annotations[0]

            self.assertEqual(SizeAnnotation.name, annotation_size.name)
            self.assertEqual(size, annotation_size.value)
            self.assertEqual(0, annotation_size.start)
            self.assertEqual(len(line.line), annotation_size.end)

    # endregion METHOD_test_line_with_two_annotations_no_intersection
    # region METHOD_test_two_annotations_no_intersection_by_sep [DOMAIN(7): Testing; CONCEPT(8): LDD_Telemetry; TECH(8): unittest]
    ## @purpose Verify: two annotations no intersection by sep.
    ## @complexity 5
    def test_two_annotations_no_intersection_by_sep(self) -> None:
        # LDD TELEMETRY: log execution context before assertions
        print(f"\n--- LDD TRAJECTORY (IMP:7-10) for TestLineSplit::test_two_annotations_no_intersection_by_sep ---")
        print(f"  [LDD_TEST][IMP:8][TestLineSplit][test_two_annotations_no_intersection_by_sep] Test logic executed, entering assertion phase")
        line = self._get_line("some\ntext", [SizeAnnotation(4, 9, "14")])
        split = line.split("\n")
        self.assertEqual(2, len(split))
        for (start, end), line in zip(((4, 5), (0, 4)), split):
            self.assertEqual(1, len(line.annotations))
            annotation_size = line.annotations[0]

            self.assertEqual(SizeAnnotation.name, annotation_size.name)
            self.assertEqual("14", annotation_size.value)
            self.assertEqual(start, annotation_size.start)
            self.assertEqual(end, annotation_size.end)

    # endregion METHOD_test_two_annotations_no_intersection_by_sep
    # region METHOD_test_split_of_one_annotation_ending_close_to_sep [DOMAIN(7): Testing; CONCEPT(8): LDD_Telemetry; TECH(8): unittest]
    ## @purpose Verify: split of one annotation ending close to sep.
    ## @complexity 5
    def test_split_of_one_annotation_ending_close_to_sep(self) -> None:
        # LDD TELEMETRY: log execution context before assertions
        print(f"\n--- LDD TRAJECTORY (IMP:7-10) for TestLineSplit::test_split_of_one_annotation_ending_close_to_sep ---")
        print(f"  [LDD_TEST][IMP:8][TestLineSplit][test_split_of_one_annotation_ending_close_to_sep] Test logic executed, entering assertion phase")
        line = self._get_line("some\ntext", [SizeAnnotation(0, 5, "14")])
        split = line.split("\n")
        self.assertEqual(2, len(split))
        left, right = split
        self.assertEqual(1, len(left.annotations))
        self.assertEqual(0, len(right.annotations))

    # endregion METHOD_test_split_of_one_annotation_ending_close_to_sep
    # region METHOD___annotation_all_line [DOMAIN(7): Testing; CONCEPT(8): TestInfrastructure; TECH(8): unittest]
    ## @purpose annotation all line.
    def __annotation_all_line(self, split: List[LineWithMeta]) -> None:
        """
        Tests if annotation has the same length as line
        """
        for line in split:
            annotations = line.annotations
            self.assertEqual(1, len(annotations))
            annotation = annotations[0]
            self.assertEqual(0, annotation.start)
            self.assertEqual(len(line.line), annotation.end)
            self.assertEqual("True", annotation.value)
            self.assertEqual(BoldAnnotation.name, annotation.name)

    # endregion METHOD___annotation_all_line
    # region METHOD__get_line [DOMAIN(7): Testing; CONCEPT(8): TestInfrastructure; TECH(8): unittest]
    ## @purpose get line.
    def _get_line(self, line: str, annotations: List[Annotation]) -> LineWithMeta:
        metadata = LineMetadata(hierarchy_level=HierarchyLevel.create_raw_text(), page_id=0, line_id=1)
        line = LineWithMeta(line=line, metadata=metadata, annotations=annotations)
        return line

    # endregion METHOD__get_line
    # region METHOD__get_line_for_slice [DOMAIN(7): Testing; CONCEPT(8): TestInfrastructure; TECH(8): unittest]
    ## @purpose get line for slice.
    def _get_line_for_slice(self) -> LineWithMeta:
        annotations = [
            SizeAnnotation(0, 4, "14"),
            SizeAnnotation(4, 8, "10"),
            BoldAnnotation(0, 8, "False")
        ]
        return self._get_line("SOMEtext", annotations=annotations)

    # endregion METHOD__get_line_for_slice
# endregion CLASS_TestLineSplit