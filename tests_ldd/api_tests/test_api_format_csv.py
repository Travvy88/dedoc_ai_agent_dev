# region MODULE_CONTRACT [DOMAIN(7): Testing; CONCEPT(7): CSVFormat, TabularData; TECH(7): unittest]
## @modulecontract
## @purpose Verify Dedoc API CSV parsing with delimiter detection, encoding handling (UTF-8, CP1251), and multi-row table extraction.
## @scope CSV/TSV document processing: encoding detection, delimiter inference, table cell extraction.
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
## CLASS [API integration test class] => TestApiCSVReader
## @usecases
## - [TestClass]: Developer (Run) => VerifyAPIBehavior => TestPassOrFail
def _module_contract():
    pass
# endregion MODULE_CONTRACT
# GREP_SUMMARY: csv, tsv, delimiter, encoding, table, tabular, API test
# STRUCTURE: ▶ ┌csv/tsv file┐ → ○ _send_request → ⊕ detect delimiter + encoding → ⊕ extract table rows → ⎋ content assertions

import os
from typing import List

from tests.api_tests.abstract_api_test import AbstractTestApiDocReader


# region CLASS_TestApiCSVReader [DOMAIN(7): Testing, DocumentProcessing; CONCEPT(7): APITest; TECH(7): unittest]
## @purpose API integration tests for Dedoc document processing — TestApiCSVReader.
class TestApiCSVReader(AbstractTestApiDocReader):

    data_directory_path = os.path.join(AbstractTestApiDocReader.data_directory_path, "csvs")


# region FUNC_test_csv [DOMAIN(7): Testing; CONCEPT(7): ResponseValidation; TECH(7): unittest]
## @purpose Verify API response for csv
## @complexity 6
    def test_csv(self) -> None:
        file_name = "csv_coma.csv"
        result = self._send_request(file_name)
        print("[LDD_TEST] Test result obtained, proceeding to assertions")
        self.assertIn("delimiter is ','", result["warnings"])
        tables = result["content"]["tables"]
        self.__check_content(tables)

# endregion FUNC_test_csv

# region FUNC_test_csv_encoding [DOMAIN(7): Testing; CONCEPT(7): ResponseValidation; TECH(7): unittest]
## @purpose Verify API response for csv encoding
## @complexity 6
    def test_csv_encoding(self) -> None:
        for file_name in ("utf-8.csv", "cp1251.csv", "utf-8.tsv", "cp1251.tsv"):
            result = self._send_request(file_name)
            tables = result["content"]["tables"]
            print("[LDD_TEST] Test result obtained, proceeding to assertions")
            self.assertEqual(1, len(tables))
            table = tables[0]["cells"]
            row0 = self._get_text_of_row(table[0])
            row1 = self._get_text_of_row(table[1])
            row2 = self._get_text_of_row(table[2])
            self.assertListEqual(["имя", "фамилия", "возраст"], row0)
            self.assertListEqual(["Иванов", "Иван", "31"], row1)
            self.assertListEqual(["Алексей", "Петров", "15"], row2)

# endregion FUNC_test_csv_encoding

# region FUNC_test_csv_books [DOMAIN(7): Testing; CONCEPT(7): ResponseValidation; TECH(7): unittest]
## @purpose Verify API response for csv books
## @complexity 6
    def test_csv_books(self) -> None:
        file_name = "books.csv"
        result = self._send_request(file_name, dict(different_param="some value"))

        print("[LDD_TEST] Test result obtained, proceeding to assertions")
        self.assertIn("delimiter is ','", result["warnings"])

        tables = result["content"]["tables"]
        table = tables[0]["cells"]
        row0 = self._get_text_of_row(table[0])
        row3 = self._get_text_of_row(table[3])
        self.assertListEqual(["id", "cat", "name", "price", "inStock", "author", "series_t", "sequence_i", "genre_s"], row0)
        self.assertListEqual(["055357342X", "book", "A Storm of Swords", "7.99", "true", "George R.R. Martin", "A Song of Ice and Fire", "3", "fantasy"], row3)
        self.assertEqual("", table[-1][5]["lines"][0]["text"])

# endregion FUNC_test_csv_books

# region FUNC_test_csv_books2 [DOMAIN(7): Testing; CONCEPT(7): ResponseValidation; TECH(7): unittest]
## @purpose Verify API response for csv books2
## @complexity 6
    def test_csv_books2(self) -> None:
        file_name = "books_2.csv"
        result = self._send_request(file_name)
        print("[LDD_TEST] Test result obtained, proceeding to assertions")
        self.assertIn("delimiter is ','", result["warnings"])
        tables = result["content"]["tables"]
        table = tables[0]["cells"]
        row1 = self._get_text_of_row(table[1])
        row2 = self._get_text_of_row(table[2])
        self.assertListEqual([
            "0553573403", "book", "A Game of Throne, kings and other stuff", "7.99", "True", "George R.R. Martin", "A Song of Ice and Fire", "1", "fantasy"
        ], row1)
        self.assertListEqual(["0553579908", "book", 'A Clash of "Kings"', "7.99", "True", "George R.R. Martin", "A Song of Ice and Fire", "2", "fantasy"], row2)

# endregion FUNC_test_csv_books2

# region FUNC_test_bom_char [DOMAIN(7): Testing; CONCEPT(7): ResponseValidation; TECH(7): unittest]
## @purpose Verify API response for bom char
## @complexity 6
    def test_bom_char(self) -> None:
        file_name = "jpnum_test.csv"
        result = self._send_request(file_name)
        row1 = result["content"]["tables"][0]["cells"][0]
        print("[LDD_TEST] Test result obtained, proceeding to assertions")
        self.assertListEqual(["JPNUM"], self._get_text_of_row(row1))

# endregion FUNC_test_bom_char

# region METHOD___check_content [DOMAIN(6): Testing; CONCEPT(6): Helper; TECH(6): unittest]
## @purpose Helper method for test assertions
## @complexity 4
    def __check_content(self, tables: List[dict]) -> None:
        self.assertEqual(1, len(tables))
        table1 = tables[0]["cells"]

        row0 = self._get_text_of_row(table1[0])
        row1 = self._get_text_of_row(table1[1])
        row2 = self._get_text_of_row(table1[2])

        self.assertEqual("1", row0[0])
        self.assertEqual("2", row0[1])
        self.assertEqual("3", row0[2])

        self.assertEqual("2", row1[0])
        self.assertEqual("1", row1[1])
        self.assertEqual("5", row1[2])

        self.assertEqual("5", row2[0])
        self.assertEqual("3", row2[1])
        self.assertEqual("1", row2[2])

# endregion METHOD___check_content
# endregion CLASS_TestApiCSVReader