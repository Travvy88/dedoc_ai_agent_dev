# region MODULE_CONTRACT [DOMAIN(7): Testing; CONCEPT(7): TZDoctype, TechnicalTask; TECH(7): unittest]
## @modulecontract
## @purpose Validate Dedoc API parsing of technical task (TZ) documents with TOC, items, parts, and named sections.
## @scope TZ document processing: table of contents validation, part/subitem hierarchy, multi-format (DOC/DOCX/PDF/TXT).
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
## CLASS [API integration test class] => TestTZApiDocReader
## @usecases
## - [TestClass]: Developer (Run) => VerifyAPIBehavior => TestPassOrFail
def _module_contract():
    pass
# endregion MODULE_CONTRACT
# GREP_SUMMARY: tz, technical task, TOC, part, item, named_item, API test
# STRUCTURE: ▶ ┌tz.{doc,docx,pdf,txt}┐ → ○ _send_request(document_type=tz) → ⊕ _check_tz_tree → ◇ validate toc + body + items → ⎋ hierarchy assertions

import os
import re
from typing import Dict

from tests.api_tests.abstract_api_test import AbstractTestApiDocReader
from tests.test_utils import tree2linear


# region CLASS_TestTZApiDocReader [DOMAIN(7): Testing, DocumentProcessing; CONCEPT(7): APITest; TECH(7): unittest]
## @purpose API integration tests for Dedoc document processing — TestTZApiDocReader.
class TestTZApiDocReader(AbstractTestApiDocReader):


# region FUNC_test_doc_tz [DOMAIN(7): Testing; CONCEPT(7): ResponseValidation; TECH(7): unittest]
## @purpose Verify API response for doc tz
## @complexity 6
    def test_doc_tz(self) -> None:
        file_name = "alpaca_tz.doc"
        result = self._send_request(file_name, dict(document_type="tz"))
        self._check_content(result, file_name)

# endregion FUNC_test_doc_tz

# region FUNC_test_docx_tz [DOMAIN(7): Testing; CONCEPT(7): ResponseValidation; TECH(7): unittest]
## @purpose Verify API response for docx tz
## @complexity 6
    def test_docx_tz(self) -> None:
        file_name = "alpaca_tz.docx"
        result = self._send_request(file_name, dict(document_type="tz"))
        self._check_content(result, file_name)

# endregion FUNC_test_docx_tz

# region FUNC_test_pdf_tz [DOMAIN(7): Testing; CONCEPT(7): ResponseValidation; TECH(7): unittest]
## @purpose Verify API response for pdf tz
## @complexity 6
    def test_pdf_tz(self) -> None:
        file_name = "alpaca_tz.pdf"
        result = self._send_request(file_name, dict(document_type="tz"))
        print("[LDD_TEST] Test result obtained, proceeding to assertions")
        self.assertIn("metadata", result)

# endregion FUNC_test_pdf_tz

# region FUNC_test_txt_tz [DOMAIN(7): Testing; CONCEPT(7): ResponseValidation; TECH(7): unittest]
## @purpose Verify API response for txt tz
## @complexity 6
    def test_txt_tz(self) -> None:
        file_name = "tz.txt"
        result = self._send_request(file_name, dict(document_type="tz"))
        content = result["content"]
        tree = content["structure"]
        self._check_tz_tree(tree)
        print("[LDD_TEST] Test result obtained, proceeding to assertions")
        self.assertIn("metadata", result)

# endregion FUNC_test_txt_tz

# region FUNC_test_moloko_tz [DOMAIN(7): Testing; CONCEPT(7): ResponseValidation; TECH(7): unittest]
## @purpose Verify API response for moloko tz
## @complexity 6
    def test_moloko_tz(self) -> None:
        file_name = "13 молоко 1 полуг.docx"
        result = self._send_request(file_name, dict(document_type="tz"))
        print("[LDD_TEST] Test result obtained, proceeding to assertions")
        self.assertIn("metadata", result)
        tree = result["content"]["structure"]
        self._check_tz_tree(tree)
        lines = tree2linear(tree)
        num_regexp = re.compile(r"\s*6\.\d")
        self.assertSetEqual({4}, {len(line["node_id"].split(".")) for line in lines if num_regexp.match(line["text"])})

# endregion FUNC_test_moloko_tz

# region FUNC_test_gasu_tz [DOMAIN(7): Testing; CONCEPT(7): ResponseValidation; TECH(7): unittest]
## @purpose Verify API response for gasu tz
## @complexity 6
    def test_gasu_tz(self) -> None:
        file_name = "Технические_требования_ГАСУ_(2012-2014)(1)(1)(1).docx"
        result = self._send_request(file_name, dict(document_type="tz"))
        print("[LDD_TEST] Test result obtained, proceeding to assertions")
        self.assertIn("metadata", result)
        tree = result["content"]["structure"]
        self._check_tz_tree(tree)

        node = self._get_by_tree_path(tree, "0")
        self.assertEqual("Технические требования на дора", node["text"].replace("\n", "")[:30])
        self.assertEqual("root", node["metadata"]["paragraph_type"])

        node = self._get_by_tree_path(tree, "0.0")
        self.assertEqual("СОДЕРЖАНИЕ", node["text"][:30].strip())
        self.assertEqual("toc", node["metadata"]["paragraph_type"])

        node = self._get_by_tree_path(tree, "0.1.5")
        self.assertEqual("5.\tТехнические требования к ГАС «Управление»", node["text"].strip())
        self.assertEqual("part", node["metadata"]["paragraph_type"])

        node = self._get_by_tree_path(tree, "0.1.5.0")
        self.assertEqual("5.1.\tТребования к функционированию", node["text"].strip())
        self.assertEqual("named_item", node["metadata"]["paragraph_type"])

        node = self._get_by_tree_path(tree, "0.1.4")
        self.assertIn("«Управление»", node["text"])
        self.assertEqual("4.\tОбщие требования к техническим компонентам ГАС«Управление»", node["text"].strip())
        self.assertEqual("part", node["metadata"]["paragraph_type"])

        node = self._get_by_tree_path(tree, "0.1.5.0.0.19.0")
        self.assertIn("10 лет) ", node["text"])
        self.assertEqual("raw_text", node["metadata"]["paragraph_type"])

# endregion FUNC_test_gasu_tz

# region METHOD__check_tz_tree [DOMAIN(6): Testing; CONCEPT(6): Helper; TECH(6): unittest]
## @purpose Helper method for test assertions
## @complexity 4
    def _check_tz_tree(self, tree: Dict[str, dict]) -> None:
        self._check_tree_sanity(tree)
        lines = list(tree2linear(tree))
        toc_end = max((line_id for line_id, line in enumerate(lines) if line["metadata"]["paragraph_type"].startswith("toc")), default=0)
        body_line = [line_id for line_id, line in enumerate(lines) if line["metadata"]["paragraph_type"] == "body"]
        self.assertEqual(1, len(body_line))
        self.assertGreater(max(body_line), toc_end)

# endregion METHOD__check_tz_tree

# region FUNC_test_small_image_tz [DOMAIN(7): Testing; CONCEPT(7): ResponseValidation; TECH(7): unittest]
## @purpose Verify API response for small image tz
## @complexity 6
    def test_small_image_tz(self) -> None:
        file_name = "small_image.jpg"
        result = self._send_request(file_name, dict(document_type="tz"))
        self._check_tz_tree(result["content"]["structure"])
        print("[LDD_TEST] Test result obtained, proceeding to assertions")
        self.assertIn("metadata", result)

# endregion FUNC_test_small_image_tz

# region FUNC_test_fail_tz [DOMAIN(7): Testing; CONCEPT(7): ResponseValidation; TECH(7): unittest]
## @purpose Verify API response for fail tz
## @complexity 6
    def test_fail_tz(self) -> None:
        file_name = "failed.docx"
        result = self._send_request(file_name, dict(document_type="tz"))
        print("[LDD_TEST] Test result obtained, proceeding to assertions")
        self.assertIn("metadata", result)
        self._check_tz_tree(result["content"]["structure"])

# endregion FUNC_test_fail_tz

# region METHOD__get_abs_path [DOMAIN(6): Testing; CONCEPT(6): Helper; TECH(6): unittest]
## @purpose Helper method for test assertions
## @complexity 4
    def _get_abs_path(self, file_name: str) -> str:
        return os.path.join(self.data_directory_path, "tz", file_name)

# endregion METHOD__get_abs_path

# region METHOD__check_content [DOMAIN(6): Testing; CONCEPT(6): Helper; TECH(6): unittest]
## @purpose Helper method for test assertions
## @complexity 4
    def _check_content(self, result: dict, file_name: str) -> None:
        self.assertEqual(file_name, result["metadata"]["file_name"])
        content = result["content"]
        structure = content["structure"]

        annotations = structure["annotations"]
        self.assertGreater(len(annotations), 0)

        self._check_tz_tree(structure)
        self.assertEqual("ТЕХНИЧЕСКОЕ ЗАДАНИЕ \nНа разведение и уход за альпаками. Принято министерством по делам альпаководства.", structure["text"].strip())
        toc = structure["subparagraphs"][0]
        self.assertEqual("содержание", toc["text"].strip().lower())
        self.assertEqual("toc", toc["metadata"]["paragraph_type"])
        self.assertIn("bold", (annotation["name"] for annotation in toc["annotations"]))
        first_toc_item = toc["subparagraphs"][0]
        self.assertEqual("1\tкормление альпака\t1", first_toc_item["text"].strip().lower())
        self.assertEqual("toc_item", first_toc_item["metadata"]["paragraph_type"])
        second_toc_item = toc["subparagraphs"][1]
        self.assertEqual("2\tуход за альпаками\t2", second_toc_item["text"].strip().lower())
        self.assertEqual("toc_item", second_toc_item["metadata"]["paragraph_type"])

        body = structure["subparagraphs"][1]
        self.assertEqual("body", body["metadata"]["paragraph_type"])
        items = [item for item in body["subparagraphs"] if len(item["text"].strip()) > 0]

        first_item = items[0]
        self.assertEqual("1.", first_item["text"].strip())
        self.assertEqual("item", first_item["metadata"]["paragraph_type"])
        first_item_text = first_item["subparagraphs"][0]["text"]
        self.assertEqual("Кормление альпака", first_item_text.strip())
        first_subitem = first_item["subparagraphs"][1]
        self.assertEqual("-", first_subitem["text"].strip())
        self.assertEqual("Качество корма должно быть хорошим", first_subitem["subparagraphs"][0]["text"].strip())
        second_subitem = first_item["subparagraphs"][2]
        self.assertEqual("-", first_subitem["text"].strip())
        self.assertEqual("Количество корма дожно быть достаточным", second_subitem["subparagraphs"][0]["text"].strip())

        second_item = items[1]
        self.assertEqual("2.", second_item["text"].strip())
        self.assertEqual("item", first_item["metadata"]["paragraph_type"])
        first_item_text = second_item["subparagraphs"][0]["text"]
        self.assertEqual("Уход за альпаками", first_item_text.strip())
        first_subitem = second_item["subparagraphs"][1]
        self.assertEqual("-", first_subitem["text"].strip())
        self.assertEqual("Альпаку надо стричь", first_subitem["subparagraphs"][0]["text"].strip())
        second_subitem = second_item["subparagraphs"][2]
        self.assertEqual("-", first_subitem["text"].strip())
        self.assertEqual("Альпаку надо пасти на высоте около 3500 метров над уровнем моря.", second_subitem["subparagraphs"][0]["text"].strip())

# endregion METHOD__check_content
# endregion CLASS_TestTZApiDocReader