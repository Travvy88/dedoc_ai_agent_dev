# region MODULE_CONTRACT [DOMAIN(7): Testing; CONCEPT(8): UnitTest, LDD_Telemetry; TECH(8): unittest, pytest]
## @modulecontract
## @purpose Verify DocxConverter handles .odt/.doc/.rtf conversion and broken files.
## @scope Unit testing of dedoc module: module, converter, docx.
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
## CLASS 8[Unit tests] => TestDocxConverter
## @usecases
## - [Tests]: QA Agent (Verify) => RunTestsWithTelemetry => DiagnosticTrajectoryVisible
def _module_contract():
    pass
# endregion MODULE_CONTRACT
# GREP_SUMMARY: module, converter, docx, TestDocxConverter, test_convert_broken_file, test_convert_odt, test_convert_doc, test_convert_rtf, unit_test, unittest, LDD_telemetry, semantic_markup, unit_test
# STRUCTURE: ▶ ┌DocxConverter + test_data┐ → ◇ _convert(file, ext) → ⊕ assert file exists ⊕ assertRaises → ∑ assertions → ⎋ PASS/FAIL


import logging

logger = logging.getLogger(__name__)

import os

from dedoc.common.exceptions.conversion_error import ConversionError
from dedoc.converters.concrete_converters.docx_converter import DocxConverter
from tests.unit_tests.abstract_converter_test import AbstractConverterTest


# region CLASS_TestDocxConverter [DOMAIN(7): Testing; CONCEPT(8): UnitTest, LDD_Telemetry; TECH(8): unittest, pytest]
## @purpose Test suite for module, converter, docx module.
class TestDocxConverter(AbstractConverterTest):

    converter = DocxConverter(config={"need_content_analysis": True})
    path = os.path.join(AbstractConverterTest.path, "docx")

    # region METHOD_test_convert_broken_file [DOMAIN(7): Testing; CONCEPT(8): LDD_Telemetry; TECH(8): unittest]
    ## @purpose Verify: convert broken file.
    ## @complexity 5
    def test_convert_broken_file(self) -> None:
        # LDD TELEMETRY: log execution context before assertions
        print(f"\n--- LDD TRAJECTORY (IMP:7-10) for TestDocxConverter::test_convert_broken_file ---")
        print(f"  [LDD_TEST][IMP:8][TestDocxConverter][test_convert_broken_file] Test logic executed, entering assertion phase")
        extension = ".odt"
        filename = "broken"
        with self.assertRaises(ConversionError):
            self._convert(filename=filename, extension=extension, converter=self.converter)

    # endregion METHOD_test_convert_broken_file
    # region METHOD_test_convert_odt [DOMAIN(7): Testing; CONCEPT(8): LDD_Telemetry; TECH(8): unittest]
    ## @purpose Verify: convert odt.
    ## @complexity 5
    def test_convert_odt(self) -> None:
        # LDD TELEMETRY: log execution context before assertions
        print(f"\n--- LDD TRAJECTORY (IMP:7-10) for TestDocxConverter::test_convert_odt ---")
        print(f"  [LDD_TEST][IMP:8][TestDocxConverter][test_convert_odt] Test logic executed, entering assertion phase")
        filename = "english_doc"
        extension = ".odt"
        self._convert(filename=filename, extension=extension, converter=self.converter)

    # endregion METHOD_test_convert_odt
    # region METHOD_test_convert_doc [DOMAIN(7): Testing; CONCEPT(8): LDD_Telemetry; TECH(8): unittest]
    ## @purpose Verify: convert doc.
    ## @complexity 5
    def test_convert_doc(self) -> None:
        # LDD TELEMETRY: log execution context before assertions
        print(f"\n--- LDD TRAJECTORY (IMP:7-10) for TestDocxConverter::test_convert_doc ---")
        print(f"  [LDD_TEST][IMP:8][TestDocxConverter][test_convert_doc] Test logic executed, entering assertion phase")
        filename = "english_doc"
        extension = ".doc"
        self._convert(filename=filename, extension=extension, converter=self.converter)

    # endregion METHOD_test_convert_doc
    # region METHOD_test_convert_rtf [DOMAIN(7): Testing; CONCEPT(8): LDD_Telemetry; TECH(8): unittest]
    ## @purpose Verify: convert rtf.
    ## @complexity 5
    def test_convert_rtf(self) -> None:
        # LDD TELEMETRY: log execution context before assertions
        print(f"\n--- LDD TRAJECTORY (IMP:7-10) for TestDocxConverter::test_convert_rtf ---")
        print(f"  [LDD_TEST][IMP:8][TestDocxConverter][test_convert_rtf] Test logic executed, entering assertion phase")
        filename = "english_doc"
        extension = ".rtf"
        self._convert(filename=filename, extension=extension, converter=self.converter)

    # endregion METHOD_test_convert_rtf
# endregion CLASS_TestDocxConverter