# region MODULE_CONTRACT [DOMAIN(7): Testing; CONCEPT(7): XMLFormat, StructuredData; TECH(7): unittest]
## @modulecontract
## @purpose Test Dedoc API XML document parsing with structure extraction and content validation.
## @scope XML document processing: structure parsing, element extraction, content validation.
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
## CLASS [API integration test class] => TestApiXML
## @usecases
## - [TestClass]: Developer (Run) => VerifyAPIBehavior => TestPassOrFail
def _module_contract():
    pass
# endregion MODULE_CONTRACT
# GREP_SUMMARY: xml, structured, markup, parsing, API test
# STRUCTURE: ▶ ┌example.xml┐ → ○ _send_request → ⊕ parse XML structure → ⎋ content validation

import os

from tests.api_tests.abstract_api_test import AbstractTestApiDocReader


# region CLASS_TestApiXML [DOMAIN(7): Testing, DocumentProcessing; CONCEPT(7): APITest; TECH(7): unittest]
## @purpose API integration tests for Dedoc document processing — TestApiXML.
class TestApiXML(AbstractTestApiDocReader):

    data_directory_path = os.path.join(AbstractTestApiDocReader.data_directory_path, "xml")


# region FUNC_test_xml [DOMAIN(7): Testing; CONCEPT(7): ResponseValidation; TECH(7): unittest]
## @purpose Verify API response for xml
## @complexity 6
    def test_xml(self) -> None:
        file_name = "simple.xml"
        result = self._send_request(file_name, data={"structure_type": "linear"})
        subparagraphs = result["content"]["structure"]["subparagraphs"]
        print("[LDD_TEST] Test result obtained, proceeding to assertions")
        self.assertEqual('<?xml version="1.0" encoding="UTF-8"?>\n', subparagraphs[0]["text"])
        self.assertEqual("<note>\n", subparagraphs[1]["text"])
        self.assertEqual("  <to>Tove</to>\n", subparagraphs[2]["text"])
        self.assertEqual("</note>", subparagraphs[3]["text"])

# endregion FUNC_test_xml
# endregion CLASS_TestApiXML