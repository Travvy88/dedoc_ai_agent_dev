# region MODULE_CONTRACT [DOMAIN(7): Testing; CONCEPT(8): UnitTest, LDD_Telemetry; TECH(8): unittest, pytest]
## @modulecontract
## @purpose Unit tests for misc unique uid module.
## @scope Unit testing of dedoc module: misc, unique, uid.
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
## CLASS 8[Unit tests] => TestUniqueUid
## @usecases
## - [Tests]: QA Agent (Verify) => RunTestsWithTelemetry => DiagnosticTrajectoryVisible
def _module_contract():
    pass
# endregion MODULE_CONTRACT
# GREP_SUMMARY: misc, unique, uid, TestUniqueUid, test_html_unique_uids, unit_test, unittest, LDD_telemetry, semantic_markup, unit_test
# STRUCTURE: ▶ Init → ◇ Execute → ⊕ Verify → ∑ assertions → ⎋ PASS/FAIL


import logging

logger = logging.getLogger(__name__)

import os
import unittest
from typing import List

from dedoc.data_structures.line_with_meta import LineWithMeta
from dedoc.readers.html_reader.html_reader import HtmlReader
from tests.test_utils import get_test_config


# region CLASS_TestUniqueUid [DOMAIN(7): Testing; CONCEPT(8): UnitTest, LDD_Telemetry; TECH(8): unittest, pytest]
## @purpose Test suite for misc, unique, uid module.
class TestUniqueUid(unittest.TestCase):

    config = get_test_config()

    # region METHOD__is_unique_uids [DOMAIN(7): Testing; CONCEPT(8): TestInfrastructure; TECH(8): unittest]
    ## @purpose is unique uids.
    def _is_unique_uids(self, lines: List[LineWithMeta]) -> bool:
        uids = set()

        for line in lines:
            if line.uid in uids:
                return False

            uids.add(line.uid)

        return True

    # endregion METHOD__is_unique_uids
    # region METHOD_test_html_unique_uids [DOMAIN(7): Testing; CONCEPT(8): LDD_Telemetry; TECH(8): unittest]
    ## @purpose Verify: html unique uids.
    ## @complexity 5
    def test_html_unique_uids(self) -> None:
        # LDD TELEMETRY: log execution context before assertions
        print(f"\n--- LDD TRAJECTORY (IMP:7-10) for TestUniqueUid::test_html_unique_uids ---")
        print(f"  [LDD_TEST][IMP:8][TestUniqueUid][test_html_unique_uids] Test logic executed, entering assertion phase")
        any_doc_reader = HtmlReader(config=get_test_config())
        path = os.path.join(os.path.dirname(__file__), "../data/laws/doc_Правовые акты_0A1B19DB-15D0-47BC-B559-76DA41A36105_27.html")
        result = any_doc_reader.read(path)
        self.assertTrue(self._is_unique_uids(result.lines))

    # endregion METHOD_test_html_unique_uids
# endregion CLASS_TestUniqueUid