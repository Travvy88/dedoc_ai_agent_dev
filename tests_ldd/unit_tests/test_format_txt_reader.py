# region MODULE_CONTRACT [DOMAIN(7): Testing; CONCEPT(8): UnitTest, LDD_Telemetry; TECH(8): unittest, pytest]
## @modulecontract
## @purpose Unit tests for format txt reader module.
## @scope Unit testing of dedoc module: format, txt, reader.
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
## CLASS 8[Unit tests] => TestRawTextReader
## @usecases
## - [Tests]: QA Agent (Verify) => RunTestsWithTelemetry => DiagnosticTrajectoryVisible
def _module_contract():
    pass
# endregion MODULE_CONTRACT
# GREP_SUMMARY: format, txt, reader, TestRawTextReader, test_read_law, test_read_tz, test_get_lines_with_meta, unit_test, unittest, LDD_telemetry, semantic_markup, unit_test
# STRUCTURE: ▶ Init → ◇ Execute → ⊕ Verify → ∑ assertions → ⎋ PASS/FAIL


import logging

logger = logging.getLogger(__name__)

import os
from unittest import TestCase

from dedoc.config import get_config
from dedoc.readers.txt_reader.raw_text_reader import RawTextReader
from tests.test_utils import get_test_config


# region CLASS_TestRawTextReader [DOMAIN(7): Testing; CONCEPT(8): UnitTest, LDD_Telemetry; TECH(8): unittest, pytest]
## @purpose Test suite for format, txt, reader module.
class TestRawTextReader(TestCase):
    config = get_test_config()
    reader = RawTextReader(config=config)
    path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "data"))

    # region METHOD_test_read_law [DOMAIN(7): Testing; CONCEPT(8): LDD_Telemetry; TECH(8): unittest]
    ## @purpose Verify: read law.
    ## @complexity 5
    def test_read_law(self) -> None:
        # LDD TELEMETRY: log execution context before assertions
        print(f"\n--- LDD TRAJECTORY (IMP:7-10) for TestRawTextReader::test_read_law ---")
        print(f"  [LDD_TEST][IMP:8][TestRawTextReader][test_read_law] Test logic executed, entering assertion phase")
        file = os.path.join(self.path, "laws", "коап_москвы_8_7_2015_utf.txt")
        uids_set = set()
        prefix = "txt_6210f1fb59150aae33a09f49c8724baf"  # это строка, содержащая хэш файла, который обратаывается ридером
        document = self.reader.read(file, {})
        for line in document.lines:
            self.assertNotIn(line.uid, uids_set)
            uids_set.add(line.uid)
            self.assertEqual(prefix, line.uid[:len(prefix)])  # в поле uid содержится хэш файла, в котором находитс строка, и id самой строки

    # endregion METHOD_test_read_law
    # region METHOD_test_read_tz [DOMAIN(7): Testing; CONCEPT(8): LDD_Telemetry; TECH(8): unittest]
    ## @purpose Verify: read tz.
    ## @complexity 5
    def test_read_tz(self) -> None:
        # LDD TELEMETRY: log execution context before assertions
        print(f"\n--- LDD TRAJECTORY (IMP:7-10) for TestRawTextReader::test_read_tz ---")
        print(f"  [LDD_TEST][IMP:8][TestRawTextReader][test_read_tz] Test logic executed, entering assertion phase")
        file = os.path.join(self.path, "tz", "tz.txt")
        uids_set = set()
        prefix = "txt_0e576a9e0008225ac27f961af60c0bee"
        document = self.reader.read(file, {})
        for line in document.lines:
            self.assertNotIn(line.uid, uids_set)
            uids_set.add(line.uid)
            self.assertEqual(prefix, line.uid[:len(prefix)])

    # endregion METHOD_test_read_tz
    # region METHOD_test_get_lines_with_meta [DOMAIN(7): Testing; CONCEPT(8): LDD_Telemetry; TECH(8): unittest]
    ## @purpose Verify: get lines with meta.
    ## @complexity 5
    def test_get_lines_with_meta(self) -> None:
        # LDD TELEMETRY: log execution context before assertions
        print(f"\n--- LDD TRAJECTORY (IMP:7-10) for TestRawTextReader::test_get_lines_with_meta ---")
        print(f"  [LDD_TEST][IMP:8][TestRawTextReader][test_get_lines_with_meta] Test logic executed, entering assertion phase")
        file = os.path.join(self.path, "txt", "pr_17.txt")
        reader = RawTextReader(config=get_config())
        for line in reader._get_lines_with_meta(path=file, encoding="utf-8"):
            expected_uid = f"txt_1a3cd561910506d56a65db1d1dcb5049_{line.metadata.line_id}"
            self.assertEqual(expected_uid, line.uid)

    # endregion METHOD_test_get_lines_with_meta
# endregion CLASS_TestRawTextReader