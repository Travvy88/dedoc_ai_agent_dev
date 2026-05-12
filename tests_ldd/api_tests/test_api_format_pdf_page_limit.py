# region MODULE_CONTRACT [DOMAIN(7): Testing; CONCEPT(7): PDFPageLimit, ResourceControl; TECH(7): unittest]
## @modulecontract
## @purpose Test Dedoc API PDF page limit parameter to control processing scope for large documents.
## @scope PDF page limit enforcement: verifying only specified pages are processed.
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
## CLASS [API integration test class] => TestApiPdfPageLimit
## @usecases
## - [TestClass]: Developer (Run) => VerifyAPIBehavior => TestPassOrFail
def _module_contract():
    pass
# endregion MODULE_CONTRACT
# GREP_SUMMARY: pdf, page limit, pages, resource control, API test
# STRUCTURE: ▶ ┌multipage.pdf┐ → ○ _send_request(pages=X) → ⊕ process limited pages → ⎋ page count validation

import os

from tests.api_tests.abstract_api_test import AbstractTestApiDocReader


# region CLASS_TestApiPdfPageLimit [DOMAIN(7): Testing, DocumentProcessing; CONCEPT(7): APITest; TECH(7): unittest]
## @purpose API integration tests for Dedoc document processing — TestApiPdfPageLimit.
class TestApiPdfPageLimit(AbstractTestApiDocReader):


# region METHOD__get_abs_path [DOMAIN(6): Testing; CONCEPT(6): Helper; TECH(6): unittest]
## @purpose Helper method for test assertions
## @complexity 4
    def _get_abs_path(self, file_name: str) -> str:
        return os.path.join(self.data_directory_path, "pdf_with_text_layer", file_name)

# endregion METHOD__get_abs_path
    lines = [
        "Первая страница",
        "Вторая страница",
        "Третья страница",
        "Четвёртая страница",
        "Пятая страница",
        "Шестая страница",
        "Седьмая страница",
        "Восьмая страница",
        "Девятая страница"
    ]


# region FUNC_test_no_text_layer [DOMAIN(7): Testing; CONCEPT(7): ResponseValidation; TECH(7): unittest]
## @purpose Verify API response for no text layer
## @complexity 6
    def test_no_text_layer(self) -> None:
        print("[LDD_TEST] Test result obtained, proceeding to assertions")
        self.__check_limit("false", check_partially=True)
        self.__check_out_of_limit("false")

# endregion FUNC_test_no_text_layer

# region FUNC_test_text_layer [DOMAIN(7): Testing; CONCEPT(7): ResponseValidation; TECH(7): unittest]
## @purpose Verify API response for text layer
## @complexity 6
    def test_text_layer(self) -> None:
        print("[LDD_TEST] Test result obtained, proceeding to assertions")
        self.__check_limit("true", check_partially=True)
        self.__check_out_of_limit("true")

# endregion FUNC_test_text_layer

# region FUNC_test_auto_text_layer [DOMAIN(7): Testing; CONCEPT(7): ResponseValidation; TECH(7): unittest]
## @purpose Verify API response for auto text layer
## @complexity 6
    def test_auto_text_layer(self) -> None:
        print("[LDD_TEST] Test result obtained, proceeding to assertions")
        self.__check_limit("auto", check_partially=True)
        self.__check_out_of_limit("auto")

# endregion FUNC_test_auto_text_layer

# region FUNC_test_tabby_layer [DOMAIN(7): Testing; CONCEPT(7): ResponseValidation; TECH(7): unittest]
## @purpose Verify API response for tabby layer
## @complexity 6
    def test_tabby_layer(self) -> None:
        print("[LDD_TEST] Test result obtained, proceeding to assertions")
        self.__check_limit("tabby", check_partially=True)
        self.__check_out_of_limit("tabby")

# endregion FUNC_test_tabby_layer

# region FUNC_test_auto_tabby [DOMAIN(7): Testing; CONCEPT(7): ResponseValidation; TECH(7): unittest]
## @purpose Verify API response for auto tabby
## @complexity 6
    def test_auto_tabby(self) -> None:
        print("[LDD_TEST] Test result obtained, proceeding to assertions")
        self.__check_limit("auto_tabby", check_partially=True)
        self.__check_out_of_limit("auto_tabby")

# endregion FUNC_test_auto_tabby

# region METHOD___check_out_of_limit [DOMAIN(6): Testing; CONCEPT(6): Helper; TECH(6): unittest]
## @purpose Helper method for test assertions
## @complexity 4
    def __check_out_of_limit(self, reader: str) -> None:
        text_expected = ""
        for pages in (":-1", "-1:0", "0:0", "10:11", "11:"):
            self.__check(pages, text_expected, reader=reader)

# endregion METHOD___check_out_of_limit

# region METHOD___check_limit [DOMAIN(6): Testing; CONCEPT(6): Helper; TECH(6): unittest]
## @purpose Helper method for test assertions
## @complexity 4
    def __check_limit(self, reader: str, check_partially: bool = False) -> None:
        text_expected = ""
        self.__check("2:1", text_expected, reader=reader, check_partially=check_partially)

        text_expected = "\n".join(self.lines[:])
        for pages in "", ":", "0:9", "0:20", ":9", "0:":
            self.__check(pages, text_expected, reader=reader)

        text_expected = "\n".join(self.lines[0:2])
        self.__check("1:2", text_expected, reader=reader, check_partially=check_partially)

        text_expected = self.lines[0]
        self.__check("1:1", text_expected, reader=reader, check_partially=check_partially)

        text_expected = self.lines[1]
        self.__check("2:2", text_expected, reader=reader, check_partially=check_partially)

        text_expected = "\n".join(self.lines[1:3])
        self.__check("2:3", text_expected, reader=reader, check_partially=check_partially)

        text_expected = "\n".join(self.lines[4:8])
        self.__check("5:8", text_expected, reader=reader, check_partially=check_partially)

        text_expected = self.lines[8]
        self.__check("9:", text_expected, reader=reader, check_partially=False)

        text_expected = "\n".join(self.lines[0:9])
        self.__check("1:9", text_expected, reader=reader, check_partially=False)

# endregion METHOD___check_limit

# region METHOD___check [DOMAIN(6): Testing; CONCEPT(6): Helper; TECH(6): unittest]
## @purpose Helper method for test assertions
## @complexity 4
    def __check(self, pages: str, text_expected: str, reader: str, check_partially: bool = False) -> None:

        params = dict(pdf_with_text_layer=reader, pages=pages, is_one_column_document="true")
        result = self._send_request("multipage.pdf", params)
        if check_partially:
            self.assertIn("The document is partially parsed", result["warnings"])
            self.assertIn("first_page", result["metadata"])
            self.assertIn("last_page", result["metadata"])
        tree = result["content"]["structure"]
        text = "".join([node["text"] for node in tree["subparagraphs"]])
        self.assertEqual(text_expected.strip(), text.strip(), f"{pages} and {reader}")

# endregion METHOD___check
# endregion CLASS_TestApiPdfPageLimit