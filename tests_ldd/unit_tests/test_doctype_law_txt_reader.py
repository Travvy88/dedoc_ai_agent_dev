# region MODULE_CONTRACT [DOMAIN(7): Testing; CONCEPT(8): UnitTest, LDD_Telemetry; TECH(8): unittest, pytest]
## @modulecontract
## @purpose Unit tests for doctype law txt reader module.
## @scope Unit testing of dedoc module: doctype, law, txt, reader.
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
## CLASS 8[Unit tests] => TestLawTxtReader
## @usecases
## - [Tests]: QA Agent (Verify) => RunTestsWithTelemetry => DiagnosticTrajectoryVisible
def _module_contract():
    pass
# endregion MODULE_CONTRACT
# GREP_SUMMARY: doctype, law, txt, reader, TestLawTxtReader, test_law_document_spaces_correctness, unit_test, unittest, LDD_telemetry, semantic_markup, unit_test
# STRUCTURE: ▶ Init → ◇ Execute → ⊕ Verify → ∑ assertions → ⎋ PASS/FAIL


import logging

logger = logging.getLogger(__name__)

import os

from dedoc.metadata_extractors.concrete_metadata_extractors.base_metadata_extractor import BaseMetadataExtractor
from dedoc.readers.txt_reader.raw_text_reader import RawTextReader
from dedoc.structure_extractors.concrete_structure_extractors.law_structure_excractor import LawStructureExtractor
from tests.api_tests.abstract_api_test import AbstractTestApiDocReader
from tests.test_utils import get_test_config


# region CLASS_TestLawTxtReader [DOMAIN(7): Testing; CONCEPT(8): UnitTest, LDD_Telemetry; TECH(8): unittest, pytest]
## @purpose Test suite for doctype, law, txt, reader module.
class TestLawTxtReader(AbstractTestApiDocReader):
    config = get_test_config()
    txt_reader = RawTextReader(config=config)
    metadata_extractor = BaseMetadataExtractor()
    law_extractor = LawStructureExtractor(config=config)

    # region METHOD__get_abs_path [DOMAIN(7): Testing; CONCEPT(8): TestInfrastructure; TECH(8): unittest]
    ## @purpose get abs path.
    def _get_abs_path(self, file_name: str) -> str:
        return os.path.join(self.data_directory_path, "laws", file_name)

    # endregion METHOD__get_abs_path
    # region METHOD_test_law_document_spaces_correctness [DOMAIN(7): Testing; CONCEPT(8): LDD_Telemetry; TECH(8): unittest]
    ## @purpose Verify: law document spaces correctness.
    ## @complexity 5
    def test_law_document_spaces_correctness(self) -> None:
        # LDD TELEMETRY: log execution context before assertions
        print(f"\n--- LDD TRAJECTORY (IMP:7-10) for TestLawTxtReader::test_law_document_spaces_correctness ---")
        print(f"  [LDD_TEST][IMP:8][TestLawTxtReader][test_law_document_spaces_correctness] Test logic executed, entering assertion phase")
        path = self._get_abs_path("коап_москвы_8_7_2015_utf.txt")
        document = self.txt_reader.read(file_path=path)
        document.metadata = self.metadata_extractor.extract(path)
        document = self.law_extractor.extract(document)

        self.assertListEqual([], document.attachments)
        self.assertListEqual([], document.tables)
        lines = document.lines
        self.assertEqual("\n", lines[0].line)
        self.assertEqual(0, lines[0].metadata.line_id)
        self.assertEqual("    \n", lines[1].line)
        self.assertEqual(1, lines[1].metadata.line_id)
        self.assertEqual("\n", lines[2].line)
        self.assertEqual(2, lines[2].metadata.line_id)
        self.assertEqual("   \n", lines[3].line)
        self.assertEqual(3, lines[3].metadata.line_id)
        self.assertEqual("ЗАКОН\n", lines[4].line)
        self.assertEqual(4, lines[4].metadata.line_id)

    # endregion METHOD_test_law_document_spaces_correctness
# endregion CLASS_TestLawTxtReader