# region MODULE_CONTRACT [DOMAIN(7): Testing; CONCEPT(8): UnitTest, LDD_Telemetry; TECH(8): unittest, pytest]
## @modulecontract
## @purpose Verify Location comparison operators (same/different pages) for PDF line ordering.
## @scope Unit testing of dedoc module: misc, location.
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
## CLASS 8[Unit tests] => TestLocation
## @usecases
## - [Tests]: QA Agent (Verify) => RunTestsWithTelemetry => DiagnosticTrajectoryVisible
def _module_contract():
    pass
# endregion MODULE_CONTRACT
# GREP_SUMMARY: misc, location, TestLocation, test_same_page, test_other_page, unit_test, unittest, LDD_telemetry, semantic_markup, unit_test
# STRUCTURE: ▶ ┌Location(page, BBox) pairs┐ → ◇ assertLess/Greater → ⊕ verify ordering → ∑ assertions → ⎋ PASS/FAIL


import logging

logger = logging.getLogger(__name__)

import unittest

from dedocutils.data_structures import BBox

from dedoc.readers.pdf_reader.data_classes.tables.location import Location


# region CLASS_TestLocation [DOMAIN(7): Testing; CONCEPT(8): UnitTest, LDD_Telemetry; TECH(8): unittest, pytest]
## @purpose Test suite for misc, location module.
class TestLocation(unittest.TestCase):

    # region METHOD_test_same_page [DOMAIN(7): Testing; CONCEPT(8): LDD_Telemetry; TECH(8): unittest]
    ## @purpose Verify: same page.
    ## @complexity 5
    def test_same_page(self) -> None:
        # LDD TELEMETRY: log execution context before assertions
        print(f"\n--- LDD TRAJECTORY (IMP:7-10) for TestLocation::test_same_page ---")
        print(f"  [LDD_TEST][IMP:8][TestLocation][test_same_page] Test logic executed, entering assertion phase")
        loc1 = Location(page_number=1, bbox=BBox(y_top_left=10, x_top_left=10, height=2, width=3))
        loc2 = Location(page_number=1, bbox=BBox(y_top_left=20, x_top_left=10, height=2, width=3))
        self.assertLess(loc1, loc2)
        loc3 = Location(page_number=1, bbox=BBox(y_top_left=20, x_top_left=5, height=2, width=3))
        self.assertLess(loc1, loc3)

    # endregion METHOD_test_same_page
    # region METHOD_test_other_page [DOMAIN(7): Testing; CONCEPT(8): LDD_Telemetry; TECH(8): unittest]
    ## @purpose Verify: other page.
    ## @complexity 5
    def test_other_page(self) -> None:
        # LDD TELEMETRY: log execution context before assertions
        print(f"\n--- LDD TRAJECTORY (IMP:7-10) for TestLocation::test_other_page ---")
        print(f"  [LDD_TEST][IMP:8][TestLocation][test_other_page] Test logic executed, entering assertion phase")
        loc1 = Location(page_number=0, bbox=BBox(y_top_left=20, x_top_left=10, height=2, width=3))
        loc2 = Location(page_number=1, bbox=BBox(y_top_left=10, x_top_left=10, height=2, width=3))
        self.assertLess(loc1, loc2)
        loc3 = Location(page_number=1, bbox=BBox(y_top_left=5, x_top_left=5, height=2, width=3))
        self.assertLess(loc1, loc3)
        self.assertGreater(loc2, loc3)

    # endregion METHOD_test_other_page
# endregion CLASS_TestLocation