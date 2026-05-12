# region MODULE_CONTRACT [DOMAIN(7): Testing; CONCEPT(7): EmailFormat, MIME; TECH(7): unittest]
## @modulecontract
## @purpose Test Dedoc API parsing of email files with attachment extraction and content analysis.
## @scope Email format processing: MIME parsing, attachment extraction, content analysis.
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
## CLASS [API integration test class] => TestApiEmailReader
## @usecases
## - [TestClass]: Developer (Run) => VerifyAPIBehavior => TestPassOrFail
def _module_contract():
    pass
# endregion MODULE_CONTRACT
# GREP_SUMMARY: email, EML, MIME, attachment, API test
# STRUCTURE: ▶ ┌email.eml/msg┐ → ○ _send_request → ⊕ parse MIME + extract attachments → ⎋ content validation

import os

from tests.api_tests.abstract_api_test import AbstractTestApiDocReader


# region CLASS_TestApiEmailReader [DOMAIN(7): Testing, DocumentProcessing; CONCEPT(7): APITest; TECH(7): unittest]
## @purpose API integration tests for Dedoc document processing — TestApiEmailReader.
class TestApiEmailReader(AbstractTestApiDocReader):


# region METHOD__get_abs_path [DOMAIN(6): Testing; CONCEPT(6): Helper; TECH(6): unittest]
## @purpose Helper method for test assertions
## @complexity 4
    def _get_abs_path(self, file_name: str) -> str:
        return os.path.join(self.data_directory_path, "eml", file_name)

# endregion METHOD__get_abs_path

# region FUNC_test_email_file [DOMAIN(7): Testing; CONCEPT(7): ResponseValidation; TECH(7): unittest]
## @purpose Verify API response for email file
## @complexity 6
    def test_email_file(self) -> None:
        file_name = "spam_mail.eml"
        result = self._send_request(file_name, data={"with_attachments": "true"})
        attachments = result["attachments"]

        print("[LDD_TEST] Test result obtained, proceeding to assertions")
        self.assertEqual(len(attachments), 1)  # message header fields
        self.assertIn("message_header_", attachments[0]["metadata"]["file_name"])
        content = result["content"]
        structure = content["structure"]
        self._check_tree_sanity(structure)
        self.assertEqual("[Spam]Artificial flowers  for decors", structure["text"])

        # require fields [subject, from, to, cc, bcc, date, reply-to]

        from_message = structure["subparagraphs"][1]
        to_message = structure["subparagraphs"][2]
        self.assertEqual("modis@ispras.ru", to_message["text"])
        self.assertEqual("to", to_message["metadata"]["paragraph_type"])
        self.assertEqual('"sunny_goldensun@126.com" <sunny_goldensun@126.com>', from_message["text"])
        self.assertEqual("from", from_message["metadata"]["paragraph_type"])

# endregion FUNC_test_email_file

# region FUNC_test_email_with_attachments [DOMAIN(7): Testing; CONCEPT(7): ResponseValidation; TECH(7): unittest]
## @purpose Verify API response for email with attachments
## @complexity 6
    def test_email_with_attachments(self) -> None:
        file_name = "message.eml"
        result = self._send_request(file_name, data={"with_attachments": "true"})
        structure = result["content"]["structure"]
        attachments = result["attachments"]
        self._check_tree_sanity(structure)

        print("[LDD_TEST] Test result obtained, proceeding to assertions")
        self.assertEqual("TetSubj", structure["text"])
        from_message = structure["subparagraphs"][1]
        to_message = structure["subparagraphs"][2]
        self.assertEqual('"bb@bb.bb" <bb@bb.bb>', to_message["text"])
        self.assertEqual("to", to_message["metadata"]["paragraph_type"])
        self.assertEqual('"aa@aa.aa" <aa@aa.aa>', from_message["text"])
        self.assertEqual("from", from_message["metadata"]["paragraph_type"])

        self.assertEqual(3, len(attachments))
        self.assertIn("message_header_", attachments[0]["metadata"]["file_name"])
        self.assertEqual("grafana.jpg", attachments[1]["metadata"]["file_name"])
        self.assertEqual("KY100Product SheetProduct Sheet.pdf", attachments[2]["metadata"]["file_name"])

# endregion FUNC_test_email_with_attachments
# endregion CLASS_TestApiEmailReader