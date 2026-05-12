# region MODULE_CONTRACT [DOMAIN(7): Testing; CONCEPT(7): HTMLFormat, WebDocuments; TECH(7): unittest]
## @modulecontract
## @purpose Test Dedoc API HTML document parsing with structure extraction, encoding detection, and attachment handling.
## @scope HTML document processing: structure parsing, encoding detection, table extraction, language parameter.
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
## CLASS [API integration test class] => TestApiHtmlReader
## @usecases
## - [TestClass]: Developer (Run) => VerifyAPIBehavior => TestPassOrFail
def _module_contract():
    pass
# endregion MODULE_CONTRACT
# GREP_SUMMARY: html, web, structure, encoding, table, paragraphs, API test
# STRUCTURE: ▶ ┌example.html┐ → ○ _send_request → ⊕ parse structure + encoding → ◇ validate paragraphs + tables + language → ⎋ assertions

import os

from dedoc.data_structures.concrete_annotations.bold_annotation import BoldAnnotation
from tests.api_tests.abstract_api_test import AbstractTestApiDocReader


# region CLASS_TestApiHtmlReader [DOMAIN(7): Testing, DocumentProcessing; CONCEPT(7): APITest; TECH(7): unittest]
## @purpose API integration tests for Dedoc document processing — TestApiHtmlReader.
class TestApiHtmlReader(AbstractTestApiDocReader):


# region METHOD__get_abs_path [DOMAIN(6): Testing; CONCEPT(6): Helper; TECH(6): unittest]
## @purpose Helper method for test assertions
## @complexity 4
    def _get_abs_path(self, file_name: str) -> str:
        return os.path.join(self.data_directory_path, "htmls", file_name)

# endregion METHOD__get_abs_path

# region FUNC_test_html [DOMAIN(7): Testing; CONCEPT(7): ResponseValidation; TECH(7): unittest]
## @purpose Verify API response for html
## @complexity 6
    def test_html(self) -> None:
        file_name = "example.html"
        result = self._send_request(file_name)
        self.__check_example_file(result, file_name)

# endregion FUNC_test_html

# region FUNC_test_html_cp1251 [DOMAIN(7): Testing; CONCEPT(7): ResponseValidation; TECH(7): unittest]
## @purpose Verify API response for html cp1251
## @complexity 6
    def test_html_cp1251(self) -> None:
        file_name = "example_cp1251.html"
        result = self._send_request(file_name)
        self.__check_example_file(result, file_name)

# endregion FUNC_test_html_cp1251

# region FUNC_test_html_koi8 [DOMAIN(7): Testing; CONCEPT(7): ResponseValidation; TECH(7): unittest]
## @purpose Verify API response for html koi8
## @complexity 6
    def test_html_koi8(self) -> None:
        file_name = "example_koi.html"
        result = self._send_request(file_name)
        self.__check_example_file(result, file_name)

# endregion FUNC_test_html_koi8

# region METHOD___check_example_file [DOMAIN(6): Testing; CONCEPT(6): Helper; TECH(6): unittest]
## @purpose Helper method for test assertions
## @complexity 4
    def __check_example_file(self, result: dict, file_name: str) -> None:
        content = result["content"]
        tree = content["structure"]
        self._check_tree_sanity(tree)

        node = self._get_by_tree_path(tree, "0")
        self.assertEqual("root", node["metadata"]["paragraph_type"])
        self.assertEqual("", node["text"].strip()[:30])

        node = self._get_by_tree_path(tree, "0.0")
        self.assertEqual("header", node["metadata"]["paragraph_type"])
        self.assertEqual("Пример документа", node["text"].strip()[:30])

        node = self._get_by_tree_path(tree, "0.0.0")
        self.assertEqual("header", node["metadata"]["paragraph_type"])
        self.assertEqual("Глава 1", node["text"].strip()[:30])

        node = self._get_by_tree_path(tree, "0.0.0.0")
        self.assertEqual("raw_text", node["metadata"]["paragraph_type"])
        self.assertEqual("Какие то определения", node["text"].strip()[:30])

        node = self._get_by_tree_path(tree, "0.0.0.1")
        self.assertEqual("header", node["metadata"]["paragraph_type"])
        self.assertEqual("Статья 1", node["text"].strip()[:30])

        node = self._get_by_tree_path(tree, "0.0.0.1.0")
        self.assertEqual("raw_text", node["metadata"]["paragraph_type"])
        self.assertEqual("Определим определения  \nТекст ", node["text"].strip()[:30])
        self.assertIn({"start": 1, "end": 31, "name": "bold", "value": "True"}, node["annotations"])
        self.assertIn({"start": 46, "end": 52, "name": "bold", "value": "True"}, node["annotations"])
        self.assertIn({"start": 42, "end": 45, "name": "underlined", "value": "True"}, node["annotations"])
        self.assertIn({"start": 32, "end": 42, "name": "italic", "value": "True"}, node["annotations"])

        node = self._get_by_tree_path(tree, "0.0.0.2")
        self.assertEqual("header", node["metadata"]["paragraph_type"])
        self.assertEqual("Статья 2", node["text"].strip()[:30])

        node = self._get_by_tree_path(tree, "0.0.0.2.0")
        self.assertEqual("raw_text", node["metadata"]["paragraph_type"])
        self.assertEqual("Дадим пояснения", node["text"].strip()[:30])

        node = self._get_by_tree_path(tree, "0.0.0.2.1")
        self.assertEqual("list", node["metadata"]["paragraph_type"])
        self.assertEqual("", node["text"].strip()[:30])

        node = self._get_by_tree_path(tree, "0.0.0.2.1.0")
        self.assertEqual("list_item", node["metadata"]["paragraph_type"])
        self.assertEqual("1.2.1.  Поясним за непонятное", node["text"].strip()[:30])
        bold = [annotation for annotation in node["annotations"] if annotation["name"] == BoldAnnotation.name]
        bold.sort(key=lambda a: a["start"])
        first, second = bold
        self.assertEqual("Поясним", node["text"][first["start"]: first["end"]].strip())
        self.assertEqual("непонятное", node["text"][second["start"]: second["end"]].strip())

        node = self._get_by_tree_path(tree, "0.0.0.2.1.1")
        self.assertEqual("list_item", node["metadata"]["paragraph_type"])
        self.assertEqual("1.2.2. Поясним за понятное", node["text"].strip()[:30])

        node = self._get_by_tree_path(tree, "0.0.0.2.1.1.0")
        self.assertEqual("list", node["metadata"]["paragraph_type"])
        self.assertEqual("", node["text"].strip()[:30])

        node = self._get_by_tree_path(tree, "0.0.0.2.1.1.0.0")
        self.assertEqual("list_item", node["metadata"]["paragraph_type"])
        self.assertEqual("a) это даже ежу понятно", node["text"].strip()[:30])

        node = self._get_by_tree_path(tree, "0.0.0.2.1.1.0.1")
        self.assertEqual("list_item", node["metadata"]["paragraph_type"])
        self.assertEqual("b) это ежу не понятно", node["text"].strip()[:30])

        node = self._get_by_tree_path(tree, "0.0.0.2.1.2")
        self.assertEqual("list_item", node["metadata"]["paragraph_type"])
        self.assertEqual("1.2.3.", node["text"].strip()[:30])

        table1 = result["content"]["tables"][0]

        self.assertListEqual(["N", "Фамилия", "Имя", "Организация", "Телефон", "Примечания"], self._get_text_of_row(table1["cells"][0]))
        self.assertListEqual(["1", "Иванов", "Иван", "ИСП", "8-800", ""], self._get_text_of_row(table1["cells"][1]))

        table2 = result["content"]["tables"][1]
        self.assertListEqual(["Фамилия", "Имя", "Отчество"], self._get_text_of_row(table2["cells"][0]))
        self.assertListEqual(["Иванов", "Иван", "Иванович"], self._get_text_of_row(table2["cells"][1]))
        self.assertListEqual(["Петров", "Пётр", "Петрович"], self._get_text_of_row(table2["cells"][2]))
        self.assertListEqual(["Сидоров", "Сидор", "Сидорович"], self._get_text_of_row(table2["cells"][3]))

        self.__check_metainfo(result["metadata"], "text/html", file_name)

# endregion METHOD___check_example_file

# region FUNC_test_part_html [DOMAIN(7): Testing; CONCEPT(7): ResponseValidation; TECH(7): unittest]
## @purpose Verify API response for part html
## @complexity 6
    def test_part_html(self) -> None:
        file_name = "part.html"
        result = self._send_request(file_name)

        content = result["content"]["structure"]
        self._check_tree_sanity(content)
        print("[LDD_TEST] Test result obtained, proceeding to assertions")
        self.assertEqual("Лесные слоны", content["subparagraphs"][0]["text"].strip())
        self.assertEqual("В данном разделе мы поговорим о малоизвестных лесных слонах...", content["subparagraphs"][0]["subparagraphs"][0]["text"].strip())
        self.assertEqual("Среда обитания", content["subparagraphs"][0]["subparagraphs"][1]["text"].strip())
        self.assertEqual("Лесные слоны живут не на деревьях, а под ними.", content["subparagraphs"][0]["subparagraphs"][1]["subparagraphs"][0]["text"].strip())

# endregion FUNC_test_part_html

# region FUNC_test_plain_text_html [DOMAIN(7): Testing; CONCEPT(7): ResponseValidation; TECH(7): unittest]
## @purpose Verify API response for plain text html
## @complexity 6
    def test_plain_text_html(self) -> None:
        file_name = "plain.html"
        result = self._send_request(file_name)

        content = result["content"]["structure"]
        self._check_tree_sanity(content)
        print("[LDD_TEST] Test result obtained, proceeding to assertions")
        self.assertEqual(content["subparagraphs"][0]["text"], "February 24, 2021 and some text")

# endregion FUNC_test_plain_text_html

# region FUNC_test_html_with_styles_as_attribute [DOMAIN(7): Testing; CONCEPT(7): ResponseValidation; TECH(7): unittest]
## @purpose Verify API response for html with styles as attribute
## @complexity 6
    def test_html_with_styles_as_attribute(self) -> None:
        file_name = "html_with_styles.html"
        result = self._send_request(file_name)
        content = result["content"]["structure"]
        self._check_tree_sanity(content)
        annotations = content["subparagraphs"][0]["annotations"]

        text = "Some right text\nSome center text\nSome left text\n\nBIG TEXT"
        print("[LDD_TEST] Test result obtained, proceeding to assertions")
        self.assertEqual(text, content["subparagraphs"][0]["text"])
        self.assertEqual(len(annotations), 4)
        for annotation in annotations:
            self.assertGreater(len(text), annotation["start"])
        self.assertIn({"name": "alignment", "value": "right", "start": 0, "end": 15}, annotations)
        self.assertIn({"name": "alignment", "value": "left", "start": 33, "end": 47}, annotations)
        self.assertIn({"name": "bold", "value": "True", "start": 33, "end": 47}, annotations)
        self.assertIn({"name": "bold", "value": "True", "start": 0, "end": 15}, annotations)

# endregion FUNC_test_html_with_styles_as_attribute

# region FUNC_test_html_table_with_styles [DOMAIN(7): Testing; CONCEPT(7): ResponseValidation; TECH(7): unittest]
## @purpose Verify API response for html table with styles
## @complexity 6
    def test_html_table_with_styles(self) -> None:
        file_name = "table_with_styles.html"
        result = self._send_request(file_name)
        table = result["content"]["tables"][0]
        print("[LDD_TEST] Test result obtained, proceeding to assertions")
        self.assertIn({"start": 0, "end": 6, "name": "bold", "value": "True"}, table["cells"][1][0]["lines"][0]["annotations"])
        self.assertIn({"start": 0, "end": 10, "name": "italic", "value": "True"}, table["cells"][1][1]["lines"][0]["annotations"])
        self.assertIn({"start": 0, "end": 10, "name": "linked_text", "value": "some_text"}, table["cells"][2][0]["lines"][0]["annotations"])
        self.assertIn({"start": 0, "end": 16, "name": "strike", "value": "True"}, table["cells"][2][1]["lines"][0]["annotations"])
        self.assertEqual(table["cells"][3][0]["rowspan"], 2)
        self.assertEqual(table["cells"][3][0]["colspan"], 2)
        self.assertEqual(table["cells"][3][0]["invisible"], False)
        self.assertEqual(table["cells"][3][1]["rowspan"], 1)
        self.assertEqual(table["cells"][3][1]["colspan"], 1)
        self.assertEqual(table["cells"][3][1]["invisible"], True)
        self.assertEqual(table["cells"][4][0]["rowspan"], 1)
        self.assertEqual(table["cells"][4][0]["colspan"], 1)
        self.assertEqual(table["cells"][4][0]["invisible"], True)

# endregion FUNC_test_html_table_with_styles

# region FUNC_test_html_font_style_attribute [DOMAIN(7): Testing; CONCEPT(7): ResponseValidation; TECH(7): unittest]
## @purpose Verify API response for html font style attribute
## @complexity 6
    def test_html_font_style_attribute(self) -> None:
        file_name = "210.html"
        self._send_request(file_name)

# endregion FUNC_test_html_font_style_attribute

# region FUNC_test_html_newlines [DOMAIN(7): Testing; CONCEPT(7): ResponseValidation; TECH(7): unittest]
## @purpose Verify API response for html newlines
## @complexity 6
    def test_html_newlines(self) -> None:
        file_name = "some.html"
        result = self._send_request(file_name)
        content = result["content"]["structure"]

        node = self._get_by_tree_path(content, "0.0")
        text = node["text"]
        print("[LDD_TEST] Test result obtained, proceeding to assertions")
        self.assertEqual("Support", text.strip())
        self.assertEqual("header", node["metadata"]["paragraph_type"])

        node = self._get_by_tree_path(content, "0.0.0")
        text = node["text"]
        self.assertIn("Technical support:", text)
        self.assertIn("Facility / Shipping / Mailing address:", text)
        self.assertIn("Grand Rapids, MI 49512-9704 USA", text)
        self.assertIn("Repair and overhaul administration: ", text)
        self.assertIn("Data services:", text)
        self.assertIn("For service repair (Part 145) returned material authorizations (RMA):", text)

# endregion FUNC_test_html_newlines

# region METHOD___check_metainfo [DOMAIN(6): Testing; CONCEPT(6): Helper; TECH(6): unittest]
## @purpose Helper method for test assertions
## @complexity 4
    def __check_metainfo(self, metainfo: dict, actual_type: str, actual_name: str) -> None:
        self.assertEqual(metainfo["file_type"], actual_type)
        self.assertEqual(metainfo["file_name"], actual_name)

# endregion METHOD___check_metainfo

# region FUNC_test_html_encoding [DOMAIN(7): Testing; CONCEPT(7): ResponseValidation; TECH(7): unittest]
## @purpose Verify API response for html encoding
## @complexity 6
    def test_html_encoding(self) -> None:
        file_name = "53.html"
        result = self._send_request(file_name)
        content = result["content"]["structure"]
        text = content["subparagraphs"][0]["text"]
        print("[LDD_TEST] Test result obtained, proceeding to assertions")
        self.assertTrue(text.startswith("\n\n"))

# endregion FUNC_test_html_encoding

# region FUNC_test_html_no_newline [DOMAIN(7): Testing; CONCEPT(7): ResponseValidation; TECH(7): unittest]
## @purpose Verify API response for html no newline
## @complexity 6
    def test_html_no_newline(self) -> None:
        file_name = "no_new_line.html"
        result = self._send_request(file_name)
        content = result["content"]["structure"]
        node = content["subparagraphs"][0]
        text = node["text"]
        expected_text = (
            '"I can’t bring myself to feel too sorry for Amazon or textbook publishers, given how much they tend to gouge on the prices of those books."'
        )
        print("[LDD_TEST] Test result obtained, proceeding to assertions")
        self.assertEqual(expected_text, text.strip())
        italics = [text[annotation["start"]: annotation["end"]] for annotation in node["annotations"] if annotation["name"] == "italic"]
        self.assertIn("or", italics)

# endregion FUNC_test_html_no_newline

# region FUNC_test_html_none_display [DOMAIN(7): Testing; CONCEPT(7): ResponseValidation; TECH(7): unittest]
## @purpose Verify API response for html none display
## @complexity 6
    def test_html_none_display(self) -> None:
        file_name = "none_display.html"
        result = self._send_request(file_name)
        content = result["content"]["structure"]
        annotations = content["subparagraphs"][0]["annotations"]
        print("[LDD_TEST] Test result obtained, proceeding to assertions")
        self.assertIn({"name": "style", "value": "hidden", "start": 24, "end": 39}, annotations)
        self.assertIn({"name": "bold", "value": "True", "start": 45, "end": 49}, annotations)

# endregion FUNC_test_html_none_display
# endregion CLASS_TestApiHtmlReader