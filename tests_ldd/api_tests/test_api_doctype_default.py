# region MODULE_CONTRACT [DOMAIN(7): Testing; CONCEPT(7): DefaultStructure, CustomPatterns; TECH(7): unittest]
## @modulecontract
## @purpose Test custom pattern-based structure extraction via the patterns parameter and error handling for invalid patterns.
## @scope Custom structure pattern validation, error responses for malformed patterns.
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
## CLASS [API integration test class] => TestApiDefaultStructure
## @usecases
## - [TestClass]: Developer (Run) => VerifyAPIBehavior => TestPassOrFail
def _module_contract():
    pass
# endregion MODULE_CONTRACT
# GREP_SUMMARY: default doctype, patterns, regexp, structure, custom parsing, API test
# STRUCTURE: ⚡ ┌patterns json┐ → ○ _send_request(structure_type) → ⊕ validate paragraph_type + hierarchy → ⎋ pattern match assertions

from tests.api_tests.abstract_api_test import AbstractTestApiDocReader


# region CLASS_TestApiDefaultStructure [DOMAIN(7): Testing, DocumentProcessing; CONCEPT(7): APITest; TECH(7): unittest]
## @purpose API integration tests for Dedoc document processing — TestApiDefaultStructure.
class TestApiDefaultStructure(AbstractTestApiDocReader):


# region FUNC_test_patterns [DOMAIN(7): Testing; CONCEPT(7): ResponseValidation; TECH(7): unittest]
## @purpose Verify API response for patterns
## @complexity 6
    def test_patterns(self) -> None:
        file_name = "docx/without_numbering.docx"
        patterns = [
            {"name": "regexp", "regexp": "^глава\s\d+\.", "line_type": "глава", "level_1": 1},  # noqa
            {"name": "start_word", "start_word": "статья", "level_1": 2, "line_type": "статья"},
            {"name": "dotted_list", "level_1": 3, "line_type": "list_item", "can_be_multiline": False},
            {"name": "bracket_list", "level_1": 4, "level_2": 1, "line_type": "bracket_list_item", "can_be_multiline": "false"}
        ]
        result = self._send_request(file_name, {"patterns": str(patterns)})
        structure = result["content"]["structure"]

        node = self._get_by_tree_path(structure, "0.1")
        print("[LDD_TEST] Test result obtained, proceeding to assertions")
        self.assertEqual(node["text"].strip(), "Глава 1. Общие положения")
        self.assertEqual(node["metadata"]["paragraph_type"], "глава")
        node = self._get_by_tree_path(structure, "0.1.1")
        self.assertIn("Статья 1.1.", node["text"])
        self.assertEqual(node["metadata"]["paragraph_type"], "статья")
        node = self._get_by_tree_path(structure, "0.1.1.0")
        self.assertEqual(node["metadata"]["paragraph_type"], "list")
        node = self._get_by_tree_path(structure, "0.1.1.0.0")
        self.assertIn("1. Законодательство", node["text"])
        self.assertEqual(node["metadata"]["paragraph_type"], "list_item")
        node = self._get_by_tree_path(structure, "0.1.2.0.0.0")
        self.assertEqual(node["text"].strip(), "1) предупреждение;")
        self.assertEqual(node["metadata"]["paragraph_type"], "bracket_list_item")
        node = self._get_by_tree_path(structure, "0.2")
        self.assertEqual(node["text"].strip(), "Глава 2. Административные правонарушения, посягающие на права граждан и здоровье населения")
        self.assertEqual(node["metadata"]["paragraph_type"], "глава")

# endregion FUNC_test_patterns

# region FUNC_test_empty_patterns [DOMAIN(7): Testing; CONCEPT(7): ResponseValidation; TECH(7): unittest]
## @purpose Verify API response for empty patterns
## @complexity 6
    def test_empty_patterns(self) -> None:
        file_name = "docx/example.docx"
        self._send_request(file_name, {"patterns": ""})
        self._send_request(file_name, {"patterns": "[]"})

# endregion FUNC_test_empty_patterns

# region FUNC_test_wrong_patterns [DOMAIN(7): Testing; CONCEPT(7): ResponseValidation; TECH(7): unittest]
## @purpose Verify API response for wrong patterns
## @complexity 6
    def test_wrong_patterns(self) -> None:
        file_name = "docx/example.docx"
        self._send_request(file_name, {"patterns": str([{"regexp": "^глава\s\d+\.", "line_type": "глава", "level_1": 1}])}, expected_code=400)  # noqa
        self._send_request(file_name, {"patterns": str([{"name": "start_word", "line_type": "глава", "level_1": 1}])}, expected_code=400)
        self._send_request(file_name, {"patterns": str([{"name": "unknown", "line_type": "глава", "level_1": 1}])}, expected_code=400)
        self._send_request(file_name, {"patterns": "{1: blabla}"}, expected_code=400)
        self._send_request(file_name, {"patterns": "{1: 2}"}, expected_code=400)
        self._send_request(file_name, {"patterns": "[1]"}, expected_code=400)

# endregion FUNC_test_wrong_patterns
# endregion CLASS_TestApiDefaultStructure