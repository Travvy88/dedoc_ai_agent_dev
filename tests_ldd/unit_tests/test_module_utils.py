# region MODULE_CONTRACT [DOMAIN(7): Testing; CONCEPT(8): UnitTest, LDD_Telemetry; TECH(8): unittest, pytest]
## @modulecontract
## @purpose Verify splitext_() utility correctly separates filename from extension for edge cases.
## @scope Unit testing of dedoc module: module, utils.
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
## CLASS 8[Unit tests] => TestUtils
## @usecases
## - [Tests]: QA Agent (Verify) => RunTestsWithTelemetry => DiagnosticTrajectoryVisible
def _module_contract():
    pass
# endregion MODULE_CONTRACT
# GREP_SUMMARY: module, utils, TestUtils, test_splitext_simple_name, test_splitext_apostrophe_name, test_splitext_space_name, test_splitext_dots_name, test_splitext_double_dot_extension, unit_test, unittest, LDD_telemetry, semantic_markup, unit_test
# STRUCTURE: ▶ Input ┌filename_with_ext┐ → ◇ splitext_(string) → ⊕ (name, ext) → ∑ assert_equal → ⎋ PASS/FAIL


import logging

logger = logging.getLogger(__name__)

import unittest

from dedoc.utils.utils import splitext_


# region CLASS_TestUtils [DOMAIN(7): Testing; CONCEPT(8): UnitTest, LDD_Telemetry; TECH(8): unittest, pytest]
## @purpose Test suite for module, utils module.
class TestUtils(unittest.TestCase):

    # region METHOD_test_splitext_simple_name [DOMAIN(7): Testing; CONCEPT(8): LDD_Telemetry; TECH(8): unittest]
    ## @purpose Verify: splitext simple name.
    ## @complexity 5
    def test_splitext_simple_name(self) -> None:
        # LDD TELEMETRY: log execution context before assertions
        print(f"\n--- LDD TRAJECTORY (IMP:7-10) for TestUtils::test_splitext_simple_name ---")
        print(f"  [LDD_TEST][IMP:8][TestUtils][test_splitext_simple_name] Test logic executed, entering assertion phase")
        name_extension = "name.doc"
        name, extension = splitext_(name_extension)
        self.assertEqual("name", name)
        self.assertEqual(".doc", extension)

    # endregion METHOD_test_splitext_simple_name
    # region METHOD_test_splitext_apostrophe_name [DOMAIN(7): Testing; CONCEPT(8): LDD_Telemetry; TECH(8): unittest]
    ## @purpose Verify: splitext apostrophe name.
    ## @complexity 5
    def test_splitext_apostrophe_name(self) -> None:
        # LDD TELEMETRY: log execution context before assertions
        print(f"\n--- LDD TRAJECTORY (IMP:7-10) for TestUtils::test_splitext_apostrophe_name ---")
        print(f"  [LDD_TEST][IMP:8][TestUtils][test_splitext_apostrophe_name] Test logic executed, entering assertion phase")
        name_extension = "Well. Known -Nik O'Tinn -Ireland 2023- DRAFT.doc"
        name, extension = splitext_(name_extension)
        self.assertEqual("Well. Known -Nik O'Tinn -Ireland 2023- DRAFT", name)
        self.assertEqual(".doc", extension)

    # endregion METHOD_test_splitext_apostrophe_name
    # region METHOD_test_splitext_space_name [DOMAIN(7): Testing; CONCEPT(8): LDD_Telemetry; TECH(8): unittest]
    ## @purpose Verify: splitext space name.
    ## @complexity 5
    def test_splitext_space_name(self) -> None:
        # LDD TELEMETRY: log execution context before assertions
        print(f"\n--- LDD TRAJECTORY (IMP:7-10) for TestUtils::test_splitext_space_name ---")
        print(f"  [LDD_TEST][IMP:8][TestUtils][test_splitext_space_name] Test logic executed, entering assertion phase")
        name_extension = "some file .doc"
        name, extension = splitext_(name_extension)
        self.assertEqual("some file ", name)
        self.assertEqual(".doc", extension)

    # endregion METHOD_test_splitext_space_name
    # region METHOD_test_splitext_dots_name [DOMAIN(7): Testing; CONCEPT(8): LDD_Telemetry; TECH(8): unittest]
    ## @purpose Verify: splitext dots name.
    ## @complexity 5
    def test_splitext_dots_name(self) -> None:
        # LDD TELEMETRY: log execution context before assertions
        print(f"\n--- LDD TRAJECTORY (IMP:7-10) for TestUtils::test_splitext_dots_name ---")
        print(f"  [LDD_TEST][IMP:8][TestUtils][test_splitext_dots_name] Test logic executed, entering assertion phase")
        name_extension = "1700134420_941.23_to_csv.csv"
        name, extension = splitext_(name_extension)
        self.assertEqual("1700134420_941.23_to_csv", name)
        self.assertEqual(".csv", extension)

    # endregion METHOD_test_splitext_dots_name
    # region METHOD_test_splitext_double_dot_extension [DOMAIN(7): Testing; CONCEPT(8): LDD_Telemetry; TECH(8): unittest]
    ## @purpose Verify: splitext double dot extension.
    ## @complexity 5
    def test_splitext_double_dot_extension(self) -> None:
        # LDD TELEMETRY: log execution context before assertions
        print(f"\n--- LDD TRAJECTORY (IMP:7-10) for TestUtils::test_splitext_double_dot_extension ---")
        print(f"  [LDD_TEST][IMP:8][TestUtils][test_splitext_double_dot_extension] Test logic executed, entering assertion phase")
        name_extension = "some_name.tar.gz"
        name, extension = splitext_(name_extension)
        self.assertEqual("some_name", name)
        self.assertEqual(".tar.gz", extension)

    # endregion METHOD_test_splitext_double_dot_extension
# endregion CLASS_TestUtils