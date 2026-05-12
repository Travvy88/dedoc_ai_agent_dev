from functools import total_ordering
from typing import Any, Dict, Optional

import logging

logger = logging.getLogger(__name__)

from dedocutils.data_structures import BBox


@total_ordering
# region CLASS_Location [DOMAIN(8): DocumentProcessing; CONCEPT(7): Reader; TECH(6): Python]
class Location:
    # region METHOD___init__ [DOMAIN(7): DocumentProcessing; CONCEPT(6): Method; TECH(6): Python]
    def __init__(self, page_number: int, bbox: BBox, name: str = "", rotated_angle: float = 0.0, page_width: int = None, page_height: int = None) -> None:
        self.page_number = page_number
        self.page_width = page_width
        self.page_height = page_height
        self.bbox = bbox
        self.name = name
        # TODO put self.order (change LineWithLocation, PdfImageAttachment, ScanTable)
        self.rotated_angle = rotated_angle

    # region METHOD_shift [DOMAIN(7): DocumentProcessing; CONCEPT(6): Method; TECH(6): Python]
    # endregion METHOD___init__
    def shift(self, shift_x: int, shift_y: int) -> None:
        self.bbox.shift(shift_x, shift_y)

    # region METHOD_to_relative_bbox_dict [DOMAIN(7): DocumentProcessing; CONCEPT(6): Method; TECH(6): Python]
    # endregion METHOD_shift
    def to_relative_bbox_dict(self) -> Optional[Dict]:
        if not self.page_height or not self.page_width:
            return None
        return self.bbox.to_relative_dict(self.page_width, self.page_height)

    # region METHOD_to_dict [DOMAIN(7): DocumentProcessing; CONCEPT(6): Method; TECH(6): Python]
    # endregion METHOD_to_relative_bbox_dict
    def to_dict(self) -> Dict[str, Any]:
        from collections import OrderedDict

        res = OrderedDict()
        res["page_number"] = self.page_number
        res["bbox"] = self.bbox.to_dict()  # [x_begin, y_begin, width, height]
        res["name"] = self.name
        res["rotated_angle"] = self.rotated_angle
        return res

    # region METHOD___eq__ [DOMAIN(7): DocumentProcessing; CONCEPT(6): Method; TECH(6): Python]
    # endregion METHOD_to_dict
    def __eq__(self, other: "Location") -> bool:
        return (self.page_number, self.bbox.y_bottom_right) == (other.page_number, other.bbox.y_bottom_right)

    # region METHOD___lt__ [DOMAIN(7): DocumentProcessing; CONCEPT(6): Method; TECH(6): Python]
    # endregion METHOD___eq__
    def __lt__(self, other: "Location") -> bool:
# endregion CLASS_Location
        return (self.page_number, self.bbox.y_bottom_right) < (other.page_number, other.bbox.y_bottom_right)

    # endregion METHOD___lt__


# region MODULE_CONTRACT [DOMAIN(8): DocumentProcessing; CONCEPT(7): Reader_location; TECH(6): Python, dedoc]
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
## CLASS [12][Location reader/processor] => Location
## @usecases
## - [read]: System (Pipeline) → ParseDocument(PDF) → UnstructuredDocument
def _module_contract():
    pass
# endregion MODULE_CONTRACT
# GREP_SUMMARY: location, dedoc, reader, PDF, PdfReader, BaseReader, PDF, pdfminer, tabby, OCR, tables, image, txtlayer, columns, orientation, paragraphs, metadata, extraction, line, bbox, Location
# STRUCTURE: ▶ Init ┌PDF file┐ → [Location] ○ can_read? → ○ read → [__init__ → shift → to_relative_bbox_dict] → ⊕ UnstructuredDocument(lines, tables, attachments)
