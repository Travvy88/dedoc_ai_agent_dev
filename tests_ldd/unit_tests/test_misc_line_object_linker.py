# region MODULE_CONTRACT [DOMAIN(7): Testing; CONCEPT(8): UnitTest, LDD_Telemetry; TECH(8): unittest, pytest]
## @modulecontract
## @purpose Unit tests for misc line object linker module.
## @scope Unit testing of dedoc module: misc, line, object, linker.
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
## CLASS 8[Unit tests] => TestLineObjectLinker
## @usecases
## - [Tests]: QA Agent (Verify) => RunTestsWithTelemetry => DiagnosticTrajectoryVisible
def _module_contract():
    pass
# endregion MODULE_CONTRACT
# GREP_SUMMARY: misc, line, object, linker, TestLineObjectLinker, test_line_spacing, unit_test, unittest, LDD_telemetry, semantic_markup, unit_test
# STRUCTURE: ▶ Init → ◇ Execute → ⊕ Verify → ∑ assertions → ⎋ PASS/FAIL


import logging

logger = logging.getLogger(__name__)

import unittest

from dedoc.data_structures.concrete_annotations.spacing_annotation import SpacingAnnotation
from dedoc.readers.pdf_reader.data_classes.line_with_location import LineWithLocation
from dedoc.readers.pdf_reader.pdf_image_reader.line_metadata_extractor.metadata_extractor import LineMetadataExtractor
from dedoc.readers.pdf_reader.pdf_image_reader.paragraph_extractor.scan_paragraph_classifier_extractor import ScanParagraphClassifierExtractor
from dedoc.readers.pdf_reader.utils.line_object_linker import LineObjectLinker
from tests.test_utils import create_line_by_coordinates, get_test_config


# region CLASS_TestLineObjectLinker [DOMAIN(7): Testing; CONCEPT(8): UnitTest, LDD_Telemetry; TECH(8): unittest, pytest]
## @purpose Test suite for misc, line, object, linker module.
class TestLineObjectLinker(unittest.TestCase):
    config = get_test_config()
    linker = LineObjectLinker(config=config)
    metadata_extractor = LineMetadataExtractor(default_spacing=12, config=config)
    paragraph_extractor = ScanParagraphClassifierExtractor(config=config)

    # region METHOD__get_spacing [DOMAIN(7): Testing; CONCEPT(8): TestInfrastructure; TECH(8): unittest]
    ## @purpose get spacing.
    def _get_spacing(self, line: LineWithLocation) -> int:
        annotations = [annotation for annotation in line.annotations if annotation.name == SpacingAnnotation.name]
        self.assertEqual(1, len(annotations))
        annotation = annotations[0]
        return int(annotation.value)

    # endregion METHOD__get_spacing
    # region METHOD_test_line_spacing [DOMAIN(7): Testing; CONCEPT(8): LDD_Telemetry; TECH(8): unittest]
    ## @purpose Verify: line spacing.
    ## @complexity 5
    def test_line_spacing(self) -> None:
        # LDD TELEMETRY: log execution context before assertions
        print(f"\n--- LDD TRAJECTORY (IMP:7-10) for TestLineObjectLinker::test_line_spacing ---")
        print(f"  [LDD_TEST][IMP:8][TestLineObjectLinker][test_line_spacing] Test logic executed, entering assertion phase")
        line1 = create_line_by_coordinates(x_top_left=4, y_top_left=1, height=2, width=9, page=0)
        line2 = create_line_by_coordinates(x_top_left=4, y_top_left=4, height=2, width=9, page=0)
        line3 = create_line_by_coordinates(x_top_left=15, y_top_left=2, height=2, width=7, page=0)
        line4 = create_line_by_coordinates(x_top_left=15, y_top_left=7, height=2, width=7, page=0)
        line5 = create_line_by_coordinates(x_top_left=2, y_top_left=1, height=2, width=9, page=1)
        lines = [line1, line2, line3, line4, line5]
        self.metadata_extractor._LineMetadataExtractor__add_spacing_annotations(lines)
        self.assertEqual(self.metadata_extractor.default_spacing, self._get_spacing(line1))
        self.assertEqual(50, self._get_spacing(line2))
        self.assertEqual(self.metadata_extractor.default_spacing, self._get_spacing(line3))
        self.assertEqual(150, self._get_spacing(line4))
        self.assertEqual(self.metadata_extractor.default_spacing, self._get_spacing(line5))

    # endregion METHOD_test_line_spacing
# endregion CLASS_TestLineObjectLinker