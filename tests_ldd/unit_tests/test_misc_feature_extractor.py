# region MODULE_CONTRACT [DOMAIN(7): Testing; CONCEPT(8): UnitTest, LDD_Telemetry; TECH(8): unittest, pytest]
## @modulecontract
## @purpose Unit tests for misc feature extractor module.
## @scope Unit testing of dedoc module: misc, feature, extractor.
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
## CLASS 8[Unit tests] => TestRegexpFeatures
## @usecases
## - [Tests]: QA Agent (Verify) => RunTestsWithTelemetry => DiagnosticTrajectoryVisible
def _module_contract():
    pass
# endregion MODULE_CONTRACT
# GREP_SUMMARY: misc, feature, extractor, TestRegexpFeatures, test_prev_line_features, test_prev_line_features_2, test_prev_line_features_3, test_prev_line_features_4, test_next_line_features, test_next_line_features_2, test_next_line_features_3, test_next_line_features_4, test_previous_element_single, test_previous_element_multiple, unit_test, unittest, LDD_telemetry, semantic_markup, unit_test
# STRUCTURE: ▶ Init → ◇ Execute → ⊕ Verify → ∑ assertions → ⎋ PASS/FAIL


import logging

logger = logging.getLogger(__name__)

import unittest
from typing import List

import numpy as np

from dedoc.structure_extractors.feature_extractors.abstract_extractor import AbstractFeatureExtractor


# region CLASS_TestRegexpFeatures [DOMAIN(7): Testing; CONCEPT(8): UnitTest, LDD_Telemetry; TECH(8): unittest, pytest]
## @purpose Test suite for misc, feature, extractor module.
class TestRegexpFeatures(unittest.TestCase):
    result_matrix = np.array([[1, 0, 0], [0, 1, 1], [0, 0, 1]])

    # region METHOD_compare_with_expected [DOMAIN(7): Testing; CONCEPT(8): TestInfrastructure; TECH(8): unittest]
    ## @purpose compare with expected.
    def compare_with_expected(self, expected_matrix: List[List[int]], result: np.ndarray) -> None:
        self.assertEqual(len(expected_matrix), result.shape[0])
        self.assertEqual(len(expected_matrix[0]), result.shape[1])
        for row_res, row_exp in zip(result, expected_matrix):
            row_res = list(row_res)
            self.assertListEqual(row_exp, row_res)

    # endregion METHOD_compare_with_expected
    # region METHOD_test_prev_line_features [DOMAIN(7): Testing; CONCEPT(8): LDD_Telemetry; TECH(8): unittest]
    ## @purpose Verify: prev line features.
    ## @complexity 5
    def test_prev_line_features(self) -> None:
        """
        Tests shift on 1 line backward
        """
        # LDD TELEMETRY: log execution context before assertions
        print(f"\n--- LDD TRAJECTORY (IMP:7-10) for TestRegexpFeatures::test_prev_line_features ---")
        print(f"  [LDD_TEST][IMP:8][TestRegexpFeatures][test_prev_line_features] Test logic executed, entering assertion phase")
        expected_matrix = [
            [0, 0, 0],
            [1, 0, 0],
            [0, 1, 1],
        ]
        result = AbstractFeatureExtractor._prev_line_features(self.result_matrix, 1)
        self.compare_with_expected(expected_matrix, result)

    # endregion METHOD_test_prev_line_features
    # region METHOD_test_prev_line_features_2 [DOMAIN(7): Testing; CONCEPT(8): LDD_Telemetry; TECH(8): unittest]
    ## @purpose Verify: prev line features 2.
    ## @complexity 5
    def test_prev_line_features_2(self) -> None:
        """
        Tests shift on 2 lines backward
        """
        # LDD TELEMETRY: log execution context before assertions
        print(f"\n--- LDD TRAJECTORY (IMP:7-10) for TestRegexpFeatures::test_prev_line_features_2 ---")
        print(f"  [LDD_TEST][IMP:8][TestRegexpFeatures][test_prev_line_features_2] Test logic executed, entering assertion phase")
        expected_matrix = [
            [0, 0, 0],
            [0, 0, 0],
            [1, 0, 0],
        ]
        result = AbstractFeatureExtractor._prev_line_features(self.result_matrix, 2)
        self.compare_with_expected(expected_matrix, result)

    # endregion METHOD_test_prev_line_features_2
    # region METHOD_test_prev_line_features_3 [DOMAIN(7): Testing; CONCEPT(8): LDD_Telemetry; TECH(8): unittest]
    ## @purpose Verify: prev line features 3.
    ## @complexity 5
    def test_prev_line_features_3(self) -> None:
        """
        Tests shift on 3 lines backward
        """
        # LDD TELEMETRY: log execution context before assertions
        print(f"\n--- LDD TRAJECTORY (IMP:7-10) for TestRegexpFeatures::test_prev_line_features_3 ---")
        print(f"  [LDD_TEST][IMP:8][TestRegexpFeatures][test_prev_line_features_3] Test logic executed, entering assertion phase")
        expected_matrix = [
            [0, 0, 0],
            [0, 0, 0],
            [0, 0, 0],
        ]
        result = AbstractFeatureExtractor._prev_line_features(self.result_matrix, 3)
        self.compare_with_expected(expected_matrix, result)

    # endregion METHOD_test_prev_line_features_3
    # region METHOD_test_prev_line_features_4 [DOMAIN(7): Testing; CONCEPT(8): LDD_Telemetry; TECH(8): unittest]
    ## @purpose Verify: prev line features 4.
    ## @complexity 5
    def test_prev_line_features_4(self) -> None:
        """
        Tests shift on 4 lines backward
        """
        # LDD TELEMETRY: log execution context before assertions
        print(f"\n--- LDD TRAJECTORY (IMP:7-10) for TestRegexpFeatures::test_prev_line_features_4 ---")
        print(f"  [LDD_TEST][IMP:8][TestRegexpFeatures][test_prev_line_features_4] Test logic executed, entering assertion phase")
        expected_matrix = [
            [0, 0, 0],
            [0, 0, 0],
            [0, 0, 0],
        ]
        result = AbstractFeatureExtractor._prev_line_features(self.result_matrix, 4)
        self.compare_with_expected(expected_matrix, result)

    # endregion METHOD_test_prev_line_features_4
    # region METHOD_test_next_line_features [DOMAIN(7): Testing; CONCEPT(8): LDD_Telemetry; TECH(8): unittest]
    ## @purpose Verify: next line features.
    ## @complexity 5
    def test_next_line_features(self) -> None:
        """
        Tests shift on 1 line forward
        """
        # LDD TELEMETRY: log execution context before assertions
        print(f"\n--- LDD TRAJECTORY (IMP:7-10) for TestRegexpFeatures::test_next_line_features ---")
        print(f"  [LDD_TEST][IMP:8][TestRegexpFeatures][test_next_line_features] Test logic executed, entering assertion phase")
        expected_matrix = [
            [0, 1, 1],
            [0, 0, 1],
            [0, 0, 0],
        ]
        result = AbstractFeatureExtractor._next_line_features(self.result_matrix, 1)
        self.compare_with_expected(expected_matrix, result)

    # endregion METHOD_test_next_line_features
    # region METHOD_test_next_line_features_2 [DOMAIN(7): Testing; CONCEPT(8): LDD_Telemetry; TECH(8): unittest]
    ## @purpose Verify: next line features 2.
    ## @complexity 5
    def test_next_line_features_2(self) -> None:
        """
        Tests shift on 2 lines forward
        """
        # LDD TELEMETRY: log execution context before assertions
        print(f"\n--- LDD TRAJECTORY (IMP:7-10) for TestRegexpFeatures::test_next_line_features_2 ---")
        print(f"  [LDD_TEST][IMP:8][TestRegexpFeatures][test_next_line_features_2] Test logic executed, entering assertion phase")
        expected_matrix = [
            [0, 0, 1],
            [0, 0, 0],
            [0, 0, 0],
        ]
        result = AbstractFeatureExtractor._next_line_features(self.result_matrix, 2)
        self.compare_with_expected(expected_matrix, result)

    # endregion METHOD_test_next_line_features_2
    # region METHOD_test_next_line_features_3 [DOMAIN(7): Testing; CONCEPT(8): LDD_Telemetry; TECH(8): unittest]
    ## @purpose Verify: next line features 3.
    ## @complexity 5
    def test_next_line_features_3(self) -> None:
        """
        Tests shift on 3 lines forward
        """
        # LDD TELEMETRY: log execution context before assertions
        print(f"\n--- LDD TRAJECTORY (IMP:7-10) for TestRegexpFeatures::test_next_line_features_3 ---")
        print(f"  [LDD_TEST][IMP:8][TestRegexpFeatures][test_next_line_features_3] Test logic executed, entering assertion phase")
        expected_matrix = [
            [0, 0, 0],
            [0, 0, 0],
            [0, 0, 0],
        ]
        result = AbstractFeatureExtractor._next_line_features(self.result_matrix, 3)
        self.compare_with_expected(expected_matrix, result)

    # endregion METHOD_test_next_line_features_3
    # region METHOD_test_next_line_features_4 [DOMAIN(7): Testing; CONCEPT(8): LDD_Telemetry; TECH(8): unittest]
    ## @purpose Verify: next line features 4.
    ## @complexity 5
    def test_next_line_features_4(self) -> None:
        """
        Tests shift on 4 lines forward
        """
        # LDD TELEMETRY: log execution context before assertions
        print(f"\n--- LDD TRAJECTORY (IMP:7-10) for TestRegexpFeatures::test_next_line_features_4 ---")
        print(f"  [LDD_TEST][IMP:8][TestRegexpFeatures][test_next_line_features_4] Test logic executed, entering assertion phase")
        expected_matrix = [
            [0, 0, 0],
            [0, 0, 0],
            [0, 0, 0],
        ]
        result = AbstractFeatureExtractor._next_line_features(self.result_matrix, 4)
        self.compare_with_expected(expected_matrix, result)

    # endregion METHOD_test_next_line_features_4
    # region METHOD_test_previous_element_single [DOMAIN(7): Testing; CONCEPT(8): LDD_Telemetry; TECH(8): unittest]
    ## @purpose Verify: previous element single.
    ## @complexity 5
    def test_previous_element_single(self) -> None:
        """
        Tests if a single element can be a previous element for another single element
        """
        # LDD TELEMETRY: log execution context before assertions
        print(f"\n--- LDD TRAJECTORY (IMP:7-10) for TestRegexpFeatures::test_previous_element_single ---")
        print(f"  [LDD_TEST][IMP:8][TestRegexpFeatures][test_previous_element_single] Test logic executed, entering assertion phase")
        self.assertTrue(AbstractFeatureExtractor._can_be_prev_element(this_item="2", prev_item="1"))
        self.assertTrue(AbstractFeatureExtractor._can_be_prev_element(this_item="2.", prev_item="1"))
        self.assertTrue(AbstractFeatureExtractor._can_be_prev_element(this_item="2.", prev_item="1."))
        self.assertTrue(AbstractFeatureExtractor._can_be_prev_element(this_item="1.", prev_item="2"))
        self.assertTrue(AbstractFeatureExtractor._can_be_prev_element(this_item="1", prev_item="3."))
        self.assertFalse(AbstractFeatureExtractor._can_be_prev_element(this_item="3.", prev_item="1."))
        self.assertFalse(AbstractFeatureExtractor._can_be_prev_element(this_item="3.", prev_item="5."))

    # endregion METHOD_test_previous_element_single
    # region METHOD_test_previous_element_multiple [DOMAIN(7): Testing; CONCEPT(8): LDD_Telemetry; TECH(8): unittest]
    ## @purpose Verify: previous element multiple.
    ## @complexity 5
    def test_previous_element_multiple(self) -> None:
        """
        Tests if a complex element can be a previous element for another complex element
        """
        # LDD TELEMETRY: log execution context before assertions
        print(f"\n--- LDD TRAJECTORY (IMP:7-10) for TestRegexpFeatures::test_previous_element_multiple ---")
        print(f"  [LDD_TEST][IMP:8][TestRegexpFeatures][test_previous_element_multiple] Test logic executed, entering assertion phase")
        self.assertFalse(AbstractFeatureExtractor._can_be_prev_element(this_item="2.1.2", prev_item="2.1."))
        self.assertTrue(AbstractFeatureExtractor._can_be_prev_element(this_item="2.1.2", prev_item="2.1.1"))
        self.assertTrue(AbstractFeatureExtractor._can_be_prev_element(this_item="2.1.1", prev_item="2.1"))
        self.assertTrue(AbstractFeatureExtractor._can_be_prev_element(this_item="2.2", prev_item="2.1"))

    # endregion METHOD_test_previous_element_multiple
# endregion CLASS_TestRegexpFeatures