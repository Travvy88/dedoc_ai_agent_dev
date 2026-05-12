# region MODULE_CONTRACT [DOMAIN(7): Testing; CONCEPT(8): UnitTest, LDD_Telemetry; TECH(8): unittest, pytest]
## @modulecontract
## @purpose Verify DedocManager::parse() returns correct ParsedDocument and handles missing files.
## @scope Unit testing of dedoc module: misc, dedoc, manager.
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
## CLASS 8[Unit tests] => TestDedocManager
## @usecases
## - [Tests]: QA Agent (Verify) => RunTestsWithTelemetry => DiagnosticTrajectoryVisible
def _module_contract():
    pass
# endregion MODULE_CONTRACT
# GREP_SUMMARY: misc, dedoc, manager, TestDedocManager, test_parse_file, test_file_not_exists, unit_test, unittest, LDD_telemetry, semantic_markup, unit_test
# STRUCTURE: ▶ ┌config + manager_config┐ → ○ Init DedocManager → ◇ parse(tsv) → ⊕ verify cells ⊕ metadata → ∑ assertions → ⎋ PASS/FAIL


import logging

logger = logging.getLogger(__name__)

import os
from unittest import TestCase

from dedoc.config import get_config
from dedoc.dedoc_manager import DedocManager
from dedoc.manager_config import get_manager_config


# region CLASS_TestDedocManager [DOMAIN(7): Testing; CONCEPT(8): UnitTest, LDD_Telemetry; TECH(8): unittest, pytest]
## @purpose Test suite for misc, dedoc, manager module.
class TestDedocManager(TestCase):
    path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "data", "csvs"))
    config = get_config()
    manager_config = get_manager_config(config=config)
    dedoc_manager = DedocManager(manager_config=manager_config, config=config)

    # region METHOD_test_parse_file [DOMAIN(7): Testing; CONCEPT(8): LDD_Telemetry; TECH(8): unittest]
    ## @purpose Verify: parse file.
    ## @complexity 5
    def test_parse_file(self) -> None:
        # LDD TELEMETRY: log execution context before assertions
        print(f"\n--- LDD TRAJECTORY (IMP:7-10) for TestDedocManager::test_parse_file ---")
        print(f"  [LDD_TEST][IMP:8][TestDedocManager][test_parse_file] Test logic executed, entering assertion phase")
        filename = "csv_tab.tsv"
        result = self.dedoc_manager.parse(os.path.join(self.path, filename))
        cells = result.content.tables[0].cells
        self.assertEqual(filename, result.metadata.file_name)
        self.assertLessEqual(["1", "2", "3"], [cell.get_text() for cell in cells[0]])
        self.assertLessEqual(["2", "1", "5"], [cell.get_text() for cell in cells[1]])
        self.assertLessEqual(["5", "3", "1"], [cell.get_text() for cell in cells[2]])

    # endregion METHOD_test_parse_file
    # region METHOD_test_file_not_exists [DOMAIN(7): Testing; CONCEPT(8): LDD_Telemetry; TECH(8): unittest]
    ## @purpose Verify: file not exists.
    ## @complexity 5
    def test_file_not_exists(self) -> None:
        # LDD TELEMETRY: log execution context before assertions
        print(f"\n--- LDD TRAJECTORY (IMP:7-10) for TestDedocManager::test_file_not_exists ---")
        print(f"  [LDD_TEST][IMP:8][TestDedocManager][test_file_not_exists] Test logic executed, entering assertion phase")
        with self.assertRaises(FileNotFoundError):
            self.dedoc_manager.parse("afagahcr")

    # endregion METHOD_test_file_not_exists
# endregion CLASS_TestDedocManager