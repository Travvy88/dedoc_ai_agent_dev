from collections import namedtuple
from typing import List, Optional

import numpy as np
from dedocutils.data_structures import BBox
from numpy import ndarray

from dedoc.data_structures.line_with_meta import LineWithMeta

"""-------------------------------Таблица в виде дерева, полученная от OpenCV----------------------------------------"""
ContourCell = namedtuple("ContourCell", ["id_con", "image"])


# region CLASS_TableTree [DOMAIN(8): DocumentProcessing; CONCEPT(7): Reader; TECH(6): Python]
class TableTree(object):
    """
    Table which has cells as sorted childs of tree.
    Table has type of tree and was obtained with help contour analysis.
    """
    min_h_cell = 8
    min_w_cell = 20
    minimal_cell_cnt_line = 5
    minimal_cell_avg_length_line = 10

    # region METHOD___init__ [DOMAIN(7): DocumentProcessing; CONCEPT(6): Method; TECH(6): Python]
    def __init__(self, *, config: dict) -> None:
        import logging

        self.left = None
        self.right = None
        self.cell_box: Optional[BBox] = None  # [x_begin, y_begin, width, height]
        self.crop_text_box: Optional[BBox] = None
        self.id_contours = None
        self.parent = None
        self.children: List[TableTree] = []  # table cells
        self.lines: List[LineWithMeta] = []
        self.config = config
        self.logger = config.get("logger", logging.getLogger())

    # region METHOD_set_text_into_tree [DOMAIN(7): DocumentProcessing; CONCEPT(6): Method; TECH(6): Python]
    # endregion METHOD___init__
    def set_text_into_tree(self, tree: "TableTree", src_image: ndarray, language: str = "rus", *, config: dict, engine=None) -> None:
        import logging
        from dedoc.readers.pdf_reader.pdf_image_reader.ocr.ocr_cell_extractor import OCRCellExtractor

        if engine is None:
            from dedoc.readers.pdf_reader.pdf_image_reader.ocr.tesseract_ocr_engine import TesseractOCREngine
            engine = TesseractOCREngine(config=config)

        # get List of TableTree
        cur_depth = 0
        begin_depth = 2
        end_depth = 2
        stack = [(tree, cur_depth, begin_depth, end_depth)]
        trees = []
        while len(stack) > 0:
            node_tree, cur_depth, begin_depth, end_depth = stack.pop()
            if begin_depth <= cur_depth <= end_depth:
                # img_cell = [pair.image for i, pair in enumerate(cell_images) if pair.id_con == tree.id_contours][0]
                trees.append(node_tree)
                if tree.config.get("debug_mode", False):
                    config.get("logger", logging.getLogger()).debug(f"{tree.id_contours} : text : {tree.get_text()}")
            for ch in node_tree.children:
                stack.append((ch, cur_depth + 1, begin_depth, end_depth))

        cell_extractor = OCRCellExtractor(config=config, engine=engine)
        lines_with_meta = cell_extractor.get_cells_text(page_image=src_image, tree_nodes=trees, language=language)
        assert len(trees) == len(lines_with_meta)

        for lines, tree in zip(lines_with_meta, trees):
            tree.lines = lines

    # region METHOD_set_crop_text_box [DOMAIN(7): DocumentProcessing; CONCEPT(6): Method; TECH(6): Python]
    # endregion METHOD_set_text_into_tree
    def set_crop_text_box(self, page_image: ndarray) -> None:
        from dedoc.utils.image_utils import crop_image_text

        cell_image = BBox.crop_image_by_box(page_image, self.cell_box)
        self.crop_text_box = crop_image_text(cell_image)
        # make crop_text_box'coordinates relative page_image
        self.crop_text_box.x_top_left += self.cell_box.x_top_left
        self.crop_text_box.y_top_left += self.cell_box.y_top_left

    # endregion METHOD_set_crop_text_box
    @staticmethod
    # region METHOD_parse_contours_to_tree [DOMAIN(7): DocumentProcessing; CONCEPT(6): Method; TECH(6): Python]
    def parse_contours_to_tree(contours: List, hierarchy: List, *, config: dict) -> "TableTree":
        import cv2

        table_tree = TableTree(config=config)
        table_tree.id_contours = 0
        if len(contours) == 0:
            return table_tree

        bbox = cv2.boundingRect(contours[0].astype(np.int32))   # [x_begin, y_begin, width, height]
        table_tree.cell_box = BBox(x_top_left=bbox[0], y_top_left=bbox[1], width=bbox[2], height=bbox[3])

        table_tree = table_tree.__build_childs(table_tree, hierarchy, contours)
        return table_tree

    # region METHOD_print_tree [DOMAIN(7): DocumentProcessing; CONCEPT(6): Method; TECH(6): Python]
    # endregion METHOD_parse_contours_to_tree
    def print_tree(self, depth: int) -> None:
        if not self.cell_box or not self.id_contours:
            return

        indent = "".join(["\t" for _ in range(depth)])
        self.logger.debug(f"{indent}{self.id_contours} : coord: {self.cell_box.x_top_left}, {self.cell_box.y_top_left}, "
                          f"{self.cell_box.width}, {self.cell_box.height}")
        for ch in self.children:
            ch.print_tree(depth + 1)

    # region METHOD___build_childs [DOMAIN(7): DocumentProcessing; CONCEPT(6): Method; TECH(6): Python]
    # endregion METHOD_print_tree
    def __build_childs(self, cur: "TableTree", hierarchy: List, contours: List) -> "TableTree":
        import cv2

        list_childs = []
        for i, h in enumerate(hierarchy[0]):
            if h[3] == cur.id_contours:
                bbox = cv2.boundingRect(contours[i].astype(np.int32))  # [x_begin, y_begin, width, height]
                # Эвристика №1 на ячейку
                if bbox[2] < self.min_w_cell or bbox[3] < self.min_h_cell:
                    if self.config.get("debug_mode", False):
                        self.logger.debug(f"Contour {i} isn't correct")
                    continue
                tnode = TableTree(config=self.config)
                tnode.id_contours = i
                tnode.cell_box = BBox(x_top_left=bbox[0], y_top_left=bbox[1], width=bbox[2], height=bbox[3])
                tnode.parent = cur
                list_childs.append(tnode)
                if h[2] != -1:
                    tnode = TableTree(config=self.config).__build_childs(tnode, hierarchy, contours)
                cur.__add_child(tnode)
        cur.children = sorted(cur.children, key=lambda ch: (ch.cell_box.x_top_left, ch.cell_box.y_top_left), reverse=False)
        return cur

    # region METHOD_get_text [DOMAIN(7): DocumentProcessing; CONCEPT(6): Method; TECH(6): Python]
    # endregion METHOD___build_childs
    def get_text(self) -> str:
        return "\n".join([line.line for line in self.lines])

    # region METHOD___add_child [DOMAIN(7): DocumentProcessing; CONCEPT(6): Method; TECH(6): Python]
    # endregion METHOD_get_text
    def __add_child(self, child_tree: "TableTree") -> None:
# endregion CLASS_TableTree
        self.children.append(child_tree)

    # endregion METHOD___add_child


# region MODULE_CONTRACT [DOMAIN(8): DocumentProcessing; CONCEPT(7): Reader_table_tree; TECH(6): Python, dedoc]
## @modulecontract
## @purpose Read and parse PDF documents, extracting lines with metadata, tables, and attachments into UnstructuredDocument.
## @scope Data model definitions.
## @input [File path (str), parameters (Optional[dict]) — document on disk.]
## @output [UnstructuredDocument with lines, tables, attachments, and warnings.]
## @links [USES_API(9): dedoc.data_structures.*; USES_API(8): dedoc.readers.BaseReader]
## @invariants
## - read() ALWAYS returns an UnstructuredDocument.
## @rationale
## Q: Why is this reader separated from others?
## A: Each reader handles one format family — isolation prevents format coupling and simplifies extension.
## @changes
## LAST_CHANGE: [v1.0.0 – Added SEMANTIC TEMPLATE markup and LDD logging.]
## @modulemap
## CLASS [16][TableTree reader/processor] => TableTree
## @usecases
## - [read]: System (Pipeline) → ParseDocument(PDF) → UnstructuredDocument
def _module_contract():
    pass
# endregion MODULE_CONTRACT
# GREP_SUMMARY: table_tree, dedoc, reader, PDF, PdfReader, BaseReader, PDF, pdfminer, tabby, OCR, tables, image, txtlayer, columns, orientation, paragraphs, metadata, extraction, line, bbox, TableTree
# STRUCTURE: ▶ Init ┌PDF file┐ → [TableTree] ○ can_read? → ○ read → [__init__ → set_text_into_tree → set_crop_text_box] → ⊕ UnstructuredDocument(lines, tables, attachments)
