# region MODULE_CONTRACT [DOMAIN(7): Testing; CONCEPT(7): PDFTextLayer, NativePDF; TECH(7): unittest]
## @modulecontract
## @purpose Verify Dedoc API processing of PDFs with embedded text layers, including PDF/A format handling.
## @scope PDF with native text: text extraction, structure construction, PDF/A support.
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
## CLASS [API integration test class] => TestApiPdfWithText
## @usecases
## - [TestClass]: Developer (Run) => VerifyAPIBehavior => TestPassOrFail
def _module_contract():
    pass
# endregion MODULE_CONTRACT
# GREP_SUMMARY: pdf, text layer, PDF/A, native text, structure, API test
# STRUCTURE: ▶ ┌pdf_with_text_layer┐ → ○ _send_request(pdf_with_text_layer=true) → ⊕ text extraction + structure → ⎋ validation

import os
from typing import List

from tests.api_tests.abstract_api_test import AbstractTestApiDocReader


# region CLASS_TestApiPdfWithText [DOMAIN(7): Testing, DocumentProcessing; CONCEPT(7): APITest; TECH(7): unittest]
## @purpose API integration tests for Dedoc document processing — TestApiPdfWithText.
class TestApiPdfWithText(AbstractTestApiDocReader):


# region METHOD__get_abs_path [DOMAIN(6): Testing; CONCEPT(6): Helper; TECH(6): unittest]
## @purpose Helper method for test assertions
## @complexity 4
    def _get_abs_path(self, file_name: str) -> str:
        return os.path.join(self.data_directory_path, "pdf_with_text_layer", file_name)

# endregion METHOD__get_abs_path

# region METHOD___filter_by_name [DOMAIN(6): Testing; CONCEPT(6): Helper; TECH(6): unittest]
## @purpose Helper method for test assertions
## @complexity 4
    def __filter_by_name(self, annotations: List[dict], name: str) -> List[dict]:
        return [annotation for annotation in annotations if annotation["name"] == name]

# endregion METHOD___filter_by_name

# region METHOD___get_annotation_names [DOMAIN(6): Testing; CONCEPT(6): Helper; TECH(6): unittest]
## @purpose Helper method for test assertions
## @complexity 4
    def __get_annotation_names(self, annotations: List[dict]) -> List[str]:
        return [annotation["name"] for annotation in annotations]

# endregion METHOD___get_annotation_names

# region METHOD___extract_node_with_annotation [DOMAIN(6): Testing; CONCEPT(6): Helper; TECH(6): unittest]
## @purpose Helper method for test assertions
## @complexity 4
    def __extract_node_with_annotation(self, tree: dict, node_id: str, ann_name: str) -> List[dict]:
        node_with_annotation = self._get_by_tree_path(tree["content"]["structure"], node_id)
        return self.__filter_by_name(node_with_annotation["annotations"], ann_name)

# endregion METHOD___extract_node_with_annotation

# region FUNC_test_ref_tables [DOMAIN(7): Testing; CONCEPT(7): ResponseValidation; TECH(7): unittest]
## @purpose Verify API response for ref tables
## @complexity 6
    def test_ref_tables(self) -> None:
        result = self._send_request("example.pdf", dict(pdf_with_text_layer="true"))
        tables_uids = [table["metadata"]["uid"] for table in result["content"]["tables"]]
        print("[LDD_TEST] Test result obtained, proceeding to assertions")
        self.assertEqual(len(tables_uids), 2)
        ref0 = self.__extract_node_with_annotation(result, "0.6.2", "table")[0]["value"]
        ref1 = self.__extract_node_with_annotation(result, "0.6.2.0", "table")[0]["value"]
        self.assertEqual(ref0, tables_uids[0])
        self.assertEqual(ref1, tables_uids[1])

        result = self._send_request("example.pdf", dict(pdf_with_text_layer="tabby"))
        tables_uids = [table["metadata"]["uid"] for table in result["content"]["tables"]]
        self.assertEqual(len(tables_uids), 2)
        annotations = self.__extract_node_with_annotation(result, "0.7.2", "table")
        ref0 = annotations[0]["value"]
        ref1 = annotations[1]["value"]
        self.assertEqual(ref0, tables_uids[0])
        self.assertEqual(ref1, tables_uids[1])

# endregion FUNC_test_ref_tables

# region FUNC_test_pdf_with_text_style [DOMAIN(7): Testing; CONCEPT(7): ResponseValidation; TECH(7): unittest]
## @purpose Verify API response for pdf with text style
## @complexity 6
    def test_pdf_with_text_style(self) -> None:
        file_name = "diff_styles.pdf"
        result = self._send_request(file_name, dict(pdf_with_text_layer="true", document_type="", need_pdf_table_analysis="false"))
        tree = result["content"]["structure"]
        self._check_tree_sanity(tree)

        node = self._get_by_tree_path(tree, "0.0.0")
        print("[LDD_TEST] Test result obtained, proceeding to assertions")
        self.assertEqual("1.1TimesNewRomanItalicBold20\n", node["text"])
        self.assertIn({"start": 0, "end": 28, "name": "size", "value": "20.0"}, node["annotations"])
        annotation_names = self.__get_annotation_names(node["annotations"])
        self.assertListEqual(["bounding box", "style", "size", "color_annotation", "spacing"], annotation_names)

        node = self._get_by_tree_path(tree, "0.0.0.0")
        annotations_size = self.__filter_by_name(name="size", annotations=node["annotations"])
        self.assertIn({"start": 0, "end": 26, "name": "size", "value": "16.0"}, annotations_size)
        self.assertEqual(len(node["annotations"]), 6)
        annotation_names = self.__get_annotation_names(node["annotations"])
        self.assertEqual("Different styles(Arial16):\n", node["text"])
        self.assertListEqual(["bounding box", "bounding box", "style", "size", "color_annotation", "spacing"], annotation_names)

        node = self._get_by_tree_path(tree, "0.1.2")
        self.assertEqual("3. TimesNewRomanItalic14, Calibri18, Tahoma16\n", node["text"])
        self.assertEqual("3. ", node["text"][0:3])
        self.assertIn({"start": 0, "end": 36, "name": "style", "value": "TimesNewRomanPSMT"}, node["annotations"])
        self.assertIn({"start": 0, "end": 2, "name": "size", "value": "16.0"}, node["annotations"])
        self.assertEqual("TimesNewRomanItalic14, ", node["text"][3:26])
        self.assertIn({"start": 0, "end": 36, "name": "style", "value": "TimesNewRomanPSMT"}, node["annotations"])
        self.assertIn({"start": 3, "end": 25, "name": "size", "value": "14.0"}, node["annotations"])
        self.assertEqual("Calibri18, ", node["text"][26:37])
        self.assertIn({"start": 0, "end": 36, "name": "style", "value": "TimesNewRomanPSMT"}, node["annotations"])
        self.assertIn({"start": 26, "end": 36, "value": "18.0", "name": "size"}, node["annotations"])
        self.assertEqual("Tahoma16\n", node["text"][37:46])
        self.assertIn({"start": 37, "end": 45, "value": "Tahoma", "name": "style"}, node["annotations"])
        self.assertIn({"start": 37, "end": 45, "name": "size", "value": "16.0"}, node["annotations"])
        self.assertEqual(12, len(node["annotations"]))

        word_bboxes = self.__filter_by_name(node["annotations"], "bounding box")
        self.assertEqual(len(word_bboxes), 4)
        self.assertEqual("3.", node["text"][word_bboxes[0]["start"]:word_bboxes[0]["end"]])
        self.assertEqual("TimesNewRomanItalic14,", node["text"][word_bboxes[1]["start"]:word_bboxes[1]["end"]])
        self.assertEqual("Calibri18,", node["text"][word_bboxes[2]["start"]:word_bboxes[2]["end"]])
        self.assertEqual("Tahoma16", node["text"][word_bboxes[3]["start"]:word_bboxes[3]["end"]])

# endregion FUNC_test_pdf_with_text_style

# region FUNC_test_pdf_with_text_style_2 [DOMAIN(7): Testing; CONCEPT(7): ResponseValidation; TECH(7): unittest]
## @purpose Verify API response for pdf with text style 2
## @complexity 6
    def test_pdf_with_text_style_2(self) -> None:
        file_name = "2-column-state.pdf"
        result = self._send_request(file_name, dict(pdf_with_text_layer="true", need_pdf_table_analysis="false"))
        tree = result["content"]["structure"]
        self._check_tree_sanity(tree)
        subs = tree["subparagraphs"]
        sub = self._get_by_tree_path(tree, "0.0")
        print("[LDD_TEST] Test result obtained, proceeding to assertions")
        self.assertEqual("Compromising Tor Anonymity\n", sub["text"][0:27])
        annotations_size = self.__filter_by_name(name="size", annotations=subs[0]["annotations"])
        self.assertIn({"start": 0, "end": 61, "name": "size", "value": "18.0"}, annotations_size)

        annotations_style = self.__filter_by_name(name="style", annotations=subs[0]["annotations"])
        self.assertIn({"start": 0, "end": 61, "name": "style", "value": "Helvetica-Bold"}, annotations_style)

        annotations_bold = self.__filter_by_name(name="bold", annotations=subs[0]["annotations"])
        self.assertIn({"start": 0, "end": 61, "name": "bold", "value": "True"}, annotations_bold)

        self.assertIn("Pere Manils, Abdelberi Chaabane, Stevens Le Blond,", self._get_by_tree_path(tree, "0.1")["text"])

# endregion FUNC_test_pdf_with_text_style_2

# region FUNC_test_pdf_with_2_columns_text [DOMAIN(7): Testing; CONCEPT(7): ResponseValidation; TECH(7): unittest]
## @purpose Verify API response for pdf with 2 columns text
## @complexity 6
    def test_pdf_with_2_columns_text(self) -> None:
        file_name = "2-column-state.pdf"
        result = self._send_request(file_name, dict(pdf_with_text_layer="tabby", document_type=""))

        tree = result["content"]["structure"]
        self._check_tree_sanity(tree)
        print("[LDD_TEST] Test result obtained, proceeding to assertions")
        self.assertIn("Privacy of users in P2P networks goes far beyond their\n"
                      "current usage and is a fundamental requirement to the adop-\n"
                      "tion of P2P protocols for legal usage. In a climate of cold",
                      self._get_by_tree_path(tree, "0.5")["text"])

        self.assertIn("Keywords", self._get_by_tree_path(tree, "0.6")["text"])
        self.assertIn("Anonymizing Networks, Privacy, Tor, BitTorrent", self._get_by_tree_path(tree, "0.7")["text"])

        self.assertIn("INTRODUCTION\n", self._get_by_tree_path(tree, "0.8.0")["text"])
        self.assertIn("The Tor network was designed to provide freedom\n"
                      "of speech by guaranteeing anonymous communications.\n"
                      "Whereas the cryptographic foundations of Tor, based on\n"
                      "onion-routing [3, 9, 22, 24], are known to be robust, identity",
                      self._get_by_tree_path(tree, "0.8.0.0")["text"])

# endregion FUNC_test_pdf_with_2_columns_text

# region FUNC_test_pdf_with_2_columns_text_2 [DOMAIN(7): Testing; CONCEPT(7): ResponseValidation; TECH(7): unittest]
## @purpose Verify API response for pdf with 2 columns text 2
## @complexity 6
    def test_pdf_with_2_columns_text_2(self) -> None:
        file_name = "liters_state.pdf"
        result = self._send_request(file_name, dict(pdf_with_text_layer="true", need_pdf_table_analysis="false"))

        tree = result["content"]["structure"]

        print("[LDD_TEST] Test result obtained, proceeding to assertions")
        self.assertIn("References", self._get_by_tree_path(tree, "0.0")["text"])
        self.assertIn("[1] Navaneeth Bodla, Bharat Singh, Rama Chellappa, and", self._get_by_tree_path(tree, "0.1")["text"])

# endregion FUNC_test_pdf_with_2_columns_text_2

# region FUNC_test_pdf_with_some_tables [DOMAIN(7): Testing; CONCEPT(7): ResponseValidation; TECH(7): unittest]
## @purpose Verify API response for pdf with some tables
## @complexity 6
    def test_pdf_with_some_tables(self) -> None:
        file_name = "VVP_6_tables.pdf"
        result = self._send_request(file_name, dict(pdf_with_text_layer="true"))
        content = result["content"]
        self._test_table_refs(content)
        tree = content["structure"]
        self._check_tree_sanity(tree)

        # checks indentations
        par = self._get_by_tree_path(tree, "0.4.0.0")
        print("[LDD_TEST] Test result obtained, proceeding to assertions")
        self.assertIn({"end": 170, "value": "600", "name": "indentation", "start": 0}, par["annotations"])
        self.assertIn("Методика расчета ВВП по доходам характеризуется суммой национального\n", par["text"])

# endregion FUNC_test_pdf_with_some_tables

# region FUNC_test_pdf_with_only_table [DOMAIN(7): Testing; CONCEPT(7): ResponseValidation; TECH(7): unittest]
## @purpose Verify API response for pdf with only table
## @complexity 6
    def test_pdf_with_only_table(self) -> None:
        file_name = "VVP_global_table.pdf"
        result = self._send_request(file_name, dict(pdf_with_text_layer="true"))

        print("[LDD_TEST] Test result obtained, proceeding to assertions")
        self.assertEqual(result["content"]["tables"][0]["metadata"]["uid"], result["content"]["structure"]["subparagraphs"][0]["annotations"][0]["value"])

# endregion FUNC_test_pdf_with_only_table

# region FUNC_test_pdf_with_only_mp_table [DOMAIN(7): Testing; CONCEPT(7): ResponseValidation; TECH(7): unittest]
## @purpose Verify API response for pdf with only mp table
## @complexity 6
    def test_pdf_with_only_mp_table(self) -> None:
        file_name = os.path.join("..", "tables", "multipage_table.pdf")
        result = self._send_request(file_name, dict(pdf_with_text_layer="true", need_header_footer_analysis=True))

        table_refs = [ann["value"] for ann in result["content"]["structure"]["subparagraphs"][0]["annotations"] if ann["name"] == "table"]

        print("[LDD_TEST] Test result obtained, proceeding to assertions")
        self.assertTrue(len(result["content"]["tables"]), len(table_refs))
        for table in result["content"]["tables"]:
            self.assertTrue(table["metadata"]["uid"] in table_refs)

# endregion FUNC_test_pdf_with_only_mp_table

# region FUNC_test_pdf_tabby_with_header_footer [DOMAIN(7): Testing; CONCEPT(7): ResponseValidation; TECH(7): unittest]
## @purpose Verify API response for pdf tabby with header footer
## @complexity 6
    def test_pdf_tabby_with_header_footer(self) -> None:
        file_name = "riscv-spec-v2.2.pdf"
        result = self._send_request(file_name, dict(pdf_with_text_layer="tabby", need_header_footer_analysis=True, pages="10:25"))

        tree = result["content"]["structure"]
        self._check_tree_sanity(tree)

        # page 1 without a header
        node = self._get_by_tree_path(tree, "0.0")
        print("[LDD_TEST] Test result obtained, proceeding to assertions")
        self.assertEqual("16 “P” Standard Extension for Packed-SIMD Instructions, Version 0.1 91\n", node["text"])

        # page 2 without a header
        node = self._get_by_tree_path(tree, "0.2.18")
        self.assertEqual("22.4 Version Numbers . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 122\n", node["text"])

# endregion FUNC_test_pdf_tabby_with_header_footer

# region FUNC_test_pdf_pdfminer_with_header_footer [DOMAIN(7): Testing; CONCEPT(7): ResponseValidation; TECH(7): unittest]
## @purpose Verify API response for pdf pdfminer with header footer
## @complexity 6
    def test_pdf_pdfminer_with_header_footer(self) -> None:
        file_name = "riscv-spec-v2.2.pdf"
        result = self._send_request(file_name, dict(pdf_with_text_layer="true", need_header_footer_analysis=True, pages="10:25"))

        tree = result["content"]["structure"]
        self._check_tree_sanity(tree)

        # page 1 without a header
        node = self._get_by_tree_path(tree, "0.0")
        print("[LDD_TEST] Test result obtained, proceeding to assertions")
        self.assertEqual("16 “P” Standard Extension for Packed-SIMD Instructions, Version 0.1\n91\n", node["text"])

# endregion FUNC_test_pdf_pdfminer_with_header_footer
# endregion CLASS_TestApiPdfWithText