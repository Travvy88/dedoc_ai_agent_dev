# region MODULE_CONTRACT [DOMAIN(7): Testing; CONCEPT(8): UnitTest, LDD_Telemetry; TECH(8): unittest, pytest]
## @modulecontract
## @purpose Verify ProcessHandler::handle() async CSV processing and FileNotFoundError handling.
## @scope Unit testing of dedoc module: misc, process, handler.
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
## CLASS 8[Unit tests] => TestProcessHandler
## @usecases
## - [Tests]: QA Agent (Verify) => RunTestsWithTelemetry => DiagnosticTrajectoryVisible
def _module_contract():
    pass
# endregion MODULE_CONTRACT
# GREP_SUMMARY: misc, process, handler, TestProcessHandler, test_handle_file, test_file_not_exists, unit_test, unittest, LDD_telemetry, semantic_markup, unit_test
# STRUCTURE: ▶ ┌ProcessHandler + test_data┐ → ◇ async handle(tsv) → ⊕ verify cells ⊕ metadata → ∑ assertions → ⎋ PASS/FAIL


import logging

logger = logging.getLogger(__name__)

import logging
import os
import tempfile
from unittest import IsolatedAsyncioTestCase

from dedoc.api.process_handler import ProcessHandler


# region CLASS_TestProcessHandler [DOMAIN(7): Testing; CONCEPT(8): UnitTest, LDD_Telemetry; TECH(8): unittest, pytest]
## @purpose Test suite for misc, process, handler module.
class TestProcessHandler(IsolatedAsyncioTestCase):
    path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "data", "csvs"))
    process_handler = ProcessHandler(logger=logging.getLogger())

    # region METHOD_test_handle_file [DOMAIN(7): Testing; CONCEPT(8): LDD_Telemetry; TECH(8): unittest]
    ## @purpose Verify: handle file.
    ## @complexity 5
    async def test_handle_file(self) -> None:
        # LDD TELEMETRY: log execution context before assertions
        print(f"\n--- LDD TRAJECTORY (IMP:7-10) for TestProcessHandler::test_handle_file ---")
        print(f"  [LDD_TEST][IMP:8][TestProcessHandler][test_handle_file] Test logic executed, entering assertion phase")
        filename = "csv_tab.tsv"
        with tempfile.TemporaryDirectory() as tmpdir:
            result = await self.process_handler.handle(None, {}, os.path.join(self.path, filename), tmpdir)
        cells = result.content.tables[0].cells
        self.assertEqual(filename, result.metadata.file_name)
        self.assertLessEqual(["1", "2", "3"], ["".join([line.text for line in cell.lines]) for cell in cells[0]])

    async def test_file_not_exists(self) -> None:
        with self.assertRaises(FileNotFoundError):
            with tempfile.TemporaryDirectory() as tmpdir:
                _ = await self.process_handler.handle(None, {}, "afagahcr", tmpdir)

    # endregion METHOD_test_handle_file
# endregion CLASS_TestProcessHandler