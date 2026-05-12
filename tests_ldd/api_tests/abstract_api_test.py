# region MODULE_CONTRACT [DOMAIN(7): Testing, DocumentProcessing; CONCEPT(8): APIIntegration, BaseClass; TECH(8): unittest, requests]
## @modulecontract
## @purpose Provide a base test class with HTTP request helpers for all Dedoc API integration tests.
## @scope HTTP request sending, response parsing, content similarity checks, metadata validation.
## @input File paths, request data dictionaries, expected HTTP codes.
## @output Parsed JSON responses or raw content from Dedoc API.
## @links [USES_API(9): Dedoc FastAPI /upload, /version endpoints; READS_DATA_FROM(8): tests/data/]
## @invariants
## - _send_request always returns dict (JSON) for code 200 with default return_format.
## - _check_metainfo checks file_type and file_name keys.
## @rationale
## Q: Why a base class with _send_request instead of pytest fixtures?
## A: unittest.TestCase inheritance allows shared assertion methods and simplifies test organization for the existing test suite.
## @changes
## LAST_CHANGE: [v1.0.0 – Initial LDD migration: added semantic markup]
## @modulemap
## CLASS 9[Base class for API doc reader tests] => AbstractTestApiDocReader
## @usecases
## - [AbstractTestApiDocReader]: TestClass (Inherit) => SendHTTPRequests => ValidateAPIResponses
def _module_contract():
    pass
# endregion MODULE_CONTRACT
# GREP_SUMMARY: API test base, HTTP requests, dedoc upload, abstract test class, response parsing, metadata check
# STRUCTURE: ⚡ ┌file_name + data + expected_code┐ → ○ _send_request → ▶ POST http://host:port/upload → ⊕ json response → ⎋ result ⟦dict|str⟧

import json
import os

import requests

from dedoc.utils.utils import similarity as utils_similarity
from tests.api_tests.content_checker import ContentChecker
from tests.test_utils import tree2linear


# region CLASS_AbstractTestApiDocReader [DOMAIN(7): Testing, DocumentProcessing; CONCEPT(8): APIIntegration, HTTPClient; TECH(8): unittest, requests]
## @purpose Base class enabling API integration tests to send documents to Dedoc and validate structured responses.
class AbstractTestApiDocReader(ContentChecker):
    data_directory_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "data"))

    # region METHOD__check_similarity [DOMAIN(6): Testing; CONCEPT(7): TextComparison; TECH(6): StringSimilarity]
    ## @purpose Compare actual text against expected text with a similarity threshold, falling back to exact assertEqual.
    ## @uses dedoc.utils.utils.similarity
    ## @io (str, str, float) -> None (asserts)
    ## @complexity 3
    def _check_similarity(self, actual: str, expected: str, threshold: float = 0.8) -> None:
        if utils_similarity(actual, expected) <= threshold:
            self.assertEqual(expected, actual)
    # endregion METHOD__check_similarity

    # region METHOD__check_metainfo [DOMAIN(5): Testing; CONCEPT(6): MetadataValidation; TECH(5): unittest]
    ## @purpose Validate that response metadata contains expected file_type and file_name.
    ## @io (dict, str, str) -> None (asserts)
    ## @complexity 2
    def _check_metainfo(self, metainfo: dict, actual_type: str, actual_name: str) -> None:
        self.assertEqual(metainfo["file_type"], actual_type)
        self.assertEqual(metainfo["file_name"], actual_name)
    # endregion METHOD__check_metainfo

    # region METHOD__get_host [DOMAIN(5): Testing; CONCEPT(5): Configuration; TECH(5): EnvironmentVariables]
    ## @purpose Resolve the Dedoc API host from environment or default to localhost.
    ## @io None -> str
    ## @complexity 1
    def _get_host(self) -> str:
        host = os.environ.get("DOC_READER_HOST", "localhost")
        return host
    # endregion METHOD__get_host

    # region METHOD__get_port [DOMAIN(5): Testing; CONCEPT(5): Configuration; TECH(5): EnvironmentVariables]
    ## @purpose Resolve the Dedoc API port from environment or default to 1231.
    ## @io None -> int
    ## @complexity 1
    def _get_port(self) -> int:
        port = int(os.environ.get("DOCREADER_PORT", "1231"))
        return port
    # endregion METHOD__get_port

    # region METHOD__get_abs_path [DOMAIN(5): Testing; CONCEPT(5): FileResolution; TECH(5): os.path]
    ## @purpose Construct absolute path to a test data file relative to data_directory_path.
    ## @io str -> str
    ## @complexity 1
    def _get_abs_path(self, file_name: str) -> str:
        return os.path.join(self.data_directory_path, file_name)
    # endregion METHOD__get_abs_path

    # region METHOD__send_request [DOMAIN(8): Testing, Networking; CONCEPT(8): HTTPRequest, APIClient; TECH(8): requests, JSON]
    ## @purpose Send a file via POST to the Dedoc upload endpoint with parameters, validate HTTP status, and parse the response.
    ## @uses requests.post
    ## @io (str, dict, int) -> dict | str
    ## @complexity 6
    def _send_request(self, file_name: str, data: dict = None, expected_code: int = 200) -> dict:
        if data is None:
            data = {}

        host = self._get_host()
        port = self._get_port()
        abs_path = self._get_abs_path(file_name)

        with open(abs_path, "rb") as file:
            files = {"file": (file_name, file)}
            r = requests.post(f"http://{host}:{port}/upload", files=files, data=data)
            self.assertEqual(expected_code, r.status_code)
            if expected_code != 200:
                return r.content.decode()
            if "return_format" in data and data["return_format"] in ("html", "tree"):
                return r.content.decode()
            else:
                return json.loads(r.content.decode())
    # endregion METHOD__send_request

    # region METHOD__send_request_wo_file [DOMAIN(8): Testing, Networking; CONCEPT(8): HTTPRequest, APIClient; TECH(8): requests, JSON]
    ## @purpose Send a POST request to Dedoc upload endpoint without an attached file, parse JSON response.
    ## @uses requests.post
    ## @io (dict, int) -> dict | None
    ## @complexity 4
    def _send_request_wo_file(self, data: dict = None, expected_code: int = 200) -> dict:
        host = self._get_host()
        port = self._get_port()

        if data is None:
            data = {}

        r = requests.post(f"http://{host}:{port}/upload", data=data)

        self.assertEqual(expected_code, r.status_code)
        if expected_code != 200:
            return None

        result = json.loads(r.content.decode())
        return result
    # endregion METHOD__send_request_wo_file

    # region METHOD__test_table_refs [DOMAIN(7): Testing; CONCEPT(7): TableAnnotation, CrossReference; TECH(6): TreeTraversal]
    ## @purpose Verify that table UID references in document structure annotations match the actual tables in content.
    ## @uses tree2linear (test_utils)
    ## @io dict -> None (asserts)
    ## @complexity 5
    def _test_table_refs(self, content: dict) -> None:
        tree = content["structure"]
        tables = content["tables"]
        lines = tree2linear(tree)
        annotations = []
        for line in lines:
            for annotation in line["annotations"]:
                if annotation["name"] == "table":
                    annotations.append(annotation["value"])
        tables_uids = {table["metadata"]["uid"] for table in tables}
        self.assertSetEqual(set(tables_uids), set(annotations))
    # endregion METHOD__test_table_refs

# endregion CLASS_AbstractTestApiDocReader
