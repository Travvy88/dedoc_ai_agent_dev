# region MODULE_CONTRACT [DOMAIN(7): Testing; CONCEPT(7): PDFAutoDetection, TextLayer; TECH(7): unittest]
## @modulecontract
## @purpose Test Dedoc API auto-detection of PDF text layer presence, verifying correct reader selection (tabby vs OCR).
## @scope PDF text layer auto-detection: distinguishing PDFs with/without embedded text, reader selection.
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
## CLASS [API integration test class] => TestApiPdfAutoTextLayer
## @usecases
## - [TestClass]: Developer (Run) => VerifyAPIBehavior => TestPassOrFail
def _module_contract():
    pass
# endregion MODULE_CONTRACT
# GREP_SUMMARY: pdf, auto, text layer, detection, tabby, OCR, reader selection, API test
# STRUCTURE: ▶ ┌pdf (mixed types)┐ → ○ _send_request(pdf_with_text_layer=auto) → ⊕ auto-detect text layer → ◇ select correct reader → ⎋ output validation

import os
from typing import List

from tests.api_tests.abstract_api_test import AbstractTestApiDocReader


# region CLASS_TestApiPdfAutoTextLayer [DOMAIN(7): Testing, DocumentProcessing; CONCEPT(7): APITest; TECH(7): unittest]
## @purpose API integration tests for Dedoc document processing — TestApiPdfAutoTextLayer.
class TestApiPdfAutoTextLayer(AbstractTestApiDocReader):


# region METHOD__get_abs_path [DOMAIN(6): Testing; CONCEPT(6): Helper; TECH(6): unittest]
## @purpose Helper method for test assertions
## @complexity 4
    def _get_abs_path(self, file_name: str) -> str:
        return os.path.join(self.data_directory_path, "pdf_auto", file_name)

# endregion METHOD__get_abs_path

# region FUNC_test_pdf_auto_auto_columns [DOMAIN(7): Testing; CONCEPT(7): ResponseValidation; TECH(7): unittest]
## @purpose Verify API response for pdf auto auto columns
## @complexity 6
    def test_pdf_auto_auto_columns(self) -> None:
        file_name = "0004057v1.pdf"
        parameters = dict(with_attachments=True, pdf_with_text_layer="auto", is_one_column_document="auto")
        result = self._send_request(file_name, parameters)
        warnings = self.__prepare_warnings(result["warnings"])
        print("[LDD_TEST] Test result obtained, proceeding to assertions")
        self.assertIn("Assume document has correct textual layer on pages [1:]", warnings)

# endregion FUNC_test_pdf_auto_auto_columns

# region FUNC_test_pdf_auto_auto_columns_each_page_have_different_columns [DOMAIN(7): Testing; CONCEPT(7): ResponseValidation; TECH(7): unittest]
## @purpose Verify API response for pdf auto auto columns each page have different columns
## @complexity 6
    def test_pdf_auto_auto_columns_each_page_have_different_columns(self) -> None:
        file_name = "liao2020_merged_organized.pdf"
        parameters = dict(with_attachments=True, pdf_with_text_layer="auto", is_one_column_document="auto")
        result = self._send_request(file_name, parameters)
        warnings = self.__prepare_warnings(result["warnings"])
        print("[LDD_TEST] Test result obtained, proceeding to assertions")
        self.assertIn("Assume document has correct textual layer on pages [1:]", warnings)

# endregion FUNC_test_pdf_auto_auto_columns_each_page_have_different_columns

# region FUNC_test_pdf_auto_auto_columns_each_page_have_same_columns_except_first [DOMAIN(7): Testing; CONCEPT(7): ResponseValidation; TECH(7): unittest]
## @purpose Verify API response for pdf auto auto columns each page have same columns except first
## @complexity 6
    def test_pdf_auto_auto_columns_each_page_have_same_columns_except_first(self) -> None:
        file_name = "liao2020_merged-1-5.pdf"
        parameters = dict(with_attachments=True, pdf_with_text_layer="auto", is_one_column_document="auto")
        result = self._send_request(file_name, parameters)
        warnings = self.__prepare_warnings(result["warnings"])
        print("[LDD_TEST] Test result obtained, proceeding to assertions")
        self.assertIn("Assume document has correct textual layer on pages [1:]", warnings)

# endregion FUNC_test_pdf_auto_auto_columns_each_page_have_same_columns_except_first

# region FUNC_test_pdf_auto_text_layer_2 [DOMAIN(7): Testing; CONCEPT(7): ResponseValidation; TECH(7): unittest]
## @purpose Verify API response for pdf auto text layer 2
## @complexity 6
    def test_pdf_auto_text_layer_2(self) -> None:
        file_name = "e09d__cs-pspc-xg-15p-portable-radio-quick-guide.pdf"
        result = self._send_request(file_name, dict(with_attachments=True, pdf_with_text_layer="auto"))
        warnings = self.__prepare_warnings(result["warnings"])
        print("[LDD_TEST] Test result obtained, proceeding to assertions")
        self.assertIn("Assume document has correct textual layer on pages [1:]", warnings)

# endregion FUNC_test_pdf_auto_text_layer_2

# region FUNC_test_auto_pdf_with_scans [DOMAIN(7): Testing; CONCEPT(7): ResponseValidation; TECH(7): unittest]
## @purpose Verify API response for auto pdf with scans
## @complexity 6
    def test_auto_pdf_with_scans(self) -> None:
        file_name = "tz_scan_1page.pdf"
        result = self._send_request(file_name, dict(pdf_with_text_layer="auto"))
        tree = result["content"]["structure"]
        self._check_tree_sanity(tree)
        print("[LDD_TEST] Test result obtained, proceeding to assertions")
        self.assertIn("Техническое задание", self._get_by_tree_path(tree, "0.0")["text"])

# endregion FUNC_test_auto_pdf_with_scans

# region FUNC_test_auto_pdf_with_text_layer [DOMAIN(7): Testing; CONCEPT(7): ResponseValidation; TECH(7): unittest]
## @purpose Verify API response for auto pdf with text layer
## @complexity 6
    def test_auto_pdf_with_text_layer(self) -> None:
        file_name = os.path.join("..", "pdf_with_text_layer", "english_doc.pdf")
        result = self._send_request(file_name, dict(pdf_with_text_layer="auto"))
        warnings = self.__prepare_warnings(result["warnings"])
        print("[LDD_TEST] Test result obtained, proceeding to assertions")
        self.assertIn("Assume document has correct textual layer on pages [1:]", warnings)
        self._check_english_doc(result)

# endregion FUNC_test_auto_pdf_with_text_layer

# region FUNC_test_auto_pdf_with_wrong_text_layer [DOMAIN(7): Testing; CONCEPT(7): ResponseValidation; TECH(7): unittest]
## @purpose Verify API response for auto pdf with wrong text layer
## @complexity 6
    def test_auto_pdf_with_wrong_text_layer(self) -> None:
        file_name = "english_doc_bad_text.pdf"
        result = self._send_request(file_name, dict(pdf_with_text_layer="auto"))
        warnings = self.__prepare_warnings(result["warnings"])
        print("[LDD_TEST] Test result obtained, proceeding to assertions")
        self.assertIn("Assume document has incorrect textual layer on pages [1:]", warnings)
        self._check_english_doc(result)

# endregion FUNC_test_auto_pdf_with_wrong_text_layer

# region FUNC_test_auto_document_mixed [DOMAIN(7): Testing; CONCEPT(7): ResponseValidation; TECH(7): unittest]
## @purpose Verify API response for auto document mixed
## @complexity 6
    def test_auto_document_mixed(self) -> None:
        file_name = "mixed_pdf.pdf"
        for pdf_with_text_layer in "auto", "auto_tabby":
            result = self._send_request(file_name, dict(pdf_with_text_layer=pdf_with_text_layer))
            warnings = self.__prepare_warnings(result["warnings"])
            print("[LDD_TEST] Test result obtained, proceeding to assertions")
            self.assertIn("Assume document has incorrect textual layer on pages [1:1]", warnings)
            self.assertIn("Assume document has correct textual layer on pages [2:]", warnings)
            self._check_english_doc(result)
            structure = result["content"]["structure"]
            list_items = structure["subparagraphs"][1]["subparagraphs"]
            self.assertEqual("3) продолжаем список\n", list_items[2]["text"])
            self.assertEqual("4) Список идёт своим чередом\n", list_items[3]["text"])
            self.assertEqual("5) заканчиваем список\n", list_items[4]["text"])
            self.assertEqual("6) последний элемент списка.\n", list_items[5]["text"])

# endregion FUNC_test_auto_document_mixed

# region FUNC_test_auto_partially_read [DOMAIN(7): Testing; CONCEPT(7): ResponseValidation; TECH(7): unittest]
## @purpose Verify API response for auto partially read
## @complexity 6
    def test_auto_partially_read(self) -> None:
        file_name = "mixed_pdf.pdf"
        data = {"pdf_with_text_layer": "auto", "pages": "2:"}
        result = self._send_request(file_name, data)
        structure = result["content"]["structure"]
        print("[LDD_TEST] Test result obtained, proceeding to assertions")
        self.assertEqual("", structure["subparagraphs"][0]["text"])
        list_items = structure["subparagraphs"][0]["subparagraphs"]
        self.assertEqual("3) продолжаем список\n", list_items[0]["text"])
        self.assertEqual("4) Список идёт своим чередом\n", list_items[1]["text"])
        self.assertEqual("5) заканчиваем список\n", list_items[2]["text"])
        self.assertEqual("6) последний элемент списка.\n", list_items[3]["text"])

# endregion FUNC_test_auto_partially_read

# region FUNC_test_simple_textual_layer_detection [DOMAIN(7): Testing; CONCEPT(7): ResponseValidation; TECH(7): unittest]
## @purpose Verify API response for simple textual layer detection
## @complexity 6
    def test_simple_textual_layer_detection(self) -> None:
        file_name = "0004057v1.pdf"
        parameters = dict(pdf_with_text_layer="auto", textual_layer_classifier="simple")
        result = self._send_request(file_name, parameters)
        warnings = self.__prepare_warnings(result["warnings"])
        print("[LDD_TEST] Test result obtained, proceeding to assertions")
        self.assertIn("Assume document has correct textual layer on pages [1:]", warnings)
        self.assertIn("FinTOC-2019", result["content"]["structure"]["subparagraphs"][0]["text"])

        file_name = "tz_scan_1page.pdf"
        parameters = dict(pdf_with_text_layer="auto_tabby", textual_layer_classifier="simple")
        result = self._send_request(file_name, parameters)
        warnings = self.__prepare_warnings(result["warnings"])
        self.assertIn("Assume document has incorrect textual layer on pages [1:]", warnings)

        file_name = "mixed_pdf.pdf"
        parameters = dict(pdf_with_text_layer="auto", textual_layer_classifier="simple")
        result = self._send_request(file_name, parameters)
        warnings = self.__prepare_warnings(result["warnings"])
        self.assertIn("Assume document has incorrect textual layer on pages [1:1]", warnings)
        self.assertIn("Assume document has correct textual layer on pages [2:]", warnings)

# endregion FUNC_test_simple_textual_layer_detection

# region FUNC_test_letter_textual_layer_detection [DOMAIN(7): Testing; CONCEPT(7): ResponseValidation; TECH(7): unittest]
## @purpose Verify API response for letter textual layer detection
## @complexity 6
    def test_letter_textual_layer_detection(self) -> None:
        file_name = "prospectus_merged.pdf"
        parameters = dict(each_page_textual_layer_detection=True, textual_layer_classifier="letter", language="eng")
        result = self._send_request(file_name, parameters)
        warnings = self.__prepare_warnings(result["warnings"])
        print("[LDD_TEST] Test result obtained, proceeding to assertions")
        self.assertIn("Assume document has correct textual layer on pages [1:7]", warnings)
        self.assertIn("Assume document has incorrect textual layer on pages [8:8]", warnings)
        self.assertIn("Assume document has correct textual layer on pages [9:9]", warnings)

# endregion FUNC_test_letter_textual_layer_detection

# region FUNC_test_each_page_textual_layer_detection [DOMAIN(7): Testing; CONCEPT(7): ResponseValidation; TECH(7): unittest]
## @purpose Verify API response for each page textual layer detection
## @complexity 6
    def test_each_page_textual_layer_detection(self) -> None:
        file_name = "prospectus_merged.pdf"
        parameters = dict(each_page_textual_layer_detection=True)
        result = self._send_request(file_name, parameters)
        warnings = self.__prepare_warnings(result["warnings"])
        print("[LDD_TEST] Test result obtained, proceeding to assertions")
        self.assertIn("Assume document has correct textual layer on pages [1:6]", warnings)
        self.assertIn("Assume document has incorrect textual layer on pages [7:8]", warnings)
        self.assertIn("Assume document has correct textual layer on pages [9:9]", warnings)

        parameters = dict(each_page_textual_layer_detection=True, textual_layer_classifier="simple")
        result = self._send_request(file_name, parameters)
        warnings = self.__prepare_warnings(result["warnings"])
        self.assertIn("Assume document has correct textual layer on pages [1:7]", warnings)
        self.assertIn("Assume document has incorrect textual layer on pages [8:8]", warnings)
        self.assertIn("Assume document has correct textual layer on pages [9:9]", warnings)

        parameters = dict(each_page_textual_layer_detection=True, pages=":5")
        result = self._send_request(file_name, parameters)
        warnings = self.__prepare_warnings(result["warnings"])
        self.assertIn("Assume document has correct textual layer on pages [1:5]", warnings)

        parameters = dict(each_page_textual_layer_detection=True, pages="5:8")
        result = self._send_request(file_name, parameters)
        warnings = self.__prepare_warnings(result["warnings"])
        self.assertIn("Assume document has correct textual layer on pages [5:6]", warnings)
        self.assertIn("Assume document has incorrect textual layer on pages [7:8]", warnings)

        parameters = dict(each_page_textual_layer_detection=True, pages="7:8")
        result = self._send_request(file_name, parameters)
        warnings = self.__prepare_warnings(result["warnings"])
        self.assertIn("Assume document has incorrect textual layer on pages [7:8]", warnings)

        parameters = dict(each_page_textual_layer_detection=True, pages="7:")
        result = self._send_request(file_name, parameters)
        warnings = self.__prepare_warnings(result["warnings"])
        self.assertIn("Assume document has incorrect textual layer on pages [7:8]", warnings)
        self.assertIn("Assume document has correct textual layer on pages [9:9]", warnings)

# endregion FUNC_test_each_page_textual_layer_detection

# region METHOD___prepare_warnings [DOMAIN(6): Testing; CONCEPT(6): Helper; TECH(6): unittest]
## @purpose Helper method for test assertions
## @complexity 4
    def __prepare_warnings(self, warnings: List[str]) -> List[str]:
        preprocessed_warnings = []
        for warning in warnings:
            if not warning.startswith("Assume document"):
                continue

            words = warning.split()
            warning = " ".join(words[:2] + words[3:])
            preprocessed_warnings.append(warning)
        return preprocessed_warnings

# endregion METHOD___prepare_warnings
# endregion CLASS_TestApiPdfAutoTextLayer