# region MODULE_CONTRACT [DOMAIN(7): Testing; CONCEPT(8): UnitTest, LDD_Telemetry; TECH(8): unittest, pytest]
## @modulecontract
## @purpose Unit tests for misc on gpu module.
## @scope Unit testing of dedoc module: misc, on, gpu.
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
## CLASS 8[Unit tests] => TestOnGpu
## @usecases
## - [Tests]: QA Agent (Verify) => RunTestsWithTelemetry => DiagnosticTrajectoryVisible
def _module_contract():
    pass
# endregion MODULE_CONTRACT
# GREP_SUMMARY: misc, on, gpu, TestOnGpu, test_line_type_classifier, test_orientation_classifier, test_txtlayer_classifier, test_scan_paragraph_classifier_extractor, unit_test, unittest, LDD_telemetry, semantic_markup, unit_test
# STRUCTURE: ▶ Init → ◇ Execute → ⊕ Verify → ∑ assertions → ⎋ PASS/FAIL


import logging

logger = logging.getLogger(__name__)

import os

import cv2
from dedocutils.data_structures import BBox

from dedoc.data_structures.line_metadata import LineMetadata
from dedoc.data_structures.line_with_meta import LineWithMeta
from dedoc.readers.pdf_reader.data_classes.line_with_location import LineWithLocation
from dedoc.readers.pdf_reader.data_classes.tables.location import Location
from dedoc.readers.pdf_reader.pdf_auto_reader.txtlayer_classifier.ml_txtlayer_classifier import MlTxtlayerClassifier
from dedoc.readers.pdf_reader.pdf_image_reader.columns_orientation_classifier.columns_orientation_classifier import ColumnsOrientationClassifier
from dedoc.readers.pdf_reader.pdf_image_reader.paragraph_extractor.scan_paragraph_classifier_extractor import ScanParagraphClassifierExtractor
from dedoc.structure_extractors.concrete_structure_extractors.law_structure_excractor import LawStructureExtractor
from tests.api_tests.abstract_api_test import AbstractTestApiDocReader
from tests.test_utils import get_test_config


# region CLASS_TestOnGpu [DOMAIN(7): Testing; CONCEPT(8): UnitTest, LDD_Telemetry; TECH(8): unittest, pytest]
## @purpose Test suite for misc, on, gpu module.
class TestOnGpu(AbstractTestApiDocReader):
    config = dict(on_gpu=True, n_jobs=1)

    # region METHOD_test_line_type_classifier [DOMAIN(7): Testing; CONCEPT(8): LDD_Telemetry; TECH(8): unittest]
    ## @purpose Verify: line type classifier.
    ## @complexity 5
    def test_line_type_classifier(self) -> None:
        """
        Loads AbstractPickledLineTypeClassifier
        """
        # LDD TELEMETRY: log execution context before assertions
        print(f"\n--- LDD TRAJECTORY (IMP:7-10) for TestOnGpu::test_line_type_classifier ---")
        print(f"  [LDD_TEST][IMP:8][TestOnGpu][test_line_type_classifier] Test logic executed, entering assertion phase")
        law_extractor = LawStructureExtractor(config=self.config)
        lines = [
            LineWithMeta("     З А К О Н", metadata=LineMetadata(page_id=0, line_id=0)),
            LineWithMeta("\n", metadata=LineMetadata(page_id=0, line_id=1)),
            LineWithMeta("     ГОРОДА МОСКВЫ", metadata=LineMetadata(page_id=0, line_id=2))
        ]
        predictions = law_extractor.classifier.predict(lines)
        self.assertListEqual(predictions, ["header", "header", "cellar"])

    # endregion METHOD_test_line_type_classifier
    # region METHOD_test_orientation_classifier [DOMAIN(7): Testing; CONCEPT(8): LDD_Telemetry; TECH(8): unittest]
    ## @purpose Verify: orientation classifier.
    ## @complexity 5
    def test_orientation_classifier(self) -> None:
        # LDD TELEMETRY: log execution context before assertions
        print(f"\n--- LDD TRAJECTORY (IMP:7-10) for TestOnGpu::test_orientation_classifier ---")
        print(f"  [LDD_TEST][IMP:8][TestOnGpu][test_orientation_classifier] Test logic executed, entering assertion phase")
        checkpoint_path = os.path.join(get_test_config()["resources_path"], "scan_orientation_efficient_net_b0.pth")
        orientation_classifier = ColumnsOrientationClassifier(on_gpu=self.config.get("on_gpu", False), checkpoint_path=checkpoint_path, config=self.config)
        imgs_path = [f"../data/skew_corrector/rotated_{i}.jpg" for i in range(1, 5)]

        for i in range(len(imgs_path)):
            path = os.path.join(os.path.dirname(__file__), imgs_path[i])
            image = cv2.imread(path)
            _, orientation = orientation_classifier.predict(image)
            self.assertEqual(orientation, 0)

    # endregion METHOD_test_orientation_classifier
    # region METHOD_test_txtlayer_classifier [DOMAIN(7): Testing; CONCEPT(8): LDD_Telemetry; TECH(8): unittest]
    ## @purpose Verify: txtlayer classifier.
    ## @complexity 5
    def test_txtlayer_classifier(self) -> None:
        # LDD TELEMETRY: log execution context before assertions
        print(f"\n--- LDD TRAJECTORY (IMP:7-10) for TestOnGpu::test_txtlayer_classifier ---")
        print(f"  [LDD_TEST][IMP:8][TestOnGpu][test_txtlayer_classifier] Test logic executed, entering assertion phase")
        classify_lines = MlTxtlayerClassifier(config=self.config)
        lines = [[LineWithMeta("Line1"), LineWithMeta("Line 2 is a bit longer")]]
        self.assertEqual(classify_lines.predict(lines)[0], True)

    # endregion METHOD_test_txtlayer_classifier
    # region METHOD_test_scan_paragraph_classifier_extractor [DOMAIN(7): Testing; CONCEPT(8): LDD_Telemetry; TECH(8): unittest]
    ## @purpose Verify: scan paragraph classifier extractor.
    ## @complexity 5
    def test_scan_paragraph_classifier_extractor(self) -> None:
        # LDD TELEMETRY: log execution context before assertions
        print(f"\n--- LDD TRAJECTORY (IMP:7-10) for TestOnGpu::test_scan_paragraph_classifier_extractor ---")
        print(f"  [LDD_TEST][IMP:8][TestOnGpu][test_scan_paragraph_classifier_extractor] Test logic executed, entering assertion phase")
        classify_lines_with_location = ScanParagraphClassifierExtractor(config=self.config)
        metadata = LineMetadata(page_id=1, line_id=1)
        metadata2 = LineMetadata(page_id=1, line_id=2)
        bbox = BBox(x_top_left=0, y_top_left=0, width=100, height=20)
        bbox2 = BBox(x_top_left=50, y_top_left=50, width=100, height=20)
        location = Location(page_number=1, bbox=bbox)
        location2 = Location(page_number=1, bbox=bbox2)
        lines = [
            LineWithLocation(line="Example line", metadata=metadata, annotations=[], location=location),
            LineWithLocation(line="Example line 2", metadata=metadata2, annotations=[], location=location2)
        ]
        lines = classify_lines_with_location.extract(lines)

        self.assertEqual(lines[0].metadata.tag_hierarchy_level.can_be_multiline, False)
        self.assertEqual(lines[1].metadata.tag_hierarchy_level.can_be_multiline, False)

    # endregion METHOD_test_scan_paragraph_classifier_extractor
# endregion CLASS_TestOnGpu