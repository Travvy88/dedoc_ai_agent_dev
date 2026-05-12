# region MODULE_CONTRACT [DOMAIN(7): Testing; CONCEPT(8): UnitTest, LDD_Telemetry; TECH(8): unittest, pytest]
## @modulecontract
## @purpose Unit tests for module skew corrector module.
## @scope Unit testing of dedoc module: module, skew, corrector.
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
## CLASS 8[Unit tests] => TestSkewCorrector
## @usecases
## - [Tests]: QA Agent (Verify) => RunTestsWithTelemetry => DiagnosticTrajectoryVisible
def _module_contract():
    pass
# endregion MODULE_CONTRACT
# GREP_SUMMARY: module, skew, corrector, TestSkewCorrector, test_documents_with_short_lines, unit_test, unittest, LDD_telemetry, semantic_markup, unit_test
# STRUCTURE: ▶ Init → ◇ Execute → ⊕ Verify → ∑ assertions → ⎋ PASS/FAIL


import logging

logger = logging.getLogger(__name__)

import os
import unittest

import cv2
from dedocutils.preprocessing import SkewCorrector


# region CLASS_TestSkewCorrector [DOMAIN(7): Testing; CONCEPT(8): UnitTest, LDD_Telemetry; TECH(8): unittest, pytest]
## @purpose Test suite for module, skew, corrector module.
class TestSkewCorrector(unittest.TestCase):
    skew_corrector = SkewCorrector()

    # region METHOD__get_abs_path [DOMAIN(7): Testing; CONCEPT(8): TestInfrastructure; TECH(8): unittest]
    ## @purpose get abs path.
    def _get_abs_path(self, file_name: str) -> str:
        data_directory_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "data"))
        return os.path.join(data_directory_path, "skew_corrector", file_name)

    # endregion METHOD__get_abs_path
    # region METHOD_test_documents_with_short_lines [DOMAIN(7): Testing; CONCEPT(8): LDD_Telemetry; TECH(8): unittest]
    ## @purpose Verify: documents with short lines.
    ## @complexity 5
    def test_documents_with_short_lines(self) -> None:
        # LDD TELEMETRY: log execution context before assertions
        print(f"\n--- LDD TRAJECTORY (IMP:7-10) for TestSkewCorrector::test_documents_with_short_lines ---")
        print(f"  [LDD_TEST][IMP:8][TestSkewCorrector][test_documents_with_short_lines] Test logic executed, entering assertion phase")
        for i in range(1, 6):
            file_name = f"short_lines-{i}.png"
            img = cv2.imread(self._get_abs_path(file_name))
            image, angle = self.skew_corrector.preprocess(img)
            angle = angle["rotated_angle"]
            self.assertEqual(0, angle)

    # endregion METHOD_test_documents_with_short_lines
# endregion CLASS_TestSkewCorrector