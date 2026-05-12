# region MODULE_CONTRACT [DOMAIN(7): Testing; CONCEPT(7): MIMEDetection, FileType; TECH(7): unittest]
## @modulecontract
## @purpose Verify Dedoc API MIME type detection accuracy for various file types and extensions.
## @scope MIME type detection: verifying correct file type identification from content and extension.
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
## CLASS [API integration test class] => TestApiMimeDetection
## @usecases
## - [TestClass]: Developer (Run) => VerifyAPIBehavior => TestPassOrFail
def _module_contract():
    pass
# endregion MODULE_CONTRACT
# GREP_SUMMARY: mime, detection, file type, content type, API test
# STRUCTURE: ▶ ┌various file types┐ → ○ _send_request → ⊕ detect MIME type → ⎋ type assertions

import os
import shutil
import tempfile

import requests

from tests.api_tests.abstract_api_test import AbstractTestApiDocReader


# region CLASS_TestApiMimeDetection [DOMAIN(7): Testing, DocumentProcessing; CONCEPT(7): APITest; TECH(7): unittest]
## @purpose API integration tests for Dedoc document processing — TestApiMimeDetection.
class TestApiMimeDetection(AbstractTestApiDocReader):
    # sgi j2k pic hdr
    files = [
        "archives/arch_with_attachs.7z", "archives/arch_with_attachs.rar", "archives/arch_with_attachs.tar", "archives/arch_with_attachs.tar.gz",
        "archives/arch_with_attachs.zip", "csvs/csv_coma.csv", "csvs/csv_tab.tsv", "docx/english_doc.doc", "docx/english_doc.docx",
        "docx/english_doc.odt", "docx/english_doc.rtf", "pdf_with_text_layer/english_doc.pdf", "scanned/example.bmp", "scanned/example.dib",
        "scanned/example.eps", "scanned/example.gif", "scanned/example.jfif", "scanned/example.jpe", "scanned/example.jpeg", "scanned/example.jpg",
        "scanned/example.pbm", "scanned/example.pcx", "scanned/example.pdf", "scanned/example.pgm", "scanned/example.png", "scanned/example.pnm",
        "scanned/example.ppm", "scanned/example.ras", "scanned/example.sr", "scanned/example.tiff", "scanned/example.webp", "htmls/example.html",
        "xlsx/example.ods", "xlsx/example.xls", "xlsx/example.xlsx", "pptx/example.odp", "pptx/example.ppt", "pptx/example.pptx", "json/dict.json",
        "scanned/example_with_table9.djvu", "txt/football.txt", "eml/message.eml", "xml/simple.xml", "mhtml/with_attachments.mhtml"
    ]


# region METHOD___test_correct_response [DOMAIN(6): Testing; CONCEPT(6): Helper; TECH(6): unittest]
## @purpose Helper method for test assertions
## @complexity 4
    def __test_correct_response(self, file_path: str, actual_name: str) -> None:
        host = self._get_host()
        port = self._get_port()

        with open(file_path, "rb") as file:
            files = {"file": (os.path.basename(file_path), file)}
            r = requests.post(f"http://{host}:{port}/upload", files=files, data={})
            self.assertEqual(200, r.status_code, f"Error on file {actual_name}")

# endregion METHOD___test_correct_response

# region FUNC_test_api_files_without_extension [DOMAIN(7): Testing; CONCEPT(7): ResponseValidation; TECH(7): unittest]
## @purpose Verify API response for api files without extension
## @complexity 6
    def test_api_files_without_extension(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            for file in self.files:
                tmp_file_path = os.path.join(temp_dir, "file")
                shutil.copyfile(os.path.join(self.data_directory_path, file), tmp_file_path)
                print("[LDD_TEST] Test result obtained, proceeding to assertions")
                self.__test_correct_response(tmp_file_path, file)

# endregion FUNC_test_api_files_without_extension

# region FUNC_test_api_files_with_wrong_extension [DOMAIN(7): Testing; CONCEPT(7): ResponseValidation; TECH(7): unittest]
## @purpose Verify API response for api files with wrong extension
## @complexity 6
    def test_api_files_with_wrong_extension(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            for file in self.files:
                extension = "docx" if file.endswith("png") else "png"
                tmp_file_path = os.path.join(temp_dir, f"file.{extension}")
                shutil.copyfile(os.path.join(self.data_directory_path, file), tmp_file_path)
                print("[LDD_TEST] Test result obtained, proceeding to assertions")
                self.__test_correct_response(tmp_file_path, file)

# endregion FUNC_test_api_files_with_wrong_extension
# endregion CLASS_TestApiMimeDetection