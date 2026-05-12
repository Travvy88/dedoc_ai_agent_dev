# region MODULE_CONTRACT [DOMAIN(7): Testing; CONCEPT(9): PDFFormat, OCR, ImageProcessing; TECH(8): unittest]
## @modulecontract
## @purpose Comprehensive Dedoc API PDF/image document tests: OCR, annotations (bold, spacing, confidence, BBox), table extraction, image orientation, binarization, metadata.
## @scope PDF and image formats: scanned PDF, DJVU, PNG, JPG, TIFF — OCR with confidence, annotation extraction, table detection, orientation, binarization.
## @input Document files via Dedoc API upload endpoint.
## @output unittest assertions validating response structure and content.
## @links [USES_API(9): Dedoc /upload endpoint; READS_DATA_FROM(7): tests/data/]
## @invariants
## - All test methods follow arrange-act-assert pattern via _send_request.
## - Test data files reside in tests/data/ subdirectories.
## @rationale
## Q: Why API-level integration tests instead of unit tests?
## A: These tests validate the full pipeline from HTTP request through parsing to structured output, ensuring end-to-end correctness.
## @changes
## LAST_CHANGE: [v1.0.0 – Initial LDD migration: added semantic markup and LDD telemetry]
## @modulemap
## CLASS [API integration test class] => TestApiPdfReader
## @usecases
## - [TestClass]: Developer (Run) => VerifyAPIBehavior => TestPassOrFail
def _module_contract():
    pass
# endregion MODULE_CONTRACT
# GREP_SUMMARY: pdf, scanned, OCR, DJVU, image, annotations, bold, spacing, confidence, BBox, table, orientation, API test
# STRUCTURE: ▶ ┌pdf/image file┐ → ○ _send_request(pdf_with_text_layer, need_binarization) → ⊕ OCR + annotate → ◇ validate bold/spacing/confidence/bbox + table refs → ⎋ structural assertions

import os
import unittest

from dedoc.data_structures.concrete_annotations.bbox_annotation import BBoxAnnotation
from dedoc.data_structures.concrete_annotations.bold_annotation import BoldAnnotation
from dedoc.data_structures.concrete_annotations.confidence_annotation import ConfidenceAnnotation
from dedoc.data_structures.concrete_annotations.spacing_annotation import SpacingAnnotation
from dedoc.utils import supported_image_types
from tests.api_tests.abstract_api_test import AbstractTestApiDocReader


# region CLASS_TestApiPdfReader [DOMAIN(7): Testing, DocumentProcessing; CONCEPT(7): APITest; TECH(7): unittest]
## @purpose API integration tests for Dedoc document processing — TestApiPdfReader.
class TestApiPdfReader(AbstractTestApiDocReader):


# region METHOD__get_abs_path [DOMAIN(6): Testing; CONCEPT(6): Helper; TECH(6): unittest]
## @purpose Helper method for test assertions
## @complexity 4
    def _get_abs_path(self, file_name: str) -> str:
        return os.path.join(self.data_directory_path, "scanned", file_name)

# endregion METHOD__get_abs_path

# region METHOD___check_example_file [DOMAIN(6): Testing; CONCEPT(6): Helper; TECH(6): unittest]
## @purpose Helper method for test assertions
## @complexity 4
    def __check_example_file(self, result: dict) -> None:
        tree = result["content"]["structure"]
        node = self._get_by_tree_path(tree, "0.0")
        self._check_similarity("Пример документа", node["text"].strip().split("\n")[0])
        annotations = node["annotations"]
        annotation_names = {annotation["name"] for annotation in annotations}
        self.assertIn(BoldAnnotation.name, annotation_names)
        self.assertIn(SpacingAnnotation.name, annotation_names)
        self.assertIn(ConfidenceAnnotation.name, annotation_names)
        self.assertIn(BBoxAnnotation.name, annotation_names)

# endregion METHOD___check_example_file

# region METHOD___check_metainfo [DOMAIN(6): Testing; CONCEPT(6): Helper; TECH(6): unittest]
## @purpose Helper method for test assertions
## @complexity 4
    def __check_metainfo(self, metainfo: dict, actual_type: str, actual_name: str) -> None:
        self.assertEqual(metainfo["file_type"], actual_type)
        self.assertEqual(metainfo["file_name"], actual_name)

# endregion METHOD___check_metainfo

# region FUNC_test_pdf [DOMAIN(7): Testing; CONCEPT(7): ResponseValidation; TECH(7): unittest]
## @purpose Verify API response for pdf
## @complexity 6
    def test_pdf(self) -> None:
        file_name = "example.pdf"
        result = self._send_request(file_name, data=dict(with_attachments=True, document_type="", pdf_with_text_layer="false"))
        self.__check_example_file(result)
        self.__check_metainfo(result["metadata"], "application/pdf", file_name)
        print("[LDD_TEST] Test result obtained, proceeding to assertions")
        self.assertEqual([], result["attachments"])

# endregion FUNC_test_pdf

# region FUNC_test_djvu [DOMAIN(7): Testing; CONCEPT(7): ResponseValidation; TECH(7): unittest]
## @purpose Verify API response for djvu
## @complexity 6
    def test_djvu(self) -> None:
        file_name = "example_with_table7.djvu"
        result = self._send_request(file_name, dict(document_type=""))
        tree = result["content"]["structure"]
        self._check_tree_sanity(tree)
        print("[LDD_TEST] Test result obtained, proceeding to assertions")
        self.assertEqual("2. Срок поставки в течении 70 дней с момента внесения авансового платежа.\n", self._get_by_tree_path(tree, "0.3.1")["text"])
        self.assertEqual("3. Срок изготовления не ранее 2018г.\n", self._get_by_tree_path(tree, "0.3.2")["text"])

        self.__check_metainfo(result["metadata"], "image/vnd.djvu", file_name)

# endregion FUNC_test_djvu

# region FUNC_test_djvu_2 [DOMAIN(7): Testing; CONCEPT(7): ResponseValidation; TECH(7): unittest]
## @purpose Verify API response for djvu 2
## @complexity 6
    def test_djvu_2(self) -> None:
        file_name = "example_with_table9.djvu"
        result = self._send_request(file_name)
        content = result["content"]["structure"]
        self._check_tree_sanity(content)
        print("[LDD_TEST] Test result obtained, proceeding to assertions")
        self.assertEqual("Приложение № 1", self._get_by_tree_path(content, "0.0")["text"].split("\n")[0])
        self.assertEqual("Приложение №1 к договору подряда № от 2019г.", self._get_by_tree_path(content, "0.1")["text"].split("\n")[0])
        self.assertEqual("ТЕХНИЧЕСКОЕ ЗАДАНИЕ (ТЗ)", self._get_by_tree_path(content, "0.2")["text"].split("\n")[0])
        self.assertEqual("1. Предмет закупки, источник финансирования :\n", self._get_by_tree_path(content, "0.3.0")["text"])
        self.assertEqual("2.   Место выполнения Работ:\n", self._get_by_tree_path(content, "0.3.1")["text"])

        self.__check_metainfo(result["metadata"], "image/vnd.djvu", file_name)

# endregion FUNC_test_djvu_2

# region FUNC_test_broken_djvu [DOMAIN(7): Testing; CONCEPT(7): ResponseValidation; TECH(7): unittest]
## @purpose Verify API response for broken djvu
## @complexity 6
    def test_broken_djvu(self) -> None:
        file_name = "broken.djvu"
        _ = self._send_request(file_name, expected_code=415)

# endregion FUNC_test_broken_djvu

# region FUNC_test_header_pdf [DOMAIN(7): Testing; CONCEPT(7): ResponseValidation; TECH(7): unittest]
## @purpose Verify API response for header pdf
## @complexity 6
    def test_header_pdf(self) -> None:
        file_name = "header_test.pdf"
        result = self._send_request(file_name, data=dict(pdf_with_text_layer="true"))
        tree = result["content"]["structure"]
        self._check_tree_sanity(tree)
        self._check_similarity("Глава 543", self._get_by_tree_path(tree, "0.0")["text"])
        self._check_similarity("Какой-то текст.", self._get_by_tree_path(tree, "0.1")["text"])
        self._check_similarity("1. Текстового", self._get_by_tree_path(tree, "0.2.0")["text"])
        self._check_similarity("2. Текстового", self._get_by_tree_path(tree, "0.2.1")["text"])
        self._check_similarity("3. Еще текстового", self._get_by_tree_path(tree, "0.2.2")["text"])
        self._check_similarity("4. Пам", self._get_by_tree_path(tree, "0.2.3")["text"])
        self._check_similarity("4.1. авп", self._get_by_tree_path(tree, "0.2.3.0.0")["text"])
        self._check_similarity("4.2. текстового", self._get_by_tree_path(tree, "0.2.3.0.1")["text"])
        self._check_similarity("4.3. п", self._get_by_tree_path(tree, "0.2.3.0.2")["text"])
        self._check_similarity("4.4. п", self._get_by_tree_path(tree, "0.2.3.0.3")["text"])
        self._check_similarity("4.5. п", self._get_by_tree_path(tree, "0.2.3.0.4")["text"])
        self._check_similarity("4.6. п", self._get_by_tree_path(tree, "0.2.3.0.5")["text"])

        self.__check_metainfo(result["metadata"], "application/pdf", file_name)

# endregion FUNC_test_header_pdf

# region FUNC_test_images [DOMAIN(7): Testing; CONCEPT(7): ResponseValidation; TECH(7): unittest]
## @purpose Verify API response for images
## @complexity 6
    def test_images(self) -> None:
        formats = [
            ".png", ".jpg", ".jpeg", ".tiff", ".bmp", ".gif", ".ppm", ".pnm", ".pgm",
            ".pbm", ".webp", ".pcx", ".eps", ".sgi", ".hdr", ".pic", ".sr", ".ras",
            ".dib", ".jpe", ".jfif", ".j2k"
        ]

        for image_format in formats:
            print("[LDD_TEST] Test result obtained, proceeding to assertions")
            self.assertIn(image_format, supported_image_types)
            file_name = "example"
            result = self._send_request(file_name + image_format)
            self.__check_example_file(result)

# endregion FUNC_test_images

# region FUNC_test_image_metadata [DOMAIN(7): Testing; CONCEPT(7): ResponseValidation; TECH(7): unittest]
## @purpose Verify API response for image metadata
## @complexity 6
    def test_image_metadata(self) -> None:
        file_name = "orient_3.png"
        result = self._send_request(file_name)
        print("[LDD_TEST] Test result obtained, proceeding to assertions")
        self.assertEqual(result["metadata"]["exif_image_width"], 1654)
        self.assertEqual(result["metadata"]["exif_image_height"], 2338)
        self.assertIn("rotated_page_angles", result["metadata"])

# endregion FUNC_test_image_metadata

# region FUNC_test_image_binarization [DOMAIN(7): Testing; CONCEPT(7): ResponseValidation; TECH(7): unittest]
## @purpose Verify API response for image binarization
## @complexity 6
    def test_image_binarization(self) -> None:
        result = self._send_request("01_МФО_Наклон.jpg", data=dict(need_binarization="true"))

        print("[LDD_TEST] Test result obtained, proceeding to assertions")
        self.assertIn("ЦЕНТРАЛЬНЫЙ БАНК РОССИЙСКОЙ ФЕДЕРАЦИИ\n", result["content"]["structure"]["subparagraphs"][0]["text"])
        self.assertIn("Е.И Курицына\n(расшифровка подлиси", result["content"]["structure"]["subparagraphs"][-1]["text"])

# endregion FUNC_test_image_binarization

# region FUNC_test_on_ocr_conf_threshold [DOMAIN(7): Testing; CONCEPT(7): ResponseValidation; TECH(7): unittest]
## @purpose Verify API response for on ocr conf threshold
## @complexity 6
    def test_on_ocr_conf_threshold(self) -> None:
        result = self._send_request("with_trash.jpg", data=dict(structure_type="tree"))
        tree = result["content"]["structure"]
        self._check_tree_sanity(tree)
        # check, that handwritten text was filtered
        self._check_similarity("ФИО  года рождения, паспорт: серия \n№ выдан _, дата выдачи\nт. код подразделения зарегистрированный по адресу:\n \n",
                               self._get_by_tree_path(tree, "0.3")["text"])

# endregion FUNC_test_on_ocr_conf_threshold

# region FUNC_test_rotated_image [DOMAIN(7): Testing; CONCEPT(7): ResponseValidation; TECH(7): unittest]
## @purpose Verify API response for rotated image
## @complexity 6
    def test_rotated_image(self) -> None:
        result = self._send_request("orient_1.png", data=dict(need_pdf_table_analysis="false"))
        tree = result["content"]["structure"]
        self._check_tree_sanity(tree)

        print("[LDD_TEST] Test result obtained, proceeding to assertions")
        self.assertIn("Приложение к Положению о порядке\n", tree["subparagraphs"][0]["text"])

# endregion FUNC_test_rotated_image

# region FUNC_test_pdf_with_only_mp_table [DOMAIN(7): Testing; CONCEPT(7): ResponseValidation; TECH(7): unittest]
## @purpose Verify API response for pdf with only mp table
## @complexity 6
    def test_pdf_with_only_mp_table(self) -> None:
        file_name = os.path.join("..", "tables", "multipage_table.pdf")
        result = self._send_request(file_name)

        table_refs = [ann["value"] for ann in result["content"]["structure"]["subparagraphs"][0]["annotations"] if ann["name"] == "table"]

        print("[LDD_TEST] Test result obtained, proceeding to assertions")
        self.assertTrue(len(result["content"]["tables"]), len(table_refs))
        for table in result["content"]["tables"]:
            self.assertTrue(table["metadata"]["uid"] in table_refs)

# endregion FUNC_test_pdf_with_only_mp_table

# region FUNC_test_pdf_with_some_tables [DOMAIN(7): Testing; CONCEPT(7): ResponseValidation; TECH(7): unittest]
## @purpose Verify API response for pdf with some tables
## @complexity 6
    def test_pdf_with_some_tables(self) -> None:
        file_name = os.path.join("..", "pdf_with_text_layer", "VVP_6_tables.pdf")
        result = self._send_request(file_name, data={"pdf_with_text_layer": "true"})
        tree = result["content"]["structure"]
        self._check_tree_sanity(tree)
        self._test_table_refs(result["content"])

        # checks indentations
        par = self._get_by_tree_path(tree, "0.4.0.0")
        annotations = par["annotations"]
        print("[LDD_TEST] Test result obtained, proceeding to assertions")
        self.assertIn({"end": 170, "value": "600", "name": "indentation", "start": 0}, annotations)
        self.assertIn("Методика расчета ВВП по доходам характеризуется суммой национального\n", par["text"])

# endregion FUNC_test_pdf_with_some_tables

# region FUNC_test_pdf_with_only_table [DOMAIN(7): Testing; CONCEPT(7): ResponseValidation; TECH(7): unittest]
## @purpose Verify API response for pdf with only table
## @complexity 6
    def test_pdf_with_only_table(self) -> None:
        file_name = os.path.join("..", "pdf_with_text_layer", "VVP_global_table.pdf")
        result = self._send_request(file_name)

        print("[LDD_TEST] Test result obtained, proceeding to assertions")
        self.assertEqual(result["content"]["tables"][0]["metadata"]["uid"], result["content"]["structure"]["subparagraphs"][0]["annotations"][0]["value"])
# endregion FUNC_test_pdf_with_only_table

# region FUNC_test_2_columns [DOMAIN(7): Testing; CONCEPT(7): ResponseValidation; TECH(7): unittest]
## @purpose Verify API response for 2 columns
## @complexity 6

    @unittest.skip("TLDR-768 Жирность на сканах не работает -> Отсюда классификатор параграфов может сработать неверно")
    def test_2_columns(self) -> None:
        file_name = os.path.join("..", "scanned", "example_2_columns.png")
        result = self._send_request(file_name)
        tree = result["content"]["structure"]
        self._check_tree_sanity(tree)
        print("[LDD_TEST] Test result obtained, proceeding to assertions")
        self.assertEqual(797, len(self._get_by_tree_path(tree, "0.0")["text"]))

# endregion FUNC_test_2_columns

# region FUNC_test_document_orientation [DOMAIN(7): Testing; CONCEPT(7): ResponseValidation; TECH(7): unittest]
## @purpose Verify API response for document orientation
## @complexity 6
    def test_document_orientation(self) -> None:
        file_name = "orient_3.png"
        result = self._send_request(file_name, data=dict(document_orientation="auto"))
        tree = result["content"]["structure"]
        self._check_similarity(tree["subparagraphs"][0]["text"], "Приложение к постановлению\n"
                                                                 "Губернатора Камчатского края")

# endregion FUNC_test_document_orientation

# region FUNC_test_bold_annotation [DOMAIN(7): Testing; CONCEPT(7): ResponseValidation; TECH(7): unittest]
## @purpose Verify API response for bold annotation
## @complexity 6
    def test_bold_annotation(self) -> None:
        file_name = "bold_font.png"
        result = self._send_request(file_name)
        tree = result["content"]["structure"]

        node = tree["subparagraphs"][0]
        bold_annotations = [annotation for annotation in node["annotations"] if annotation["name"] == "bold" and annotation["value"] == "True"]
        print("[LDD_TEST] Test result obtained, proceeding to assertions")
        self.assertEqual(len(bold_annotations), 1)
        self.assertEqual((bold_annotations[0]["start"], bold_annotations[0]["end"]), (8, 12))
        node = tree["subparagraphs"][1]
        bold_annotations = [annotation for annotation in node["annotations"] if annotation["name"] == "bold" and annotation["value"] == "True"]
        self.assertEqual(len(bold_annotations), 1)
        self.assertEqual((bold_annotations[0]["start"], bold_annotations[0]["end"]), (0, 4))
        node = tree["subparagraphs"][2]
        bold_annotations = [annotation for annotation in node["annotations"] if annotation["name"] == "bold" and annotation["value"] == "True"]
        self.assertEqual(len(bold_annotations), 1)
        self.assertEqual((bold_annotations[0]["start"], bold_annotations[0]["end"]), (0, 15))

# endregion FUNC_test_bold_annotation
# endregion CLASS_TestApiPdfReader