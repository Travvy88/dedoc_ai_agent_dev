# region MODULE_CONTRACT [DOMAIN(7): Testing; CONCEPT(8): UnitTest, LDD_Telemetry; TECH(8): unittest, pytest]
## @modulecontract
## @purpose Base class for converter tests. Provides _convert() helper: copies file to tmpdir, runs converter, validates output exists.
## @scope Unit testing of dedoc module: abstract, converter, test.
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
## CLASS 8[Unit tests] => AbstractConverterTest
## @usecases
## - [Tests]: QA Agent (Verify) => RunTestsWithTelemetry => DiagnosticTrajectoryVisible
def _module_contract():
    pass
# endregion MODULE_CONTRACT
# GREP_SUMMARY: abstract, converter, test, AbstractConverterTest, unit_test, unittest, LDD_telemetry, semantic_markup, unit_test
# STRUCTURE: ▶ setUp(tmpdir) → ⊙ _convert(file, ext, converter) ┌copy → convert → assert exists┐ → ⎋ PASS/FAIL


import logging

logger = logging.getLogger(__name__)

import os
import shutil
from tempfile import TemporaryDirectory
from unittest import TestCase

from dedoc.converters.concrete_converters.abstract_converter import AbstractConverter


# region CLASS_AbstractConverterTest [DOMAIN(7): Testing; CONCEPT(8): UnitTest, LDD_Telemetry; TECH(8): unittest, pytest]
## @purpose Test suite for abstract, converter, test module.
class AbstractConverterTest(TestCase):
    path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "data"))

    # region METHOD_setUp [DOMAIN(7): Testing; CONCEPT(8): TestInfrastructure; TECH(8): unittest]
    ## @purpose setUp.
    def setUp(self) -> None:
        """
        Method that runs before AbstractConverterTest testing
        """
        super().setUp()
        self.tmp_dir = TemporaryDirectory()

    # endregion METHOD_setUp
    # region METHOD_tearDown [DOMAIN(7): Testing; CONCEPT(8): TestInfrastructure; TECH(8): unittest]
    ## @purpose tearDown.
    def tearDown(self) -> None:
        """
        Method that runs after AbstractConverterTest testing
        """
        super().tearDown()
        self.tmp_dir.cleanup()

    # endregion METHOD_tearDown
    # region METHOD__convert [DOMAIN(7): Testing; CONCEPT(8): LDD_Telemetry; TECH(8): unittest]
    ## @purpose Helper: copy file to tmpdir, run converter, validate output exists.
    ## @complexity 5
    def _convert(self, filename: str, extension: str, converter: AbstractConverter) -> None:
        # LDD TELEMETRY: log execution context before assertions
        print(f"\n--- LDD TRAJECTORY (IMP:7-10) for AbstractConverterTest::_convert ---")
        print(f"  [LDD_TEST][IMP:8][AbstractConverterTest][_convert] filename={filename}{extension}, converter={converter.__class__.__name__}")
        filename_with_extension = filename + extension
        file = os.path.join(self.path, filename_with_extension)
        tmp_file = os.path.join(self.tmp_dir.name, filename_with_extension)
        self.assertTrue(os.path.isfile(file), f"no such file {file}")
        shutil.copy(file, tmp_file)
        result = converter.convert(file_path=tmp_file)
        self.assertTrue(os.path.isfile(result), f"no such file {result}")

    # endregion METHOD__convert
# endregion CLASS_AbstractConverterTest