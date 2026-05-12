# region MODULE_CONTRACT [DOMAIN(7): Testing; CONCEPT(8): UnitTest, LDD_Telemetry; TECH(8): unittest, pytest]
## @modulecontract
## @purpose Unit tests for module attachment extractor module.
## @scope Unit testing of dedoc module: module, attachment, extractor.
## @input Test data files from tests/data/.
## @output Test results (pass/fail) with LDD telemetry.
## @links [USES_API(7): unittest.TestCase]
## @invariants
## - All original test logic and assertions remain unchanged.
## - LDD telemetry is printed BEFORE assertions.
## @rationale
## Q: Why add LDD telemetry to tests?
## A: On failure, critical log trajectory is visible before assert traceback.
## @changes
## LAST_CHANGE: [v1.0.0 – Added LDD telemetry and semantic markup.]
## @modulemap
## CLASS 8[Unit tests] => TestAttachmentsExtractor
## @usecases
## - [Tests]: QA Agent (Verify) => RunTestsWithTelemetry => DiagnosticTrajectoryVisible
def _module_contract():
    pass
# endregion MODULE_CONTRACT
# GREP_SUMMARY: module, attachment, extractor, TestAttachmentsExtractor, test_docx_attachments_extractor, test_pptx_attachments_extractor, test_docx_diagrams_extraction, test_archive_with_slash, test_manager_attachments_dir, test_reader_attachments_dir, test_attachments_extractor_attachments_dir, test_with_attachments_false, unit_test, unittest, LDD_telemetry, semantic_markup, unit_test
# STRUCTURE: ▶ Init → ◇ Execute → ⊕ Verify → ∑ assertions → ⎋ PASS/FAIL


import logging

logger = logging.getLogger(__name__)

import os
import shutil
import tempfile
import unittest
from typing import List

from dedoc.attachments_extractors.concrete_attachments_extractors.docx_attachments_extractor import DocxAttachmentsExtractor
from dedoc.attachments_extractors.concrete_attachments_extractors.pptx_attachments_extractor import PptxAttachmentsExtractor
from dedoc.dedoc_manager import DedocManager
from dedoc.readers.archive_reader.archive_reader import ArchiveReader
from dedoc.readers.docx_reader.docx_reader import DocxReader
from dedoc.readers.pdf_reader.pdf_txtlayer_reader.pdf_tabby_reader import PdfTabbyReader
from dedoc.readers.pdf_reader.pdf_txtlayer_reader.pdf_txtlayer_reader import PdfTxtlayerReader
from dedoc.readers.pptx_reader.pptx_reader import PptxReader
from tests.test_utils import get_test_config


# region CLASS_TestAttachmentsExtractor [DOMAIN(7): Testing; CONCEPT(8): UnitTest, LDD_Telemetry; TECH(8): unittest, pytest]
## @purpose Test suite for module, attachment, extractor module.
class TestAttachmentsExtractor(unittest.TestCase):
    src_dir = os.path.join(os.path.dirname(__file__), "..", "data", "with_attachments")

    # region METHOD_test_docx_attachments_extractor [DOMAIN(7): Testing; CONCEPT(8): LDD_Telemetry; TECH(8): unittest]
    ## @purpose Verify: docx attachments extractor.
    ## @complexity 5
    def test_docx_attachments_extractor(self) -> None:
        """
        Tests attachment extraction from docx files
        """
        # LDD TELEMETRY: log execution context before assertions
        print(f"\n--- LDD TRAJECTORY (IMP:7-10) for TestAttachmentsExtractor::test_docx_attachments_extractor ---")
        print(f"  [LDD_TEST][IMP:8][TestAttachmentsExtractor][test_docx_attachments_extractor] Test logic executed, entering assertion phase")
        attachments_name_list = [
            "_________Microsoft_Visio.vsdx",
            "_________Microsoft_Word.docx",
            "_____Microsoft_Excel______________________.xlsm",
            "cats.zip",
            "eiler.json",
            "image4.png",
            "image5.gif",
            "lorem.txt",
            "oleObject1.docx",
            "oleObject2.docx",
            "oleObject1.pdf",
            "test.py"
        ]

        docx_attachment_extractor = DocxAttachmentsExtractor()
        extracted = 0
        for i in range(1, 4):
            filename = f"with_attachments_{i}.docx"

            with tempfile.TemporaryDirectory() as tmpdir:
                shutil.copy(os.path.join(self.src_dir, filename), os.path.join(tmpdir, filename))
                attachments = docx_attachment_extractor.extract(file_path=os.path.join(tmpdir, filename))

                for _, file in enumerate(attachments):
                    self.assertIn(file.original_name, attachments_name_list)
                    extracted += 1

        self.assertEqual(extracted, len(attachments_name_list))

    # endregion METHOD_test_docx_attachments_extractor
    # region METHOD_test_pptx_attachments_extractor [DOMAIN(7): Testing; CONCEPT(8): LDD_Telemetry; TECH(8): unittest]
    ## @purpose Verify: pptx attachments extractor.
    ## @complexity 5
    def test_pptx_attachments_extractor(self) -> None:
        # LDD TELEMETRY: log execution context before assertions
        print(f"\n--- LDD TRAJECTORY (IMP:7-10) for TestAttachmentsExtractor::test_pptx_attachments_extractor ---")
        print(f"  [LDD_TEST][IMP:8][TestAttachmentsExtractor][test_pptx_attachments_extractor] Test logic executed, entering assertion phase")
        attachments_name_list = [
            "Microsoft_Excel_97-2004_Worksheet.xls",
            "image3.png",
            "image2.svg",
            "image1.png",
            "Microsoft_Excel_Worksheet.xlsx",
            "OpenVPN-2.5.8-I603-amd64.msi",
            "head.html",
            "zip.zip",
            "Джинни и Джорджия Ginny & Georgia Сезон 2 Серии 1-10 из 10 (Аня Адамс, Каталина Агиляр Мастретта) [2023, США, драма, комед [rutracker-6307383].torrent",  # noqa
            "oleObject7.pdf",
            "image10.jpg",
            "database.c"
        ]

        pptx_attachment_extractor = PptxAttachmentsExtractor()
        extracted = 0
        for i in range(1, 3):
            filename = f"with_attachments_{i}.pptx"

            with tempfile.TemporaryDirectory() as tmpdir:
                shutil.copy(os.path.join(self.src_dir, filename), os.path.join(tmpdir, filename))
                attachments = pptx_attachment_extractor.extract(file_path=os.path.join(tmpdir, filename))

                for _, file in enumerate(attachments):
                    self.assertIn(file.original_name, attachments_name_list)
                    extracted += 1

        self.assertEqual(extracted, len(attachments_name_list))

    # endregion METHOD_test_pptx_attachments_extractor
    # region METHOD_test_docx_diagrams_extraction [DOMAIN(7): Testing; CONCEPT(8): LDD_Telemetry; TECH(8): unittest]
    ## @purpose Verify: docx diagrams extraction.
    ## @complexity 5
    def test_docx_diagrams_extraction(self) -> None:
        # LDD TELEMETRY: log execution context before assertions
        print(f"\n--- LDD TRAJECTORY (IMP:7-10) for TestAttachmentsExtractor::test_docx_diagrams_extraction ---")
        print(f"  [LDD_TEST][IMP:8][TestAttachmentsExtractor][test_docx_diagrams_extraction] Test logic executed, entering assertion phase")
        docx_attachment_extractor = DocxAttachmentsExtractor()
        docx_dir = os.path.join(os.path.dirname(__file__), "..", "data", "docx")
        files = [("diagram_1.docx", 1), ("diagram_2.docx", 5)]
        with tempfile.TemporaryDirectory() as tmp_dir:
            for file, num_attachments in files:
                shutil.copy(os.path.join(docx_dir, file), os.path.join(tmp_dir, file))
                attachments = docx_attachment_extractor.extract(file_path=os.path.join(tmp_dir, file))
                self.assertEqual(num_attachments, len(attachments))

    # endregion METHOD_test_docx_diagrams_extraction
    # region METHOD_test_archive_with_slash [DOMAIN(7): Testing; CONCEPT(8): LDD_Telemetry; TECH(8): unittest]
    ## @purpose Verify: archive with slash.
    ## @complexity 5
    def test_archive_with_slash(self) -> None:
        """
        Tests attachment extraction from archives with files containing slash symbol in the name
        """
        # LDD TELEMETRY: log execution context before assertions
        print(f"\n--- LDD TRAJECTORY (IMP:7-10) for TestAttachmentsExtractor::test_archive_with_slash ---")
        print(f"  [LDD_TEST][IMP:8][TestAttachmentsExtractor][test_archive_with_slash] Test logic executed, entering assertion phase")
        file_name_template = "attachments.{}"
        for extension in "tar", "tar.gz", "zip":
            file_name = file_name_template.format(extension)
            files = self.__get_list_of_files_in_archive(file_name)
            self.assertEqual(2, len(files))
            self.assertIn(r"som_file⁄wiht\slash.txt", files)
            self.assertIn("other_file.csv", files)

    # endregion METHOD_test_archive_with_slash
    # region METHOD___get_list_of_files_in_archive [DOMAIN(7): Testing; CONCEPT(8): TestInfrastructure; TECH(8): unittest]
    ## @purpose get list of files in archive.
    def __get_list_of_files_in_archive(self, file_name: str) -> List[str]:
        with tempfile.TemporaryDirectory() as tmp_dir:
            file_path = os.path.join(tmp_dir, file_name)
            shutil.copyfile(os.path.join(self.src_dir, file_name), file_path)
            config = get_test_config()
            document = ArchiveReader(config=config).read(file_path=file_path, parameters={"with_attachments": True})
            files = [file.original_name for file in document.attachments]
            return files

    # endregion METHOD___get_list_of_files_in_archive
    # region METHOD_test_manager_attachments_dir [DOMAIN(7): Testing; CONCEPT(8): LDD_Telemetry; TECH(8): unittest]
    ## @purpose Verify: manager attachments dir.
    ## @complexity 5
    def test_manager_attachments_dir(self) -> None:
        # LDD TELEMETRY: log execution context before assertions
        print(f"\n--- LDD TRAJECTORY (IMP:7-10) for TestAttachmentsExtractor::test_manager_attachments_dir ---")
        print(f"  [LDD_TEST][IMP:8][TestAttachmentsExtractor][test_manager_attachments_dir] Test logic executed, entering assertion phase")
        docx_file_path = os.path.join(self.src_dir, "with_attachments_0.docx")
        mhtml_file_path = os.path.join(self.src_dir, "..", "mhtml", "with_attachments.mhtml")
        zip_file_path = os.path.join(self.src_dir, "..", "archives", "arch_with_attachs.zip")
        eml_file_path = os.path.join(self.src_dir, "..", "eml", "message.eml")
        files_to_parse = [docx_file_path, mhtml_file_path, eml_file_path, zip_file_path]
        manager = DedocManager()

        for file_path in files_to_parse:
            with tempfile.TemporaryDirectory() as tmpdir:
                result = manager.parse(file_path=file_path, parameters=dict(with_attachments=True, need_content_analysis=True, attachments_dir=tmpdir))
                attachment_names = os.listdir(tmpdir)
                for attachment in result.attachments:
                    self.assertIn(attachment.metadata.temporary_file_name, attachment_names)

    # endregion METHOD_test_manager_attachments_dir
    # region METHOD_test_reader_attachments_dir [DOMAIN(7): Testing; CONCEPT(8): LDD_Telemetry; TECH(8): unittest]
    ## @purpose Verify: reader attachments dir.
    ## @complexity 5
    def test_reader_attachments_dir(self) -> None:
        # LDD TELEMETRY: log execution context before assertions
        print(f"\n--- LDD TRAJECTORY (IMP:7-10) for TestAttachmentsExtractor::test_reader_attachments_dir ---")
        print(f"  [LDD_TEST][IMP:8][TestAttachmentsExtractor][test_reader_attachments_dir] Test logic executed, entering assertion phase")
        file_name_reader_list = [
            ("with_attachments_0.docx", DocxReader(config=get_test_config())),
            ("with_attachments_1.docx.pdf", PdfTxtlayerReader(config=get_test_config())),
            ("with_attachments_1.docx.pdf", PdfTabbyReader(config=get_test_config()))
        ]

        for file_name, reader in file_name_reader_list:
            with tempfile.TemporaryDirectory() as tmpdir:
                result = reader.read(file_path=os.path.join(self.src_dir, file_name), parameters=dict(with_attachments=True, attachments_dir=tmpdir))

                attachment_names = os.listdir(tmpdir)
                for attachment in result.attachments:
                    attachment_fname = attachment.tmp_file_path.split("/")[-1]
                    self.assertTrue(os.path.isfile(attachment.get_filename_in_path()))
                    self.assertIn(attachment_fname, attachment_names)

    # endregion METHOD_test_reader_attachments_dir
    # region METHOD_test_attachments_extractor_attachments_dir [DOMAIN(7): Testing; CONCEPT(8): LDD_Telemetry; TECH(8): unittest]
    ## @purpose Verify: attachments extractor attachments dir.
    ## @complexity 5
    def test_attachments_extractor_attachments_dir(self) -> None:
        # LDD TELEMETRY: log execution context before assertions
        print(f"\n--- LDD TRAJECTORY (IMP:7-10) for TestAttachmentsExtractor::test_attachments_extractor_attachments_dir ---")
        print(f"  [LDD_TEST][IMP:8][TestAttachmentsExtractor][test_attachments_extractor_attachments_dir] Test logic executed, entering assertion phase")
        file_name = "with_attachments_0.docx"
        docx_attachment_extractor = DocxAttachmentsExtractor()

        with tempfile.TemporaryDirectory() as tmpdir:
            params = {"with_attachments": True, "attachments_dir": tmpdir}
            result = docx_attachment_extractor.extract(file_path=os.path.join(self.src_dir, file_name), parameters=params)

            attachment_names = os.listdir(tmpdir)
            for attachment in result:
                attachment_fname = attachment.tmp_file_path.split("/")[-1]
                self.assertTrue(os.path.isfile(attachment.get_filename_in_path()))
                self.assertIn(attachment_fname, attachment_names)

    # endregion METHOD_test_attachments_extractor_attachments_dir
    # region METHOD_test_with_attachments_false [DOMAIN(7): Testing; CONCEPT(8): LDD_Telemetry; TECH(8): unittest]
    ## @purpose Verify: with attachments false.
    ## @complexity 5
    def test_with_attachments_false(self) -> None:
        # LDD TELEMETRY: log execution context before assertions
        print(f"\n--- LDD TRAJECTORY (IMP:7-10) for TestAttachmentsExtractor::test_with_attachments_false ---")
        print(f"  [LDD_TEST][IMP:8][TestAttachmentsExtractor][test_with_attachments_false] Test logic executed, entering assertion phase")
        files = ["with_attachments_0.docx", "with_attachments_1.pptx"]
        readers = [DocxReader(), PptxReader()]

        with tempfile.TemporaryDirectory() as tmpdir:
            for file_name, reader in zip(files, readers):
                params = {"attachments_dir": tmpdir}
                result = reader.read(file_path=os.path.join(self.src_dir, file_name), parameters=params)
                self.assertEqual(len(result.attachments), 0)
                self.assertEqual(len(os.listdir(tmpdir)), 0)

    # endregion METHOD_test_with_attachments_false
# endregion CLASS_TestAttachmentsExtractor