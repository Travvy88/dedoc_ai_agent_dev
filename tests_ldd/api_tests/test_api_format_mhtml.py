# region MODULE_CONTRACT [DOMAIN(7): Testing; CONCEPT(7): MHTMLFormat, WebArchive; TECH(7): unittest]
## @modulecontract
## @purpose Test Dedoc API MHTML (web archive) document parsing with content extraction.
## @scope MHTML format processing: web archive content extraction, structure validation.
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
## CLASS [API integration test class] => TestApiMhtmlReader
## @usecases
## - [TestClass]: Developer (Run) => VerifyAPIBehavior => TestPassOrFail
def _module_contract():
    pass
# endregion MODULE_CONTRACT
# GREP_SUMMARY: mhtml, web archive, content extraction, API test
# STRUCTURE: ▶ ┌example.mhtml┐ → ○ _send_request → ⊕ parse mhtml → ⎋ content validation

from tests.api_tests.abstract_api_test import AbstractTestApiDocReader


# region CLASS_TestApiMhtmlReader [DOMAIN(7): Testing, DocumentProcessing; CONCEPT(7): APITest; TECH(7): unittest]
## @purpose API integration tests for Dedoc document processing — TestApiMhtmlReader.
class TestApiMhtmlReader(AbstractTestApiDocReader):

# region FUNC_test_mhtml [DOMAIN(7): Testing; CONCEPT(7): ResponseValidation; TECH(7): unittest]
## @purpose Verify API response for mhtml
## @complexity 6
    def test_mhtml(self) -> None:
        file_name = "mhtml/Валентин Николаевич Ничипоренко биография, досье, компромат, фото и видео - ЗНАЙ ЮА.mhtml"
        result = self._send_request(file_name, dict(with_attachments=True), expected_code=200)
        print("[LDD_TEST] Test result obtained, proceeding to assertions")
        self.assertEqual(17, len(result["attachments"]))

# endregion FUNC_test_mhtml

# region FUNC_test_mhtml_antivaxxers [DOMAIN(7): Testing; CONCEPT(7): ResponseValidation; TECH(7): unittest]
## @purpose Verify API response for mhtml antivaxxers
## @complexity 6
    def test_mhtml_antivaxxers(self) -> None:
        file_name = "mhtml/antivaxxers.mhtml.gz"
        result = self._send_request(file_name)
        content = result["content"]["structure"]
        node = self._get_by_tree_path(content, "0.3.0")
        print("[LDD_TEST] Test result obtained, proceeding to assertions")
        self.assertIn("Эрнест Валеев", node["text"])

# endregion FUNC_test_mhtml_antivaxxers
# endregion CLASS_TestApiMhtmlReader