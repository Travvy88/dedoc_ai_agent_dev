# region MODULE_CONTRACT [DOMAIN(7): Testing; CONCEPT(7): PDFEncoding, ErrorHandling; TECH(7): unittest]
## @modulecontract
## @purpose Validate Dedoc API handling of PDFs with broken/incorrect text encoding, verifying graceful degradation.
## @scope PDF encoding error resilience: handling corrupted or incorrectly encoded text in PDFs.
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
## CLASS [API integration test class] => TestApiPdfBrokenEncodingReader
## @usecases
## - [TestClass]: Developer (Run) => VerifyAPIBehavior => TestPassOrFail
def _module_contract():
    pass
# endregion MODULE_CONTRACT
# GREP_SUMMARY: pdf, broken, encoding, error handling, resilience, API test
# STRUCTURE: ▶ ┌broken_encoding.pdf┐ → ○ _send_request → ⊕ detect encoding issues → ⊕ graceful degradation → ⎋ output validation

import os

import Levenshtein

from tests.api_tests.abstract_api_test import AbstractTestApiDocReader


# region CLASS_TestApiPdfBrokenEncodingReader [DOMAIN(7): Testing, DocumentProcessing; CONCEPT(7): APITest; TECH(7): unittest]
## @purpose API integration tests for Dedoc document processing — TestApiPdfBrokenEncodingReader.
class TestApiPdfBrokenEncodingReader(AbstractTestApiDocReader):


# region METHOD__get_abs_path [DOMAIN(6): Testing; CONCEPT(6): Helper; TECH(6): unittest]
## @purpose Helper method for test assertions
## @complexity 4
    def _get_abs_path(self, file_name: str) -> str:
        return os.path.join(self.data_directory_path, "pdf_with_text_layer", file_name)

# endregion METHOD__get_abs_path

# region FUNC_test_bad_encoding [DOMAIN(7): Testing; CONCEPT(7): ResponseValidation; TECH(7): unittest]
## @purpose Verify API response for bad encoding
## @complexity 6
    def test_bad_encoding(self) -> None:
        file_name = "mongolo.pdf"
        result = self._send_request(file_name, dict(pdf_with_text_layer="bad_encoding"))
        tree = result["content"]["structure"]

        text_list = []
        for node_id in ("0.0", "0.1", "0.2", "0.3", "0.4.0", "0.4.1", "0.4.2"):
            text_list.append(self._get_by_tree_path(tree, node_id)["text"])
        text_list.append("\n".join(self._get_by_tree_path(tree, "0.4.2.0")["text"].split("\n")[:3]))

        with open(os.path.join(self.data_directory_path, "txt", "mongolo.txt"), encoding="utf8", mode="r") as txt:
            accuracy = Levenshtein.ratio(txt.read(), "".join(text_list))
            print("[LDD_TEST] Test result obtained, proceeding to assertions")
            self.assertTrue(accuracy > 0.7)

# endregion FUNC_test_bad_encoding
# endregion CLASS_TestApiPdfBrokenEncodingReader