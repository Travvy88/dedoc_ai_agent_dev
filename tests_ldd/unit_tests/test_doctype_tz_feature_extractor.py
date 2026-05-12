# region MODULE_CONTRACT [DOMAIN(7): Testing; CONCEPT(8): UnitTest, LDD_Telemetry; TECH(8): unittest, pytest]
## @modulecontract
## @purpose Unit tests for doctype tz feature extractor module.
## @scope Unit testing of dedoc module: doctype, tz, feature, extractor.
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
## CLASS 8[Unit tests] => TestTzTextFeatures
## @usecases
## - [Tests]: QA Agent (Verify) => RunTestsWithTelemetry => DiagnosticTrajectoryVisible
def _module_contract():
    pass
# endregion MODULE_CONTRACT
# GREP_SUMMARY: doctype, tz, feature, extractor, TestTzTextFeatures, test_extractor, test_start_regexp, test_end_regexp, test_named_item_regexp, unit_test, unittest, LDD_telemetry, semantic_markup, unit_test
# STRUCTURE: ▶ Init → ◇ Execute → ⊕ Verify → ∑ assertions → ⎋ PASS/FAIL


import logging

logger = logging.getLogger(__name__)

import os
from unittest import TestCase

from dedoc.readers.docx_reader.docx_reader import DocxReader
from dedoc.structure_extractors.feature_extractors.tz_feature_extractor import TzTextFeatures
from tests.test_utils import get_test_config


# region CLASS_TestTzTextFeatures [DOMAIN(7): Testing; CONCEPT(8): UnitTest, LDD_Telemetry; TECH(8): unittest, pytest]
## @purpose Test suite for doctype, tz, feature, extractor module.
class TestTzTextFeatures(TestCase):

    docx_reader = DocxReader(config=get_test_config())
    feature_extractor = TzTextFeatures()

    # region METHOD_test_extractor [DOMAIN(7): Testing; CONCEPT(8): LDD_Telemetry; TECH(8): unittest]
    ## @purpose Verify: extractor.
    ## @complexity 5
    def test_extractor(self) -> None:
        # LDD TELEMETRY: log execution context before assertions
        print(f"\n--- LDD TRAJECTORY (IMP:7-10) for TestTzTextFeatures::test_extractor ---")
        print(f"  [LDD_TEST][IMP:8][TestTzTextFeatures][test_extractor] Test logic executed, entering assertion phase")
        document_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "data", "docx", "english_doc.docx"))
        self.assertTrue(os.path.isfile(document_path))
        unstructured_document = self.docx_reader.read(document_path)
        lines = [unstructured_document.lines]
        matrix = self.feature_extractor.transform(lines)
        self.assertEqual(len(lines[0]), matrix.shape[0])
        self.assertTrue(matrix.shape[1] > 0)

    # endregion METHOD_test_extractor
    # region METHOD_test_start_regexp [DOMAIN(7): Testing; CONCEPT(8): LDD_Telemetry; TECH(8): unittest]
    ## @purpose Verify: start regexp.
    ## @complexity 5
    def test_start_regexp(self) -> None:
        # LDD TELEMETRY: log execution context before assertions
        print(f"\n--- LDD TRAJECTORY (IMP:7-10) for TestTzTextFeatures::test_start_regexp ---")
        print(f"  [LDD_TEST][IMP:8][TestTzTextFeatures][test_start_regexp] Test logic executed, entering assertion phase")
        line1 = "РАЗДЕЛ 4. РЕЗУЛЬТАТ ОКАЗАННЫХ УСЛУГ"
        self.assertEqual(2, self.__count_start(line1.lower()))
        line2 = "- протоколы аттестационных испытаний;"
        self.assertEqual(2, self.__count_start(line2))
        line3 = ". ГОСТРО 0043-003-2012 «Защита информации. Аттестация объектов"
        self.assertEqual(2, self.__count_start(line3))
        line4 = "3.2.1. Проектная и рабочая документация должны разрабатываться в"
        self.assertEqual(0, self.__count_start(line4))
        line5 = "1.	Наименование оказываемых услуг."
        self.assertEqual(0, self.__count_start(line5))

    # endregion METHOD_test_start_regexp
    # region METHOD___count_start [DOMAIN(7): Testing; CONCEPT(8): TestInfrastructure; TECH(8): unittest]
    ## @purpose count start.
    def __count_start(self, line: str) -> int:
        return sum([1 for _, i in self.feature_extractor._start_regexp(line, self.feature_extractor.list_item_regexp) if i > 0])

    # endregion METHOD___count_start
    # region METHOD_test_end_regexp [DOMAIN(7): Testing; CONCEPT(8): LDD_Telemetry; TECH(8): unittest]
    ## @purpose Verify: end regexp.
    ## @complexity 5
    def test_end_regexp(self) -> None:
        # LDD TELEMETRY: log execution context before assertions
        print(f"\n--- LDD TRAJECTORY (IMP:7-10) for TestTzTextFeatures::test_end_regexp ---")
        print(f"  [LDD_TEST][IMP:8][TestTzTextFeatures][test_end_regexp] Test logic executed, entering assertion phase")
        line1 = "Подраздел 3.2 Требования к качеству оказываемых услуг\t12"
        self.assertEqual(2, sum(self.feature_extractor._end_regexp(line1)))
        line2 = "Подраздел 3.2 Требования к качеству оказываемых услуг"
        self.assertEqual(0, sum(self.feature_extractor._end_regexp(line2)))

    # endregion METHOD_test_end_regexp
    # region METHOD_test_named_item_regexp [DOMAIN(7): Testing; CONCEPT(8): LDD_Telemetry; TECH(8): unittest]
    ## @purpose Verify: named item regexp.
    ## @complexity 5
    def test_named_item_regexp(self) -> None:
        # LDD TELEMETRY: log execution context before assertions
        print(f"\n--- LDD TRAJECTORY (IMP:7-10) for TestTzTextFeatures::test_named_item_regexp ---")
        print(f"  [LDD_TEST][IMP:8][TestTzTextFeatures][test_named_item_regexp] Test logic executed, entering assertion phase")
        self.assertTrue(self.feature_extractor.named_item_regexp.fullmatch("раздел"))
        self.assertTrue(self.feature_extractor.named_item_regexp.fullmatch("подраздел"))
        self.assertTrue(self.feature_extractor.named_item_regexp.fullmatch("подраздел           \t        "))
        self.assertTrue(self.feature_extractor.named_item_regexp.fullmatch("разделывать") is None)

    # endregion METHOD_test_named_item_regexp
# endregion CLASS_TestTzTextFeatures