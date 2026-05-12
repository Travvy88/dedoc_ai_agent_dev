# region MODULE_CONTRACT [DOMAIN(7): Testing; CONCEPT(7): Multilingual, LanguageDetection; TECH(7): unittest]
## @modulecontract
## @purpose Verify Dedoc API language detection and multilingual document processing across various languages.
## @scope Language detection: auto-detection and manual language parameter for multilingual documents.
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
## CLASS [API integration test class] => TestLanguage
## @usecases
## - [TestClass]: Developer (Run) => VerifyAPIBehavior => TestPassOrFail
def _module_contract():
    pass
# endregion MODULE_CONTRACT
# GREP_SUMMARY: language, multilingual, detection, localization, API test
# STRUCTURE: ▶ ┌multilingual docs┐ → ○ _send_request(language=X|auto) → ⊕ detect/apply language → ⎋ content checks

import os.path

from tests.api_tests.abstract_api_test import AbstractTestApiDocReader


# region CLASS_TestLanguage [DOMAIN(7): Testing, DocumentProcessing; CONCEPT(7): APITest; TECH(7): unittest]
## @purpose API integration tests for Dedoc document processing — TestLanguage.
class TestLanguage(AbstractTestApiDocReader):

    data_directory_path = os.path.join(AbstractTestApiDocReader.data_directory_path, "docx")


# region FUNC_test_en_doc [DOMAIN(7): Testing; CONCEPT(7): ResponseValidation; TECH(7): unittest]
## @purpose Verify API response for en doc
## @complexity 6
    def test_en_doc(self) -> None:
        file_name = "english_doc.doc"
        result = self._send_request(file_name, dict(language="eng", structure_type="tree"))
        print("[LDD_TEST] Test result obtained, proceeding to assertions")
        self._check_english_doc(result)

# endregion FUNC_test_en_doc

# region FUNC_test_en_docx [DOMAIN(7): Testing; CONCEPT(7): ResponseValidation; TECH(7): unittest]
## @purpose Verify API response for en docx
## @complexity 6
    def test_en_docx(self) -> None:
        file_name = "english_doc.docx"
        result = self._send_request(file_name, dict(language="eng", structure_type="tree"))
        print("[LDD_TEST] Test result obtained, proceeding to assertions")
        self._check_english_doc(result)

# endregion FUNC_test_en_docx

# region FUNC_test_en_odt [DOMAIN(7): Testing; CONCEPT(7): ResponseValidation; TECH(7): unittest]
## @purpose Verify API response for en odt
## @complexity 6
    def test_en_odt(self) -> None:
        file_name = "english_doc.odt"
        result = self._send_request(file_name, dict(language="eng", structure_type="tree"))
        print("[LDD_TEST] Test result obtained, proceeding to assertions")
        self._check_english_doc(result)

# endregion FUNC_test_en_odt

# region FUNC_test_en_pdf [DOMAIN(7): Testing; CONCEPT(7): ResponseValidation; TECH(7): unittest]
## @purpose Verify API response for en pdf
## @complexity 6
    def test_en_pdf(self) -> None:
        file_name = "pdf_with_text_layer/english_doc.pdf"
        result = self._send_request(file_name, dict(language="eng"))
        print("[LDD_TEST] Test result obtained, proceeding to assertions")
        self._check_english_doc(result)

# endregion FUNC_test_en_pdf
# endregion CLASS_TestLanguage