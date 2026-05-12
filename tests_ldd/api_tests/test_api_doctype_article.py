# region MODULE_CONTRACT [DOMAIN(7): Testing, DocumentProcessing; CONCEPT(8): ArticleDoctype, Grobid; TECH(7): unittest]
## @modulecontract
## @purpose Verify Dedoc API responses for article-type documents (Grobid-based structure extraction, bibliography, citations).
## @scope Article document parsing via Grobid: author info, sections, bibliography, cross-references, tables.
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
## CLASS [API integration test class] => TestApiArticle
## @usecases
## - [TestClass]: Developer (Run) => VerifyAPIBehavior => TestPassOrFail
def _module_contract():
    pass
# endregion MODULE_CONTRACT
# GREP_SUMMARY: article, Grobid, bibliography, citation, author, section, doctype, API test, document processing
# STRUCTURE: ▶ ┌article.pdf┐ → ○ _send_request(document_type=article) → ⊕ validate authors + sections + bibliography → ∑ bib citations + table refs → ⎋ sanity check

from tests.api_tests.abstract_api_test import AbstractTestApiDocReader


# region CLASS_TestApiArticle [DOMAIN(7): Testing, DocumentProcessing; CONCEPT(7): APITest; TECH(7): unittest]
## @purpose API integration tests for Dedoc document processing — TestApiArticle.
class TestApiArticle(AbstractTestApiDocReader):


# region FUNC_test_article [DOMAIN(7): Testing; CONCEPT(7): ResponseValidation; TECH(7): unittest]
## @purpose Verify API response for article
## @complexity 6
    def test_article(self) -> None:
        file_name = "pdf_with_text_layer/article.pdf"
        result = self._send_request(file_name, dict(document_type="article"))
        print("[LDD_TEST] Test result obtained, proceeding to assertions")
        self.assertEqual(result["warnings"], ["use GROBID (version: 0.8.0)"])

        tree = result["content"]["structure"]
        self._check_tree_sanity(tree)

        # author 1 info
        self.assertEqual("author", self._get_by_tree_path(tree, "0.0")["metadata"]["paragraph_type"])
        self.assertEqual("author_first_name", self._get_by_tree_path(tree, "0.0.0")["metadata"]["paragraph_type"])  # author 1 first name
        self.assertEqual("Sonia", self._get_by_tree_path(tree, "0.0.0")["text"])
        self.assertEqual("author_surname", self._get_by_tree_path(tree, "0.0.1")["metadata"]["paragraph_type"])  # author 1 second name
        self.assertEqual("Belaïd", self._get_by_tree_path(tree, "0.0.1")["text"])
        self.assertEqual("author_affiliation", self._get_by_tree_path(tree, "0.0.2")["metadata"]["paragraph_type"])  # the first affiliation of author 1
        self.assertEqual("org_name", self._get_by_tree_path(tree, "0.0.2.0")["metadata"]["paragraph_type"])
        self.assertEqual("École Normale Supérieure", self._get_by_tree_path(tree, "0.0.2.0")["text"])
        self.assertEqual("author_affiliation", self._get_by_tree_path(tree, "0.0.3")["metadata"]["paragraph_type"])  # the second affiliation of author 1
        self.assertEqual("org_name", self._get_by_tree_path(tree, "0.0.3.0")["metadata"]["paragraph_type"])
        self.assertEqual("Thales Communications & Security", self._get_by_tree_path(tree, "0.0.3.0")["text"])

        # author 3 info
        self.assertEqual("author", self._get_by_tree_path(tree, "0.2")["metadata"]["paragraph_type"])
        self.assertEqual("author_first_name", self._get_by_tree_path(tree, "0.2.0")["metadata"]["paragraph_type"])  # author 3 first name
        self.assertEqual("François", self._get_by_tree_path(tree, "0.2.0")["text"])
        self.assertEqual("author_surname", self._get_by_tree_path(tree, "0.2.1")["metadata"]["paragraph_type"])  # author 3 second name
        self.assertEqual("Xavier-Standaert", self._get_by_tree_path(tree, "0.2.1")["text"])
        self.assertEqual("author_affiliation", self._get_by_tree_path(tree, "0.2.2")["metadata"]["paragraph_type"])  # the first affiliation of author 3
        self.assertEqual("org_name", self._get_by_tree_path(tree, "0.2.2.0")["metadata"]["paragraph_type"])
        self.assertEqual("ICTEAM/ELEN/Crypto Group", self._get_by_tree_path(tree, "0.2.2.0")["text"])

        # check section
        self.assertEqual("section", self._get_by_tree_path(tree, "0.4")["metadata"]["paragraph_type"])
        self.assertEqual("1 Introduction", self._get_by_tree_path(tree, "0.4")["text"])

        # check bibliography list
        self.assertEqual("bibliography", self._get_by_tree_path(tree, "0.12")["metadata"]["paragraph_type"])
        self.assertEqual(65, len(self._get_by_tree_path(tree, "0.12")["subparagraphs"]))

        # check bib_item 1 recognizing
        self.assertEqual("title", self._get_by_tree_path(tree, "0.12.0.0")["metadata"]["paragraph_type"])
        self.assertEqual("Leakage-resilient symmetric encryption via re-keying", self._get_by_tree_path(tree, "0.12.0.0")["text"])
        self.assertEqual("title_conference_proceedings", self._get_by_tree_path(tree, "0.12.0.1")["metadata"]["paragraph_type"])
        self.assertEqual("Bertoni and Coron", self._get_by_tree_path(tree, "0.12.0.1")["text"])
        self.assertEqual("author", self._get_by_tree_path(tree, "0.12.0.2")["metadata"]["paragraph_type"])  # author 1
        self.assertEqual("Michel Abdalla", self._get_by_tree_path(tree, "0.12.0.2")["text"])
        self.assertEqual("biblScope_volume", self._get_by_tree_path(tree, "0.12.0.5")["metadata"]["paragraph_type"])  # author 1
        self.assertEqual("4", self._get_by_tree_path(tree, "0.12.0.5")["text"])
        self.assertEqual("biblScope_page", self._get_by_tree_path(tree, "0.12.0.6")["metadata"]["paragraph_type"])  # author 1
        self.assertEqual("471-488", self._get_by_tree_path(tree, "0.12.0.6")["text"])

        # check cite on bib_item
        bibliography_item_uuid = self._get_by_tree_path(tree, "0.12.57")["metadata"]["uid"]  # checking on [58] references
        section = self._get_by_tree_path(tree, "0.4.0")
        bibliography_refs_in_text = [ann for ann in section["annotations"] if ann["name"] == "reference" and ann["value"] == bibliography_item_uuid]
        # We must found two refs [58] in Introduction section
        self.assertEqual(len(bibliography_refs_in_text), 2)
        self.assertEqual(["58,", "58,"], [section["text"][bibliography_refs_in_text[n]["start"]:bibliography_refs_in_text[n]["end"]] for n in range(2)])

        # check tables
        self.assertEqual(len(result["content"]["tables"]), 2)
        table = result["content"]["tables"][0]
        self.assertEqual(table["metadata"]["title"], "Table 1 .Performance of some illustrative AES implementations.")
        self.assertEqual(self._get_text_of_row(table["cells"][0]), ["Software (8-bit)", "code size", "cycle", "cost", "physical"])
        section_with_table_refs = self._get_by_tree_path(tree, "0.7.0")
        table_refs_in_text = [ann for ann in section_with_table_refs["annotations"] if ann["name"] == "table" and ann["value"] == table["metadata"]["uid"]]
        self.assertEqual(len(table_refs_in_text), 2)
        self.assertEqual(["1", "1"], [section_with_table_refs["text"][table_refs_in_text[n]["start"]:table_refs_in_text[n]["end"]] for n in range(2)])

        table = result["content"]["tables"][1]  # Grobid can't recognize vertical orientation tables
        self.assertEqual(table["metadata"]["title"], "Table 2 .List of our target implementations.")

# endregion FUNC_test_article
# endregion CLASS_TestApiArticle