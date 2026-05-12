# region MODULE_CONTRACT [DOMAIN(7): Testing; CONCEPT(7): NestedLists, ListHierarchy; TECH(7): unittest]
## @modulecontract
## @purpose Validate Dedoc API nested list parsing with deep hierarchy (items, subitems, bracket lists).
## @scope Nested list processing: multi-level list items, subitems, bracket enumeration, hierarchy depth.
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
## CLASS [API integration test class] => TestNestingList
## @usecases
## - [TestClass]: Developer (Run) => VerifyAPIBehavior => TestPassOrFail
def _module_contract():
    pass
# endregion MODULE_CONTRACT
# GREP_SUMMARY: nesting, list, hierarchy, subitem, bracket, depth, API test
# STRUCTURE: ▶ ┌document with nested lists┐ → ○ _send_request → ⊕ parse list hierarchy → ◇ validate items + subitems → ⎋ depth assertions

from tests.api_tests.abstract_api_test import AbstractTestApiDocReader


# region CLASS_TestNestingList [DOMAIN(7): Testing, DocumentProcessing; CONCEPT(7): APITest; TECH(7): unittest]
## @purpose API integration tests for Dedoc document processing — TestNestingList.
class TestNestingList(AbstractTestApiDocReader):


# region FUNC_test_list_nesting_content [DOMAIN(7): Testing; CONCEPT(7): ResponseValidation; TECH(7): unittest]
## @purpose Verify API response for list nesting content
## @complexity 6
    def test_list_nesting_content(self) -> None:
        file_name = "docx/pr14tz_v5_2007_03_01.docx"
        result = self._send_request(file_name, data={"structure_type": "tree"})
        content = result["content"]["structure"]

        lst = content["subparagraphs"][2]
        print("[LDD_TEST] Test result obtained, proceeding to assertions")
        self.assertEqual(lst["subparagraphs"][4]["text"], "1.5.\tОснования разработки")
        self.assertEqual(lst["subparagraphs"][5]["text"], "1.6.\tНормативные документы")
        self.assertEqual(lst["subparagraphs"][6]["text"], "1.7.\tСведения об источниках и порядке финансирования работ")
        self.assertEqual(len(lst["subparagraphs"][5]["subparagraphs"][0]["subparagraphs"]), 12)

        lst = content["subparagraphs"][5]
        lst = lst["subparagraphs"][0]["subparagraphs"][0]
        self.assertEqual(lst["text"], "4.1.1.	Требования к структуре и функционированию")
        self.assertEqual(lst["subparagraphs"][0]["text"].startswith("Система должна иметь базу хранения"), True)
        self.assertEqual(len(lst["subparagraphs"][1]["subparagraphs"]), 13)

# endregion FUNC_test_list_nesting_content
# endregion CLASS_TestNestingList