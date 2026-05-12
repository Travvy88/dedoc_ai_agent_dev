# region MODULE_CONTRACT [DOMAIN(7): Testing; CONCEPT(7): FintocDoctype, Multilingual; TECH(7): unittest]
## @modulecontract
## @purpose Test Dedoc API parsing of financial prospectus documents (fintoc type) in EN, FR, SP languages.
## @scope Multilingual fintoc document parsing: header/raw_text paragraph types, language parameter.
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
## CLASS [API integration test class] => TestApiFintoc
## @usecases
## - [TestClass]: Developer (Run) => VerifyAPIBehavior => TestPassOrFail
def _module_contract():
    pass
# endregion MODULE_CONTRACT
# GREP_SUMMARY: fintoc, financial, prospectus, multilingual, header, raw_text, API test
# STRUCTURE: ▶ ┌prospectus_{en,fr,sp}.pdf┐ → ○ _send_request(document_type=fintoc, language=X) → ⊕ validate header + raw_text nodes → ⎋ language-specific checks

from tests.api_tests.abstract_api_test import AbstractTestApiDocReader


# region CLASS_TestApiFintoc [DOMAIN(7): Testing, DocumentProcessing; CONCEPT(7): APITest; TECH(7): unittest]
## @purpose API integration tests for Dedoc document processing — TestApiFintoc.
class TestApiFintoc(AbstractTestApiDocReader):


# region FUNC_test_article_en [DOMAIN(7): Testing; CONCEPT(7): ResponseValidation; TECH(7): unittest]
## @purpose Verify API response for article en
## @complexity 6
    def test_article_en(self) -> None:
        file_name = "fintoc/prospectus_en.pdf"
        result = self._send_request(file_name, dict(document_type="fintoc", pdf_with_text_layer="true"))

        tree = result["content"]["structure"]
        self._check_tree_sanity(tree)

        # headers
        node = self._get_by_tree_path(tree, "0.0")
        print("[LDD_TEST] Test result obtained, proceeding to assertions")
        self.assertEqual("header", node["metadata"]["paragraph_type"])
        self.assertEqual("Key Information Document (KID)", node["text"].strip())
        node = self._get_by_tree_path(tree, "0.0.0")
        self.assertEqual("header", node["metadata"]["paragraph_type"])
        self.assertEqual("PURPOSE", node["text"].strip())

        # raw text
        node = self._get_by_tree_path(tree, "0.0.0.0")
        self.assertEqual("raw_text", node["metadata"]["paragraph_type"])
        self.assertTrue(node["text"].startswith("This document provides"))

# endregion FUNC_test_article_en

# region FUNC_test_article_fr [DOMAIN(7): Testing; CONCEPT(7): ResponseValidation; TECH(7): unittest]
## @purpose Verify API response for article fr
## @complexity 6
    def test_article_fr(self) -> None:
        file_name = "fintoc/prospectus_fr.pdf"
        result = self._send_request(file_name, dict(document_type="fintoc", pdf_with_text_layer="true", language="fr", need_pdf_table_analysis="false"))

        tree = result["content"]["structure"]
        self._check_tree_sanity(tree)

        # headers
        node = self._get_by_tree_path(tree, "0.0")
        print("[LDD_TEST] Test result obtained, proceeding to assertions")
        self.assertEqual("header", node["metadata"]["paragraph_type"])
        self.assertEqual("INFORMATIONS CLES POUR L’INVESTISSEUR", node["text"].strip())
        node = self._get_by_tree_path(tree, "0.1")
        self.assertEqual("header", node["metadata"]["paragraph_type"])
        self.assertEqual("Prospectus", node["text"].strip())

        # raw text
        node = self._get_by_tree_path(tree, "0.1.0")
        self.assertEqual("raw_text", node["metadata"]["paragraph_type"])
        self.assertEqual("OPCVM relevant de la directive européenne 2009/65/CE", node["text"].strip())

# endregion FUNC_test_article_fr

# region FUNC_test_article_sp [DOMAIN(7): Testing; CONCEPT(7): ResponseValidation; TECH(7): unittest]
## @purpose Verify API response for article sp
## @complexity 6
    def test_article_sp(self) -> None:
        file_name = "fintoc/prospectus_sp.pdf"
        result = self._send_request(file_name, dict(document_type="fintoc", pdf_with_text_layer="true", language="sp", need_pdf_table_analysis="false"))

        tree = result["content"]["structure"]
        self._check_tree_sanity(tree)

        # headers
        node = self._get_by_tree_path(tree, "0.0")
        print("[LDD_TEST] Test result obtained, proceeding to assertions")
        self.assertEqual("header", node["metadata"]["paragraph_type"])
        self.assertEqual("INFORME ANUAL", node["text"].strip())
        node = self._get_by_tree_path(tree, "0.0.1")
        self.assertEqual("header", node["metadata"]["paragraph_type"])
        self.assertEqual("ÍNDICE.", node["text"].strip())

        # raw text
        node = self._get_by_tree_path(tree, "0.0.0")
        self.assertEqual("raw_text", node["metadata"]["paragraph_type"])
        self.assertTrue(node["text"].startswith("2015"))

# endregion FUNC_test_article_sp
# endregion CLASS_TestApiFintoc