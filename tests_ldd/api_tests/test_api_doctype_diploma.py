# region MODULE_CONTRACT [DOMAIN(7): Testing; CONCEPT(7): DiplomaDoctype, TOC; TECH(7): unittest]
## @modulecontract
## @purpose Validate Dedoc API responses for diploma/thesis documents with TOC, named items, and sections.
## @scope Diploma PDF and DOCX parsing: table of contents, named items, root/body structure.
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
## CLASS [API integration test class] => TestApiDiploma
## @usecases
## - [TestClass]: Developer (Run) => VerifyAPIBehavior => TestPassOrFail
def _module_contract():
    pass
# endregion MODULE_CONTRACT
# GREP_SUMMARY: diploma, thesis, TOC, named_item, document structure, API test
# STRUCTURE: ▶ ┌diploma.pdf/diploma.docx┐ → ○ _send_request(document_type=diploma) → ⊕ verify root + body + toc + named_items → ⎋ structure assertions

import os

from tests.api_tests.abstract_api_test import AbstractTestApiDocReader


# region CLASS_TestApiDiploma [DOMAIN(7): Testing, DocumentProcessing; CONCEPT(7): APITest; TECH(7): unittest]
## @purpose API integration tests for Dedoc document processing — TestApiDiploma.
class TestApiDiploma(AbstractTestApiDocReader):


# region METHOD__get_abs_path [DOMAIN(6): Testing; CONCEPT(6): Helper; TECH(6): unittest]
## @purpose Helper method for test assertions
## @complexity 4
    def _get_abs_path(self, file_name: str) -> str:
        return os.path.join(self.data_directory_path, "diplomas", file_name)

# endregion METHOD__get_abs_path

# region FUNC_test_diploma_pdf [DOMAIN(7): Testing; CONCEPT(7): ResponseValidation; TECH(7): unittest]
## @purpose Verify API response for diploma pdf
## @complexity 6
    def test_diploma_pdf(self) -> None:
        file_name = "diploma.pdf"
        result = self._send_request(file_name, dict(document_type="diploma", pdf_with_text_layer="tabby"))
        structure = result["content"]["structure"]

        node = self._get_by_tree_path(structure, "0")
        print("[LDD_TEST] Test result obtained, proceeding to assertions")
        self.assertEqual("Москва, 2021 г.", node["text"].strip()[-15:])
        self.assertEqual("root", node["metadata"]["paragraph_type"])

        node = self._get_by_tree_path(structure, "0.0")
        self.assertEqual("", node["text"])
        self.assertEqual("body", node["metadata"]["paragraph_type"])

        node = self._get_by_tree_path(structure, "0.1")
        self.assertEqual("СОДЕРЖАНИЕ", node["text"].strip())
        self.assertEqual("toc", node["metadata"]["paragraph_type"])
        node = self._get_by_tree_path(structure, "0.1.0")
        self.assertEqual("ВВЕДЕНИЕ", node["text"][:8])
        self.assertEqual("toc_item", node["metadata"]["paragraph_type"])
        node = self._get_by_tree_path(structure, "0.1.1")
        self.assertEqual("1. ТЕОРЕТИЧЕСКОЕ", node["text"][:16])
        self.assertEqual("toc_item", node["metadata"]["paragraph_type"])

        node = self._get_by_tree_path(structure, "0.2")
        self.assertEqual("ВВЕДЕНИЕ", node["text"].strip())
        self.assertEqual("named_item", node["metadata"]["paragraph_type"])

        node = self._get_by_tree_path(structure, "0.6")
        self.assertEqual("1. ТЕОРЕТИЧЕСКОЕ", node["text"][:16])
        self.assertEqual("named_item", node["metadata"]["paragraph_type"])

        node = self._get_by_tree_path(structure, "0.7")
        self.assertEqual("2. АНАЛИЗ", node["text"][:9])
        self.assertEqual("named_item", node["metadata"]["paragraph_type"])

        node = self._get_by_tree_path(structure, "0.8")
        self.assertEqual("ЗАКЛЮЧЕНИЕ", node["text"].strip())
        self.assertEqual("named_item", node["metadata"]["paragraph_type"])

        node = self._get_by_tree_path(structure, "0.9")
        self.assertEqual("БИБЛИОГРАФИЧЕСКИЙ СПИСОК", node["text"].strip())
        self.assertEqual("named_item", node["metadata"]["paragraph_type"])

# endregion FUNC_test_diploma_pdf

# region FUNC_test_diploma_docx [DOMAIN(7): Testing; CONCEPT(7): ResponseValidation; TECH(7): unittest]
## @purpose Verify API response for diploma docx
## @complexity 6
    def test_diploma_docx(self) -> None:
        file_name = "diploma.docx"
        result = self._send_request(file_name, dict(document_type="diploma"))
        structure = result["content"]["structure"]

        node = self._get_by_tree_path(structure, "0")
        print("[LDD_TEST] Test result obtained, proceeding to assertions")
        self.assertEqual("Москва 2023 г.", node["text"].strip()[-14:])
        self.assertEqual("root", node["metadata"]["paragraph_type"])

        node = self._get_by_tree_path(structure, "0.0")
        self.assertEqual("", node["text"])
        self.assertEqual("body", node["metadata"]["paragraph_type"])

        node = self._get_by_tree_path(structure, "0.1")
        self.assertEqual("Содержание", node["text"].strip())
        self.assertEqual("toc", node["metadata"]["paragraph_type"])

        node = self._get_by_tree_path(structure, "0.1.0")
        self.assertEqual("Введение", node["text"][:8])
        self.assertEqual("toc_item", node["metadata"]["paragraph_type"])

        node = self._get_by_tree_path(structure, "0.2")
        self.assertEqual("Введение", node["text"].strip())
        self.assertEqual("named_item", node["metadata"]["paragraph_type"])

        node = self._get_by_tree_path(structure, "0.3")
        self.assertEqual("Глава 1.", node["text"][:8])
        self.assertEqual("named_item", node["metadata"]["paragraph_type"])

        node = self._get_by_tree_path(structure, "0.6")
        self.assertEqual("Глава 2.", node["text"][:8])
        self.assertEqual("named_item", node["metadata"]["paragraph_type"])

        node = self._get_by_tree_path(structure, "0.7")
        self.assertEqual("Глава 3.", node["text"][:8])
        self.assertEqual("named_item", node["metadata"]["paragraph_type"])

# endregion FUNC_test_diploma_docx
# endregion CLASS_TestApiDiploma