# region MODULE_CONTRACT [DOMAIN(7): Testing; CONCEPT(7): JSONFormat, StructuredData; TECH(7): unittest]
## @modulecontract
## @purpose Verify Dedoc API JSON document parsing with attachment extraction and HTML field configuration.
## @scope JSON document processing: structure extraction, attachment handling, html_fields parameter.
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
## CLASS [API integration test class] => TestApiJSONReader
## @usecases
## - [TestClass]: Developer (Run) => VerifyAPIBehavior => TestPassOrFail
def _module_contract():
    pass
# endregion MODULE_CONTRACT
# GREP_SUMMARY: json, structured, attachment, html_fields, API test
# STRUCTURE: ▶ ┌example.json┐ → ○ _send_request(html_fields) → ⊕ parse json + extract attachments → ⎋ content checks

import json
import os
from json import JSONDecodeError

from tests.api_tests.abstract_api_test import AbstractTestApiDocReader


# region CLASS_TestApiJSONReader [DOMAIN(7): Testing, DocumentProcessing; CONCEPT(7): APITest; TECH(7): unittest]
## @purpose API integration tests for Dedoc document processing — TestApiJSONReader.
class TestApiJSONReader(AbstractTestApiDocReader):


# region METHOD__get_abs_path [DOMAIN(6): Testing; CONCEPT(6): Helper; TECH(6): unittest]
## @purpose Helper method for test assertions
## @complexity 4
    def _get_abs_path(self, file_name: str) -> str:
        return os.path.abspath(os.path.join(self.data_directory_path, "json", file_name))

# endregion METHOD__get_abs_path

# region FUNC_test_string [DOMAIN(7): Testing; CONCEPT(7): ResponseValidation; TECH(7): unittest]
## @purpose Verify API response for string
## @complexity 6
    def test_string(self) -> None:
        file_name = "string.json"
        result = self._send_request(file_name)["content"]["structure"]["subparagraphs"][0]
        print("[LDD_TEST] Test result obtained, proceeding to assertions")
        self.assertEqual("у попа была собака", result["text"])

# endregion FUNC_test_string

# region FUNC_test_list [DOMAIN(7): Testing; CONCEPT(7): ResponseValidation; TECH(7): unittest]
## @purpose Verify API response for list
## @complexity 6
    def test_list(self) -> None:
        file_name = "list.json"
        result = self._send_request(file_name)["content"]["structure"]
        list_node = result["subparagraphs"][0]
        print("[LDD_TEST] Test result obtained, proceeding to assertions")
        self.assertEqual("list", list_node["metadata"]["paragraph_type"])
        list_items = list_node["subparagraphs"]
        self.assertEqual(2, len(list_items))
        self.assertEqual("list_item", list_items[0]["metadata"]["paragraph_type"])
        self.assertEqual("у попа была собака", list_items[0]["text"])
        self.assertEqual("list_item", list_items[1]["metadata"]["paragraph_type"])
        self.assertEqual("он её любил", list_items[1]["text"])

# endregion FUNC_test_list

# region FUNC_test_dict [DOMAIN(7): Testing; CONCEPT(7): ResponseValidation; TECH(7): unittest]
## @purpose Verify API response for dict
## @complexity 6
    def test_dict(self) -> None:
        file_name = "dict.json"
        result = self._send_request(file_name)["content"]["structure"]
        nodes = result["subparagraphs"]
        print("[LDD_TEST] Test result obtained, proceeding to assertions")
        self.assertEqual("key", nodes[0]["metadata"]["paragraph_type"])
        self.assertEqual("у попа была собака", nodes[0]["subparagraphs"][0]["text"])
        self.assertEqual("key", nodes[1]["metadata"]["paragraph_type"])
        self.assertEqual("он её любил", nodes[1]["subparagraphs"][0]["text"])

# endregion FUNC_test_dict

# region FUNC_test_dict_with_list [DOMAIN(7): Testing; CONCEPT(7): ResponseValidation; TECH(7): unittest]
## @purpose Verify API response for dict with list
## @complexity 6
    def test_dict_with_list(self) -> None:
        file_name = "dict_with_list.json"
        result = self._send_request(file_name)["content"]["structure"]
        first_list_items = result["subparagraphs"][0]["subparagraphs"][0]["subparagraphs"]
        second_list_items = result["subparagraphs"][1]["subparagraphs"][0]["subparagraphs"]
        first_list_items, second_list_items = sorted([first_list_items, second_list_items], key=lambda value: -len(value))

        nodes = result["subparagraphs"][1]["subparagraphs"]
        print("[LDD_TEST] Test result obtained, proceeding to assertions")
        self.assertEqual("list", nodes[0]["metadata"]["paragraph_type"])
        self.assertEqual(3, len(first_list_items))
        self.assertEqual("июнь", first_list_items[0]["text"])
        self.assertEqual("июль", first_list_items[1]["text"])
        self.assertEqual("август", first_list_items[2]["text"])

        self.assertEqual(2, len(second_list_items))
        self.assertEqual("понедельник", second_list_items[0]["text"])
        self.assertEqual("вторник", second_list_items[1]["text"])

# endregion FUNC_test_dict_with_list

# region FUNC_test_list_with_dict [DOMAIN(7): Testing; CONCEPT(7): ResponseValidation; TECH(7): unittest]
## @purpose Verify API response for list with dict
## @complexity 6
    def test_list_with_dict(self) -> None:
        file_name = "list_with_dict.json"
        result = self._send_request(file_name)["content"]["structure"]
        self._check_tree_sanity(tree=result)
        print("[LDD_TEST] Test result obtained, proceeding to assertions")
        self.assertEqual("month", self._get_by_tree_path(result, "0.0.0.0")["text"])
        self.assertEqual("июнь", self._get_by_tree_path(result, "0.0.0.0.0.0")["text"])
        self.assertEqual("июль", self._get_by_tree_path(result, "0.0.0.0.0.1")["text"])
        self.assertEqual("август", self._get_by_tree_path(result, "0.0.0.0.0.2")["text"])

        self.assertEqual("days", self._get_by_tree_path(result, "0.1.0.0")["text"])
        self.assertEqual("понедельник", self._get_by_tree_path(result, "0.1.0.0.0.0")["text"])
        self.assertEqual("вторник", self._get_by_tree_path(result, "0.1.0.0.0.1")["text"])

# endregion FUNC_test_list_with_dict

# region FUNC_test_realistic [DOMAIN(7): Testing; CONCEPT(7): ResponseValidation; TECH(7): unittest]
## @purpose Verify API response for realistic
## @complexity 6
    def test_realistic(self) -> None:
        file_name = "realistic_json.json"
        result = self._send_request(file_name)["content"]["structure"]["subparagraphs"]
        result_dict = [(node["metadata"]["paragraph_type"], node["text"]) for node in result]
        with open(self._get_abs_path(file_name)) as file:
            real_dict = json.load(file)
        print("[LDD_TEST] Test result obtained, proceeding to assertions")
        self.assertEqual(len(result_dict), len(real_dict))

# endregion FUNC_test_realistic

# region FUNC_test_broken [DOMAIN(7): Testing; CONCEPT(7): ResponseValidation; TECH(7): unittest]
## @purpose Verify API response for broken
## @complexity 6
    def test_broken(self) -> None:
        file_name = "broken.json"
        result = self._send_request(file_name, expected_code=200)
        warnings = [warning for warning in result["warnings"] if warning.startswith("Incorrect extension")]
        print("[LDD_TEST] Test result obtained, proceeding to assertions")
        self.assertEqual(len(warnings), 1)

# endregion FUNC_test_broken

# region FUNC_test_json_attachments2 [DOMAIN(7): Testing; CONCEPT(7): ResponseValidation; TECH(7): unittest]
## @purpose Verify API response for json attachments2
## @complexity 6
    def test_json_attachments2(self) -> None:
        file_name = "test2.json"
        data = {"html_fields": '[["e"], ["f"]]', "with_attachments": "True", "return_base64": "true"}
        self._send_request(file_name, expected_code=200, data=data)

# endregion FUNC_test_json_attachments2

# region FUNC_test_json_null [DOMAIN(7): Testing; CONCEPT(7): ResponseValidation; TECH(7): unittest]
## @purpose Verify API response for json null
## @complexity 6
    def test_json_null(self) -> None:
        file_name = "test_null.json"
        result = self._send_request(file_name, expected_code=200)
        paragraphs = result["content"]["structure"]["subparagraphs"]
        print("[LDD_TEST] Test result obtained, proceeding to assertions")
        self.assertEqual(paragraphs[0]["text"], "author")
        self.assertEqual(paragraphs[0]["metadata"]["paragraph_type"], "key")
        self.assertEqual(paragraphs[0]["subparagraphs"][0]["text"], "James Fontanella-Khan")
        self.assertEqual(paragraphs[0]["subparagraphs"][0]["metadata"]["paragraph_type"], "raw_text")

        self.assertEqual(paragraphs[1]["text"], "category")
        self.assertEqual(paragraphs[1]["metadata"]["paragraph_type"], "key")
        self.assertEqual(len(paragraphs[1]["subparagraphs"]), 0)

        self.assertEqual(paragraphs[5]["text"], "tags")
        self.assertEqual(paragraphs[5]["metadata"]["paragraph_type"], "key")
        self.assertEqual(len(paragraphs[5]["subparagraphs"]), 0)
        pass

# endregion FUNC_test_json_null

# region FUNC_test_json_broken_parameters [DOMAIN(7): Testing; CONCEPT(7): ResponseValidation; TECH(7): unittest]
## @purpose Verify API response for json broken parameters
## @complexity 6
    def test_json_broken_parameters(self) -> None:
        file_name = "test2.json"
        data = {"html_fields": "[[ef]]", "with_attachments": "True", "return_base64": "true"}
        print("[LDD_TEST] Test result obtained, proceeding to assertions")
        with self.assertRaises(JSONDecodeError):
            json.loads(data["html_fields"])
        self._send_request(file_name, expected_code=400, data=data)

# endregion FUNC_test_json_broken_parameters
# endregion CLASS_TestApiJSONReader