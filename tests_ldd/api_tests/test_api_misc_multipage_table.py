# region MODULE_CONTRACT [DOMAIN(7): Testing; CONCEPT(8): MultipageTable, TableDetection; TECH(7): unittest]
## @modulecontract
## @purpose Test Dedoc API multipage table detection and merging across page boundaries in PDF documents.
## @scope Multipage table processing: detection of tables spanning multiple pages, merging logic.
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
## CLASS [API integration test class] => TestMultipageTable
## @usecases
## - [TestClass]: Developer (Run) => VerifyAPIBehavior => TestPassOrFail
def _module_contract():
    pass
# endregion MODULE_CONTRACT
# GREP_SUMMARY: multipage, table, page, merge, detection, PDF, API test
# STRUCTURE: ▶ ┌multipage_table.pdf┐ → ○ _send_request → ⊕ detect + merge multipage tables → ⎋ table integrity checks

import os
import unittest
from typing import List

from tests.api_tests.abstract_api_test import AbstractTestApiDocReader


# region CLASS_TestMultipageTable [DOMAIN(7): Testing, DocumentProcessing; CONCEPT(7): APITest; TECH(7): unittest]
## @purpose API integration tests for Dedoc document processing — TestMultipageTable.
class TestMultipageTable(AbstractTestApiDocReader):


# region METHOD__get_abs_path [DOMAIN(6): Testing; CONCEPT(6): Helper; TECH(6): unittest]
## @purpose Helper method for test assertions
## @complexity 4
    def _get_abs_path(self, file_name: str) -> str:
        return os.path.join(self.data_directory_path, "tables", file_name)

# endregion METHOD__get_abs_path

# region METHOD__get_tables [DOMAIN(6): Testing; CONCEPT(6): Helper; TECH(6): unittest]
## @purpose Helper method for test assertions
## @complexity 4
    def _get_tables(self, file_name: str, pdf_with_text_layer: str) -> List[dict]:
        result = self._send_request(file_name, {"pdf_with_text_layer": pdf_with_text_layer})
        content = result["content"]
        self._test_table_refs(content=content)
        tables = content["tables"]
        tree = content["structure"]
        self._check_tree_sanity(tree=tree)
        return tables

# endregion METHOD__get_tables

# region FUNC_test_api_ml_table_recognition_0 [DOMAIN(7): Testing; CONCEPT(7): ResponseValidation; TECH(7): unittest]
## @purpose Verify API response for api ml table recognition 0
## @complexity 6
    def test_api_ml_table_recognition_0(self) -> None:
        file_name = "example_with_table0.pdf"
        tables = self._get_tables(file_name, pdf_with_text_layer="false")
        print("[LDD_TEST] Test result obtained, proceeding to assertions")
        self.assertEqual(len(tables), 1)

# endregion FUNC_test_api_ml_table_recognition_0

# region FUNC_test_api_ml_table_recognition_3 [DOMAIN(7): Testing; CONCEPT(7): ResponseValidation; TECH(7): unittest]
## @purpose Verify API response for api ml table recognition 3
## @complexity 6
    def test_api_ml_table_recognition_3(self) -> None:
        file_name = "example_with_table9.pdf"
        for pdf_param in ["false", "true", "tabby"]:
            tables = self._get_tables(file_name, pdf_with_text_layer=pdf_param)
            print("[LDD_TEST] Test result obtained, proceeding to assertions")
            self.assertEqual(len(tables), 1)

# endregion FUNC_test_api_ml_table_recognition_3

# region FUNC_test_api_ml_table_recognition_7 [DOMAIN(7): Testing; CONCEPT(7): ResponseValidation; TECH(7): unittest]
## @purpose Verify API response for api ml table recognition 7
## @complexity 6
    def test_api_ml_table_recognition_7(self) -> None:
        file_name = "example_table_with_90_orient_cells.pdf"
        tables = self._get_tables(file_name, pdf_with_text_layer="false")
        print("[LDD_TEST] Test result obtained, proceeding to assertions")
        self.assertEqual(len(tables), 1)

# endregion FUNC_test_api_ml_table_recognition_7

# region FUNC_test_api_ml_table_recognition_8 [DOMAIN(7): Testing; CONCEPT(7): ResponseValidation; TECH(7): unittest]
## @purpose Verify API response for api ml table recognition 8
## @complexity 6
    def test_api_ml_table_recognition_8(self) -> None:
        file_name = "example_with_table8.pdf"
        tables = self._get_tables(file_name, pdf_with_text_layer="false")
        print("[LDD_TEST] Test result obtained, proceeding to assertions")
        self.assertEqual(len(tables), 1)

# endregion FUNC_test_api_ml_table_recognition_8

# region FUNC_test_api_ml_table_recognition_synthetic_data_1 [DOMAIN(7): Testing; CONCEPT(7): ResponseValidation; TECH(7): unittest]
## @purpose Verify API response for api ml table recognition synthetic data 1
## @complexity 6
    def test_api_ml_table_recognition_synthetic_data_1(self) -> None:
        file_name = "example_mp_table_wo_repeate_header.pdf"
        for pdf_param in ["false", "true", "tabby"]:
            tables = self._get_tables(file_name, pdf_with_text_layer=pdf_param)
            print("[LDD_TEST] Test result obtained, proceeding to assertions")
            self.assertEqual(len(tables), 1)
# endregion FUNC_test_api_ml_table_recognition_synthetic_data_1

# region FUNC_test_api_ml_table_recognition_synthetic_data_3 [DOMAIN(7): Testing; CONCEPT(7): ResponseValidation; TECH(7): unittest]
## @purpose Verify API response for api ml table recognition synthetic data 3
## @complexity 6

    @unittest.skip("TLDR-886 подправить координаты ячеек таблиц табби")
    def test_api_ml_table_recognition_synthetic_data_3(self) -> None:
        file_name = "example_mp_table_with_repeate_header_2.pdf"
        for pdf_param in ["false", "true", "tabby"]:
            tables = self._get_tables(file_name, pdf_with_text_layer=pdf_param)

            print("[LDD_TEST] Test result obtained, proceeding to assertions")
            self.assertEqual(len(tables), 1, f"Error when pdf_with_text_layer={pdf_param}")
            table = tables[0]["cells"]

            self.assertListEqual(
                ["Заголовок\nБольшой", "Еще один большой заголовок", "Еще один большой заголовок", "Еще один большой заголовок", "Еще один большой заголовок"],
                self._get_text_of_row(table[0])
            )
            self.assertListEqual(["Заголовок\nБольшой", "Заголовок поменьше 1", "Заголовок поменьше 1", "Заголовок поменьше 2", "Заголовок поменьше 2"],
                                 self._get_text_of_row(table[1]))
            self.assertListEqual(["Заголовок\nБольшой", "Заголовочек 1", "Заголовочек 2", "Заголовочек 3", "Заголовочек 4"], self._get_text_of_row(table[2]))
            self.assertListEqual(["Данные 1", "Данные 1", "Данные 1", "Данные 1", "Данные 1"], self._get_text_of_row(table[3]))
            self.assertListEqual(["Данные 2", "Данные 2", "Данные 2", "Данные 2", "Данные 2"], self._get_text_of_row(table[4]))
            self.assertListEqual(["Данные 3", "Данные 3", "Данные 3", "Данные 3", "Данные 3"], self._get_text_of_row(table[5]))
            self.assertListEqual(["Данные 4", "Данные 4", "Данные 4", "Данные 4", "Данные 4"], self._get_text_of_row(table[6]))
            self.assertListEqual(["Данные 5", "Данные 5", "Данные 5", "Данные 5", "Данные 5"], self._get_text_of_row(table[7]))
            self.assertListEqual(["Данные 6", "Данные 6", "Данные 6", "Данные 6", "Данные 6"], self._get_text_of_row(table[8]))
            self.assertListEqual(["Данные 7", "Данные 7", "Данные 7", "Данные 7", "Данные 7"], self._get_text_of_row(table[9]))

# endregion FUNC_test_api_ml_table_recognition_synthetic_data_3
# endregion CLASS_TestMultipageTable