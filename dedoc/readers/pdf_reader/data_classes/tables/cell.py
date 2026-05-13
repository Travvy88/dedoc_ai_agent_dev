import copy
from typing import List, Optional

import logging

logger = logging.getLogger(__name__)

from dedocutils.data_structures import BBox

from dedoc.data_structures.cell_with_meta import CellWithMeta
from dedoc.data_structures.line_with_meta import LineWithMeta


# region CLASS_Cell [DOMAIN(8): DocumentProcessing; CONCEPT(7): Reader; TECH(6): Python]
class Cell(CellWithMeta):

    @staticmethod
    # region METHOD_copy_from [DOMAIN(7): DocumentProcessing; CONCEPT(6): Method; TECH(6): Python]
    def copy_from(cell: "Cell", bbox: Optional[BBox] = None) -> "Cell":
        copy_cell = copy.deepcopy(cell)
        if bbox:
            copy_cell.bbox = bbox

        return copy_cell

    # region METHOD_shift [DOMAIN(7): DocumentProcessing; CONCEPT(6): Method; TECH(6): Python]
    # endregion METHOD_copy_from
    def shift(self, shift_x: int, shift_y: int, image_width: int, image_height: int) -> None:
        if self.lines:
            for line in self.lines:
                line.shift(shift_x=shift_x, shift_y=shift_y, image_width=image_width, image_height=image_height)

        self.bbox.shift(shift_x=shift_x, shift_y=shift_y)
        if self.contour_coord:
            self.contour_coord.shift(shift_x=shift_x, shift_y=shift_y)

    # region METHOD___init__ [DOMAIN(7): DocumentProcessing; CONCEPT(6): Method; TECH(6): Python]
    # endregion METHOD_shift
    def __init__(self, bbox: BBox, id_con: int = -1, lines: Optional[List[LineWithMeta]] = None,
                 is_attribute: bool = False, is_attribute_required: bool = False, rotated_angle: int = 0, uid: Optional[str] = None,
                 contour_coord: Optional[BBox] = None, colspan: int = 1, rowspan: int = 1, invisible: bool = False) -> None:

        import uuid

        super().__init__(lines=lines, colspan=colspan, rowspan=rowspan, invisible=invisible)

        self.bbox = bbox
        self.id_con = id_con
        self.is_attribute = is_attribute
        self.is_attribute_required = is_attribute_required
        self.rotated_angle = rotated_angle
        self.uuid = uuid.uuid4() if uuid is None else uid
        self.contour_coord = contour_coord or BBox(0, 0, 0, 0)

    # region METHOD_change_lines_boxes_page_width_height [DOMAIN(7): DocumentProcessing; CONCEPT(6): Method; TECH(6): Python]
    # endregion METHOD___init__
    def change_lines_boxes_page_width_height(self, new_page_width: int, new_page_height: int) -> None:
        from dedoc.data_structures.concrete_annotations.bbox_annotation import BBoxAnnotation

        for i_line, _ in enumerate(self.lines):
            for i_ann, annotation in enumerate(self.lines[i_line].annotations):
                if annotation.name != "bounding box":
                    continue

                bbox, page_width, page_height = BBoxAnnotation.get_bbox_from_value(annotation.value)
                k_w = new_page_width / page_width
                k_h = new_page_height / page_height
                new_bbox = BBox(x_top_left=int(bbox.x_top_left * k_w), y_top_left=int(bbox.y_top_left * k_h),
                                width=int(bbox.width * k_w), height=int(bbox.height * k_h))

                self.lines[i_line].annotations[i_ann] = BBoxAnnotation(start=annotation.start,
                                                                       end=annotation.end,
                                                                       value=new_bbox,
                                                                       page_width=new_page_width,
                                                                       page_height=new_page_height)

    # region METHOD___repr__ [DOMAIN(7): DocumentProcessing; CONCEPT(6): Method; TECH(6): Python]
    # endregion METHOD_change_lines_boxes_page_width_height
    def __repr__(self) -> str:
# endregion CLASS_Cell
        return self.__str__()

    # endregion METHOD___repr__


# region MODULE_CONTRACT [DOMAIN(8): DocumentProcessing; CONCEPT(7): Reader_cell; TECH(6): Python, dedoc]
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
## CLASS [10][Cell reader/processor] => Cell
## @usecases
## - [read]: System (Pipeline) → ParseDocument(PDF) → UnstructuredDocument
def _module_contract():
    pass
# endregion MODULE_CONTRACT
# GREP_SUMMARY: cell, dedoc, reader, PDF, PdfReader, BaseReader, PDF, pdfminer, tabby, OCR, tables, image, txtlayer, columns, orientation, paragraphs, metadata, extraction, line, bbox, Cell
# STRUCTURE: ▶ Init ┌PDF file┐ → [Cell] ○ can_read? → ○ read → [copy_from → shift → __init__] → ⊕ UnstructuredDocument(lines, tables, attachments)
