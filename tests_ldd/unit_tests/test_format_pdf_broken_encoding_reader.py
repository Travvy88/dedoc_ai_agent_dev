# region MODULE_CONTRACT [DOMAIN(7): Testing; CONCEPT(8): UnitTest, LDD_Telemetry; TECH(8): unittest, pytest]
## @modulecontract
## @purpose Unit tests for format pdf broken encoding reader module.
## @scope Unit testing of dedoc module: format, pdf, broken, encoding, reader.
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
## CLASS 8[Unit tests] => TestPdfBrokenEncodingReader
## @usecases
## - [Tests]: QA Agent (Verify) => RunTestsWithTelemetry => DiagnosticTrajectoryVisible
def _module_contract():
    pass
# endregion MODULE_CONTRACT
# GREP_SUMMARY: format, pdf, broken, encoding, reader, TestPdfBrokenEncodingReader, test_pdf_broken_encoding, unit_test, unittest, LDD_telemetry, semantic_markup, unit_test
# STRUCTURE: ▶ Init → ◇ Execute → ⊕ Verify → ∑ assertions → ⎋ PASS/FAIL


import logging

logger = logging.getLogger(__name__)

import os
import unittest

import Levenshtein

from dedoc.readers.pdf_reader.pdf_txtlayer_reader.pdf_broken_encoding_reader import PdfBrokenEncodingReader


# region CLASS_TestPdfBrokenEncodingReader [DOMAIN(7): Testing; CONCEPT(8): UnitTest, LDD_Telemetry; TECH(8): unittest, pytest]
## @purpose Test suite for format, pdf, broken, encoding, reader module.
class TestPdfBrokenEncodingReader(unittest.TestCase):
    # region METHOD_test_pdf_broken_encoding [DOMAIN(7): Testing; CONCEPT(8): LDD_Telemetry; TECH(8): unittest]
    ## @purpose Verify: pdf broken encoding.
    ## @complexity 5
    def test_pdf_broken_encoding(self) -> None:
        # LDD TELEMETRY: log execution context before assertions
        print(f"\n--- LDD TRAJECTORY (IMP:7-10) for TestPdfBrokenEncodingReader::test_pdf_broken_encoding ---")
        print(f"  [LDD_TEST][IMP:8][TestPdfBrokenEncodingReader][test_pdf_broken_encoding] Test logic executed, entering assertion phase")
        pdf_path = os.path.join(os.path.dirname(__file__), "..", "data", "pdf_with_text_layer", "mongolo.pdf")
        orig_path = os.path.join(os.path.dirname(__file__), "..", "data", "txt", "mongolo.txt")
        reader = PdfBrokenEncodingReader()
        result = reader.read(file_path=pdf_path)
        lines = "".join([i.line for i in result.lines[0:10]])
        with open(orig_path, encoding="utf8", mode="r") as txt:
            accuracy = Levenshtein.ratio(txt.read(), lines)
            self.assertTrue(accuracy > 0.7)

    # endregion METHOD_test_pdf_broken_encoding
# endregion CLASS_TestPdfBrokenEncodingReader