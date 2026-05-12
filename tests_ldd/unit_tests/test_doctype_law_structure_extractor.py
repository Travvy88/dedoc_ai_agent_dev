# region MODULE_CONTRACT [DOMAIN(7): Testing; CONCEPT(8): UnitTest, LDD_Telemetry; TECH(8): unittest, pytest]
## @modulecontract
## @purpose Unit tests for doctype law structure extractor module.
## @scope Unit testing of dedoc module: doctype, law, structure, extractor.
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
## CLASS 8[Unit tests] => TestLawStructureExtractor
## @usecases
## - [Tests]: QA Agent (Verify) => RunTestsWithTelemetry => DiagnosticTrajectoryVisible
def _module_contract():
    pass
# endregion MODULE_CONTRACT
# GREP_SUMMARY: doctype, law, structure, extractor, TestLawStructureExtractor, test_item, test_subitem, test_article_part, test_begin_application, test_string_number_correctness_with_regexp, test_number_ends, test_postprocessing_of_strings_with_roman_numerals, test_empty_document, test_fix_labels, unit_test, unittest, LDD_telemetry, semantic_markup, unit_test
# STRUCTURE: ▶ Init → ◇ Execute → ⊕ Verify → ∑ assertions → ⎋ PASS/FAIL


import logging

logger = logging.getLogger(__name__)

import random
import time
import unittest
from collections import defaultdict
from typing import List

from dedoc.data_structures.hierarchy_level import HierarchyLevel
from dedoc.data_structures.line_metadata import LineMetadata
from dedoc.data_structures.line_with_meta import LineWithMeta
from dedoc.structure_extractors.concrete_structure_extractors.law_structure_excractor import LawStructureExtractor
from dedoc.structure_extractors.hierarchy_level_builders.law_builders.body_builder.body_law_hierarchy_level_builder import BodyLawHierarchyLevelBuilder
from dedoc.structure_extractors.hierarchy_level_builders.utils_reg import regexps_ends_of_number
from tests.test_utils import TestTimeout, get_test_config


# region CLASS_TestLawStructureExtractor [DOMAIN(7): Testing; CONCEPT(8): UnitTest, LDD_Telemetry; TECH(8): unittest, pytest]
## @purpose Test suite for doctype, law, structure, extractor module.
class TestLawStructureExtractor(unittest.TestCase):

    structure_extractor = LawStructureExtractor(config=get_test_config())
    body_builder = BodyLawHierarchyLevelBuilder()
    depth = 2

    # region METHOD_test_item [DOMAIN(7): Testing; CONCEPT(8): LDD_Telemetry; TECH(8): unittest]
    ## @purpose Verify: item.
    ## @complexity 5
    def test_item(self) -> None:
        # LDD TELEMETRY: log execution context before assertions
        print(f"\n--- LDD TRAJECTORY (IMP:7-10) for TestLawStructureExtractor::test_item ---")
        print(f"  [LDD_TEST][IMP:8][TestLawStructureExtractor][test_item] Test logic executed, entering assertion phase")
        hl, _ = self.body_builder._line_2level(text="1) пункт первый", label="structure_unit", init_hl_depth=self.depth)
        self.assertEqual("item", hl.line_type)
        hl, _ = self.body_builder._line_2level(text="3) пункт первый", label="structure_unit", init_hl_depth=self.depth)
        self.assertEqual("item", hl.line_type)
        hl, _ = self.body_builder._line_2level(text="1000) пункт первый", label="structure_unit", init_hl_depth=self.depth)
        self.assertEqual("item", hl.line_type)
        hl, _ = self.body_builder._line_2level(text="1.1.3) пункт первый", label="structure_unit", init_hl_depth=self.depth)
        self.assertEqual("item", hl.line_type)

    # endregion METHOD_test_item
    # region METHOD_test_subitem [DOMAIN(7): Testing; CONCEPT(8): LDD_Telemetry; TECH(8): unittest]
    ## @purpose Verify: subitem.
    ## @complexity 5
    def test_subitem(self) -> None:
        # LDD TELEMETRY: log execution context before assertions
        print(f"\n--- LDD TRAJECTORY (IMP:7-10) for TestLawStructureExtractor::test_subitem ---")
        print(f"  [LDD_TEST][IMP:8][TestLawStructureExtractor][test_subitem] Test logic executed, entering assertion phase")
        hl, _ = self.body_builder._line_2level(text="а) пункт первый", label="structure_unit", init_hl_depth=self.depth)
        self.assertEqual("subitem", hl.line_type)
        hl, _ = self.body_builder._line_2level(text="б) пункт первый", label="structure_unit", init_hl_depth=self.depth)
        self.assertEqual("subitem", hl.line_type)
        hl, _ = self.body_builder._line_2level(text="ё) пункт первый", label="structure_unit", init_hl_depth=self.depth)
        self.assertEqual("subitem", hl.line_type)

    # endregion METHOD_test_subitem
    # region METHOD_test_article_part [DOMAIN(7): Testing; CONCEPT(8): LDD_Telemetry; TECH(8): unittest]
    ## @purpose Verify: article part.
    ## @complexity 5
    def test_article_part(self) -> None:
        # LDD TELEMETRY: log execution context before assertions
        print(f"\n--- LDD TRAJECTORY (IMP:7-10) for TestLawStructureExtractor::test_article_part ---")
        print(f"  [LDD_TEST][IMP:8][TestLawStructureExtractor][test_article_part] Test logic executed, entering assertion phase")
        hl, _ = self.body_builder._line_2level(text="1. пункт первый", label="structure_unit", init_hl_depth=self.depth)
        self.assertEqual("articlePart", hl.line_type)
        hl, _ = self.body_builder._line_2level(text="2. пункт первый", label="structure_unit", init_hl_depth=self.depth)
        self.assertEqual("articlePart", hl.line_type)
        hl, _ = self.body_builder._line_2level(text="1.2.1. пункт первый", label="structure_unit", init_hl_depth=self.depth)
        self.assertEqual("articlePart", hl.line_type)
        hl, _ = self.body_builder._line_2level(text="1.2.1.2. пункт первый", label="structure_unit", init_hl_depth=self.depth)
        self.assertEqual("articlePart", hl.line_type)

    # endregion METHOD_test_article_part
    # region METHOD_test_begin_application [DOMAIN(7): Testing; CONCEPT(8): LDD_Telemetry; TECH(8): unittest]
    ## @purpose Verify: begin application.
    ## @complexity 5
    def test_begin_application(self) -> None:
        # LDD TELEMETRY: log execution context before assertions
        print(f"\n--- LDD TRAJECTORY (IMP:7-10) for TestLawStructureExtractor::test_begin_application ---")
        print(f"  [LDD_TEST][IMP:8][TestLawStructureExtractor][test_begin_application] Test logic executed, entering assertion phase")
        application_starts = [
            "Утвержден", "УТВЕРЖДЕНО \n", "Приложение №1\n", "Приложение № 45\n", "Утверждено    \n",
            "'Приложение N2", "утверждены\n", "Приложение к постановлению\n",
            "Приложение № 1 к распоряжению\n"
        ]
        for application_start in application_starts:
            self.assertIsNotNone(self.structure_extractor.classifier.regexp_application_begin.match(application_start.lower()))

    # endregion METHOD_test_begin_application
    # region METHOD_test_string_number_correctness_with_regexp [DOMAIN(7): Testing; CONCEPT(8): LDD_Telemetry; TECH(8): unittest]
    ## @purpose Verify: string number correctness with regexp.
    ## @complexity 5
    def test_string_number_correctness_with_regexp(self) -> None:
        # LDD TELEMETRY: log execution context before assertions
        print(f"\n--- LDD TRAJECTORY (IMP:7-10) for TestLawStructureExtractor::test_string_number_correctness_with_regexp ---")
        print(f"  [LDD_TEST][IMP:8][TestLawStructureExtractor][test_string_number_correctness_with_regexp] Test logic executed, entering assertion phase")
        lines = [
            "03.06.2009 № 17, от 07.10.2009 № 42, от  10.03.2010 № 6, от 14.04.2010 № 11,  от",
            "правонарушениях. (В редакции Закона Москвы от 24.06.2015 г. № 39)",
            "2. Нарушение  административного регламента",
            "1.2.2)", "1.2.4.6}", "1.23.005 ", "1.4.5 ", "1.4.5\n", "1.5.6.Закон о ...."
        ]
        answers = [False, False, True, True, True, False, True, True, True]

        for num, line in enumerate(lines):
            self.assertEqual(answers[num], self.structure_extractor.regexps_part.match(line) is not None, line)

    # endregion METHOD_test_string_number_correctness_with_regexp
    # region METHOD_test_number_ends [DOMAIN(7): Testing; CONCEPT(8): LDD_Telemetry; TECH(8): unittest]
    ## @purpose Verify: number ends.
    ## @complexity 5
    def test_number_ends(self) -> None:
        # LDD TELEMETRY: log execution context before assertions
        print(f"\n--- LDD TRAJECTORY (IMP:7-10) for TestLawStructureExtractor::test_number_ends ---")
        print(f"  [LDD_TEST][IMP:8][TestLawStructureExtractor][test_number_ends] Test logic executed, entering assertion phase")
        numbers = ["1.2.2) ", "1.4.5Д", "1.5.6.Н", "1.2.4.6}    "]
        without_ends = ["1.2.2)", "1.4.5", "1.5.6.", "1.2.4.6}"]

        for num, number in enumerate(numbers):
            res = regexps_ends_of_number.search(number)
            self.assertEqual(number[:res.start()], without_ends[num])

    # endregion METHOD_test_number_ends
    # region METHOD___get_line_with_meta [DOMAIN(7): Testing; CONCEPT(8): TestInfrastructure; TECH(8): unittest]
    ## @purpose get line with meta.
    def __get_line_with_meta(self, hierarchy_level: HierarchyLevel, text: str) -> LineWithMeta:
        return LineWithMeta(line=text, metadata=LineMetadata(page_id=0, line_id=0, hierarchy_level=hierarchy_level))

    # endregion METHOD___get_line_with_meta
    # region METHOD___check_postprocess_of_one_string_w_roman_numeral [DOMAIN(7): Testing; CONCEPT(8): TestInfrastructure; TECH(8): unittest]
    ## @purpose check postprocess of one string w roman numeral.
    def __check_postprocess_of_one_string_w_roman_numeral(self, text: str, text_expected: str) -> None:
        hierarchy_level = HierarchyLevel(4, 0, True, "subsection")
        line = self.__get_line_with_meta(hierarchy_level=hierarchy_level, text=text)
        result = self.structure_extractor._postprocess_roman(hierarchy_level=hierarchy_level, line=line)
        self.assertEqual(text_expected, result.line)

    # endregion METHOD___check_postprocess_of_one_string_w_roman_numeral
    # region METHOD_test_postprocessing_of_strings_with_roman_numerals [DOMAIN(7): Testing; CONCEPT(8): LDD_Telemetry; TECH(8): unittest]
    ## @purpose Verify: postprocessing of strings with roman numerals.
    ## @complexity 5
    def test_postprocessing_of_strings_with_roman_numerals(self) -> None:
        # LDD TELEMETRY: log execution context before assertions
        print(f"\n--- LDD TRAJECTORY (IMP:7-10) for TestLawStructureExtractor::test_postprocessing_of_strings_with_roman_numerals ---")
        print(f"  [LDD_TEST][IMP:8][TestLawStructureExtractor][test_postprocessing_of_strings_with_roman_numerals] Test logic executed, entering assertion phase")
        self.__check_postprocess_of_one_string_w_roman_numeral("I. Общие положения", "I. Общие положения")
        self.__check_postprocess_of_one_string_w_roman_numeral("Т. Общие положения", "I. Общие положения")
        self.__check_postprocess_of_one_string_w_roman_numeral("Г. Общие положения", "I. Общие положения")
        self.__check_postprocess_of_one_string_w_roman_numeral("T. Общие положения", "I. Общие положения")
        self.__check_postprocess_of_one_string_w_roman_numeral("П. Общие положения", "II. Общие положения")
        self.__check_postprocess_of_one_string_w_roman_numeral("Ш. Общие положения", "III. Общие положения")
        self.__check_postprocess_of_one_string_w_roman_numeral("ТУ. Общие положения", "IV. Общие положения")
        self.__check_postprocess_of_one_string_w_roman_numeral("УТ. Общие положения", "VI. Общие положения")
        self.__check_postprocess_of_one_string_w_roman_numeral("  УТ. Общие положения", "  VI. Общие положения")
        self.__check_postprocess_of_one_string_w_roman_numeral("У. Общие положения", "V. Общие положения")
        self.__check_postprocess_of_one_string_w_roman_numeral("V. Общие положения", "V. Общие положения")
        self.__check_postprocess_of_one_string_w_roman_numeral("Общие положения", "Общие положения")

    # endregion METHOD_test_postprocessing_of_strings_with_roman_numerals
    # region METHOD_test_empty_document [DOMAIN(7): Testing; CONCEPT(8): LDD_Telemetry; TECH(8): unittest]
    ## @purpose Verify: empty document.
    ## @complexity 5
    def test_empty_document(self) -> None:
        # LDD TELEMETRY: log execution context before assertions
        print(f"\n--- LDD TRAJECTORY (IMP:7-10) for TestLawStructureExtractor::test_empty_document ---")
        print(f"  [LDD_TEST][IMP:8][TestLawStructureExtractor][test_empty_document] Test logic executed, entering assertion phase")
        self.assertListEqual([], self.structure_extractor.classifier.predict([]))

    # endregion METHOD_test_empty_document
    # region METHOD_test_fix_labels [DOMAIN(7): Testing; CONCEPT(8): LDD_Telemetry; TECH(8): unittest]
    ## @purpose Verify: fix labels.
    ## @complexity 5
    def test_fix_labels(self) -> None:
        # LDD TELEMETRY: log execution context before assertions
        print(f"\n--- LDD TRAJECTORY (IMP:7-10) for TestLawStructureExtractor::test_fix_labels ---")
        print(f"  [LDD_TEST][IMP:8][TestLawStructureExtractor][test_fix_labels] Test logic executed, entering assertion phase")
        labels = ["title", "raw_text", "title", "structure_unit", "title", "cellar", "structure_unit", "cellar", "application"]
        labels_expected = ["title", "title", "title", "structure_unit", "raw_text", "raw_text", "structure_unit", "cellar", "application"]
        self.assertListEqual(labels_expected, self.__fix_labels(labels))

        labels = ["title", "structure_unit", "application", "structure_unit"]
        self.assertListEqual(labels, self.__fix_labels(labels))

        labels = ["structure_unit", "application", "title", "cellar", "title", "application", "structure_unit", "structure_unit", "structure_unit", "title"]
        labels_expected = [
            "structure_unit", "application", "raw_text", "raw_text", "raw_text", "application", "structure_unit", "structure_unit", "structure_unit", "raw_text"
        ]
        self.assertListEqual(labels_expected, self.__fix_labels(labels))

        classes = ["structure_unit", "cellar", "application", "title", "footer"]
        random.seed(int(time.time()))
        for _ in range(1000):
            labels = [random.choice(classes) for _ in range(10)]
            self.__fix_labels(labels, msg=str(labels))
        with TestTimeout(10):
            labels = [random.choice(classes) for _ in range(1000000)]
            self.__fix_labels(labels)

    # endregion METHOD_test_fix_labels
    # region METHOD___fix_labels [DOMAIN(7): Testing; CONCEPT(8): TestInfrastructure; TECH(8): unittest]
    ## @purpose fix labels.
    def __fix_labels(self, labels: List[str], msg: str = "") -> List[str]:
        result = self.structure_extractor._fix_labels(labels)
        dd = defaultdict(list)
        for index, label in enumerate(result):
            dd[label].append(index)
        # title before structure_unit
        if "title" in dd and "structure_unit" in dd:
            self.assertGreater(min(dd["structure_unit"]), max(dd["title"]), msg)
        return result

    # endregion METHOD___fix_labels
# endregion CLASS_TestLawStructureExtractor