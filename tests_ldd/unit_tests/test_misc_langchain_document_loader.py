# region MODULE_CONTRACT [DOMAIN(7): Testing; CONCEPT(8): UnitTest, LDD_Telemetry; TECH(8): unittest, pytest]
## @modulecontract
## @purpose Unit tests for misc langchain document loader module.
## @scope Unit testing of dedoc module: misc, langchain, document, loader.
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
## CLASS 8[Unit tests] => TestLangchainDocumentLoader
## @usecases
## - [Tests]: QA Agent (Verify) => RunTestsWithTelemetry => DiagnosticTrajectoryVisible
def _module_contract():
    pass
# endregion MODULE_CONTRACT
# GREP_SUMMARY: misc, langchain, document, loader, TestLangchainDocumentLoader, test_make_manager_config, test_make_manager_pdf_config, test_dedoc_file_loader, test_dedoc_api_loader, test_dedoc_pdf_loader, test_dedoc_base_loader, unit_test, unittest, LDD_telemetry, semantic_markup, unit_test
# STRUCTURE: ▶ Init → ◇ Execute → ⊕ Verify → ∑ assertions → ⎋ PASS/FAIL


import logging

logger = logging.getLogger(__name__)

import os
import unittest

from dedoc.dedoc_manager import DedocManager
from dedoc.utils.langchain import make_manager_config, make_manager_pdf_config


# region CLASS_TestLangchainDocumentLoader [DOMAIN(7): Testing; CONCEPT(8): UnitTest, LDD_Telemetry; TECH(8): unittest, pytest]
## @purpose Test suite for misc, langchain, document, loader module.
class TestLangchainDocumentLoader(unittest.TestCase):
    test_folder_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), "..", "data")
    test_files = [
        "archives/zipka.zip", "archives/zipka.tar", "archives/zipka.rar", "archives/zipka.7z",
        "csvs/csv_coma.csv", "csvs/csv_tab.tsv",
        "docx/english_doc.docx", "docx/english_doc.doc", "docx/english_doc.odt", "docx/english_doc.rtf",
        "xlsx/example.xlsx", "xlsx/example.xls", "xlsx/example.ods",
        "pptx/example.pptx", "pptx/example.ppt", "pptx/example.odp",
        "htmls/example.html", "eml/message.eml", "mhtml/with_attachments.mhtml",
        "json/example2.json", "txt/example.txt", "xml/simple.xml",
        "scanned/example.png", "scanned/example.pdf", "scanned/example.jpg", "scanned/example_with_table7.djvu",
        "pdf_auto/mixed_pdf.pdf", "pdf_with_text_layer/example.pdf",
    ]

    # region METHOD_test_make_manager_config [DOMAIN(7): Testing; CONCEPT(8): LDD_Telemetry; TECH(8): unittest]
    ## @purpose Verify: make manager config.
    ## @complexity 5
    def test_make_manager_config(self) -> None:
        # LDD TELEMETRY: log execution context before assertions
        print(f"\n--- LDD TRAJECTORY (IMP:7-10) for TestLangchainDocumentLoader::test_make_manager_config ---")
        print(f"  [LDD_TEST][IMP:8][TestLangchainDocumentLoader][test_make_manager_config] Test logic executed, entering assertion phase")
        for file in self.test_files:
            manager_config = make_manager_config(file_path=os.path.join(self.test_folder_path, file), split="node", parsing_params={})
            manager = DedocManager(manager_config=manager_config)
            manager.parse(file_path=os.path.join(self.test_folder_path, file))

    # endregion METHOD_test_make_manager_config
    # region METHOD_test_make_manager_pdf_config [DOMAIN(7): Testing; CONCEPT(8): LDD_Telemetry; TECH(8): unittest]
    ## @purpose Verify: make manager pdf config.
    ## @complexity 5
    def test_make_manager_pdf_config(self) -> None:
        # LDD TELEMETRY: log execution context before assertions
        print(f"\n--- LDD TRAJECTORY (IMP:7-10) for TestLangchainDocumentLoader::test_make_manager_pdf_config ---")
        print(f"  [LDD_TEST][IMP:8][TestLangchainDocumentLoader][test_make_manager_pdf_config] Test logic executed, entering assertion phase")
        pdf_file_path = os.path.join(self.test_folder_path, "pdf_auto", "mixed_pdf.pdf")
        for pdf_with_text_layer in ("true", "tabby", "false", "auto", "auto_tabby"):
            manager_config = make_manager_pdf_config(file_path=pdf_file_path, split="node", parsing_params=dict(pdf_with_text_layer=pdf_with_text_layer))
            manager = DedocManager(manager_config=manager_config)
            manager.parse(file_path=pdf_file_path, parameters=dict(pdf_with_text_layer=pdf_with_text_layer))

    # endregion METHOD_test_make_manager_pdf_config
    # region METHOD_test_dedoc_file_loader [DOMAIN(7): Testing; CONCEPT(8): LDD_Telemetry; TECH(8): unittest]
    ## @purpose Verify: dedoc file loader.
    ## @complexity 5
    def test_dedoc_file_loader(self) -> None:
        # LDD TELEMETRY: log execution context before assertions
        print(f"\n--- LDD TRAJECTORY (IMP:7-10) for TestLangchainDocumentLoader::test_dedoc_file_loader ---")
        print(f"  [LDD_TEST][IMP:8][TestLangchainDocumentLoader][test_dedoc_file_loader] Test logic executed, entering assertion phase")
        from dedoc_loader import DedocFileLoader

        for file in self.test_files:
            loader = DedocFileLoader(os.path.join(self.test_folder_path, file), split="document", with_tables=False)
            docs = loader.load()
            self.assertEqual(1, len(docs))

    # endregion METHOD_test_dedoc_file_loader
    # region METHOD_test_dedoc_api_loader [DOMAIN(7): Testing; CONCEPT(8): LDD_Telemetry; TECH(8): unittest]
    ## @purpose Verify: dedoc api loader.
    ## @complexity 5
    def test_dedoc_api_loader(self) -> None:
        # LDD TELEMETRY: log execution context before assertions
        print(f"\n--- LDD TRAJECTORY (IMP:7-10) for TestLangchainDocumentLoader::test_dedoc_api_loader ---")
        print(f"  [LDD_TEST][IMP:8][TestLangchainDocumentLoader][test_dedoc_api_loader] Test logic executed, entering assertion phase")
        from dedoc_loader import DedocAPIFileLoader

        dedoc_url = f"http://{os.environ.get('DOC_READER_HOST', '0.0.0.0')}:1231"
        for file in self.test_files:
            loader = DedocAPIFileLoader(os.path.join(self.test_folder_path, file), url=dedoc_url, split="document", with_tables=False)
            docs = loader.load()
            self.assertEqual(1, len(docs))

    # endregion METHOD_test_dedoc_api_loader
    # region METHOD_test_dedoc_pdf_loader [DOMAIN(7): Testing; CONCEPT(8): LDD_Telemetry; TECH(8): unittest]
    ## @purpose Verify: dedoc pdf loader.
    ## @complexity 5
    def test_dedoc_pdf_loader(self) -> None:
        # LDD TELEMETRY: log execution context before assertions
        print(f"\n--- LDD TRAJECTORY (IMP:7-10) for TestLangchainDocumentLoader::test_dedoc_pdf_loader ---")
        print(f"  [LDD_TEST][IMP:8][TestLangchainDocumentLoader][test_dedoc_pdf_loader] Test logic executed, entering assertion phase")
        from pdf import DedocPDFLoader

        pdf_file_path = os.path.join(self.test_folder_path, "pdf_auto", "mixed_pdf.pdf")
        for mode in ("true", "tabby", "false", "auto", "auto_tabby"):
            loader = DedocPDFLoader(pdf_file_path, split="document", with_tables=False, pdf_with_text_layer=mode)
            docs = loader.load()
            self.assertEqual(1, len(docs))

    # endregion METHOD_test_dedoc_pdf_loader
    # region METHOD_test_dedoc_base_loader [DOMAIN(7): Testing; CONCEPT(8): LDD_Telemetry; TECH(8): unittest]
    ## @purpose Verify: dedoc base loader.
    ## @complexity 5
    def test_dedoc_base_loader(self) -> None:
        # LDD TELEMETRY: log execution context before assertions
        print(f"\n--- LDD TRAJECTORY (IMP:7-10) for TestLangchainDocumentLoader::test_dedoc_base_loader ---")
        print(f"  [LDD_TEST][IMP:8][TestLangchainDocumentLoader][test_dedoc_base_loader] Test logic executed, entering assertion phase")
        from dedoc_loader import DedocFileLoader

        file_path = os.path.join(self.test_folder_path, "with_attachments", "example_with_attachments_depth_1.pdf")

        for split in ("line", "page", "node"):
            loader = DedocFileLoader(file_path, split=split, with_tables=False)
            docs = loader.load()
            if split == "page":
                self.assertEqual(1, len(docs))
            else:
                self.assertGreater(len(docs), 1)

        loader = DedocFileLoader(
            file_path, split="document", with_tables=True, with_attachments=True, need_content_analysis=True, need_pdf_table_analysis=False
        )
        text_docs, table_docs, attachment_docs = [], [], []
        for doc in loader.load():
            doc_type = doc.metadata.get("type", "")
            if doc_type == "table":
                table_docs.append(doc)
                self.assertIn("text_as_html", doc.metadata)
            elif doc_type == "attachment":
                attachment_docs.append(doc)
            else:
                text_docs.append(doc)

        self.assertEqual(1, len(text_docs))
        self.assertEqual(1, len(table_docs))
        self.assertEqual(5, len(attachment_docs))

    # endregion METHOD_test_dedoc_base_loader
# endregion CLASS_TestLangchainDocumentLoader