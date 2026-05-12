# region MODULE_CONTRACT [DOMAIN(7): Testing; CONCEPT(8): DocumentStructure, Hierarchy; TECH(7): unittest]
## @modulecontract
## @purpose Test Dedoc API structure extraction for documents with complex hierarchies, verifying correct tree construction.
## @scope Document structure extraction: tree construction, node hierarchy, various structure types (tree, linear).
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
## CLASS [API integration test class] => TestStructure
## @usecases
## - [TestClass]: Developer (Run) => VerifyAPIBehavior => TestPassOrFail
def _module_contract():
    pass
# endregion MODULE_CONTRACT
# GREP_SUMMARY: structure, hierarchy, tree, linear, node, paragraph type, API test
# STRUCTURE: ▶ ┌structured document┐ → ○ _send_request(structure_type) → ⊕ build tree → ◇ validate node types + hierarchy → ⎋ assertions

import os

from tests.api_tests.abstract_api_test import AbstractTestApiDocReader


# region CLASS_TestStructure [DOMAIN(7): Testing, DocumentProcessing; CONCEPT(7): APITest; TECH(7): unittest]
## @purpose API integration tests for Dedoc document processing — TestStructure.
class TestStructure(AbstractTestApiDocReader):

    data_directory_path = os.path.join(AbstractTestApiDocReader.data_directory_path, "docx")


# region FUNC_test_linear_structure [DOMAIN(7): Testing; CONCEPT(7): ResponseValidation; TECH(7): unittest]
## @purpose Verify API response for linear structure
## @complexity 6
    def test_linear_structure(self) -> None:
        file_name = "example.docx"
        result = self._send_request(file_name, data={"structure_type": "linear"})
        nodes = result["content"]["structure"]["subparagraphs"]
        print("[LDD_TEST] Test result obtained, proceeding to assertions")
        self.assertEqual(len(nodes), 13)
        for node in nodes:
            self.assertListEqual([], node["subparagraphs"])

# endregion FUNC_test_linear_structure

# region FUNC_test_default_structure [DOMAIN(7): Testing; CONCEPT(7): ResponseValidation; TECH(7): unittest]
## @purpose Verify API response for default structure
## @complexity 6
    def test_default_structure(self) -> None:
        file_name = "example.docx"
        result = self._send_request(file_name, data={"structure_type": "linear"})
        nodes = result["content"]["structure"]["subparagraphs"]
        print("[LDD_TEST] Test result obtained, proceeding to assertions")
        self.assertEqual(len(nodes), 13)
        for node in nodes:
            self.assertListEqual([], node["subparagraphs"])

# endregion FUNC_test_default_structure

# region FUNC_test_tree_structure [DOMAIN(7): Testing; CONCEPT(7): ResponseValidation; TECH(7): unittest]
## @purpose Verify API response for tree structure
## @complexity 6
    def test_tree_structure(self) -> None:
        file_name = "example.docx"
        result = self._send_request(file_name, data={"structure_type": "tree"})
        nodes = result["content"]["structure"]["subparagraphs"]
        print("[LDD_TEST] Test result obtained, proceeding to assertions")
        self.assertEqual(len(nodes), 2)
        self.assertEqual("Пример документа", nodes[0]["text"].split("\n")[0])
        self.assertEqual("1.2.1. Поясним за непонятное", nodes[1]["subparagraphs"][0]["text"].strip())

# endregion FUNC_test_tree_structure

# region FUNC_test_page_id_tree_structure [DOMAIN(7): Testing; CONCEPT(7): ResponseValidation; TECH(7): unittest]
## @purpose Verify API response for page id tree structure
## @complexity 6
    def test_page_id_tree_structure(self) -> None:
        file_name = os.path.join("..", "pdf_with_text_layer", "test_page_id.pdf")
        result = self._send_request(file_name, data={"structure_type": "tree"})
        node = result["content"]["structure"]["subparagraphs"][0]

        page_change_positions = [2135, 4270, 6405, 8540, 10675, 12810, 13323]
        for idx, additional_page_id in enumerate(node["metadata"]["additional_page_ids"], start=1):
            print("[LDD_TEST] Test result obtained, proceeding to assertions")
            self.assertEqual(idx, additional_page_id["page_id"])
            start, end = page_change_positions[idx - 1], page_change_positions[idx]
            self.assertEqual(start, additional_page_id["start"])
            self.assertEqual(end, additional_page_id["end"])
            self.assertFalse(node["text"][start:end].startswith("\n"))
            self.assertTrue(node["text"][start:end].endswith("\n"))

# endregion FUNC_test_page_id_tree_structure

# region FUNC_test_incorrect_structure [DOMAIN(7): Testing; CONCEPT(7): ResponseValidation; TECH(7): unittest]
## @purpose Verify API response for incorrect structure
## @complexity 6
    def test_incorrect_structure(self) -> None:
        file_name = "example.docx"
        _ = self._send_request(file_name, data={"structure_type": "bagel"}, expected_code=400)

# endregion FUNC_test_incorrect_structure
# endregion CLASS_TestStructure