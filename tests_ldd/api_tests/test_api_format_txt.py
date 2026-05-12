# region MODULE_CONTRACT [DOMAIN(7): Testing; CONCEPT(8): TXTFormat, EncodingDetection; TECH(7): unittest]
## @modulecontract
## @purpose Validate Dedoc API plain text parsing: encoding detection (UTF-8, CP1251), structure extraction (tree/pretty_json), large files, GZ compression.
## @scope TXT document processing: encoding auto-detection, tree/pretty_json output, paragraph extraction, GZ support.
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
## CLASS [API integration test class] => TestApiTxtReader
## @usecases
## - [TestClass]: Developer (Run) => VerifyAPIBehavior => TestPassOrFail
def _module_contract():
    pass
# endregion MODULE_CONTRACT
# GREP_SUMMARY: txt, plain text, encoding, utf-8, cp1251, tree, paragraph, gz, API test
# STRUCTURE: ▶ ┌example.txt┐ → ○ _send_request(structure_type=tree|pretty_json) → ⊕ detect encoding → ◇ extract paragraphs + metadata → ⎋ content + encoding assertions

import os

from tests.api_tests.abstract_api_test import AbstractTestApiDocReader
from tests.test_utils import get_by_tree_path


# region CLASS_TestApiTxtReader [DOMAIN(7): Testing, DocumentProcessing; CONCEPT(7): APITest; TECH(7): unittest]
## @purpose API integration tests for Dedoc document processing — TestApiTxtReader.
class TestApiTxtReader(AbstractTestApiDocReader):

    data_directory_path = os.path.join(AbstractTestApiDocReader.data_directory_path, "txt")


# region FUNC_test_txt_file [DOMAIN(7): Testing; CONCEPT(7): ResponseValidation; TECH(7): unittest]
## @purpose Verify API response for txt file
## @complexity 6
    def test_txt_file(self) -> None:
        file_name = "Pr_2013.02.18_21.txt"
        _ = self._send_request(file_name)

# endregion FUNC_test_txt_file

# region FUNC_test_text [DOMAIN(7): Testing; CONCEPT(7): ResponseValidation; TECH(7): unittest]
## @purpose Verify API response for text
## @complexity 6
    def test_text(self) -> None:
        file_name = "example.txt"
        result = self._send_request(file_name, data={"structure_type": "tree"})
        content = result["content"]["structure"]
        print("[LDD_TEST] Test result obtained, proceeding to assertions")
        self.assertEqual(content["subparagraphs"][0]["text"].rstrip(), "Пример документа")

        self._check_metainfo(result["metadata"], "text/plain", file_name)

# endregion FUNC_test_text

# region FUNC_test_text_pretty_json [DOMAIN(7): Testing; CONCEPT(7): ResponseValidation; TECH(7): unittest]
## @purpose Verify API response for text pretty json
## @complexity 6
    def test_text_pretty_json(self) -> None:
        file_name = "example.txt"
        result = self._send_request(file_name, data={"structure_type": "tree", "return_format": "pretty_json"})
        content = result["content"]["structure"]
        print("[LDD_TEST] Test result obtained, proceeding to assertions")
        self.assertEqual(content["subparagraphs"][0]["text"].rstrip(), "Пример документа")

        self._check_metainfo(result["metadata"], "text/plain", file_name)

# endregion FUNC_test_text_pretty_json

# region FUNC_test_text_bad_return_format [DOMAIN(7): Testing; CONCEPT(7): ResponseValidation; TECH(7): unittest]
## @purpose Verify API response for text bad return format
## @complexity 6
    def test_text_bad_return_format(self) -> None:
        file_name = "example.txt"
        result = self._send_request(file_name, data={"structure_type": "tree", "return_format": "broken"})
        content = result["content"]["structure"]
        print("[LDD_TEST] Test result obtained, proceeding to assertions")
        self.assertEqual(content["subparagraphs"][0]["text"].rstrip(), "Пример документа")

        self._check_metainfo(result["metadata"], "text/plain", file_name)

# endregion FUNC_test_text_bad_return_format

# region FUNC_test_text2 [DOMAIN(7): Testing; CONCEPT(7): ResponseValidation; TECH(7): unittest]
## @purpose Verify API response for text2
## @complexity 6
    def test_text2(self) -> None:
        file_name = "pr_17.txt"
        result = self._send_request(file_name, data={"structure_type": "tree"})
        content = result["content"]["structure"]
        print("[LDD_TEST] Test result obtained, proceeding to assertions")
        self.assertIn("УТВЕРЖДЕНЫ", get_by_tree_path(content, "0.0")["text"])
        self.assertIn("1. Настоящие Требования разработаны в соответствии с Федеральным законом", get_by_tree_path(content, "0.2.0")["text"])

# endregion FUNC_test_text2

# region FUNC_test_special_symbols [DOMAIN(7): Testing; CONCEPT(7): ResponseValidation; TECH(7): unittest]
## @purpose Verify API response for special symbols
## @complexity 6
    def test_special_symbols(self) -> None:
        file_name = "special_symbol.txt"
        result = self._send_request(file_name, data={"structure_type": "tree", "encoding": "utf-8"})
        content = result["content"]["structure"]
        with open(self._get_abs_path(file_name)) as file_in:
            print("[LDD_TEST] Test result obtained, proceeding to assertions")
            self.assertEqual(file_in.read(), content["subparagraphs"][0]["text"])

# endregion FUNC_test_special_symbols

# region FUNC_test_paragraphs [DOMAIN(7): Testing; CONCEPT(7): ResponseValidation; TECH(7): unittest]
## @purpose Verify API response for paragraphs
## @complexity 6
    def test_paragraphs(self) -> None:
        file_name = "football.txt"
        result = self._send_request(file_name, data={"structure_type": "tree"})
        content = result["content"]["structure"]["subparagraphs"]
        self.__check_football(content)

# endregion FUNC_test_paragraphs

# region FUNC_test_paragraphs_gz [DOMAIN(7): Testing; CONCEPT(7): ResponseValidation; TECH(7): unittest]
## @purpose Verify API response for paragraphs gz
## @complexity 6
    def test_paragraphs_gz(self) -> None:
        file_name = "football.txt.gz"
        result = self._send_request(file_name, data={"structure_type": "tree"})
        content = result["content"]["structure"]["subparagraphs"]
        self.__check_football(content)

# endregion FUNC_test_paragraphs_gz

# region FUNC_test_large_file [DOMAIN(7): Testing; CONCEPT(7): ResponseValidation; TECH(7): unittest]
## @purpose Verify API response for large file
## @complexity 6
    def test_large_file(self) -> None:
        file_name = "large_text.txt.gz"
        result = self._send_request(file_name, data={"structure_type": "tree"})
        content = result["content"]["structure"]["subparagraphs"][0]["text"]
        for line_id, line in enumerate(content.split("\n")):
            if line.strip() != "":
                print("[LDD_TEST] Test result obtained, proceeding to assertions")
                self.assertEqual(f"Line number {line_id:09d}", line)

# endregion FUNC_test_large_file

# region FUNC_test_txt_with_law [DOMAIN(7): Testing; CONCEPT(7): ResponseValidation; TECH(7): unittest]
## @purpose Verify API response for txt with law
## @complexity 6
    def test_txt_with_law(self) -> None:
        file_name = "17 (1).txt"
        result = self._send_request(file_name)
        metadata = result["metadata"]
        print("[LDD_TEST] Test result obtained, proceeding to assertions")
        self.assertEqual("17 (1).txt", metadata["file_name"])
        content = result["content"]
        self.assertEqual([], content["tables"])
        structure = content["structure"]
        first_child = structure["subparagraphs"][0]
        text = first_child["text"]
        self.assertTrue(text.startswith("\n\n \n\n \n\n"))
        self.assertIn("\n\n \n\nПРИКАЗ\n\n \n\n", text)
        self.assertIn("\n\n \n\nМосква\n\n \n\n", text)

# endregion FUNC_test_txt_with_law

# region FUNC_test_utf8 [DOMAIN(7): Testing; CONCEPT(7): ResponseValidation; TECH(7): unittest]
## @purpose Verify API response for utf8
## @complexity 6
    def test_utf8(self) -> None:
        file_name = "utf8.txt"
        result = self._send_request(file_name)
        self.__check_content(result, "utf_8")

# endregion FUNC_test_utf8

# region FUNC_test_cp1251 [DOMAIN(7): Testing; CONCEPT(7): ResponseValidation; TECH(7): unittest]
## @purpose Verify API response for cp1251
## @complexity 6
    def test_cp1251(self) -> None:
        file_name = "cp1251.txt"
        result = self._send_request(file_name)
        self.__check_content(result, "cp1251")

# endregion FUNC_test_cp1251

# region METHOD___check_content [DOMAIN(6): Testing; CONCEPT(6): Helper; TECH(6): unittest]
## @purpose Helper method for test assertions
## @complexity 4
    def __check_content(self, result: dict, encoding: str) -> None:
        warning = result["warnings"][0]
        self.assertEqual(warning, f"encoding is {encoding}")
        path = self._get_abs_path("utf8.txt")
        with open(path) as file:
            text = file.read()
        self.assertEqual(text, result["content"]["structure"]["subparagraphs"][0]["text"])

# endregion METHOD___check_content

# region METHOD___check_football [DOMAIN(6): Testing; CONCEPT(6): Helper; TECH(6): unittest]
## @purpose Helper method for test assertions
## @complexity 4
    def __check_football(self, content: dict) -> None:
        self.assertEqual(4, len(content))
        node = content[0]
        self.assertTrue(node["text"].startswith("    Association football, more commonly known as simply"))
        self.assertTrue(node["text"].endswith("The team with the higher number of goals wins the game.\n\n"))
        annotations = node["annotations"]
        self.assertIn({"name": "spacing", "value": "50", "start": 0, "end": 546}, annotations)
        node = content[1]
        self.assertTrue(node["text"].startswith("  Football is played in accordance with a set of rules known"))
        self.assertTrue(node["text"].strip().endswith("the coin toss prior to kick-off or penalty kicks."))
        annotations = node["annotations"]
        self.assertIn({"name": "spacing", "value": "100", "start": 0, "end": 163}, annotations)
        node = content[2]
        self.assertTrue(node["text"].startswith("    Football is governed internationally by the International"))
        self.assertTrue(node["text"].endswith("the 2019 FIFA Women's World Cup in France.\n\n"))
        annotations = node["annotations"]
        self.assertIn({"name": "spacing", "value": "400", "start": 0, "end": 164}, annotations)
        self.assertIn({"name": "spacing", "value": "50", "start": 164, "end": 1068}, annotations)
        self.assertTrue(content[3]["text"].startswith("    The most prestigious competitions in European club"))
        self.assertTrue(content[3]["text"].endswith("cost in excess of £600 million/€763 million/US$1.185 billion.\n"))

# endregion METHOD___check_football
# endregion CLASS_TestApiTxtReader