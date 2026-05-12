# region MODULE_CONTRACT [DOMAIN(7): Testing; CONCEPT(8): UnitTest, LDD_Telemetry; TECH(8): unittest, pytest]
## @modulecontract
## @purpose Unit tests for module converter ppt module.
## @scope Unit testing of dedoc module: module, converter, ppt.
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
## CLASS 8[Unit tests] => TestPPTXConverter
## @usecases
## - [Tests]: QA Agent (Verify) => RunTestsWithTelemetry => DiagnosticTrajectoryVisible
def _module_contract():
    pass
# endregion MODULE_CONTRACT
# GREP_SUMMARY: module, converter, ppt, TestPPTXConverter, test_convert_broken_file, test_convert_odp, test_convert_ppt, unit_test, unittest, LDD_telemetry, semantic_markup, unit_test
# STRUCTURE: ▶ Init → ◇ Execute → ⊕ Verify → ∑ assertions → ⎋ PASS/FAIL


import logging

logger = logging.getLogger(__name__)

import os

from dedoc.common.exceptions.conversion_error import ConversionError
from dedoc.converters.concrete_converters.pptx_converter import PptxConverter
from tests.unit_tests.abstract_converter_test import AbstractConverterTest


# region CLASS_TestPPTXConverter [DOMAIN(7): Testing; CONCEPT(8): UnitTest, LDD_Telemetry; TECH(8): unittest, pytest]
## @purpose Test suite for module, converter, ppt module.
class TestPPTXConverter(AbstractConverterTest):

    path = os.path.join(AbstractConverterTest.path, "pptx")
    converter = PptxConverter(config={"need_content_analysis": True})

    # region METHOD_test_convert_broken_file [DOMAIN(7): Testing; CONCEPT(8): LDD_Telemetry; TECH(8): unittest]
    ## @purpose Verify: convert broken file.
    ## @complexity 5
    def test_convert_broken_file(self) -> None:
        # LDD TELEMETRY: log execution context before assertions
        print(f"\n--- LDD TRAJECTORY (IMP:7-10) for TestPPTXConverter::test_convert_broken_file ---")
        print(f"  [LDD_TEST][IMP:8][TestPPTXConverter][test_convert_broken_file] Test logic executed, entering assertion phase")
        extension = ".odp"
        filename = "broken"
        with self.assertRaises(ConversionError):
            self._convert(filename=filename, extension=extension, converter=self.converter)

    # endregion METHOD_test_convert_broken_file
    # region METHOD_test_convert_odp [DOMAIN(7): Testing; CONCEPT(8): LDD_Telemetry; TECH(8): unittest]
    ## @purpose Verify: convert odp.
    ## @complexity 5
    def test_convert_odp(self) -> None:
        # LDD TELEMETRY: log execution context before assertions
        print(f"\n--- LDD TRAJECTORY (IMP:7-10) for TestPPTXConverter::test_convert_odp ---")
        print(f"  [LDD_TEST][IMP:8][TestPPTXConverter][test_convert_odp] Test logic executed, entering assertion phase")
        filename = "example"
        extension = ".odp"
        self._convert(filename=filename, extension=extension, converter=self.converter)

    # endregion METHOD_test_convert_odp
    # region METHOD_test_convert_ppt [DOMAIN(7): Testing; CONCEPT(8): LDD_Telemetry; TECH(8): unittest]
    ## @purpose Verify: convert ppt.
    ## @complexity 5
    def test_convert_ppt(self) -> None:
        # LDD TELEMETRY: log execution context before assertions
        print(f"\n--- LDD TRAJECTORY (IMP:7-10) for TestPPTXConverter::test_convert_ppt ---")
        print(f"  [LDD_TEST][IMP:8][TestPPTXConverter][test_convert_ppt] Test logic executed, entering assertion phase")
        filename = "example"
        extension = ".ppt"
        self._convert(filename=filename, extension=extension, converter=self.converter)

    # endregion METHOD_test_convert_ppt
# endregion CLASS_TestPPTXConverter