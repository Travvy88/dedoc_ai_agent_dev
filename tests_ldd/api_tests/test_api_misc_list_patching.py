# region MODULE_CONTRACT [DOMAIN(7): Testing; CONCEPT(7): ListPatching, StructureCorrection; TECH(7): unittest]
## @modulecontract
## @purpose Test Dedoc API list patching functionality for correcting list numbering and hierarchy in document structure.
## @scope List structure correction: automatic list patching for numbering consistency and hierarchy repair.
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
## CLASS [API integration test class] => TestListPatching
## @usecases
## - [TestClass]: Developer (Run) => VerifyAPIBehavior => TestPassOrFail
def _module_contract():
    pass
# endregion MODULE_CONTRACT
# GREP_SUMMARY: list, patching, numbering, hierarchy, correction, API test
# STRUCTURE: ▶ ┌document with lists┐ → ○ _send_request → ⊕ patch list numbering → ⎋ hierarchy validation

from tests.api_tests.abstract_api_test import AbstractTestApiDocReader


# region CLASS_TestListPatching [DOMAIN(7): Testing, DocumentProcessing; CONCEPT(7): APITest; TECH(7): unittest]
## @purpose API integration tests for Dedoc document processing — TestListPatching.
class TestListPatching(AbstractTestApiDocReader):


# region FUNC_test_list_patching [DOMAIN(7): Testing; CONCEPT(7): ResponseValidation; TECH(7): unittest]
## @purpose Verify API response for list patching
## @complexity 6
    def test_list_patching(self) -> None:
        file_name = "docx/13_moloko_1_polug.docx"
        result = self._send_request(file_name, data={"structure_type": "tree"})
        content = result["content"]["structure"]

        lst = content["subparagraphs"][1]
        print("[LDD_TEST] Test result obtained, proceeding to assertions")
        self.assertEqual(len(lst["subparagraphs"]), 12)

# endregion FUNC_test_list_patching

# region FUNC_test_list_patching_2 [DOMAIN(7): Testing; CONCEPT(7): ResponseValidation; TECH(7): unittest]
## @purpose Verify API response for list patching 2
## @complexity 6
    def test_list_patching_2(self) -> None:
        file_name = "list_tests/missed_list.docx"
        result = self._send_request(file_name, data={"structure_type": "tree"})
        content = result["content"]["structure"]

        subparagraphs = content["subparagraphs"][0]["subparagraphs"][0]
        print("[LDD_TEST] Test result obtained, proceeding to assertions")
        self.assertEqual(len(subparagraphs["subparagraphs"]), 5)
        self.assertEqual(subparagraphs["subparagraphs"][0]["text"].strip(), "1. list item 1")
        self.assertEqual(subparagraphs["subparagraphs"][1]["text"].strip(), "2. list item 2")
        self.assertEqual(subparagraphs["subparagraphs"][2]["text"].strip(), "3. list item 3")
        self.assertEqual(subparagraphs["subparagraphs"][3]["text"].strip(), "4. list item 4")
        self.assertEqual(subparagraphs["subparagraphs"][4]["text"].strip(), "6. list item 6")

        subparagraphs = subparagraphs["subparagraphs"][4]["subparagraphs"][0]
        self.assertEqual(len(subparagraphs["subparagraphs"]), 3)
        self.assertEqual(subparagraphs["subparagraphs"][0]["text"].strip(), "6.1. list item 6.1")
        self.assertEqual(subparagraphs["subparagraphs"][1]["text"].strip(), "6.3 list item 6.3")
        self.assertEqual(subparagraphs["subparagraphs"][2]["text"].strip(), "6.5 list item 6.5")

        subparagraphs = subparagraphs["subparagraphs"][1]["subparagraphs"][1]

        self.assertEqual(len(subparagraphs["subparagraphs"]), 2)
        self.assertEqual(subparagraphs["subparagraphs"][0]["text"].strip(), "6.3.2.3 list item 6.3.2.3")
        self.assertEqual(subparagraphs["subparagraphs"][1]["text"].strip(), "6.3.2.4. list item 6.3.2.4")

# endregion FUNC_test_list_patching_2

# region FUNC_test_list_patching_3 [DOMAIN(7): Testing; CONCEPT(7): ResponseValidation; TECH(7): unittest]
## @purpose Verify API response for list patching 3
## @complexity 6
    def test_list_patching_3(self) -> None:
        file_name = "list_tests/missed_list_2.docx"
        result = self._send_request(file_name, data={"structure_type": "tree"})
        content = result["content"]["structure"]

        subparagraphs = content["subparagraphs"][0]["subparagraphs"][0]
        print("[LDD_TEST] Test result obtained, proceeding to assertions")
        self.assertEqual(len(subparagraphs["subparagraphs"]), 5)
        self.assertEqual(subparagraphs["subparagraphs"][0]["text"].strip(), "1. list item 1")
        self.assertEqual(subparagraphs["subparagraphs"][1]["text"].strip(), "2. list item 2")
        self.assertEqual(subparagraphs["subparagraphs"][2]["text"].strip(), "3. list item 3")
        self.assertEqual(subparagraphs["subparagraphs"][3]["text"].strip(), "4. list item 4")
        self.assertEqual(subparagraphs["subparagraphs"][4]["text"].strip(), "6. list item 6")

        self.assertEqual(subparagraphs["subparagraphs"][1]["subparagraphs"][0]["subparagraphs"][0]["text"].strip(), "1)")
        self.assertEqual(subparagraphs["subparagraphs"][1]["subparagraphs"][0]["subparagraphs"][1]["text"].strip(), "3)")
        # self.assertEqual(subparagraphs["subparagraphs"][1]["subparagraphs"][0]["subparagraphs"][2]["text"].strip(), "4)")
        # self.assertEqual(subparagraphs["subparagraphs"][1]["subparagraphs"][0]["subparagraphs"][3]["text"].strip(), "7)")

        subparagraphs = subparagraphs["subparagraphs"][4]["subparagraphs"][0]
        self.assertEqual(len(subparagraphs["subparagraphs"]), 3)
        self.assertEqual(subparagraphs["subparagraphs"][0]["text"].strip(), "6.1. list item 6.1")
        # self.assertEqual(subparagraphs["subparagraphs"][1]["text"], "6.2.")
        self.assertEqual(subparagraphs["subparagraphs"][1]["text"].strip(), "6.3 list item 6.3")
        # self.assertEqual(list["subparagraphs"][3]["text"], "6.4.")
        self.assertEqual(subparagraphs["subparagraphs"][2]["text"].strip(), "6.5 list item 6.5")

        subparagraphs = subparagraphs["subparagraphs"][1]["subparagraphs"][1]

        self.assertEqual(len(subparagraphs["subparagraphs"]), 2)
        self.assertEqual(subparagraphs["subparagraphs"][0]["text"].strip(), "6.3.2.3. list item 6.3.2.3")
        self.assertEqual(subparagraphs["subparagraphs"][1]["text"].strip(), "6.3.2.4. list item 6.3.2.4")

# endregion FUNC_test_list_patching_3
# endregion CLASS_TestListPatching