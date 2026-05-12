# region MODULE_CONTRACT [DOMAIN(7): Testing, DocumentProcessing; CONCEPT(8): ContentValidation, TreeSanity; TECH(7): unittest]
## @modulecontract
## @purpose Provide content validation primitives (tree sanity, metadata checks, field checks) for all API integration tests.
## @scope Document tree traversal, node validation, required field checking, metadata assertion.
## @input Dict-based document tree and metadata structures from Dedoc API responses.
## @output None (assertion-based validation).
## @links [READS_DATA_FROM(7): Dedoc API response JSON]
## @invariants
## - _check_tree_sanity validates node_id uniqueness for every node in the tree.
## - _check_required_fields covers all top-level keys: metadata, content, warnings, tables, structure.
## @rationale
## Q: Why extract content checking into a shared base class?
## A: All API test classes validate the same response structure. DRY principle avoids duplicating tree/sanity checks.
## @changes
## LAST_CHANGE: [v1.0.0 – Initial LDD migration: added semantic markup]
## @modulemap
## CLASS 9[Content validation primitives for test assertions] => ContentChecker
## @usecases
## - [ContentChecker]: TestClass (Inherit) => ValidateTreeSanity => AssertionPassOrFail
def _module_contract():
    pass
# endregion MODULE_CONTRACT
# GREP_SUMMARY: content checker, tree sanity, metadata validation, unittest base, document structure, node_id uniqueness
# STRUCTURE: ⚡ ┌tree dict┐ → ○ stack DFS ⟅node⟆ → ⊕ check node_id unique + required keys → ∑ annotations dedup → ⎋ validate_all

import unittest
from typing import List, Union


# region CLASS_ContentChecker [DOMAIN(7): Testing, DocumentProcessing; CONCEPT(8): ContentValidation, TreeSanity; TECH(7): unittest]
## @purpose Base test case class providing content tree traversal and validation primitives for Dedoc API response checking.
class ContentChecker(unittest.TestCase):

    # region METHOD__get_by_tree_path [DOMAIN(6): Testing; CONCEPT(7): TreeNavigation; TECH(5): DictTraversal]
    ## @purpose Navigate the document tree structure by a dot-separated path or list of child indices.
    ## @io (dict, Union[List[int], str]) -> dict
    ## @complexity 3
    def _get_by_tree_path(self, tree: dict, path: Union[List[int], str]) -> dict:
        if isinstance(path, str):
            path = [int(i) for i in path.split(".") if len(i) > 0][1:]
        for child_id in path:
            tree = tree["subparagraphs"][child_id]
        return tree
    # endregion METHOD__get_by_tree_path

    # region METHOD__get_text_of_row [DOMAIN(5): Testing; CONCEPT(6): TableParsing; TECH(4): ListComprehension]
    ## @purpose Extract text from all cells in a table row, joining multi-line cell content with newlines.
    ## @io dict -> List[str]
    ## @complexity 3
    def _get_text_of_row(self, row: dict) -> List[str]:
        result = []
        for cell in row:
            result.append("\n".join([line["text"] for line in cell["lines"]]))
        return result
    # endregion METHOD__get_text_of_row

    # region METHOD__check_tree_sanity [DOMAIN(8): Testing; CONCEPT(9): StructureValidation, InvariantCheck; TECH(7): DFS]
    ## @purpose Perform depth-first sanity check on the document tree: verify unique node IDs, required keys, and annotation uniqueness.
    ## @io dict -> None (asserts)
    ## @complexity 5
    def _check_tree_sanity(self, tree: dict) -> None:
        stack = [tree]
        node_id_set = set()
        while len(stack) > 0:
            node = stack.pop()
            self.assertIn("node_id", node)
            self.assertIn("text", node)
            self.assertIn("annotations", node)
            self.assertIn("metadata", node)
            self.assertIn("subparagraphs", node)

            node_id = node["node_id"]
            self.assertNotIn(node_id, node_id_set)
            node_id_set.add(node_id)
            annotations = [(a["name"], a["value"], a["end"], a["start"]) for a in node["annotations"]]
            self.assertEqual(len(set(annotations)), len(annotations))

            self.assertIn("metadata", node)

            for subparagraph in node["subparagraphs"]:
                stack.append(subparagraph)
    # endregion METHOD__check_tree_sanity

    # region METHOD__check_required_fields [DOMAIN(8): Testing; CONCEPT(8): ResponseValidation; TECH(6): BFS]
    ## @purpose Validate that all required top-level fields exist in the Dedoc API result, including nested attachments.
    ## @io dict -> None (asserts)
    ## @complexity 4
    def _check_required_fields(self, result: dict) -> None:
        stack = [result]
        document_list = []
        while len(stack) > 0:
            document = stack.pop()
            stack.extend(document.get("attachments", []))
            document_list.append(document)
        for document in document_list:
            metadata = document["metadata"]
            self.__check_metadata(metadata)
            content = document["content"]
            self.assertIn("warnings", document)
            self.assertIn("tables", content)
            tree = content["structure"]
            self._check_tree_sanity(tree=tree)
    # endregion METHOD__check_required_fields

    # region METHOD___check_metadata [DOMAIN(7): Testing; CONCEPT(7): MetadataValidation; TECH(5): TypedAssertions]
    ## @purpose Verify that metadata dict has all required keys (file_name, size, timestamps) with correct types.
    ## @io dict -> None (asserts)
    ## @complexity 4
    def __check_metadata(self, metadata: dict) -> None:
        self.assertIn("file_name", metadata)
        self.assertIsInstance(metadata["file_name"], str)
        self.assertIn("size", metadata)
        self.assertIsInstance(metadata["size"], int)
        self.assertIn("modified_time", metadata)
        self.assertIsInstance(metadata["modified_time"], int)
        self.assertIn("created_time", metadata)
        self.assertIsInstance(metadata["created_time"], int)
        self.assertIn("access_time", metadata)
        self.assertIsInstance(metadata["access_time"], int)
        if "file_type" in metadata:
            self.assertIsInstance(metadata["file_type"], str)
    # endregion METHOD___check_metadata

    # region METHOD__check_english_doc [DOMAIN(7): Testing; CONCEPT(7): ContentValidation; TECH(6): AssertionChain]
    ## @purpose Validate the full structure and content of the standard English test document (THE GREAT ENGLISH DOCUMENT).
    ## @io dict -> None (asserts)
    ## @complexity 5
    def _check_english_doc(self, result: dict) -> None:
        content = result["content"]
        structure = content["structure"]
        self._check_tree_sanity(structure)
        self.assertEqual("THE GREAT ENGLISH DOCUMENT", structure["subparagraphs"][0]["text"].strip())
        list_elements = structure["subparagraphs"][1]["subparagraphs"]
        self.assertEqual("1) Fisrst item with some english text", list_elements[0]["text"].strip())
        self.assertEqual("2) Second item with some even more inglish text. Let me speek from my heart", list_elements[1]["text"].strip())
        table = content["tables"][0]["cells"]
        self.assertListEqual(["London", "The capital of Great Britain"], self._get_text_of_row(table[0]))
        self.assertListEqual(["Speek", "From my heart"], self._get_text_of_row(table[1]))
    # endregion METHOD__check_english_doc

# endregion CLASS_ContentChecker
