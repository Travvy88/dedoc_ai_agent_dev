# region MODULE_CONTRACT [DOMAIN(7): Testing; CONCEPT(8): CoreAPI, HealthCheck; TECH(7): unittest]
## @modulecontract
## @purpose Core Dedoc API tests: version endpoint, cancellation, binary file rejection, fileless requests, plain text processing.
## @scope Core API functionality: /version endpoint, request cancellation, error handling (415, 422), basic TXT parsing.
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
## CLASS [API integration test class] => TestApi
## @usecases
## - [TestClass]: Developer (Run) => VerifyAPIBehavior => TestPassOrFail
def _module_contract():
    pass
# endregion MODULE_CONTRACT
# GREP_SUMMARY: api, version, cancellation, binary, error handling, core, health check, API test
# STRUCTURE: ▶ ┌core scenarios┐ → ○ test_version + test_cancellation + test_bin_file + test_send_wo_file + test_text → ⎋ core API assertions

import json
import os
import time

import requests
from requests import ReadTimeout

from tests.api_tests.abstract_api_test import AbstractTestApiDocReader


# region CLASS_TestApi [DOMAIN(7): Testing, DocumentProcessing; CONCEPT(7): APITest; TECH(7): unittest]
## @purpose API integration tests for Dedoc document processing — TestApi.
class TestApi(AbstractTestApiDocReader):


# region METHOD___get_version [DOMAIN(6): Testing; CONCEPT(6): Helper; TECH(6): unittest]
## @purpose Helper method for test assertions
## @complexity 4
    def __get_version(self) -> str:
        path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "VERSION"))
        with open(path) as file:
            version = file.read().strip()
            return version

# endregion METHOD___get_version

# region FUNC_test_cancellation [DOMAIN(7): Testing; CONCEPT(7): ResponseValidation; TECH(7): unittest]
## @purpose Verify API response for cancellation
## @complexity 6
    def test_cancellation(self) -> None:
        file_name = "article.pdf"
        start_time = time.time()
        with open(self._get_abs_path(os.path.join("pdf_with_text_layer", file_name)), "rb") as file:
            files = {"file": (file_name, file)}
            parameters = dict(pdf_with_text_layer=False)
            try:
                requests.post(f"http://{self._get_host()}:{self._get_port()}/upload", files=files, data=parameters, timeout=1)
            except ReadTimeout:
                pass

        file_name = "example.txt"
        with open(self._get_abs_path(os.path.join("txt", file_name)), "rb") as file:
            files = {"file": (file_name, file)}
            r = requests.post(f"http://{self._get_host()}:{self._get_port()}/upload", files=files, data={}, timeout=60)

        end_time = time.time()
        print("[LDD_TEST] Test result obtained, proceeding to assertions")
        self.assertLess(end_time - start_time, 60)
        self.assertEqual(200, r.status_code)

# endregion FUNC_test_cancellation

# region FUNC_test_bin_file [DOMAIN(7): Testing; CONCEPT(7): ResponseValidation; TECH(7): unittest]
## @purpose Verify API response for bin file
## @complexity 6
    def test_bin_file(self) -> None:
        file_name = "file.bin"
        result = self._send_request(file_name, expected_code=415)
        result = json.loads(result)
        print("[LDD_TEST] Test result obtained, proceeding to assertions")
        self.assertIn("dedoc_version", result)
        self.assertEqual(file_name, result["file_name"])
        self.assertIn("metadata", result)

# endregion FUNC_test_bin_file

# region FUNC_test_send_wo_file [DOMAIN(7): Testing; CONCEPT(7): ResponseValidation; TECH(7): unittest]
## @purpose Verify API response for send wo file
## @complexity 6
    def test_send_wo_file(self) -> None:
        self._send_request_wo_file(expected_code=422)

# endregion FUNC_test_send_wo_file

# region FUNC_test_version [DOMAIN(7): Testing; CONCEPT(7): ResponseValidation; TECH(7): unittest]
## @purpose Verify API response for version
## @complexity 6
    def test_version(self) -> None:
        version = self.__get_version()
        r = requests.get(f"http://{self._get_host()}:{self._get_port()}/version")
        print("[LDD_TEST] Test result obtained, proceeding to assertions")
        self.assertEqual(version, r.text.strip())

# endregion FUNC_test_version

# region FUNC_test_version_parsed_file [DOMAIN(7): Testing; CONCEPT(7): ResponseValidation; TECH(7): unittest]
## @purpose Verify API response for version parsed file
## @complexity 6
    def test_version_parsed_file(self) -> None:
        version = self.__get_version()
        result = self._send_request("csvs/books.csv")
        print("[LDD_TEST] Test result obtained, proceeding to assertions")
        self.assertEqual(version, result["version"].strip())

# endregion FUNC_test_version_parsed_file

# region FUNC_test_text [DOMAIN(7): Testing; CONCEPT(7): ResponseValidation; TECH(7): unittest]
## @purpose Verify API response for text
## @complexity 6
    def test_text(self) -> None:
        file_name = "example.txt"
        result = self._send_request(os.path.join("txt", file_name), data=dict(structure_type="tree"))
        content = result["content"]["structure"]
        print("[LDD_TEST] Test result obtained, proceeding to assertions")
        self.assertEqual(content["subparagraphs"][0]["text"].strip(), "Пример документа")
        self.assertEqual(content["subparagraphs"][1]["subparagraphs"][0]["text"].strip(), "1. Элемент нумерованного списка")
        self.assertEqual(content["subparagraphs"][1]["subparagraphs"][0]["metadata"]["paragraph_type"], "list_item")
        self._check_metainfo(result["metadata"], "text/plain", file_name)

# endregion FUNC_test_text
# endregion CLASS_TestApi