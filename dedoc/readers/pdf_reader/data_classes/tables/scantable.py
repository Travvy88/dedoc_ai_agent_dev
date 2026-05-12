from typing import List

from dedocutils.data_structures import BBox

import logging

logger = logging.getLogger(__name__)

from dedoc.data_structures.cell_with_meta import CellWithMeta
from dedoc.data_structures.table import Table
from dedoc.data_structures.table_metadata import TableMetadata
from dedoc.readers.pdf_reader.data_classes.tables.cell import Cell
from dedoc.readers.pdf_reader.data_classes.tables.location import Location


# region CLASS_ScanTable [DOMAIN(8): DocumentProcessing; CONCEPT(7): Reader; TECH(6): Python]
class ScanTable(Table):
    """
    Utility class for storing recognized tables from document images. The class
    :class:`~dedoc.readers.pdf_reader.pdf_image_reader.table_recognizer.table_recognizer.TableRecognizer` works with this class.
    """
    # region METHOD___init__ [DOMAIN(7): DocumentProcessing; CONCEPT(6): Method; TECH(6): Python]
    def __init__(self, page_number: int, cells: List[List[CellWithMeta]], bbox: BBox, order: int = -1, page_width: int = None, page_height: int = None) -> None:

        super().__init__(cells, TableMetadata(page_id=page_number))
        self.order = order
        self.locations = [Location(page_number, bbox, page_width=page_width, page_height=page_height)]

    # region METHOD_extended [DOMAIN(7): DocumentProcessing; CONCEPT(6): Method; TECH(6): Python]
    # endregion METHOD___init__
    def extended(self, table: "ScanTable") -> None:
        # extend locations
        self.locations.extend(table.locations)
        # extend values
        self.cells.extend(table.cells)
        # extend order
        self.order = max(self.order, table.order)

    # region METHOD_check_on_cell_instance [DOMAIN(7): DocumentProcessing; CONCEPT(6): Method; TECH(6): Python]
    # endregion METHOD_extended
    def check_on_cell_instance(self) -> bool:
        if len(self.cells) == 0:
            return False
        if len(self.cells[0]) == 0:
            return False
        if not isinstance(self.cells[0][0], Cell):
            return False
        return True

    # region METHOD___get_cells_text [DOMAIN(7): DocumentProcessing; CONCEPT(6): Method; TECH(6): Python]
    # endregion METHOD_check_on_cell_instance
    def __get_cells_text(self, cells: List[List[CellWithMeta]]) -> List[List[str]]:
        return [[cell.get_text() for cell in row] for row in cells]

    # endregion METHOD___get_cells_text
    @property
    # region METHOD_location [DOMAIN(7): DocumentProcessing; CONCEPT(6): Method; TECH(6): Python]
    def location(self) -> Location:
        return min(self.locations)

    # endregion METHOD_location
    @property
    # region METHOD_uid [DOMAIN(7): DocumentProcessing; CONCEPT(6): Method; TECH(6): Python]
    def uid(self) -> str:
        return self.metadata.uid

    # region METHOD_to_dict [DOMAIN(7): DocumentProcessing; CONCEPT(6): Method; TECH(6): Python]
    # endregion METHOD_uid
    def to_dict(self) -> dict:
        from collections import OrderedDict

        data_text = self.__get_cells_text(self.cells)

        res = OrderedDict()
        res["locations"] = [location.to_dict() for location in self.locations]
        res["cells"] = data_text

# endregion CLASS_ScanTable
        return res

    # endregion METHOD_to_dict


# region MODULE_CONTRACT [DOMAIN(8): DocumentProcessing; CONCEPT(7): Reader_scantable; TECH(6): Python, dedoc]
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
## CLASS [14][ScanTable reader/processor] => ScanTable
## @usecases
## - [read]: System (Pipeline) → ParseDocument(PDF) → UnstructuredDocument
def _module_contract():
    pass
# endregion MODULE_CONTRACT
# GREP_SUMMARY: scantable, dedoc, reader, PDF, PdfReader, BaseReader, PDF, pdfminer, tabby, OCR, tables, image, txtlayer, columns, orientation, paragraphs, metadata, extraction, line, bbox, ScanTable
# STRUCTURE: ▶ Init ┌PDF file┐ → [ScanTable] ○ can_read? → ○ read → [__init__ → extended → check_on_cell_instance] → ⊕ UnstructuredDocument(lines, tables, attachments)
