# region MODULE_CONTRACT [DOMAIN(7): Testing; CONCEPT(8): UnitTest, LDD_Telemetry; TECH(8): unittest, pytest]
## @modulecontract
## @purpose Unit tests for doctype law text features regexps module.
## @scope Unit testing of dedoc module: doctype, law, text, features, regexps.
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
## CLASS 8[Unit tests] => TestLawTextFeaturesRegexps
## @usecases
## - [Tests]: QA Agent (Verify) => RunTestsWithTelemetry => DiagnosticTrajectoryVisible
def _module_contract():
    pass
# endregion MODULE_CONTRACT
# GREP_SUMMARY: doctype, law, text, features, regexps, TestLawTextFeaturesRegexps, test_roman_regexp, test_application_beginnings_with_regexp, test_chapter_beginnings, unit_test, unittest, LDD_telemetry, semantic_markup, unit_test
# STRUCTURE: ▶ Init → ◇ Execute → ⊕ Verify → ∑ assertions → ⎋ PASS/FAIL


import logging

logger = logging.getLogger(__name__)

import unittest

from dedoc.structure_extractors.feature_extractors.law_text_features import LawTextFeatures
from dedoc.structure_extractors.hierarchy_level_builders.utils_reg import roman_regexp


# region CLASS_TestLawTextFeaturesRegexps [DOMAIN(7): Testing; CONCEPT(8): UnitTest, LDD_Telemetry; TECH(8): unittest, pytest]
## @purpose Test suite for doctype, law, text, features, regexps module.
class TestLawTextFeaturesRegexps(unittest.TestCase):
    features = LawTextFeatures()

    # region METHOD_test_roman_regexp [DOMAIN(7): Testing; CONCEPT(8): LDD_Telemetry; TECH(8): unittest]
    ## @purpose Verify: roman regexp.
    ## @complexity 5
    def test_roman_regexp(self) -> None:
        # LDD TELEMETRY: log execution context before assertions
        print(f"\n--- LDD TRAJECTORY (IMP:7-10) for TestLawTextFeaturesRegexps::test_roman_regexp ---")
        print(f"  [LDD_TEST][IMP:8][TestLawTextFeaturesRegexps][test_roman_regexp] Test logic executed, entering assertion phase")
        self.assertTrue(roman_regexp.fullmatch("    XI. "))
        self.assertTrue(roman_regexp.fullmatch("      ") is None)
        self.assertTrue(roman_regexp.fullmatch("    XI.") is None)
        self.assertTrue(roman_regexp.fullmatch("\tIII. "))

    # endregion METHOD_test_roman_regexp
    # region METHOD_test_application_beginnings_with_regexp [DOMAIN(7): Testing; CONCEPT(8): LDD_Telemetry; TECH(8): unittest]
    ## @purpose Verify: application beginnings with regexp.
    ## @complexity 5
    def test_application_beginnings_with_regexp(self) -> None:
        # LDD TELEMETRY: log execution context before assertions
        print(f"\n--- LDD TRAJECTORY (IMP:7-10) for TestLawTextFeaturesRegexps::test_application_beginnings_with_regexp ---")
        print(f"  [LDD_TEST][IMP:8][TestLawTextFeaturesRegexps][test_application_beginnings_with_regexp] Test logic executed, entering assertion phase")
        self.assertTrue(self.features.regexp_application_begin.fullmatch("приложение"))
        self.assertTrue(self.features.regexp_application_begin.fullmatch("Приложение"))
        self.assertTrue(self.features.regexp_application_begin.fullmatch("утверждены"))
        self.assertTrue(self.features.regexp_application_begin.fullmatch("приложение к приказу"))
        self.assertTrue(self.features.regexp_application_begin.fullmatch("приложение к постановлению"))
        self.assertTrue(self.features.regexp_application_begin.fullmatch("постановление") is None)
        self.assertTrue(self.features.regexp_application_begin.fullmatch("к приказу") is None)

    # endregion METHOD_test_application_beginnings_with_regexp
    # region METHOD_test_chapter_beginnings [DOMAIN(7): Testing; CONCEPT(8): LDD_Telemetry; TECH(8): unittest]
    ## @purpose Verify: chapter beginnings.
    ## @complexity 5
    def test_chapter_beginnings(self) -> None:
        # LDD TELEMETRY: log execution context before assertions
        print(f"\n--- LDD TRAJECTORY (IMP:7-10) for TestLawTextFeaturesRegexps::test_chapter_beginnings ---")
        print(f"  [LDD_TEST][IMP:8][TestLawTextFeaturesRegexps][test_chapter_beginnings] Test logic executed, entering assertion phase")
        # note to rewrites this test if we change the num of regexps
        self.assertEqual(1, len(LawTextFeatures.named_regexp))

        regexp = LawTextFeatures.named_regexp[0]

        lines = [
            "глава v. международное сотрудничество российской\n",
            "глава vi. ответственность за нарушение\n",
            "глава 17. вступление в силу настоящего федерального закона\n",
            "глава 1. общие положения\n",
            "глава 9. финансирование в области\n",
            "глава 10. заключительные и переходные положения\n",
            "глава 7. государственное регулирование внешнеторговой\n",
            "глава 8. особые виды |\n",
            "глава 2. принципы и условия обработки персональных данных\n"
        ]
        for line in lines:
            self.assertTrue(regexp.match(line), f"doesn't match on\n ''{line}''")

    # endregion METHOD_test_chapter_beginnings
# endregion CLASS_TestLawTextFeaturesRegexps