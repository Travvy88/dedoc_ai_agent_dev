# region MODULE_CONTRACT [DOMAIN(7): Testing; CONCEPT(8): UnitTest, LDD_Telemetry; TECH(8): unittest, pytest]
## @modulecontract
## @purpose Unit tests for format pdf reader module.
## @scope Unit testing of dedoc module: format, pdf, reader.
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
## CLASS 8[Unit tests] => TestPDFReader
## @usecases
## - [Tests]: QA Agent (Verify) => RunTestsWithTelemetry => DiagnosticTrajectoryVisible
def _module_contract():
    pass
# endregion MODULE_CONTRACT
# GREP_SUMMARY: format, pdf, reader, TestPDFReader, test_skew_corrector, test_scan_orientation, test_header_footer_search, test_header_footer_search_2, test_header_footer_search_3, test_long_list_in_pdf, test_pdf_text_layer, test_table_extractor, unit_test, unittest, LDD_telemetry, semantic_markup, unit_test
# STRUCTURE: ▶ Init → ◇ Execute → ⊕ Verify → ∑ assertions → ⎋ PASS/FAIL


import logging

logger = logging.getLogger(__name__)

import os
import re
import shutil
import unittest
from tempfile import TemporaryDirectory
from typing import List

import cv2
from dedocutils.preprocessing import SkewCorrector

from dedoc.data_structures.line_with_meta import LineWithMeta
from dedoc.readers.pdf_reader.pdf_image_reader.columns_orientation_classifier.columns_orientation_classifier import ColumnsOrientationClassifier
from dedoc.readers.pdf_reader.pdf_image_reader.pdf_image_reader import PdfImageReader
from dedoc.readers.pdf_reader.pdf_txtlayer_reader.pdf_txtlayer_reader import PdfTxtlayerReader
from tests.test_utils import get_test_config


# region CLASS_TestPDFReader [DOMAIN(7): Testing; CONCEPT(8): UnitTest, LDD_Telemetry; TECH(8): unittest, pytest]
## @purpose Test suite for format, pdf, reader module.
class TestPDFReader(unittest.TestCase):
    checkpoint_path = os.path.join(get_test_config()["resources_path"], "scan_orientation_efficient_net_b0.pth")
    config = get_test_config()
    orientation_classifier = ColumnsOrientationClassifier(on_gpu=False, checkpoint_path=checkpoint_path, config=config)

    # region METHOD__split_lines_on_pages [DOMAIN(7): Testing; CONCEPT(8): TestInfrastructure; TECH(8): unittest]
    ## @purpose split lines on pages.
    def _split_lines_on_pages(self, lines: List[LineWithMeta]) -> List[List[str]]:
        pages = set(map(lambda x: x.metadata.page_id, lines))
        lines_by_page = [[line.line for line in lines if line.metadata.page_id == page_id] for page_id in pages]

        return lines_by_page

    # endregion METHOD__split_lines_on_pages
    # region METHOD_test_skew_corrector [DOMAIN(7): Testing; CONCEPT(8): LDD_Telemetry; TECH(8): unittest]
    ## @purpose Verify: skew corrector.
    ## @complexity 5
    def test_skew_corrector(self) -> None:
        # LDD TELEMETRY: log execution context before assertions
        print(f"\n--- LDD TRAJECTORY (IMP:7-10) for TestPDFReader::test_skew_corrector ---")
        print(f"  [LDD_TEST][IMP:8][TestPDFReader][test_skew_corrector] Test logic executed, entering assertion phase")
        skew_corrector = SkewCorrector()
        imgs_path = [f"../data/skew_corrector/rotated_{i}.jpg" for i in range(1, 5)]
        angles = [0.061732858955328755, -0.017535263190370427, 0.12228411148417097, 0]

        for i in range(len(imgs_path)):
            path = os.path.join(os.path.dirname(__file__), imgs_path[i])
            image = cv2.imread(path)
            _, orientation = self.orientation_classifier.predict(image)
            angle_predict = self.orientation_classifier.classes[2 + orientation]
            rotated, angle = skew_corrector.preprocess(image, {"orientation_angle": angle_predict})
            angle = angle["rotated_angle"]
            self.assertAlmostEqual(angle, angles[i], delta=8)

    # endregion METHOD_test_skew_corrector
    # region METHOD_test_scan_orientation [DOMAIN(7): Testing; CONCEPT(8): LDD_Telemetry; TECH(8): unittest]
    ## @purpose Verify: scan orientation.
    ## @complexity 5
    def test_scan_orientation(self) -> None:
        # LDD TELEMETRY: log execution context before assertions
        print(f"\n--- LDD TRAJECTORY (IMP:7-10) for TestPDFReader::test_scan_orientation ---")
        print(f"  [LDD_TEST][IMP:8][TestPDFReader][test_scan_orientation] Test logic executed, entering assertion phase")
        skew_corrector = SkewCorrector()
        imgs_path = [f"../data/scanned/orient_{i}.png"for i in range(1, 9)]
        angles = [90.0, 90.0, 270.0, 270.0, 180.0, 270.0, 180.0, 270.0]
        max_delta = 10.0
        for i in range(len(imgs_path)):
            path = os.path.join(os.path.dirname(__file__), imgs_path[i])
            image = cv2.imread(path)
            _, angle_predict = self.orientation_classifier.predict(image)
            rotated, angle = skew_corrector.preprocess(image, {"orientation_angle": angle_predict})
            angle = angle["rotated_angle"]
            self.assertTrue(abs(angle - angles[i]) < max_delta)

    # endregion METHOD_test_scan_orientation
    # region METHOD_test_header_footer_search [DOMAIN(7): Testing; CONCEPT(8): LDD_Telemetry; TECH(8): unittest]
    ## @purpose Verify: header footer search.
    ## @complexity 5
    def test_header_footer_search(self) -> None:
        # LDD TELEMETRY: log execution context before assertions
        print(f"\n--- LDD TRAJECTORY (IMP:7-10) for TestPDFReader::test_header_footer_search ---")
        print(f"  [LDD_TEST][IMP:8][TestPDFReader][test_header_footer_search] Test logic executed, entering assertion phase")
        config = get_test_config()
        any_doc_reader = PdfTxtlayerReader(config=config)
        with TemporaryDirectory() as tmpdir:
            filename = "prospectus.pdf"
            path = os.path.join(os.path.dirname(__file__), "../data/pdf_with_text_layer", filename)
            shutil.copy(path, os.path.join(tmpdir, filename))
            result = any_doc_reader.read(os.path.join(tmpdir, filename), parameters={"need_header_footer_analysis": "True", "need_pdf_table_analysis": "False"})

        lines_by_page = self._split_lines_on_pages(result.lines)

        headers = [lines[0] for lines in lines_by_page if lines[0] == "Richelieu Bond \n"]
        footers = [lines[-1] for lines in lines_by_page if re.match(r"^\s*-( )*[0-9]+( )*-\s*$", lines[-1])]

        self.assertEqual(len(headers), 0)
        self.assertEqual(len(footers), 0)

    # endregion METHOD_test_header_footer_search
    # region METHOD_test_header_footer_search_2 [DOMAIN(7): Testing; CONCEPT(8): LDD_Telemetry; TECH(8): unittest]
    ## @purpose Verify: header footer search 2.
    ## @complexity 5
    def test_header_footer_search_2(self) -> None:
        # LDD TELEMETRY: log execution context before assertions
        print(f"\n--- LDD TRAJECTORY (IMP:7-10) for TestPDFReader::test_header_footer_search_2 ---")
        print(f"  [LDD_TEST][IMP:8][TestPDFReader][test_header_footer_search_2] Test logic executed, entering assertion phase")
        config = get_test_config()
        any_doc_reader = PdfTxtlayerReader(config=config)
        with TemporaryDirectory() as tmpdir:
            filename = "with_changed_header_footer.pdf"
            path = os.path.join(os.path.dirname(__file__), "../data/pdf_with_text_layer", filename)
            shutil.copy(path, os.path.join(tmpdir, filename))
            result = any_doc_reader.read(os.path.join(tmpdir, filename), parameters={"need_header_footer_analysis": "True", "need_pdf_table_analysis": "False"})

        lines_by_page = self._split_lines_on_pages(result.lines)

        headers = [lines[0] for lines in lines_by_page if lines[0] == "Richelieu Bond \n"]
        footers = [lines[-1] for lines in lines_by_page if re.match(r"^\s*-( )*[0-9]+( )*-\s*$", lines[-1])]

        self.assertEqual(len(headers), 0)
        self.assertEqual(len(footers), 0)

    # endregion METHOD_test_header_footer_search_2
    # region METHOD_test_header_footer_search_3 [DOMAIN(7): Testing; CONCEPT(8): LDD_Telemetry; TECH(8): unittest]
    ## @purpose Verify: header footer search 3.
    ## @complexity 5
    def test_header_footer_search_3(self) -> None:
        # LDD TELEMETRY: log execution context before assertions
        print(f"\n--- LDD TRAJECTORY (IMP:7-10) for TestPDFReader::test_header_footer_search_3 ---")
        print(f"  [LDD_TEST][IMP:8][TestPDFReader][test_header_footer_search_3] Test logic executed, entering assertion phase")
        config = get_test_config()
        any_doc_reader = PdfTxtlayerReader(config=config)
        with TemporaryDirectory() as tmpdir:
            filename = "with_header_footer_2.pdf"
            path = os.path.join(os.path.dirname(__file__), "../data/pdf_with_text_layer", filename)
            shutil.copy(path, os.path.join(tmpdir, filename))
            result = any_doc_reader.read(os.path.join(tmpdir, filename), parameters={"need_header_footer_analysis": "True", "need_pdf_table_analysis": "False"})

        lines_by_page = self._split_lines_on_pages(result.lines)

        headers = [lines[0] for lines in lines_by_page if lines[0] == "QUEST MANAGEMENT, SICAV\n"]
        footers = [lines[-1] for lines in lines_by_page if re.match(r"^\s*[0-9]\s*$", lines[-1])]

        self.assertEqual(len(headers), 1)
        self.assertEqual(len(footers), 0)

    # endregion METHOD_test_header_footer_search_3
    # region METHOD_test_long_list_in_pdf [DOMAIN(7): Testing; CONCEPT(8): LDD_Telemetry; TECH(8): unittest]
    ## @purpose Verify: long list in pdf.
    ## @complexity 5
    def test_long_list_in_pdf(self) -> None:
        # LDD TELEMETRY: log execution context before assertions
        print(f"\n--- LDD TRAJECTORY (IMP:7-10) for TestPDFReader::test_long_list_in_pdf ---")
        print(f"  [LDD_TEST][IMP:8][TestPDFReader][test_long_list_in_pdf] Test logic executed, entering assertion phase")
        config = get_test_config()
        any_doc_reader = PdfImageReader(config=config)
        path = os.path.join(os.path.dirname(__file__), "../data/scanned/doc_with_long_list.pdf")
        result = any_doc_reader.read(path, parameters={"need_pdf_table_analysis": "False"})
        list_elements = result.lines[1:]
        self.assertEqual(list_elements[0].line.lower().strip(), "1. январь")
        self.assertEqual(list_elements[1].line.lower().strip(), "2. февраль")
        self.assertEqual(list_elements[2].line.lower().strip(), "3. март")
        self.assertEqual(list_elements[3].line.lower().strip(), "4. апрель")
        self.assertEqual(list_elements[4].line.lower().strip(), "5. май")
        self.assertEqual(list_elements[5].line.lower().strip(), "6. июнь")
        self.assertEqual(list_elements[6].line.lower().strip(), "7. июль")
        self.assertEqual(list_elements[7].line.lower().strip(), "8. август")
        self.assertEqual(list_elements[8].line.lower().strip(), "9. сентябрь в сентябре, в сентябре много листьев на земле желтые и красные! все такие")
        self.assertEqual(list_elements[9].line.lower().strip(), "разные!")
        self.assertEqual(list_elements[10].line.lower().strip(), "10. октябрь")
        self.assertEqual(list_elements[11].line.lower().strip(), "11. ноябрь")
        self.assertEqual(list_elements[12].line.lower().strip(), "12. декабрь")

    # endregion METHOD_test_long_list_in_pdf
    # region METHOD_test_pdf_text_layer [DOMAIN(7): Testing; CONCEPT(8): LDD_Telemetry; TECH(8): unittest]
    ## @purpose Verify: pdf text layer.
    ## @complexity 5
    def test_pdf_text_layer(self) -> None:
        # LDD TELEMETRY: log execution context before assertions
        print(f"\n--- LDD TRAJECTORY (IMP:7-10) for TestPDFReader::test_pdf_text_layer ---")
        print(f"  [LDD_TEST][IMP:8][TestPDFReader][test_pdf_text_layer] Test logic executed, entering assertion phase")
        config = get_test_config()
        any_doc_reader = PdfTxtlayerReader(config=config)
        path = os.path.join(os.path.dirname(__file__), "../data/pdf_with_text_layer/english_doc.pdf")
        result = any_doc_reader.read(path, parameters={})
        for line in result.lines:
            # check that annotations not duplicated
            annotations = line.annotations
            annotations_set = {(a.name, a.value, a.start, a.end) for a in annotations}
            self.assertEqual(len(annotations_set), len(annotations))

    # endregion METHOD_test_pdf_text_layer
    # region METHOD_test_table_extractor [DOMAIN(7): Testing; CONCEPT(8): LDD_Telemetry; TECH(8): unittest]
    ## @purpose Verify: table extractor.
    ## @complexity 5
    def test_table_extractor(self) -> None:
        # LDD TELEMETRY: log execution context before assertions
        print(f"\n--- LDD TRAJECTORY (IMP:7-10) for TestPDFReader::test_table_extractor ---")
        print(f"  [LDD_TEST][IMP:8][TestPDFReader][test_table_extractor] Test logic executed, entering assertion phase")
        config = {}  # Has to work without config
        any_doc_reader = PdfTxtlayerReader(config=config)
        path = os.path.join(os.path.dirname(__file__), "../data/pdf_with_text_layer/english_doc.pdf")
        result = any_doc_reader.read(path, parameters={"need_pdf_table_analysis": "True"})
        self.assertEqual(len(result.tables), 1)

    # endregion METHOD_test_table_extractor
# endregion CLASS_TestPDFReader