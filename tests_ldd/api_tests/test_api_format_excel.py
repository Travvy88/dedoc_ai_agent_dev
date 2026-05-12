# region MODULE_CONTRACT [DOMAIN(7): Testing; CONCEPT(7): ExcelFormat, Spreadsheet; TECH(7): unittest]
## @modulecontract
## @purpose Validate Dedoc API Excel (XLS/XLSX/ODS) parsing including formula evaluation and table extraction.
## @scope Spreadsheet processing: XLS, XLSX, ODS formats, formula computation verification.
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
## CLASS [API integration test class] => TestApiExcelReader
## @usecases
## - [TestClass]: Developer (Run) => VerifyAPIBehavior => TestPassOrFail
def _module_contract():
    pass
# endregion MODULE_CONTRACT
# GREP_SUMMARY: excel, xls, xlsx, ods, spreadsheet, formula, table, API test
# STRUCTURE: ▶ ┌example.{ods,xlsx,xls}┐ → ○ _send_request → ⊕ extract tables → ◇ validate cell contents + formulas → ⎋ content assertions

import os
from typing import List

from tests.api_tests.abstract_api_test import AbstractTestApiDocReader


# region CLASS_TestApiExcelReader [DOMAIN(7): Testing, DocumentProcessing; CONCEPT(7): APITest; TECH(7): unittest]
## @purpose API integration tests for Dedoc document processing — TestApiExcelReader.
class TestApiExcelReader(AbstractTestApiDocReader):

    data_directory_path = os.path.join(AbstractTestApiDocReader.data_directory_path, "xlsx")


# region METHOD___check_content [DOMAIN(6): Testing; CONCEPT(6): Helper; TECH(6): unittest]
## @purpose Helper method for test assertions
## @complexity 4
    def __check_content(self, tables: List[dict]) -> None:
        self.assertEqual(2, len(tables))
        table1 = tables[0]
        table2 = tables[1]

        self.assertListEqual(["1.0", "2.0", "3.0"], self._get_text_of_row(table1["cells"][0]))
        self.assertListEqual(["4.0", "5.0", "6.0"], self._get_text_of_row(table1["cells"][1]))

        self.assertListEqual(["11.0", "22.0", "33.0", "44.0"], self._get_text_of_row(table2["cells"][0]))
        self.assertListEqual(["55.0", "66.0", "77.0", "88.0"], self._get_text_of_row(table2["cells"][1]))

# endregion METHOD___check_content

# region FUNC_test_ods [DOMAIN(7): Testing; CONCEPT(7): ResponseValidation; TECH(7): unittest]
## @purpose Verify API response for ods
## @complexity 6
    def test_ods(self) -> None:
        file_name = "example.ods"
        result = self._send_request(file_name)
        tables = result["content"]["tables"]
        print("[LDD_TEST] Test result obtained, proceeding to assertions")
        self.__check_content(tables)

# endregion FUNC_test_ods

# region FUNC_test_xlsx [DOMAIN(7): Testing; CONCEPT(7): ResponseValidation; TECH(7): unittest]
## @purpose Verify API response for xlsx
## @complexity 6
    def test_xlsx(self) -> None:
        file_name = "example.xlsx"
        result = self._send_request(file_name)
        tables = result["content"]["tables"]
        print("[LDD_TEST] Test result obtained, proceeding to assertions")
        self.__check_content(tables)

# endregion FUNC_test_xlsx

# region FUNC_test_xls [DOMAIN(7): Testing; CONCEPT(7): ResponseValidation; TECH(7): unittest]
## @purpose Verify API response for xls
## @complexity 6
    def test_xls(self) -> None:
        file_name = "example.xls"
        result = self._send_request(file_name)
        tables = result["content"]["tables"]
        print("[LDD_TEST] Test result obtained, proceeding to assertions")
        self.__check_content(tables)

# endregion FUNC_test_xls

# region FUNC_test_ods_formulas [DOMAIN(7): Testing; CONCEPT(7): ResponseValidation; TECH(7): unittest]
## @purpose Verify API response for ods formulas
## @complexity 6
    def test_ods_formulas(self) -> None:
        file_name = "example_formulas.ods"
        result = self._send_request(file_name)
        tables = result["content"]["tables"]
        print("[LDD_TEST] Test result obtained, proceeding to assertions")
        self.__check_content_formulas(tables)

# endregion FUNC_test_ods_formulas

# region FUNC_test_xls_formulas [DOMAIN(7): Testing; CONCEPT(7): ResponseValidation; TECH(7): unittest]
## @purpose Verify API response for xls formulas
## @complexity 6
    def test_xls_formulas(self) -> None:
        file_name = "example_formulas.xls"
        result = self._send_request(file_name)
        tables = result["content"]["tables"]
        print("[LDD_TEST] Test result obtained, proceeding to assertions")
        self.__check_content_formulas(tables)

# endregion FUNC_test_xls_formulas

# region FUNC_test_xlsx_formulas [DOMAIN(7): Testing; CONCEPT(7): ResponseValidation; TECH(7): unittest]
## @purpose Verify API response for xlsx formulas
## @complexity 6
    def test_xlsx_formulas(self) -> None:
        file_name = "example_formulas.xlsx"
        result = self._send_request(file_name)
        tables = result["content"]["tables"]
        print("[LDD_TEST] Test result obtained, proceeding to assertions")
        self.__check_content_formulas(tables)

# endregion FUNC_test_xlsx_formulas

# region METHOD___check_content_formulas [DOMAIN(6): Testing; CONCEPT(6): Helper; TECH(6): unittest]
## @purpose Helper method for test assertions
## @complexity 4
    def __check_content_formulas(self, tables: List[dict]) -> None:
        self.assertEqual(2, len(tables))
        table1, table2 = (table["cells"] for table in tables)

        self.assertListEqual(["a", "b", "c"], self._get_text_of_row(table1[0]))
        self.assertListEqual(["1.0", "2.0", "3.0"], self._get_text_of_row(table1[1]))
        self.assertListEqual(["3.0", "4.0", "7.0"], self._get_text_of_row(table1[2]))
        self.assertListEqual(["2.0", "3.0", "5.0"], self._get_text_of_row(table1[3]))
        self.assertListEqual(["5.0", "6.0", "11.0"], self._get_text_of_row(table1[4]))
        self.assertListEqual(["7.0", "33.0", "40.0"], self._get_text_of_row(table1[5]))

        self.assertListEqual(["r", "p", "s", "pi"], self._get_text_of_row(table2[0]))
        self.assertListEqual(["1.0", "6.28", "3.14", "3.14"], self._get_text_of_row(table2[1]))
        self.assertListEqual(["2.0", "12.56", "12.56", ""], self._get_text_of_row(table2[2]))
        self.assertListEqual(["3.0", "18.84", "28.26", ""], self._get_text_of_row(table2[3]))
        self.assertListEqual(["4.0", "25.12", "50.24", ""], self._get_text_of_row(table2[4]))
        self.assertListEqual(["5.0", "31.4", "78.5", ""], self._get_text_of_row(table2[5]))
        self.assertListEqual(["6.0", "37.68", "113.04", ""], self._get_text_of_row(table2[6]))
        self.assertListEqual(["7.0", "43.96", "153.86", ""], self._get_text_of_row(table2[7]))
        self.assertListEqual(["8.0", "50.24", "200.96", ""], self._get_text_of_row(table2[8]))

# endregion METHOD___check_content_formulas
# endregion CLASS_TestApiExcelReader