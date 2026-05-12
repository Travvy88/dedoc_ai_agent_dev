# region MODULE_CONTRACT [DOMAIN(7): Testing; CONCEPT(8): DOCXFormat, OOXML; TECH(7): unittest]
## @modulecontract
## @purpose Test Dedoc API DOC/DOCX/ODT/RTF document parsing: metadata, footnotes, tables, HTML output, annotations, and structure.
## @scope Office document formats: DOCX, DOC, ODT, RTF — metadata extraction, tree/html/ujson output, footnotes, broken docs.
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
## CLASS [API integration test class] => TestApiDocReader
## @usecases
## - [TestClass]: Developer (Run) => VerifyAPIBehavior => TestPassOrFail
def _module_contract():
    pass
# endregion MODULE_CONTRACT
# GREP_SUMMARY: docx, doc, odt, rtf, office, footnotes, metadata, HTML output, API test
# STRUCTURE: ▶ ┌office doc┐ → ○ _send_request(structure_type) → ⊕ validate metadata + __check_doc_like → ◇ tables + footnotes + html → ⎋ format assertions

import os

from dedoc.data_structures.concrete_annotations.linked_text_annotation import LinkedTextAnnotation
from tests.api_tests.abstract_api_test import AbstractTestApiDocReader
from tests.test_utils import get_by_tree_path


# region CLASS_TestApiDocReader [DOMAIN(7): Testing, DocumentProcessing; CONCEPT(7): APITest; TECH(7): unittest]
## @purpose API integration tests for Dedoc document processing — TestApiDocReader.
class TestApiDocReader(AbstractTestApiDocReader):

    data_directory_path = os.path.join(AbstractTestApiDocReader.data_directory_path, "docx")


# region FUNC_test_docx_metadata [DOMAIN(7): Testing; CONCEPT(7): ResponseValidation; TECH(7): unittest]
## @purpose Verify API response for docx metadata
## @complexity 6
    def test_docx_metadata(self) -> None:
        file_name = "english_doc.docx"
        result = self._send_request(file_name)
        metadata = result["metadata"]
        print("[LDD_TEST] Test result obtained, proceeding to assertions")
        self.assertEqual("Тема", metadata["document_subject"])
        self.assertEqual("анализ естественных языков", metadata["keywords"])
        self.assertEqual("курсовая работа", metadata["category"])
        self.assertEqual("на 3 потянет", metadata["comments"])
        self.assertEqual("Андрей Пышкин", metadata["author"])
        self.assertEqual("Андреус Пышкинус", metadata["last_modified_by"])

# endregion FUNC_test_docx_metadata

# region FUNC_test_docx [DOMAIN(7): Testing; CONCEPT(7): ResponseValidation; TECH(7): unittest]
## @purpose Verify API response for docx
## @complexity 6
    def test_docx(self) -> None:
        file_name = "example.docx"
        result = self._send_request(file_name)
        self.__check_doc_like(result)
        self._check_metainfo(result["metadata"], "application/vnd.openxmlformats-officedocument.wordprocessingml.document", file_name)

# endregion FUNC_test_docx

# region FUNC_test_docx_ujson [DOMAIN(7): Testing; CONCEPT(7): ResponseValidation; TECH(7): unittest]
## @purpose Verify API response for docx ujson
## @complexity 6
    def test_docx_ujson(self) -> None:
        file_name = "example.docx"
        result = self._send_request(file_name, data={"return_format": "ujson"})
        self.__check_doc_like(result)

# endregion FUNC_test_docx_ujson

# region FUNC_test_doc [DOMAIN(7): Testing; CONCEPT(7): ResponseValidation; TECH(7): unittest]
## @purpose Verify API response for doc
## @complexity 6
    def test_doc(self) -> None:
        file_name = "example.doc"
        result = self._send_request(file_name, data={"structure_type": "tree"})
        self.__check_doc_like(result)
        self._check_metainfo(result["metadata"], "application/msword", file_name)

# endregion FUNC_test_doc

# region FUNC_test_odt [DOMAIN(7): Testing; CONCEPT(7): ResponseValidation; TECH(7): unittest]
## @purpose Verify API response for odt
## @complexity 6
    def test_odt(self) -> None:
        file_name = "example.odt"
        result = self._send_request(file_name)
        self.__check_doc_like(result)
        self._check_metainfo(result["metadata"], "application/vnd.oasis.opendocument.text", file_name)

# endregion FUNC_test_odt

# region FUNC_test_rtf [DOMAIN(7): Testing; CONCEPT(7): ResponseValidation; TECH(7): unittest]
## @purpose Verify API response for rtf
## @complexity 6
    def test_rtf(self) -> None:
        file_name = "example.rtf"
        result = self._send_request(file_name)
        self.__check_doc_like(result)
        self._check_metainfo(result["metadata"], "application/rtf", file_name)

# endregion FUNC_test_rtf

# region FUNC_test_odt_with_split [DOMAIN(7): Testing; CONCEPT(7): ResponseValidation; TECH(7): unittest]
## @purpose Verify API response for odt with split
## @complexity 6
    def test_odt_with_split(self) -> None:
        file_name = "ТЗ_ГИС_3  .odt"
        result = self._send_request(file_name)
        content = result["content"]["structure"]
        print("[LDD_TEST] Test result obtained, proceeding to assertions")
        self.assertEqual(content["subparagraphs"][0]["text"].strip(), "Система должна обеспечивать защиту от несанкционированного доступа (НСД)")

# endregion FUNC_test_odt_with_split

# region FUNC_test_broken_conversion [DOMAIN(7): Testing; CONCEPT(7): ResponseValidation; TECH(7): unittest]
## @purpose Verify API response for broken conversion
## @complexity 6
    def test_broken_conversion(self) -> None:
        file_name = "broken.odt"
        result = self._send_request(file_name, expected_code=200)
        warnings = [warning for warning in result["warnings"] if warning.startswith("Incorrect extension")]
        print("[LDD_TEST] Test result obtained, proceeding to assertions")
        self.assertEqual(len(warnings), 1)

# endregion FUNC_test_broken_conversion

# region FUNC_test_footnotes [DOMAIN(7): Testing; CONCEPT(7): ResponseValidation; TECH(7): unittest]
## @purpose Verify API response for footnotes
## @complexity 6
    def test_footnotes(self) -> None:
        file_name = "example_footnote_endnote.docx"
        result = self._send_request(file_name, data={"structure_type": "tree"})
        self.__check_doc_like(result)
        full_text = []
        tree = result["content"]["structure"]
        node = get_by_tree_path(tree, "0.0")
        annotations = [(annotation["name"], annotation["value"]) for annotation in node["annotations"]]
        print("[LDD_TEST] Test result obtained, proceeding to assertions")
        self.assertIn((LinkedTextAnnotation.name, "То – союз в русском языке"), annotations)
        self.assertIn((LinkedTextAnnotation.name, "В этом слове допущена опечатка"), annotations)

        stack = [tree]
        while stack:
            node = stack.pop()
            stack.extend(node["subparagraphs"])
            full_text.append(node["text"])
        full_text = "".join(full_text).lower()
        self.assertNotIn("союз", full_text)
        self.assertNotIn("васька", full_text)
        self.assertNotIn("опечатка", full_text)
        self.assertIn("определения", full_text)
        self.assertIn("понятное", full_text)

# endregion FUNC_test_footnotes

# region FUNC_test_tricky_doc [DOMAIN(7): Testing; CONCEPT(7): ResponseValidation; TECH(7): unittest]
## @purpose Verify API response for tricky doc
## @complexity 6
    def test_tricky_doc(self) -> None:
        file_name = "doc.docx"
        _ = self._send_request(file_name)

# endregion FUNC_test_tricky_doc

# region FUNC_test_not_stripped_xml [DOMAIN(7): Testing; CONCEPT(7): ResponseValidation; TECH(7): unittest]
## @purpose Verify API response for not stripped xml
## @complexity 6
    def test_not_stripped_xml(self) -> None:
        self._send_request("not_stripped_xml.docx", expected_code=200)

# endregion FUNC_test_not_stripped_xml

# region FUNC_test_docx_with_comments [DOMAIN(7): Testing; CONCEPT(7): ResponseValidation; TECH(7): unittest]
## @purpose Verify API response for docx with comments
## @complexity 6
    def test_docx_with_comments(self) -> None:
        _ = self._send_request("with_comments.docx", expected_code=200)

# endregion FUNC_test_docx_with_comments

# region FUNC_test_return_html [DOMAIN(7): Testing; CONCEPT(7): ResponseValidation; TECH(7): unittest]
## @purpose Verify API response for return html
## @complexity 6
    def test_return_html(self) -> None:
        file_name = "example.doc"
        result = self._send_request(file_name, data={"structure_type": "tree", "return_format": "html"})
        print("[LDD_TEST] Test result obtained, proceeding to assertions")
        self.assertIn("<p>  <strong></strong>     <sub> id = 0 ; type = root </sub></p><p> &nbsp;&nbsp;&nbsp;&nbsp; <b>Пример документа", result)
        self.assertTrue("<tbody>\n"
                        "<tr>\n"
                        '<td colspan="1" rowspan="1">N</td>\n'
                        '<td colspan="1" rowspan="1">Фамилия</td>\n'
                        '<td colspan="1" rowspan="1">Имя</td>\n'
                        '<td colspan="1" rowspan="1">Организация</td>\n'
                        '<td colspan="1" rowspan="1">Телефон</td>\n'
                        '<td colspan="1" rowspan="1">Примечания</td>\n'
                        "</tr>" in result)

# endregion FUNC_test_return_html

# region FUNC_test_newline_tree [DOMAIN(7): Testing; CONCEPT(7): ResponseValidation; TECH(7): unittest]
## @purpose Verify API response for newline tree
## @complexity 6
    def test_newline_tree(self) -> None:
        file_name = "inspector.docx"
        result = self._send_request(file_name, data={"structure_type": "tree"})
        content = result["content"]["structure"]
        print("[LDD_TEST] Test result obtained, proceeding to assertions")
        self.assertTrue(content["subparagraphs"][0]["text"].startswith("КАКОЕ-ТО ЗАДАНИЕ"))

# endregion FUNC_test_newline_tree

# region FUNC_test_docx_heading_new [DOMAIN(7): Testing; CONCEPT(7): ResponseValidation; TECH(7): unittest]
## @purpose Verify API response for docx heading new
## @complexity 6
    def test_docx_heading_new(self) -> None:
        file_name = "tz-1ek-20_minimum.docx"
        data = dict(structure_type="tree", return_format="html")
        _ = self._send_request(file_name, data=data)

# endregion FUNC_test_docx_heading_new

# region FUNC_test_properties_extractor [DOMAIN(7): Testing; CONCEPT(7): ResponseValidation; TECH(7): unittest]
## @purpose Verify API response for properties extractor
## @complexity 6
    def test_properties_extractor(self) -> None:
        file_name = "broken_properties.docx"
        result = self._send_request(file_name, data={})
        content = result["content"]["structure"]
        print("[LDD_TEST] Test result obtained, proceeding to assertions")
        self.assertEqual("FonFfff", get_by_tree_path(content, "0.0")["text"].strip())

# endregion FUNC_test_properties_extractor

# region FUNC_test_name_with_apostrophe [DOMAIN(7): Testing; CONCEPT(7): ResponseValidation; TECH(7): unittest]
## @purpose Verify API response for name with apostrophe
## @complexity 6
    def test_name_with_apostrophe(self) -> None:
        file_name = "Well. Known -Nik O'Tinn -Ireland 2023- DRAFT.doc"
        _ = self._send_request(file_name, data={})

# endregion FUNC_test_name_with_apostrophe

# region METHOD___check_doc_like [DOMAIN(6): Testing; CONCEPT(6): Helper; TECH(6): unittest]
## @purpose Helper method for test assertions
## @complexity 4
    def __check_doc_like(self, result: dict) -> None:
        content = result["content"]["structure"]
        self.assertEqual("", get_by_tree_path(content, "0")["text"])
        self.assertEqual("Пример документа\nГлава 1\nКакие то определения\nСтатья 1\nОпределим опрделения\nСтатья 2\nДадим пояснения",
                         get_by_tree_path(content, "0.0")["text"].strip())
        self.assertEqual("1.2.1. Поясним за непонятное", get_by_tree_path(content, "0.1.0")["text"].strip())
        self.assertEqual("1.2.2. Поясним за понятное", get_by_tree_path(content, "0.1.1")["text"].strip())
        self.assertEqual("1.2.3.", get_by_tree_path(content, "0.1.2")["text"].strip())
        self.assertEqual("\tа) это даже ежу понятно", get_by_tree_path(content, "0.1.1.0.0")["text"].rstrip())
        self.assertEqual("\tб) это ежу не понятно", get_by_tree_path(content, "0.1.1.0.1")["text"].rstrip())

        table1, table2 = result["content"]["tables"]

        self.assertListEqual(["N", "Фамилия", "Имя", "Организация", "Телефон", "Примечания"], self._get_text_of_row(table1["cells"][0]))
        self.assertListEqual(["1", "Иванов", "Иван", "ИСП", "8-800", ""], self._get_text_of_row(table1["cells"][1]))

        self.assertListEqual(["Фамилия", "Имя", "Отчество"], self._get_text_of_row(table2["cells"][0]))
        self.assertListEqual(["Иванов", "Иван", "Иванович"], self._get_text_of_row(table2["cells"][1]))
        self.assertListEqual(["Петров", "Пётр", "Петрович"], self._get_text_of_row(table2["cells"][2]))
        self.assertListEqual(["Сидоров", "Сидор", "Сидорович"], self._get_text_of_row(table2["cells"][3]))

        metadata = result["metadata"]
        self.assertTrue(metadata["file_name"].startswith("example"))
        self.assertTrue(metadata["modified_time"] is not None)
        self.assertTrue(metadata["created_time"] is not None)
        self.assertTrue(metadata["access_time"] is not None)
        self.assertIn("modified_date", metadata)

# endregion METHOD___check_doc_like
# endregion CLASS_TestApiDocReader