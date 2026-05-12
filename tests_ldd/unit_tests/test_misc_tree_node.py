# region MODULE_CONTRACT [DOMAIN(7): Testing; CONCEPT(8): UnitTest, LDD_Telemetry; TECH(8): unittest, pytest]
## @modulecontract
## @purpose Unit tests for misc tree node module.
## @scope Unit testing of dedoc module: misc, tree, node.
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
## CLASS 8[Unit tests] => TestTreeNode
## @usecases
## - [Tests]: QA Agent (Verify) => RunTestsWithTelemetry => DiagnosticTrajectoryVisible
def _module_contract():
    pass
# endregion MODULE_CONTRACT
# GREP_SUMMARY: misc, tree, node, TestTreeNode, test_root_node_annotations, unit_test, unittest, LDD_telemetry, semantic_markup, unit_test
# STRUCTURE: ▶ Init → ◇ Execute → ⊕ Verify → ∑ assertions → ⎋ PASS/FAIL


import logging

logger = logging.getLogger(__name__)

from unittest import TestCase

from dedoc.data_structures.concrete_annotations.bold_annotation import BoldAnnotation
from dedoc.data_structures.concrete_annotations.italic_annotation import ItalicAnnotation
from dedoc.data_structures.hierarchy_level import HierarchyLevel
from dedoc.data_structures.line_metadata import LineMetadata
from dedoc.data_structures.line_with_meta import LineWithMeta
from dedoc.data_structures.tree_node import TreeNode


# region CLASS_TestTreeNode [DOMAIN(7): Testing; CONCEPT(8): UnitTest, LDD_Telemetry; TECH(8): unittest, pytest]
## @purpose Test suite for misc, tree, node module.
class TestTreeNode(TestCase):

    # region METHOD_test_root_node_annotations [DOMAIN(7): Testing; CONCEPT(8): LDD_Telemetry; TECH(8): unittest]
    ## @purpose Verify: root node annotations.
    ## @complexity 5
    def test_root_node_annotations(self) -> None:
        # LDD TELEMETRY: log execution context before assertions
        print(f"\n--- LDD TRAJECTORY (IMP:7-10) for TestTreeNode::test_root_node_annotations ---")
        print(f"  [LDD_TEST][IMP:8][TestTreeNode][test_root_node_annotations] Test logic executed, entering assertion phase")
        lines = [
            LineWithMeta(line="bold text\n",
                         metadata=LineMetadata(hierarchy_level=HierarchyLevel.create_root(), page_id=0, line_id=0),
                         annotations=[BoldAnnotation(start=0, end=10, value="True")]),
            LineWithMeta(line="italic text\n",
                         metadata=LineMetadata(hierarchy_level=HierarchyLevel.create_root(), page_id=0, line_id=1),
                         annotations=[ItalicAnnotation(start=0, end=12, value="True")]),
        ]

        node = TreeNode.create(lines=lines)
        node_annotations = node.get_root().annotations
        node_annotations.sort(key=lambda a: a.start)
        self.assertEqual(2, len(node_annotations))
        bold, italic = node_annotations
        self.assertEqual(BoldAnnotation.name, bold.name)
        self.assertEqual("True", bold.value)
        self.assertEqual(0, bold.start)
        self.assertEqual(10, bold.end)

        self.assertEqual(ItalicAnnotation.name, italic.name)
        self.assertEqual("True", italic.value)
        self.assertEqual(10, italic.start)
        self.assertEqual(22, italic.end)

    # endregion METHOD_test_root_node_annotations
# endregion CLASS_TestTreeNode