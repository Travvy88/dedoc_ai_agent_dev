# region MODULE_CONTRACT [DOMAIN(7): Testing; CONCEPT(8): DOCXAnnotations, RichText; TECH(7): unittest]
## @modulecontract
## @purpose Verify Dedoc API extraction of DOCX/ODT/DOC annotations: bold, italic, underline, strike, spacing, indentation, alignment, superscript, subscript, and table references.
## @scope Rich text annotation extraction: style/formatting, spacing, indentation, alignment, sub/superscript, table annotations inside cells.
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
## CLASS [API integration test class] => TestApiDocxAnnotations
## @usecases
## - [TestClass]: Developer (Run) => VerifyAPIBehavior => TestPassOrFail
def _module_contract():
    pass
# endregion MODULE_CONTRACT
# GREP_SUMMARY: docx annotations, bold, italic, underline, spacing, indentation, alignment, superscript, subscript, API test
# STRUCTURE: ▶ ┌annotation.docx/odt/doc┐ → ○ _send_request(structure_type=linear|tree) → ⊕ extract annotation arrays → ◇ validate style + formatting + spacing → ⎋ annotation assertions

import os

from tests.api_tests.abstract_api_test import AbstractTestApiDocReader


# region CLASS_TestApiDocxAnnotations [DOMAIN(7): Testing, DocumentProcessing; CONCEPT(7): APITest; TECH(7): unittest]
## @purpose API integration tests for Dedoc document processing — TestApiDocxAnnotations.
class TestApiDocxAnnotations(AbstractTestApiDocReader):
    data_directory_path = os.path.join(AbstractTestApiDocReader.data_directory_path, "annotation_docx")


# region FUNC_test_example_1 [DOMAIN(7): Testing; CONCEPT(7): ResponseValidation; TECH(7): unittest]
## @purpose Verify API response for example 1
## @complexity 6
    def test_example_1(self) -> None:
        result = self._send_request("example_1.docx", data={"structure_type": "linear"})
        subparagraphs = result["content"]["structure"]["subparagraphs"]
        annotations = [subparagraph["annotations"] for subparagraph in subparagraphs]

        # bold, italic, underlined
        print("[LDD_TEST] Test result obtained, proceeding to assertions")
        self.assertIn({"start": 0, "end": 11, "name": "style", "value": "Body"}, annotations[0])
        self.assertIn({"start": 0, "end": 12, "name": "italic", "value": "True"}, annotations[1])
        self.assertIn({"start": 0, "end": 10, "name": "bold", "value": "True"}, annotations[2])
        self.assertIn({"start": 0, "end": 16, "name": "underlined", "value": "True"}, annotations[3])
        self.assertIn({"start": 0, "end": 6, "name": "italic", "value": "True"}, annotations[4])
        self.assertIn({"start": 8, "end": 13, "name": "bold", "value": "True"}, annotations[5])
        self.assertIn({"start": 0, "end": 20, "name": "bold", "value": "True"}, annotations[6])
        self.assertIn({"start": 5, "end": 20, "name": "underlined", "value": "True"}, annotations[6])
        # alignment
        self.assertIn({"start": 0, "end": 10, "name": "alignment", "value": "left"}, annotations[8])
        self.assertIn({"start": 0, "end": 14, "name": "alignment", "value": "center"}, annotations[9])
        self.assertIn({"start": 0, "end": 11, "name": "alignment", "value": "right"}, annotations[10])
        self.assertIn({"start": 0, "end": 29, "name": "alignment", "value": "both"}, annotations[11])
        # indent
        self.assertIn({"start": 0, "end": 12, "name": "indentation", "value": "0"}, annotations[12])
        self.assertIn({"start": 0, "end": 11, "name": "indentation", "value": "720.0"}, annotations[13])
        self.assertIn({"start": 0, "end": 12, "name": "indentation", "value": "1440.0"}, annotations[14])
        # strike
        self.assertIn({"start": 0, "end": 11, "name": "strike", "value": "True"}, annotations[15])

# endregion FUNC_test_example_1

# region FUNC_test_example_2 [DOMAIN(7): Testing; CONCEPT(7): ResponseValidation; TECH(7): unittest]
## @purpose Verify API response for example 2
## @complexity 6
    def test_example_2(self) -> None:
        result = self._send_request("example_2.docx", data={"structure_type": "linear"})
        subparagraphs = result["content"]["structure"]["subparagraphs"]
        annotations = [subparagraph["annotations"] for subparagraph in subparagraphs]

        # heading, italic, bold, underlined
        print("[LDD_TEST] Test result obtained, proceeding to assertions")
        self.assertIn({"start": 0, "end": 31, "name": "italic", "value": "True"}, annotations[3])
        self.assertIn({"start": 0, "end": 31, "name": "style", "value": "heading 4"}, annotations[3])
        self.assertIn({"start": 0, "end": 29, "name": "italic", "value": "True"}, annotations[8])
        self.assertIn({"start": 0, "end": 29, "name": "style", "value": "heading 9"}, annotations[8])
        self.assertIn({"start": 66, "end": 73, "name": "italic", "value": "True"}, annotations[35])
        self.assertIn({"start": 75, "end": 89, "name": "bold", "value": "True"}, annotations[35])
        self.assertIn({"start": 91, "end": 111, "name": "underlined", "value": "True"}, annotations[35])
        self.assertIn({"start": 0, "end": 153, "name": "size", "value": "14.0"}, annotations[35])
        self.assertIn({"start": 153, "end": 175, "name": "size", "value": "20.0"}, annotations[35])
        self.assertIn({"start": 183, "end": 199, "name": "size", "value": "11.0"}, annotations[35])
        # alignment
        self.assertIn({"start": 0, "end": 46, "name": "alignment", "value": "right"}, annotations[43])
        self.assertIn({"start": 0, "end": 40, "name": "alignment", "value": "center"}, annotations[44])
        self.assertIn({"start": 0, "end": 160, "name": "alignment", "value": "both"}, annotations[45])
        # bold, italic, underlined
        self.assertIn({"start": 0, "end": 26, "name": "bold", "value": "True"}, annotations[47])
        self.assertIn({"start": 0, "end": 29, "name": "italic", "value": "True"}, annotations[48])
        self.assertIn({"start": 0, "end": 32, "name": "underlined", "value": "True"}, annotations[49])
        self.assertIn({"start": 0, "end": 35, "name": "bold", "value": "True"}, annotations[50])
        self.assertIn({"start": 0, "end": 35, "name": "italic", "value": "True"}, annotations[50])
        self.assertIn({"start": 0, "end": 51, "name": "bold", "value": "True"}, annotations[51])
        self.assertIn({"start": 0, "end": 51, "name": "underlined", "value": "True"}, annotations[51])
        self.assertIn({"start": 0, "end": 51, "name": "italic", "value": "True"}, annotations[51])

# endregion FUNC_test_example_2

# region FUNC_test_spacing_1 [DOMAIN(7): Testing; CONCEPT(7): ResponseValidation; TECH(7): unittest]
## @purpose Verify API response for spacing 1
## @complexity 6
    def test_spacing_1(self) -> None:
        result = self._send_request("spacing_libreoffice.docx", data={"structure_type": "linear"})
        subparagraphs = result["content"]["structure"]["subparagraphs"]
        annotations = [subparagraph["annotations"] for subparagraph in subparagraphs]

        print("[LDD_TEST] Test result obtained, proceeding to assertions")
        self.assertIn({"start": 0, "end": 10, "name": "spacing", "value": "0"}, annotations[0])
        self.assertIn({"start": 0, "end": 10, "name": "spacing", "value": "0"}, annotations[1])
        self.assertIn({"start": 0, "end": 10, "name": "spacing", "value": "57"}, annotations[2])
        self.assertIn({"start": 0, "end": 10, "name": "spacing", "value": "114"}, annotations[3])
        self.assertIn({"start": 0, "end": 10, "name": "spacing", "value": "114"}, annotations[4])
        self.assertIn({"start": 0, "end": 10, "name": "spacing", "value": "114"}, annotations[5])
        self.assertIn({"start": 0, "end": 10, "name": "spacing", "value": "114"}, annotations[6])
        self.assertIn({"start": 0, "end": 9, "name": "spacing", "value": "0"}, annotations[7])

# endregion FUNC_test_spacing_1

# region FUNC_test_spacing_2 [DOMAIN(7): Testing; CONCEPT(7): ResponseValidation; TECH(7): unittest]
## @purpose Verify API response for spacing 2
## @complexity 6
    def test_spacing_2(self) -> None:
        result = self._send_request("spacing_microsoft_word.docx", data={"structure_type": "linear"})
        subparagraphs = result["content"]["structure"]["subparagraphs"]
        annotations = [subparagraph["annotations"] for subparagraph in subparagraphs]

        print("[LDD_TEST] Test result obtained, proceeding to assertions")
        self.assertIn({"start": 0, "end": 10, "name": "spacing", "value": "0"}, annotations[0])
        self.assertIn({"start": 0, "end": 10, "name": "spacing", "value": "0"}, annotations[1])
        self.assertIn({"start": 0, "end": 31, "name": "spacing", "value": "200"}, annotations[2])
        self.assertIn({"start": 0, "end": 31, "name": "spacing", "value": "200"}, annotations[3])
        self.assertIn({"start": 0, "end": 32, "name": "spacing", "value": "400"}, annotations[4])
        self.assertIn({"start": 0, "end": 31, "name": "spacing", "value": "400"}, annotations[5])
        self.assertIn({"start": 0, "end": 31, "name": "spacing", "value": "600"}, annotations[6])
        self.assertIn({"start": 0, "end": 10, "name": "spacing", "value": "400"}, annotations[7])
        self.assertIn({"start": 0, "end": 10, "name": "spacing", "value": "0"}, annotations[8])

# endregion FUNC_test_spacing_2

# region FUNC_test_identation [DOMAIN(7): Testing; CONCEPT(7): ResponseValidation; TECH(7): unittest]
## @purpose Verify API response for identation
## @complexity 6
    def test_identation(self) -> None:
        result = self._send_request("indentation_libreoffice.docx", data={"structure_type": "linear"})
        subparagraphs = result["content"]["structure"]["subparagraphs"]
        annotations = [subparagraph["annotations"] for subparagraph in subparagraphs]
        print("[LDD_TEST] Test result obtained, proceeding to assertions")
        self.assertIn({"start": 0, "end": 188, "name": "indentation", "value": "360.0"}, annotations[5])
        self.assertIn({"start": 0, "end": 152, "name": "indentation", "value": "708.0"}, annotations[10])
        self.assertIn({"start": 0, "end": 0, "name": "indentation", "value": "1429.0"}, annotations[12])
        self.assertIn({"start": 0, "end": 21, "name": "indentation", "value": "709.0"}, annotations[16])
        self.assertIn({"start": 0, "end": 65, "name": "indentation", "value": "786.0"}, annotations[20])

# endregion FUNC_test_identation

# region FUNC_test_table_refs [DOMAIN(7): Testing; CONCEPT(7): ResponseValidation; TECH(7): unittest]
## @purpose Verify API response for table refs
## @complexity 6
    def test_table_refs(self) -> None:
        result = self._send_request("table_refs.docx", data={"structure_type": "linear"})
        subparagraphs = result["content"]["structure"]["subparagraphs"]
        for i in [0, 2, 4, 6, 9]:
            annotations = subparagraphs[i]["annotations"]
            found = False
            for annotation in annotations:
                if annotation["name"] == "table":
                    found = True
                    break
            print("[LDD_TEST] Test result obtained, proceeding to assertions")
            self.assertTrue(found)

# endregion FUNC_test_table_refs

# region FUNC_test_subscript_docx [DOMAIN(7): Testing; CONCEPT(7): ResponseValidation; TECH(7): unittest]
## @purpose Verify API response for subscript docx
## @complexity 6
    def test_subscript_docx(self) -> None:
        file_name = "example_superscript.docx"
        self._check_superscript(file_name)

# endregion FUNC_test_subscript_docx

# region FUNC_test_subscript_odt [DOMAIN(7): Testing; CONCEPT(7): ResponseValidation; TECH(7): unittest]
## @purpose Verify API response for subscript odt
## @complexity 6
    def test_subscript_odt(self) -> None:
        file_name = "example_superscript.odt"
        self._check_superscript(file_name)

# endregion FUNC_test_subscript_odt

# region FUNC_test_subscript_doc [DOMAIN(7): Testing; CONCEPT(7): ResponseValidation; TECH(7): unittest]
## @purpose Verify API response for subscript doc
## @complexity 6
    def test_subscript_doc(self) -> None:
        file_name = "example_superscript.doc"
        self._check_superscript(file_name)

# endregion FUNC_test_subscript_doc

# region METHOD__check_superscript [DOMAIN(6): Testing; CONCEPT(6): Helper; TECH(6): unittest]
## @purpose Helper method for test assertions
## @complexity 4
    def _check_superscript(self, file_name: str) -> None:
        result = self._send_request(os.path.join("..", "docx", file_name), data={"structure_type": "tree"})
        content = result["content"]["structure"]
        subparagraph = content["subparagraphs"][0]
        annotations = subparagraph["annotations"]
        self.assertIn({"start": 5, "end": 6, "name": "superscript", "value": "True"}, annotations)
        self.assertIn({"start": 9, "end": 10, "name": "subscript", "value": "True"}, annotations)

# endregion METHOD__check_superscript

# region FUNC_test_annotations_inside_tables [DOMAIN(7): Testing; CONCEPT(7): ResponseValidation; TECH(7): unittest]
## @purpose Verify API response for annotations inside tables
## @complexity 6
    def test_annotations_inside_tables(self) -> None:
        result = self._send_request(os.path.join("..", "docx", "merged_cells.docx"))
        tables = result["content"]["tables"]

        cell_lines = tables[0]["cells"][0][0]["lines"]
        print("[LDD_TEST] Test result obtained, proceeding to assertions")
        self.assertIn({"start": 0, "end": 12, "name": "size", "value": "12.0"}, cell_lines[0]["annotations"])
        self.assertIn({"start": 0, "end": 12, "name": "bold", "value": "True"}, cell_lines[0]["annotations"])

        cell_lines = tables[0]["cells"][1][3]["lines"]
        self.assertIn({"start": 0, "end": 24, "name": "size", "value": "12.0"}, cell_lines[0]["annotations"])
        self.assertIn({"start": 0, "end": 24, "name": "bold", "value": "True"}, cell_lines[0]["annotations"])

# endregion FUNC_test_annotations_inside_tables
# endregion CLASS_TestApiDocxAnnotations