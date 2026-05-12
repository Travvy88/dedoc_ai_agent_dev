# region MODULE_CONTRACT [DOMAIN(7): Testing; CONCEPT(8): UnitTest, LDD_Telemetry; TECH(8): unittest, pytest]
## @modulecontract
## @purpose Unit tests for doctype law dynamic classifier module.
## @scope Unit testing of dedoc module: doctype, law, dynamic, classifier.
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
## CLASS 8[Unit tests] => TestFoivApiDocreader
## @usecases
## - [Tests]: QA Agent (Verify) => RunTestsWithTelemetry => DiagnosticTrajectoryVisible
def _module_contract():
    pass
# endregion MODULE_CONTRACT
# GREP_SUMMARY: doctype, law, dynamic, classifier, TestFoivApiDocreader, test_law, test_instruction, test_codex, test_definition, test_resolution, test_order, test_disposal, test_decree, test_fz, unit_test, unittest, LDD_telemetry, semantic_markup, unit_test
# STRUCTURE: ▶ Init → ◇ Execute → ⊕ Verify → ∑ assertions → ⎋ PASS/FAIL


import logging

logger = logging.getLogger(__name__)

import os
import unittest

from dedoc.readers.txt_reader.raw_text_reader import RawTextReader
from dedoc.structure_extractors.concrete_structure_extractors.classifying_law_structure_extractor import ClassifyingLawStructureExtractor
from dedoc.structure_extractors.concrete_structure_extractors.foiv_law_structure_extractor import FoivLawStructureExtractor
from dedoc.structure_extractors.concrete_structure_extractors.law_structure_excractor import LawStructureExtractor


# region CLASS_TestFoivApiDocreader [DOMAIN(7): Testing; CONCEPT(8): UnitTest, LDD_Telemetry; TECH(8): unittest, pytest]
## @purpose Test suite for doctype, law, dynamic, classifier module.
class TestFoivApiDocreader(unittest.TestCase):
    data_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "data", "laws"))
    law_extractors = {
        FoivLawStructureExtractor.document_type: FoivLawStructureExtractor(config={}),
        LawStructureExtractor.document_type: LawStructureExtractor(config={})
    }
    structure_extractor = ClassifyingLawStructureExtractor(extractors=law_extractors, config={})

    # region METHOD__get_abs_path [DOMAIN(7): Testing; CONCEPT(8): TestInfrastructure; TECH(8): unittest]
    ## @purpose get abs path.
    def _get_abs_path(self, file_name: str) -> str:
        return os.path.join(self.data_path, "doctypes", file_name)

    # endregion METHOD__get_abs_path
    # region METHOD__test_document_type [DOMAIN(7): Testing; CONCEPT(8): TestInfrastructure; TECH(8): unittest]
    ## @purpose test document type.
    def _test_document_type(self, file_name: str, expected_type: str) -> None:
        config = {}
        base_reader = RawTextReader(config=config)
        unstructured_document = base_reader.read(file_path=self._get_abs_path(file_name), parameters=None)
        result = self.structure_extractor._predict_extractor(unstructured_document.lines)

        self.assertEqual(result.document_type, expected_type)

    # endregion METHOD__test_document_type
    # region METHOD_test_law [DOMAIN(7): Testing; CONCEPT(8): LDD_Telemetry; TECH(8): unittest]
    ## @purpose Verify: law.
    ## @complexity 5
    def test_law(self) -> None:
        # LDD TELEMETRY: log execution context before assertions
        print(f"\n--- LDD TRAJECTORY (IMP:7-10) for TestFoivApiDocreader::test_law ---")
        print(f"  [LDD_TEST][IMP:8][TestFoivApiDocreader][test_law] Test logic executed, entering assertion phase")
        file_name = "закон.txt"
        expected_type = "law"
        self._test_document_type(file_name, expected_type)

    # endregion METHOD_test_law
    # region METHOD_test_instruction [DOMAIN(7): Testing; CONCEPT(8): LDD_Telemetry; TECH(8): unittest]
    ## @purpose Verify: instruction.
    ## @complexity 5
    def test_instruction(self) -> None:
        # LDD TELEMETRY: log execution context before assertions
        print(f"\n--- LDD TRAJECTORY (IMP:7-10) for TestFoivApiDocreader::test_instruction ---")
        print(f"  [LDD_TEST][IMP:8][TestFoivApiDocreader][test_instruction] Test logic executed, entering assertion phase")
        file_name = "инструкция.txt"
        expected_type = "foiv_law"
        self._test_document_type(file_name, expected_type)

    # endregion METHOD_test_instruction
    # region METHOD_test_codex [DOMAIN(7): Testing; CONCEPT(8): LDD_Telemetry; TECH(8): unittest]
    ## @purpose Verify: codex.
    ## @complexity 5
    def test_codex(self) -> None:
        # LDD TELEMETRY: log execution context before assertions
        print(f"\n--- LDD TRAJECTORY (IMP:7-10) for TestFoivApiDocreader::test_codex ---")
        print(f"  [LDD_TEST][IMP:8][TestFoivApiDocreader][test_codex] Test logic executed, entering assertion phase")
        file_name = "кодекс.txt"
        expected_type = "law"
        self._test_document_type(file_name, expected_type)

    # endregion METHOD_test_codex
    # region METHOD_test_definition [DOMAIN(7): Testing; CONCEPT(8): LDD_Telemetry; TECH(8): unittest]
    ## @purpose Verify: definition.
    ## @complexity 5
    def test_definition(self) -> None:
        # LDD TELEMETRY: log execution context before assertions
        print(f"\n--- LDD TRAJECTORY (IMP:7-10) for TestFoivApiDocreader::test_definition ---")
        print(f"  [LDD_TEST][IMP:8][TestFoivApiDocreader][test_definition] Test logic executed, entering assertion phase")
        file_name = "определение.txt"
        expected_type = "law"
        self._test_document_type(file_name, expected_type)

    # endregion METHOD_test_definition
    # region METHOD_test_resolution [DOMAIN(7): Testing; CONCEPT(8): LDD_Telemetry; TECH(8): unittest]
    ## @purpose Verify: resolution.
    ## @complexity 5
    def test_resolution(self) -> None:
        # LDD TELEMETRY: log execution context before assertions
        print(f"\n--- LDD TRAJECTORY (IMP:7-10) for TestFoivApiDocreader::test_resolution ---")
        print(f"  [LDD_TEST][IMP:8][TestFoivApiDocreader][test_resolution] Test logic executed, entering assertion phase")
        file_name = "постановление.txt"
        expected_type = "law"
        self._test_document_type(file_name, expected_type)

    # endregion METHOD_test_resolution
    # region METHOD_test_order [DOMAIN(7): Testing; CONCEPT(8): LDD_Telemetry; TECH(8): unittest]
    ## @purpose Verify: order.
    ## @complexity 5
    def test_order(self) -> None:
        # LDD TELEMETRY: log execution context before assertions
        print(f"\n--- LDD TRAJECTORY (IMP:7-10) for TestFoivApiDocreader::test_order ---")
        print(f"  [LDD_TEST][IMP:8][TestFoivApiDocreader][test_order] Test logic executed, entering assertion phase")
        file_name = "приказ.txt"
        expected_type = "foiv_law"
        self._test_document_type(file_name, expected_type)

    # endregion METHOD_test_order
    # region METHOD_test_disposal [DOMAIN(7): Testing; CONCEPT(8): LDD_Telemetry; TECH(8): unittest]
    ## @purpose Verify: disposal.
    ## @complexity 5
    def test_disposal(self) -> None:
        # LDD TELEMETRY: log execution context before assertions
        print(f"\n--- LDD TRAJECTORY (IMP:7-10) for TestFoivApiDocreader::test_disposal ---")
        print(f"  [LDD_TEST][IMP:8][TestFoivApiDocreader][test_disposal] Test logic executed, entering assertion phase")
        file_name = "распоряжение.txt"
        expected_type = "law"
        self._test_document_type(file_name, expected_type)

    # endregion METHOD_test_disposal
    # region METHOD_test_decree [DOMAIN(7): Testing; CONCEPT(8): LDD_Telemetry; TECH(8): unittest]
    ## @purpose Verify: decree.
    ## @complexity 5
    def test_decree(self) -> None:
        # LDD TELEMETRY: log execution context before assertions
        print(f"\n--- LDD TRAJECTORY (IMP:7-10) for TestFoivApiDocreader::test_decree ---")
        print(f"  [LDD_TEST][IMP:8][TestFoivApiDocreader][test_decree] Test logic executed, entering assertion phase")
        file_name = "указ.txt"
        expected_type = "law"
        self._test_document_type(file_name, expected_type)

    # endregion METHOD_test_decree
    # region METHOD_test_fz [DOMAIN(7): Testing; CONCEPT(8): LDD_Telemetry; TECH(8): unittest]
    ## @purpose Verify: fz.
    ## @complexity 5
    def test_fz(self) -> None:
        # LDD TELEMETRY: log execution context before assertions
        print(f"\n--- LDD TRAJECTORY (IMP:7-10) for TestFoivApiDocreader::test_fz ---")
        print(f"  [LDD_TEST][IMP:8][TestFoivApiDocreader][test_fz] Test logic executed, entering assertion phase")
        file_name = "федеральный_закон.txt"
        expected_type = "law"
        self._test_document_type(file_name, expected_type)

    # endregion METHOD_test_fz
# endregion CLASS_TestFoivApiDocreader