from typing import List

from dedoc.data_structures.annotation import Annotation
from dedoc.data_structures.line_metadata import LineMetadata
from dedoc.data_structures.line_with_meta import LineWithMeta
from dedoc.readers.pdf_reader.data_classes.tables.location import Location

import logging

logger = logging.getLogger(__name__)


# region CLASS_LineWithLocation [DOMAIN(8): DocumentProcessing; CONCEPT(7): Reader; TECH(6): Python]
class LineWithLocation(LineWithMeta):

    # region METHOD___init__ [DOMAIN(7): DocumentProcessing; CONCEPT(6): Method; TECH(6): Python]
    def __init__(self, line: str, metadata: LineMetadata, annotations: List[Annotation], location: Location, uid: str = None, order: int = -1) -> None:
        self.location = location
        self.order = order
        super().__init__(line, metadata, annotations, uid)

    # region METHOD_shift [DOMAIN(7): DocumentProcessing; CONCEPT(6): Method; TECH(6): Python]
    # endregion METHOD___init__
    def shift(self, shift_x: int, shift_y: int, image_width: int, image_height: int) -> None:
        super().shift(shift_x=shift_x, shift_y=shift_y, image_width=image_width, image_height=image_height)
        self.location.shift(shift_x, shift_y)

    # region METHOD___repr__ [DOMAIN(7): DocumentProcessing; CONCEPT(6): Method; TECH(6): Python]
    # endregion METHOD_shift
    def __repr__(self) -> str:
        parent_repr = super().__repr__()
        return parent_repr.replace("LineWithMeta", "LineWithLocation")

    # region METHOD___str__ [DOMAIN(7): DocumentProcessing; CONCEPT(6): Method; TECH(6): Python]
    # endregion METHOD___repr__
    def __str__(self) -> str:
# endregion CLASS_LineWithLocation
        return self.__repr__()

    # endregion METHOD___str__


# region MODULE_CONTRACT [DOMAIN(8): DocumentProcessing; CONCEPT(7): Reader_line_with_location; TECH(6): Python, dedoc]
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
## CLASS [8][LineWithLocation reader/processor] => LineWithLocation
## @usecases
## - [read]: System (Pipeline) → ParseDocument(PDF) → UnstructuredDocument
def _module_contract():
    pass
# endregion MODULE_CONTRACT
# GREP_SUMMARY: line_with_location, dedoc, reader, PDF, PdfReader, BaseReader, PDF, pdfminer, tabby, OCR, tables, image, txtlayer, columns, orientation, paragraphs, metadata, extraction, line, bbox, LineWithLocation
# STRUCTURE: ▶ Init ┌PDF file┐ → [LineWithLocation] ○ can_read? → ○ read → [__init__ → shift → __repr__] → ⊕ UnstructuredDocument(lines, tables, attachments)
