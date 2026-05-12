# region MODULE_CONTRACT [DOMAIN(7): Testing; CONCEPT(8): UnitTest, LDD_Telemetry; TECH(8): unittest, pytest]
## @modulecontract
## @purpose Unit tests for module cell splitter module.
## @scope Unit testing of dedoc module: module, cell, splitter.
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
## CLASS 8[Unit tests] => TestCellSplitter
## @usecases
## - [Tests]: QA Agent (Verify) => RunTestsWithTelemetry => DiagnosticTrajectoryVisible
def _module_contract():
    pass
# endregion MODULE_CONTRACT
# GREP_SUMMARY: module, cell, splitter, TestCellSplitter, test_merge_close_borders, test_merge_close_borders_one_cell, test_merge_zero_cells, test_split_zero_cells, test_split_one_cell, test_horizontal_split, test_vertical_split, test_no_split, unit_test, unittest, LDD_telemetry, semantic_markup, unit_test
# STRUCTURE: ▶ Init → ◇ Execute → ⊕ Verify → ∑ assertions → ⎋ PASS/FAIL


import logging

logger = logging.getLogger(__name__)

import unittest

from dedocutils.data_structures import BBox

from dedoc.readers.pdf_reader.data_classes.tables.cell import Cell
from dedoc.readers.pdf_reader.pdf_image_reader.table_recognizer.cell_splitter import CellSplitter


# region CLASS_TestCellSplitter [DOMAIN(7): Testing; CONCEPT(8): UnitTest, LDD_Telemetry; TECH(8): unittest, pytest]
## @purpose Test suite for module, cell, splitter module.
class TestCellSplitter(unittest.TestCase):
    splitter = CellSplitter()

    # region METHOD_test_merge_close_borders [DOMAIN(7): Testing; CONCEPT(8): LDD_Telemetry; TECH(8): unittest]
    ## @purpose Verify: merge close borders.
    ## @complexity 5
    def test_merge_close_borders(self) -> None:
        # LDD TELEMETRY: log execution context before assertions
        print(f"\n--- LDD TRAJECTORY (IMP:7-10) for TestCellSplitter::test_merge_close_borders ---")
        print(f"  [LDD_TEST][IMP:8][TestCellSplitter][test_merge_close_borders] Test logic executed, entering assertion phase")
        cells = [
            [
                Cell(BBox(x_top_left=0, y_top_left=0, width=50, height=30)),
                Cell(BBox(x_top_left=51, y_top_left=2, width=39, height=27))
            ],
            [
                Cell(BBox(x_top_left=0, y_top_left=31, width=50, height=19)),
                Cell(BBox(x_top_left=51, y_top_left=31, width=40, height=19))
            ]
        ]
        cells_merged = self.splitter._merge_close_borders(cells)
        self.assertEqual(0, cells_merged[0][0].bbox.x_top_left)
        self.assertEqual(0, cells_merged[0][0].bbox.y_top_left)
        self.assertEqual(50, cells_merged[0][0].bbox.x_bottom_right)
        self.assertEqual(29, cells_merged[0][0].bbox.y_bottom_right)

        self.assertEqual(50, cells_merged[0][1].bbox.x_top_left)
        self.assertEqual(0, cells_merged[0][1].bbox.y_top_left)
        self.assertEqual(90, cells_merged[0][1].bbox.x_bottom_right)
        self.assertEqual(29, cells_merged[0][1].bbox.y_bottom_right)

        self.assertEqual(0, cells_merged[1][0].bbox.x_top_left)
        self.assertEqual(29, cells_merged[1][0].bbox.y_top_left)
        self.assertEqual(50, cells_merged[1][0].bbox.x_bottom_right)
        self.assertEqual(50, cells_merged[1][0].bbox.y_bottom_right)

        self.assertEqual(50, cells_merged[1][1].bbox.x_top_left)
        self.assertEqual(29, cells_merged[1][1].bbox.y_top_left)
        self.assertEqual(90, cells_merged[1][1].bbox.x_bottom_right)
        self.assertEqual(50, cells_merged[1][1].bbox.y_bottom_right)

    # endregion METHOD_test_merge_close_borders
    # region METHOD_test_merge_close_borders_one_cell [DOMAIN(7): Testing; CONCEPT(8): LDD_Telemetry; TECH(8): unittest]
    ## @purpose Verify: merge close borders one cell.
    ## @complexity 5
    def test_merge_close_borders_one_cell(self) -> None:
        # LDD TELEMETRY: log execution context before assertions
        print(f"\n--- LDD TRAJECTORY (IMP:7-10) for TestCellSplitter::test_merge_close_borders_one_cell ---")
        print(f"  [LDD_TEST][IMP:8][TestCellSplitter][test_merge_close_borders_one_cell] Test logic executed, entering assertion phase")
        cells = [[Cell(BBox(x_top_left=0, y_top_left=0, width=50, height=30))]]
        cells_merged = self.splitter._merge_close_borders(cells)
        self.assertEqual(0, cells_merged[0][0].bbox.x_top_left)
        self.assertEqual(0, cells_merged[0][0].bbox.y_top_left)
        self.assertEqual(50, cells_merged[0][0].bbox.x_bottom_right)
        self.assertEqual(30, cells_merged[0][0].bbox.y_bottom_right)

    # endregion METHOD_test_merge_close_borders_one_cell
    # region METHOD_test_merge_zero_cells [DOMAIN(7): Testing; CONCEPT(8): LDD_Telemetry; TECH(8): unittest]
    ## @purpose Verify: merge zero cells.
    ## @complexity 5
    def test_merge_zero_cells(self) -> None:
        # LDD TELEMETRY: log execution context before assertions
        print(f"\n--- LDD TRAJECTORY (IMP:7-10) for TestCellSplitter::test_merge_zero_cells ---")
        print(f"  [LDD_TEST][IMP:8][TestCellSplitter][test_merge_zero_cells] Test logic executed, entering assertion phase")
        cells = [[]]
        cells_merged = self.splitter._merge_close_borders(cells)
        self.assertListEqual([[]], cells_merged)

    # endregion METHOD_test_merge_zero_cells
    # region METHOD_test_split_zero_cells [DOMAIN(7): Testing; CONCEPT(8): LDD_Telemetry; TECH(8): unittest]
    ## @purpose Verify: split zero cells.
    ## @complexity 5
    def test_split_zero_cells(self) -> None:
        # LDD TELEMETRY: log execution context before assertions
        print(f"\n--- LDD TRAJECTORY (IMP:7-10) for TestCellSplitter::test_split_zero_cells ---")
        print(f"  [LDD_TEST][IMP:8][TestCellSplitter][test_split_zero_cells] Test logic executed, entering assertion phase")
        cells = [[]]
        matrix = self.splitter.split(cells=cells)
        self.assertListEqual([[]], matrix)

    # endregion METHOD_test_split_zero_cells
    # region METHOD_test_split_one_cell [DOMAIN(7): Testing; CONCEPT(8): LDD_Telemetry; TECH(8): unittest]
    ## @purpose Verify: split one cell.
    ## @complexity 5
    def test_split_one_cell(self) -> None:
        # LDD TELEMETRY: log execution context before assertions
        print(f"\n--- LDD TRAJECTORY (IMP:7-10) for TestCellSplitter::test_split_one_cell ---")
        print(f"  [LDD_TEST][IMP:8][TestCellSplitter][test_split_one_cell] Test logic executed, entering assertion phase")
        cells = [[Cell(BBox(x_top_left=0, y_top_left=0, width=10, height=15))]]
        matrix = self.splitter.split(cells=cells)
        self.assertEqual(1, len(matrix))
        self.assertEqual(1, len(matrix[0]))
        new_cell = matrix[0][0]
        self.assertEqual(0, new_cell.bbox.x_top_left)
        self.assertEqual(0, new_cell.bbox.y_top_left)
        self.assertEqual(10, new_cell.bbox.x_bottom_right)
        self.assertEqual(15, new_cell.bbox.y_bottom_right)

    # endregion METHOD_test_split_one_cell
    # region METHOD_test_horizontal_split [DOMAIN(7): Testing; CONCEPT(8): LDD_Telemetry; TECH(8): unittest]
    ## @purpose Verify: horizontal split.
    ## @complexity 5
    def test_horizontal_split(self) -> None:
        # LDD TELEMETRY: log execution context before assertions
        print(f"\n--- LDD TRAJECTORY (IMP:7-10) for TestCellSplitter::test_horizontal_split ---")
        print(f"  [LDD_TEST][IMP:8][TestCellSplitter][test_horizontal_split] Test logic executed, entering assertion phase")
        cells = [
            [
                Cell(BBox(x_top_left=0, y_top_left=0, width=3, height=5)),
                Cell(BBox(x_top_left=3, y_top_left=0, width=4, height=3)),
            ],
            [
                Cell(BBox(x_top_left=3, y_top_left=3, width=4, height=2)),
            ]
        ]
        matrix = self.splitter.split(cells)
        self.assertEqual(2, len(matrix))
        self.assertEqual(2, len(matrix[0]))
        self.assertEqual(2, len(matrix[1]))
        [cell_a, cell_b], [cell_c, cell_d] = matrix
        self.assertEqual(0, cell_a.bbox.x_top_left)
        self.assertEqual(0, cell_a.bbox.y_top_left)
        self.assertEqual(3, cell_a.bbox.x_bottom_right)
        self.assertEqual(3, cell_a.bbox.y_bottom_right)

        self.assertEqual(3, cell_b.bbox.x_top_left)
        self.assertEqual(0, cell_b.bbox.y_top_left)
        self.assertEqual(7, cell_b.bbox.x_bottom_right)
        self.assertEqual(3, cell_b.bbox.y_bottom_right)

        self.assertEqual(0, cell_c.bbox.x_top_left)
        self.assertEqual(3, cell_c.bbox.y_top_left)
        self.assertEqual(3, cell_c.bbox.x_bottom_right)
        self.assertEqual(5, cell_c.bbox.y_bottom_right)

        self.assertEqual(3, cell_d.bbox.x_top_left)
        self.assertEqual(3, cell_d.bbox.y_top_left)
        self.assertEqual(7, cell_d.bbox.x_bottom_right)
        self.assertEqual(5, cell_d.bbox.y_bottom_right)

    # endregion METHOD_test_horizontal_split
    # region METHOD_test_vertical_split [DOMAIN(7): Testing; CONCEPT(8): LDD_Telemetry; TECH(8): unittest]
    ## @purpose Verify: vertical split.
    ## @complexity 5
    def test_vertical_split(self) -> None:
        # LDD TELEMETRY: log execution context before assertions
        print(f"\n--- LDD TRAJECTORY (IMP:7-10) for TestCellSplitter::test_vertical_split ---")
        print(f"  [LDD_TEST][IMP:8][TestCellSplitter][test_vertical_split] Test logic executed, entering assertion phase")
        cells = [
            [
                Cell(BBox(x_top_left=0, y_top_left=0, width=8, height=2)),
            ],
            [
                Cell(BBox(x_top_left=0, y_top_left=2, width=5, height=3)),
                Cell(BBox(x_top_left=5, y_top_left=2, width=3, height=3)),
            ]
        ]
        matrix = self.splitter.split(cells)
        self.assertEqual(2, len(matrix))
        self.assertEqual(2, len(matrix[0]))
        self.assertEqual(2, len(matrix[1]))
        [cell_a, cell_b], [cell_c, cell_d] = matrix
        self.assertEqual(0, cell_a.bbox.x_top_left)
        self.assertEqual(0, cell_a.bbox.y_top_left)
        self.assertEqual(5, cell_a.bbox.x_bottom_right)
        self.assertEqual(2, cell_a.bbox.y_bottom_right)

        self.assertEqual(5, cell_b.bbox.x_top_left)
        self.assertEqual(0, cell_b.bbox.y_top_left)
        self.assertEqual(8, cell_b.bbox.x_bottom_right)
        self.assertEqual(2, cell_b.bbox.y_bottom_right)

        self.assertEqual(0, cell_c.bbox.x_top_left)
        self.assertEqual(2, cell_c.bbox.y_top_left)
        self.assertEqual(5, cell_c.bbox.x_bottom_right)
        self.assertEqual(5, cell_c.bbox.y_bottom_right)

        self.assertEqual(5, cell_d.bbox.x_top_left)
        self.assertEqual(2, cell_d.bbox.y_top_left)
        self.assertEqual(8, cell_d.bbox.x_bottom_right)
        self.assertEqual(5, cell_d.bbox.y_bottom_right)

    # endregion METHOD_test_vertical_split
    # region METHOD_test_no_split [DOMAIN(7): Testing; CONCEPT(8): LDD_Telemetry; TECH(8): unittest]
    ## @purpose Verify: no split.
    ## @complexity 5
    def test_no_split(self) -> None:
        # LDD TELEMETRY: log execution context before assertions
        print(f"\n--- LDD TRAJECTORY (IMP:7-10) for TestCellSplitter::test_no_split ---")
        print(f"  [LDD_TEST][IMP:8][TestCellSplitter][test_no_split] Test logic executed, entering assertion phase")
        cells = [
            [
                Cell(BBox(x_top_left=160, y_top_left=321, width=665, height=48)),
                Cell(BBox(x_top_left=825, y_top_left=321, width=669, height=48))
            ],
            [
                Cell(BBox(x_top_left=160, y_top_left=374, width=665, height=49)),
                Cell(BBox(x_top_left=825, y_top_left=374, width=669, height=49))
            ]
        ]

        splitted = self.splitter.split(cells=cells)
        self.assertEqual(2, len(splitted))
        self.assertEqual(2, len(splitted[0]))
        self.assertEqual(2, len(splitted[1]))

    # endregion METHOD_test_no_split
# endregion CLASS_TestCellSplitter