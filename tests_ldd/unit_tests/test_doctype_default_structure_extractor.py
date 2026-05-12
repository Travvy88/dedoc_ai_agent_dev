# region MODULE_CONTRACT [DOMAIN(7): Testing; CONCEPT(8): UnitTest, LDD_Telemetry; TECH(8): unittest, pytest]
## @modulecontract
## @purpose Unit tests for doctype default structure extractor module.
## @scope Unit testing of dedoc module: doctype, default, structure, extractor.
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
## CLASS 8[Unit tests] => TestDefaultStructureExtractor
## @usecases
## - [Tests]: QA Agent (Verify) => RunTestsWithTelemetry => DiagnosticTrajectoryVisible
def _module_contract():
    pass
# endregion MODULE_CONTRACT
# GREP_SUMMARY: doctype, default, structure, extractor, TestDefaultStructureExtractor, test_tag_patterns, test_list_patterns, test_regexp_patterns, test_start_word_patterns, unit_test, unittest, LDD_telemetry, semantic_markup, unit_test
# STRUCTURE: ▶ Init → ◇ Execute → ⊕ Verify → ∑ assertions → ⎋ PASS/FAIL


import logging

logger = logging.getLogger(__name__)

import os
import re
import unittest

from dedoc.readers.docx_reader.docx_reader import DocxReader
from dedoc.readers.reader_composition import ReaderComposition
from dedoc.readers.txt_reader.raw_text_reader import RawTextReader
from dedoc.structure_extractors.concrete_structure_extractors.default_structure_extractor import DefaultStructureExtractor
from dedoc.structure_extractors.patterns.dotted_list_pattern import DottedListPattern
from dedoc.structure_extractors.patterns.regexp_pattern import RegexpPattern
from dedoc.structure_extractors.patterns.roman_list_pattern import RomanListPattern
from dedoc.structure_extractors.patterns.tag_header_pattern import TagHeaderPattern
from dedoc.structure_extractors.patterns.tag_list_pattern import TagListPattern
from tests.test_utils import get_test_config


# region CLASS_TestDefaultStructureExtractor [DOMAIN(7): Testing; CONCEPT(8): UnitTest, LDD_Telemetry; TECH(8): unittest, pytest]
## @purpose Test suite for doctype, default, structure, extractor module.
class TestDefaultStructureExtractor(unittest.TestCase):
    data_directory_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "data"))
    structure_extractor = DefaultStructureExtractor(config=get_test_config())
    reader = ReaderComposition(readers=[RawTextReader(), DocxReader()])

    # region METHOD_test_tag_patterns [DOMAIN(7): Testing; CONCEPT(8): LDD_Telemetry; TECH(8): unittest]
    ## @purpose Verify: tag patterns.
    ## @complexity 5
    def test_tag_patterns(self) -> None:
        # LDD TELEMETRY: log execution context before assertions
        print(f"\n--- LDD TRAJECTORY (IMP:7-10) for TestDefaultStructureExtractor::test_tag_patterns ---")
        print(f"  [LDD_TEST][IMP:8][TestDefaultStructureExtractor][test_tag_patterns] Test logic executed, entering assertion phase")
        file_path = os.path.join(self.data_directory_path, "docx", "with_tags.docx")
        patterns = [
            TagHeaderPattern(line_type="custom_header", level_1=1, can_be_multiline=False),
            TagListPattern(line_type="custom_list", level_1=2),
        ]
        document = self.reader.read(file_path=file_path)
        document = self.structure_extractor.extract(document=document, parameters={"patterns": patterns})
        self.assertEqual(document.lines[0].metadata.hierarchy_level.line_type, "custom_header")
        self.assertEqual(document.lines[0].metadata.hierarchy_level.level_1, 1)
        self.assertEqual(document.lines[0].metadata.hierarchy_level.level_2, 1)
        self.assertFalse(document.lines[0].metadata.hierarchy_level.can_be_multiline)

        self.assertEqual(document.lines[1].metadata.hierarchy_level.line_type, "custom_header")
        self.assertEqual(document.lines[1].metadata.hierarchy_level.level_1, 1)
        self.assertEqual(document.lines[1].metadata.hierarchy_level.level_2, 2)

        self.assertEqual(document.lines[3].metadata.hierarchy_level.line_type, "raw_text")
        self.assertTrue(document.lines[3].metadata.hierarchy_level.can_be_multiline)

        self.assertEqual(document.lines[4].metadata.hierarchy_level.line_type, "custom_list")
        self.assertEqual(document.lines[4].metadata.hierarchy_level.level_1, 2)
        self.assertEqual(document.lines[4].metadata.hierarchy_level.level_2, 1)
        self.assertFalse(document.lines[4].metadata.hierarchy_level.can_be_multiline)

    # endregion METHOD_test_tag_patterns
    # region METHOD_test_list_patterns [DOMAIN(7): Testing; CONCEPT(8): LDD_Telemetry; TECH(8): unittest]
    ## @purpose Verify: list patterns.
    ## @complexity 5
    def test_list_patterns(self) -> None:
        # LDD TELEMETRY: log execution context before assertions
        print(f"\n--- LDD TRAJECTORY (IMP:7-10) for TestDefaultStructureExtractor::test_list_patterns ---")
        print(f"  [LDD_TEST][IMP:8][TestDefaultStructureExtractor][test_list_patterns] Test logic executed, entering assertion phase")
        file_path = os.path.join(self.data_directory_path, "txt", "pr_17.txt")
        patterns = [
            RomanListPattern(line_type="chapter", level_1=1, level_2=1, can_be_multiline=False),
            DottedListPattern(line_type="dotted_list", level_1=2, can_be_multiline=False),
        ]
        document = self.reader.read(file_path=file_path)
        document = self.structure_extractor.extract(document=document, parameters={"patterns": patterns})

        self.assertEqual(document.lines[0].metadata.hierarchy_level.line_type, "raw_text")
        self.assertEqual(document.lines[12].metadata.hierarchy_level.line_type, "chapter")
        self.assertEqual(document.lines[14].metadata.hierarchy_level.line_type, "dotted_list")

    # endregion METHOD_test_list_patterns
    # region METHOD_test_regexp_patterns [DOMAIN(7): Testing; CONCEPT(8): LDD_Telemetry; TECH(8): unittest]
    ## @purpose Verify: regexp patterns.
    ## @complexity 5
    def test_regexp_patterns(self) -> None:
        # LDD TELEMETRY: log execution context before assertions
        print(f"\n--- LDD TRAJECTORY (IMP:7-10) for TestDefaultStructureExtractor::test_regexp_patterns ---")
        print(f"  [LDD_TEST][IMP:8][TestDefaultStructureExtractor][test_regexp_patterns] Test logic executed, entering assertion phase")
        file_path = os.path.join(self.data_directory_path, "docx", "without_numbering.docx")
        patterns = [
            RegexpPattern(regexp="^глава\s\d+\.", line_type="глава", level_1=1),  # noqa
            RegexpPattern(regexp=re.compile(r"^статья\s\d+\.\d+\."), line_type="статья", level_1=2)
        ]
        document = self.reader.read(file_path=file_path)
        document = self.structure_extractor.extract(document=document, parameters={"patterns": patterns})
        self.assertEqual(document.lines[0].metadata.hierarchy_level.line_type, "raw_text")
        self.assertEqual(document.lines[9].metadata.hierarchy_level.line_type, "глава")
        self.assertEqual(document.lines[11].metadata.hierarchy_level.line_type, "статья")
        self.assertEqual(document.lines[15].metadata.hierarchy_level.line_type, "статья")
        self.assertEqual(document.lines[83].metadata.hierarchy_level.line_type, "глава")

    # endregion METHOD_test_regexp_patterns
    # region METHOD_test_start_word_patterns [DOMAIN(7): Testing; CONCEPT(8): LDD_Telemetry; TECH(8): unittest]
    ## @purpose Verify: start word patterns.
    ## @complexity 5
    def test_start_word_patterns(self) -> None:
        # LDD TELEMETRY: log execution context before assertions
        print(f"\n--- LDD TRAJECTORY (IMP:7-10) for TestDefaultStructureExtractor::test_start_word_patterns ---")
        print(f"  [LDD_TEST][IMP:8][TestDefaultStructureExtractor][test_start_word_patterns] Test logic executed, entering assertion phase")
        file_path = os.path.join(self.data_directory_path, "docx", "example.docx")
        patterns = [
            {"name": "start_word", "start_word": "глава", "level_1": 1, "line_type": "глава"},
            {"name": "start_word", "start_word": "статья", "level_1": 2, "line_type": "статья"},
        ]
        document = self.reader.read(file_path=file_path)
        document = self.structure_extractor.extract(document=document, parameters={"patterns": patterns})
        self.assertEqual(document.lines[1].metadata.hierarchy_level.line_type, "глава")
        self.assertEqual(document.lines[3].metadata.hierarchy_level.line_type, "статья")
        self.assertEqual(document.lines[5].metadata.hierarchy_level.line_type, "статья")

    # endregion METHOD_test_start_word_patterns
# endregion CLASS_TestDefaultStructureExtractor