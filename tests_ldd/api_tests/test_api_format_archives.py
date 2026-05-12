# region MODULE_CONTRACT [DOMAIN(7): Testing; CONCEPT(7): ArchiveFormats, Compression; TECH(7): unittest]
## @modulecontract
## @purpose Test Dedoc API handling of archive files (ZIP, TAR, TAR.GZ, RAR, 7Z) with attachment extraction and content analysis.
## @scope Archive processing: multi-format extraction, subfolder traversal, unsupported file handling, broken archive resilience.
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
## CLASS [API integration test class] => TestApiArchiveReader
## @usecases
## - [TestClass]: Developer (Run) => VerifyAPIBehavior => TestPassOrFail
def _module_contract():
    pass
# endregion MODULE_CONTRACT
# GREP_SUMMARY: archive, zip, tar, rar, 7z, attachment, extraction, compression, API test
# STRUCTURE: ▶ ┌arch_with_attachs.{zip,tar,tar.gz,rar,7z}┐ → ○ _send_request(with_attachments) → ⊕ validate attachment count + content → ⎋ english_doc check

import os

from tests.api_tests.abstract_api_test import AbstractTestApiDocReader


# region CLASS_TestApiArchiveReader [DOMAIN(7): Testing, DocumentProcessing; CONCEPT(7): APITest; TECH(7): unittest]
## @purpose API integration tests for Dedoc document processing — TestApiArchiveReader.
class TestApiArchiveReader(AbstractTestApiDocReader):
    parameters = dict(with_attachments="True", need_content_analysis="True")


# region METHOD__get_abs_path [DOMAIN(6): Testing; CONCEPT(6): Helper; TECH(6): unittest]
## @purpose Helper method for test assertions
## @complexity 4
    def _get_abs_path(self, file_name: str) -> str:
        return os.path.join(self.data_directory_path, "archives", file_name)

# endregion METHOD__get_abs_path

# region METHOD__check_archive_with_english_doc [DOMAIN(6): Testing; CONCEPT(6): Helper; TECH(6): unittest]
## @purpose Helper method for test assertions
## @complexity 4
    def _check_archive_with_english_doc(self, file_name: str) -> None:
        result = self._send_request(file_name, self.parameters)
        self.assertEqual(len(result["attachments"]), 4)
        english_doc = [doc for doc in result["attachments"] if doc["metadata"]["file_name"].startswith("english_doc")][0]
        self._check_english_doc(english_doc)

# endregion METHOD__check_archive_with_english_doc

# region FUNC_test_zip [DOMAIN(7): Testing; CONCEPT(7): ResponseValidation; TECH(7): unittest]
## @purpose Verify API response for zip
## @complexity 6
    def test_zip(self) -> None:
        file_name = "arch_with_attachs.zip"
        result = self._send_request(file_name, self.parameters)
        print("[LDD_TEST] Test result obtained, proceeding to assertions")
        self.assertEqual(len(result["attachments"]), 4)

# endregion FUNC_test_zip

# region FUNC_test_tar [DOMAIN(7): Testing; CONCEPT(7): ResponseValidation; TECH(7): unittest]
## @purpose Verify API response for tar
## @complexity 6
    def test_tar(self) -> None:
        file_name = "arch_with_attachs.tar"
        result = self._send_request(file_name, self.parameters)

        print("[LDD_TEST] Test result obtained, proceeding to assertions")
        self.assertEqual(len(result["attachments"]), 4)

# endregion FUNC_test_tar

# region FUNC_test_targz [DOMAIN(7): Testing; CONCEPT(7): ResponseValidation; TECH(7): unittest]
## @purpose Verify API response for targz
## @complexity 6
    def test_targz(self) -> None:
        file_name = "arch_with_attachs.tar.gz"
        result = self._send_request(file_name, self.parameters)

        print("[LDD_TEST] Test result obtained, proceeding to assertions")
        self.assertEqual(len(result["attachments"]), 4)

# endregion FUNC_test_targz

# region FUNC_test_rar [DOMAIN(7): Testing; CONCEPT(7): ResponseValidation; TECH(7): unittest]
## @purpose Verify API response for rar
## @complexity 6
    def test_rar(self) -> None:
        file_name = "arch_with_attachs.rar"
        result = self._send_request(file_name, self.parameters)

        print("[LDD_TEST] Test result obtained, proceeding to assertions")
        self.assertEqual(len(result["attachments"]), 4)

# endregion FUNC_test_rar

# region FUNC_test_7zip [DOMAIN(7): Testing; CONCEPT(7): ResponseValidation; TECH(7): unittest]
## @purpose Verify API response for 7zip
## @complexity 6
    def test_7zip(self) -> None:
        file_name = "arch_with_attachs.7z"
        result = self._send_request(file_name, self.parameters)

        print("[LDD_TEST] Test result obtained, proceeding to assertions")
        self.assertEqual(len(result["attachments"]), 4)

# endregion FUNC_test_7zip

# region FUNC_test_zip_as_archive [DOMAIN(7): Testing; CONCEPT(7): ResponseValidation; TECH(7): unittest]
## @purpose Verify API response for zip as archive
## @complexity 6
    def test_zip_as_archive(self) -> None:
        file_name = "zipka_eng.zip"
        self._check_archive_with_english_doc(file_name)

# endregion FUNC_test_zip_as_archive

# region FUNC_test_archive_subfolder_tar [DOMAIN(7): Testing; CONCEPT(7): ResponseValidation; TECH(7): unittest]
## @purpose Verify API response for archive subfolder tar
## @complexity 6
    def test_archive_subfolder_tar(self) -> None:
        file_name = "subfolders.tar.gz"
        self._check_archive_with_english_doc(file_name)

# endregion FUNC_test_archive_subfolder_tar

# region FUNC_test_archive_subfolder_zip [DOMAIN(7): Testing; CONCEPT(7): ResponseValidation; TECH(7): unittest]
## @purpose Verify API response for archive subfolder zip
## @complexity 6
    def test_archive_subfolder_zip(self) -> None:
        file_name = "subfolders.zip"
        self._check_archive_with_english_doc(file_name)

# endregion FUNC_test_archive_subfolder_zip

# region FUNC_test_archive_subfolder_rar [DOMAIN(7): Testing; CONCEPT(7): ResponseValidation; TECH(7): unittest]
## @purpose Verify API response for archive subfolder rar
## @complexity 6
    def test_archive_subfolder_rar(self) -> None:
        file_name = "subfolders.rar"
        self._check_archive_with_english_doc(file_name)

# endregion FUNC_test_archive_subfolder_rar

# region FUNC_test_archive_subfolder_7z [DOMAIN(7): Testing; CONCEPT(7): ResponseValidation; TECH(7): unittest]
## @purpose Verify API response for archive subfolder 7z
## @complexity 6
    def test_archive_subfolder_7z(self) -> None:
        file_name = "subfolders.7z"
        self._check_archive_with_english_doc(file_name)

# endregion FUNC_test_archive_subfolder_7z

# region FUNC_test_zip_with_unsupported_file [DOMAIN(7): Testing; CONCEPT(7): ResponseValidation; TECH(7): unittest]
## @purpose Verify API response for zip with unsupported file
## @complexity 6
    def test_zip_with_unsupported_file(self) -> None:
        file_name = "arch_with_unsupport_atchs.zip"
        result = self._send_request(file_name, self.parameters)
        attachs = result["attachments"]

        print("[LDD_TEST] Test result obtained, proceeding to assertions")
        self.assertEqual(len(attachs), 7)
        unsupported = [att for att in attachs if att["metadata"]["file_name"] == "file.bin"][0]["metadata"]
        self.assertEqual(unsupported["file_type"], "application/octet-stream")

# endregion FUNC_test_zip_with_unsupported_file

# region FUNC_test_broken_archive [DOMAIN(7): Testing; CONCEPT(7): ResponseValidation; TECH(7): unittest]
## @purpose Verify API response for broken archive
## @complexity 6
    def test_broken_archive(self) -> None:
        file_name = "broken.zip"
        result = self._send_request(file_name, self.parameters)
        print("[LDD_TEST] Test result obtained, proceeding to assertions")
        self.assertEqual(len(result["attachments"]), 7)
        english_doc = [doc for doc in result["attachments"] if doc["metadata"]["file_name"].startswith("english_doc")][0]
        self._check_english_doc(english_doc)

# endregion FUNC_test_broken_archive

# region FUNC_test_empty_params [DOMAIN(7): Testing; CONCEPT(7): ResponseValidation; TECH(7): unittest]
## @purpose Verify API response for empty params
## @complexity 6
    def test_empty_params(self) -> None:
        file_name = "arch_with_attachs.zip"
        result = self._send_request(file_name, {})
        print("[LDD_TEST] Test result obtained, proceeding to assertions")
        self.assertEqual(len(result["attachments"]), 0)

# endregion FUNC_test_empty_params
# endregion CLASS_TestApiArchiveReader