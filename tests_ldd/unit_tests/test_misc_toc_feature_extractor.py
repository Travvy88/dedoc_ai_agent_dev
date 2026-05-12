# region MODULE_CONTRACT [DOMAIN(7): Testing; CONCEPT(8): UnitTest, LDD_Telemetry; TECH(8): unittest, pytest]
## @modulecontract
## @purpose Unit tests for misc toc feature extractor module.
## @scope Unit testing of dedoc module: misc, toc, feature, extractor.
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
## CLASS 8[Unit tests] => TestTOCFeatureExtractor
## @usecases
## - [Tests]: QA Agent (Verify) => RunTestsWithTelemetry => DiagnosticTrajectoryVisible
def _module_contract():
    pass
# endregion MODULE_CONTRACT
# GREP_SUMMARY: misc, toc, feature, extractor, TestTOCFeatureExtractor, test_toc_extractor, test_end_with_num, unit_test, unittest, LDD_telemetry, semantic_markup, unit_test
# STRUCTURE: ▶ Init → ◇ Execute → ⊕ Verify → ∑ assertions → ⎋ PASS/FAIL


import logging

logger = logging.getLogger(__name__)

import os
import unittest

from dedoc.data_structures.unstructured_document import UnstructuredDocument
from dedoc.readers.docx_reader.docx_reader import DocxReader
from dedoc.structure_extractors.feature_extractors.toc_feature_extractor import TOCFeatureExtractor
from tests.test_utils import get_test_config


# region CLASS_TestTOCFeatureExtractor [DOMAIN(7): Testing; CONCEPT(8): UnitTest, LDD_Telemetry; TECH(8): unittest, pytest]
## @purpose Test suite for misc, toc, feature, extractor module.
class TestTOCFeatureExtractor(unittest.TestCase):
    feature_extractor = TOCFeatureExtractor()
    reader = DocxReader(config=get_test_config())
    data_path = os.path.join(os.path.dirname(__file__), "..", "data", "tz")
    data_path = os.path.abspath(data_path)

    path = os.path.join(data_path, "tz-10ea-2020.docx")
    _document = None

    @property
    # region METHOD_document [DOMAIN(7): Testing; CONCEPT(8): TestInfrastructure; TECH(8): unittest]
    ## @purpose document.
    def document(self) -> UnstructuredDocument:
        if self._document is None:
            self._document = self.reader.read(file_path=self.path, parameters={})
        return self._document

    # endregion METHOD_document
    # region METHOD_test_toc_extractor [DOMAIN(7): Testing; CONCEPT(8): LDD_Telemetry; TECH(8): unittest]
    ## @purpose Verify: toc extractor.
    ## @complexity 5
    def test_toc_extractor(self) -> None:
        # LDD TELEMETRY: log execution context before assertions
        print(f"\n--- LDD TRAJECTORY (IMP:7-10) for TestTOCFeatureExtractor::test_toc_extractor ---")
        print(f"  [LDD_TEST][IMP:8][TestTOCFeatureExtractor][test_toc_extractor] Test logic executed, entering assertion phase")
        toc = self.feature_extractor.get_toc(document=self.document.lines)
        self.assertIn("5", str(toc[0].page))
        self.assertEqual("1.\xa0\xa0\xa0\xa0\xa0Общие сведения	5", toc[0].line.line.strip())
        self.assertIn("5", str(toc[1].page))
        self.assertEqual("1.1.\xa0Основание для выполнения	5", toc[1].line.line.strip())
        self.assertIn("6", str(toc[2].page))
        self.assertEqual("1.2.\xa0Наименование услуг	6", toc[2].line.line.strip())

        self.assertIn("26", str(toc[13].page))
        self.assertEqual("4.2.\xa0Требования к оказанию услуг по обследованию подсистем ИВС Росстата, разработке "
                         "актов классификации, моделей угроз и нарушителя безопасности информации	26",
                         toc[13].line.line.strip())

        self.assertIn("40", str(toc[26].page))
        self.assertEqual("9.\xa0Перечень материалов, передаваемых Заказчику	40", toc[26].line.line.strip())

        self.assertEqual(27, len(toc))

    # endregion METHOD_test_toc_extractor
    # region METHOD_test_end_with_num [DOMAIN(7): Testing; CONCEPT(8): LDD_Telemetry; TECH(8): unittest]
    ## @purpose Verify: end with num.
    ## @complexity 5
    def test_end_with_num(self) -> None:
        # LDD TELEMETRY: log execution context before assertions
        print(f"\n--- LDD TRAJECTORY (IMP:7-10) for TestTOCFeatureExtractor::test_end_with_num ---")
        print(f"  [LDD_TEST][IMP:8][TestTOCFeatureExtractor][test_end_with_num] Test logic executed, entering assertion phase")
        self.assertTrue(self.feature_extractor.end_with_num.match("Как кормить альпака       1"))
        self.assertTrue(self.feature_extractor.end_with_num.match("Как поить альпака.........2"))
        self.assertFalse(self.feature_extractor.end_with_num.match("Как поймать альпака"))

    # endregion METHOD_test_end_with_num
# endregion CLASS_TestTOCFeatureExtractor