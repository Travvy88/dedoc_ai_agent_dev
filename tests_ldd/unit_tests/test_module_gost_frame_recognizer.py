# region MODULE_CONTRACT [DOMAIN(7): Testing; CONCEPT(8): UnitTest, LDD_Telemetry; TECH(8): unittest, pytest]
## @modulecontract
## @purpose Unit tests for module gost frame recognizer module.
## @scope Unit testing of dedoc module: module, gost, frame, recognizer.
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
## CLASS 8[Unit tests] => TestGOSTFrameRecognizer
## @usecases
## - [Tests]: QA Agent (Verify) => RunTestsWithTelemetry => DiagnosticTrajectoryVisible
def _module_contract():
    pass
# endregion MODULE_CONTRACT
# GREP_SUMMARY: module, gost, frame, recognizer, TestGOSTFrameRecognizer, test_gost_frame_recognition, test_not_gost_frame, test_coordinates_shift, test_pdf_auto_reader, test_pdf_txtlayer_reader, test_pdf_tabby_reader, unit_test, unittest, LDD_telemetry, semantic_markup, unit_test
# STRUCTURE: ▶ Init → ◇ Execute → ⊕ Verify → ∑ assertions → ⎋ PASS/FAIL


import logging

logger = logging.getLogger(__name__)

import os.path
import unittest
from typing import Optional

import cv2
import numpy as np

import dedoc.utils.parameter_utils as param_utils
from dedoc.data_structures.unstructured_document import UnstructuredDocument
from dedoc.readers.pdf_reader.data_classes.line_with_location import LineWithLocation
from dedoc.readers.pdf_reader.pdf_auto_reader.pdf_auto_reader import PdfAutoReader
from dedoc.readers.pdf_reader.pdf_base_reader import ParametersForParseDoc
from dedoc.readers.pdf_reader.pdf_image_reader.pdf_image_reader import PdfImageReader
from dedoc.readers.pdf_reader.pdf_image_reader.table_recognizer.gost_frame_recognizer import GOSTFrameRecognizer
from dedoc.readers.pdf_reader.pdf_txtlayer_reader.pdf_tabby_reader import PdfTabbyReader
from dedoc.readers.pdf_reader.pdf_txtlayer_reader.pdf_txtlayer_reader import PdfTxtlayerReader
from tests.test_utils import get_test_config


# region CLASS_TestGOSTFrameRecognizer [DOMAIN(7): Testing; CONCEPT(8): UnitTest, LDD_Telemetry; TECH(8): unittest, pytest]
## @purpose Test suite for module, gost, frame, recognizer module.
class TestGOSTFrameRecognizer(unittest.TestCase):

    gost_frame_recognizer = GOSTFrameRecognizer(config=get_test_config())
    test_data_folder = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "data", "tables"))
    pdf_image_reader = PdfImageReader(config=get_test_config())
    pdf_auto_reader = PdfAutoReader(config=get_test_config())
    pdf_txtlayer_reader = PdfTxtlayerReader(config=get_test_config())
    pdf_tabby_reader = PdfTabbyReader(config=get_test_config())

    # region METHOD__get_params_for_parse [DOMAIN(7): Testing; CONCEPT(8): TestInfrastructure; TECH(8): unittest]
    ## @purpose get params for parse.
    def _get_params_for_parse(self, parameters: Optional[dict], file_path: Optional[str]) -> ParametersForParseDoc:
        parameters = parameters if parameters else {}
        file_path = file_path if file_path else ""
        params_for_parse = ParametersForParseDoc(
            language=param_utils.get_param_language(parameters),
            is_one_column_document=param_utils.get_param_is_one_column_document(parameters),
            document_orientation=param_utils.get_param_document_orientation(parameters),
            need_header_footers_analysis=param_utils.get_param_need_header_footers_analysis(parameters),
            need_pdf_table_analysis=param_utils.get_param_need_pdf_table_analysis(parameters),
            first_page=0,
            last_page=0,
            need_binarization=param_utils.get_param_need_binarization(parameters),
            table_type=param_utils.get_param_table_type(parameters),
            with_attachments=param_utils.get_param_with_attachments(parameters),
            attachments_dir=param_utils.get_param_attachments_dir(parameters, file_path),
            need_content_analysis=param_utils.get_param_need_content_analysis(parameters),
            need_gost_frame_analysis=param_utils.get_param_need_gost_frame_analysis(parameters),
            pdf_with_txt_layer=param_utils.get_param_pdf_with_txt_layer(parameters)
        )
        return params_for_parse

    # endregion METHOD__get_params_for_parse
    # region METHOD_test_gost_frame_recognition [DOMAIN(7): Testing; CONCEPT(8): LDD_Telemetry; TECH(8): unittest]
    ## @purpose Verify: gost frame recognition.
    ## @complexity 5
    def test_gost_frame_recognition(self) -> None:
        # LDD TELEMETRY: log execution context before assertions
        print(f"\n--- LDD TRAJECTORY (IMP:7-10) for TestGOSTFrameRecognizer::test_gost_frame_recognition ---")
        print(f"  [LDD_TEST][IMP:8][TestGOSTFrameRecognizer][test_gost_frame_recognition] Test logic executed, entering assertion phase")
        image_names = [
            "gost_frame_1.jpg", "gost_frame_2.png", "gost_frame_3.jpg", "example_with_table6.png", "example_with_table5.png", "example_with_table3.png"
        ]
        gt = [True, True, True, False, False, False]
        for index, image_name in enumerate(image_names):
            path_image = os.path.join(self.test_data_folder, image_name)
            image = cv2.imread(path_image)
            result_image, result_bbox, original_image_shape = self.gost_frame_recognizer.rec_and_clean_frame(image)
            self.assertEqual(not np.array_equal(result_image, image), gt[index])  # check if we cut something from original image or not

    # endregion METHOD_test_gost_frame_recognition
    # region METHOD_test_not_gost_frame [DOMAIN(7): Testing; CONCEPT(8): LDD_Telemetry; TECH(8): unittest]
    ## @purpose Verify: not gost frame.
    ## @complexity 5
    def test_not_gost_frame(self) -> None:
        # LDD TELEMETRY: log execution context before assertions
        print(f"\n--- LDD TRAJECTORY (IMP:7-10) for TestGOSTFrameRecognizer::test_not_gost_frame ---")
        print(f"  [LDD_TEST][IMP:8][TestGOSTFrameRecognizer][test_not_gost_frame] Test logic executed, entering assertion phase")
        path_image = os.path.join(self.test_data_folder, "not_gost_frame.jpg")
        image = cv2.imread(path_image)
        result_image, result_bbox, original_image_shape = self.gost_frame_recognizer.rec_and_clean_frame(image)
        self.assertTrue(abs(result_bbox.x_top_left - 26) < 10)
        self.assertTrue(abs(result_bbox.y_top_left - 26) < 10)
        self.assertTrue(abs(result_bbox.width - 722) < 10)
        self.assertTrue(abs(result_bbox.height - 969) < 10)

    # endregion METHOD_test_not_gost_frame
    # region METHOD_test_coordinates_shift [DOMAIN(7): Testing; CONCEPT(8): LDD_Telemetry; TECH(8): unittest]
    ## @purpose Verify: coordinates shift.
    ## @complexity 5
    def test_coordinates_shift(self) -> None:
        # LDD TELEMETRY: log execution context before assertions
        print(f"\n--- LDD TRAJECTORY (IMP:7-10) for TestGOSTFrameRecognizer::test_coordinates_shift ---")
        print(f"  [LDD_TEST][IMP:8][TestGOSTFrameRecognizer][test_coordinates_shift] Test logic executed, entering assertion phase")
        file_path = os.path.join(self.test_data_folder, "gost_frame_2.png")
        parameters = {"need_gost_frame_analysis": "True"}
        params_for_parse = self._get_params_for_parse(parameters=parameters, file_path=file_path)
        result = self.pdf_image_reader._parse_document(path=file_path, parameters=params_for_parse)
        self.assertTrue(len(result[0]) > 0)
        self.assertTrue(abs(result[0][0].location.bbox.x_top_left - 365) < 10)
        self.assertTrue(abs(result[0][0].location.bbox.y_top_left - 37) < 10)
        self.assertTrue(abs(result[0][1].location.bbox.x_top_left - 84) < 10)
        self.assertTrue(abs(result[0][1].location.bbox.y_top_left - 580) < 10)
        self.assertTrue(len(result[1]) > 0)
        self.assertTrue(abs(result[1][0].location.bbox.x_top_left - 81) < 10)
        self.assertTrue(abs(result[1][0].location.bbox.y_top_left - 49) < 10)

    # endregion METHOD_test_coordinates_shift
    # region METHOD_test_pdf_auto_reader [DOMAIN(7): Testing; CONCEPT(8): LDD_Telemetry; TECH(8): unittest]
    ## @purpose Verify: pdf auto reader.
    ## @complexity 5
    def test_pdf_auto_reader(self) -> None:
        # LDD TELEMETRY: log execution context before assertions
        print(f"\n--- LDD TRAJECTORY (IMP:7-10) for TestGOSTFrameRecognizer::test_pdf_auto_reader ---")
        print(f"  [LDD_TEST][IMP:8][TestGOSTFrameRecognizer][test_pdf_auto_reader] Test logic executed, entering assertion phase")
        file_path = os.path.join(self.test_data_folder, "gost_frame_2.png")
        parameters = {"need_gost_frame_analysis": "True"}
        result = self.pdf_auto_reader.read(file_path=file_path, parameters=parameters)
        self.assertTrue(len(result.tables) == 1)
        self.assertEqual(result.tables[0].cells[0][1].get_text(), "Колонка 2")
        self.assertEqual(result.tables[0].cells[0][2].get_text(), "Колонка 3")
        self.assertEqual(len(result.tables[0].cells), 22)
        self.assertTrue("Название таблицы (продолжение)" in result.lines[0].line)

    # endregion METHOD_test_pdf_auto_reader
    # region METHOD_test_pdf_txtlayer_reader [DOMAIN(7): Testing; CONCEPT(8): LDD_Telemetry; TECH(8): unittest]
    ## @purpose Verify: pdf txtlayer reader.
    ## @complexity 5
    def test_pdf_txtlayer_reader(self) -> None:
        # LDD TELEMETRY: log execution context before assertions
        print(f"\n--- LDD TRAJECTORY (IMP:7-10) for TestGOSTFrameRecognizer::test_pdf_txtlayer_reader ---")
        print(f"  [LDD_TEST][IMP:8][TestGOSTFrameRecognizer][test_pdf_txtlayer_reader] Test logic executed, entering assertion phase")
        file_path = os.path.join(self.test_data_folder, "gost_multipage_table_2.pdf")
        result = self.pdf_txtlayer_reader.read(file_path=file_path, parameters={"need_gost_frame_analysis": "true"})
        self.__check_content(result)
        line: LineWithLocation = result.lines[0]
        self.assertEqual(line.line.strip(), "1. Sample text 1")
        self.assertTrue(abs(line.location.bbox.x_top_left - 212) < 10)
        self.assertTrue(abs(line.location.bbox.y_top_left - 1309) < 10)

    # endregion METHOD_test_pdf_txtlayer_reader
    # region METHOD_test_pdf_tabby_reader [DOMAIN(7): Testing; CONCEPT(8): LDD_Telemetry; TECH(8): unittest]
    ## @purpose Verify: pdf tabby reader.
    ## @complexity 5
    def test_pdf_tabby_reader(self) -> None:
        # LDD TELEMETRY: log execution context before assertions
        print(f"\n--- LDD TRAJECTORY (IMP:7-10) for TestGOSTFrameRecognizer::test_pdf_tabby_reader ---")
        print(f"  [LDD_TEST][IMP:8][TestGOSTFrameRecognizer][test_pdf_tabby_reader] Test logic executed, entering assertion phase")
        file_path = os.path.join(self.test_data_folder, "gost_multipage_table_2.pdf")
        result = self.pdf_tabby_reader.read(file_path=file_path, parameters={"need_gost_frame_analysis": "true"})
        self.__check_content(result)
        line: LineWithLocation = result.lines[0]
        self.assertEqual(line.line.strip(), "1. Sample text 1")
        self.assertTrue(abs(line.location.bbox.x_top_left - 76) < 10)
        self.assertTrue(abs(line.location.bbox.y_top_left - 476) < 10)

    # endregion METHOD_test_pdf_tabby_reader
    # region METHOD___check_content [DOMAIN(7): Testing; CONCEPT(8): TestInfrastructure; TECH(8): unittest]
    ## @purpose check content.
    def __check_content(self, result: UnstructuredDocument) -> None:
        self.assertEqual(len(result.tables), 1)
        self.assertEqual(result.tables[0].cells[0][0].get_text(), "SAMPLE TEXT")
        self.assertTrue(len(result.tables[0].cells[0][0].lines[0].annotations) > 0)
        self.assertEqual(result.tables[0].cells[1][0].get_text(), "1")
        self.assertEqual(len(result.tables[0].cells), 14)

    # endregion METHOD___check_content
# endregion CLASS_TestGOSTFrameRecognizer