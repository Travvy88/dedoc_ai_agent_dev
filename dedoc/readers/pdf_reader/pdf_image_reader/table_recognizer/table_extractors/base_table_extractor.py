import logging
from typing import List

from dedoc.readers.pdf_reader.data_classes.tables.cell import Cell


# region CLASS_BaseTableExtractor [DOMAIN(8): DocumentProcessing; CONCEPT(7): Reader; TECH(6): Python]
class BaseTableExtractor(object):
    # region METHOD___init__ [DOMAIN(7): DocumentProcessing; CONCEPT(6): Method; TECH(6): Python]
    def __init__(self, *, config: dict, logger: logging.Logger) -> None:
        self.config = config
        self.logger = logger

    # region METHOD__print_matrix_table [DOMAIN(7): DocumentProcessing; CONCEPT(6): Method; TECH(6): Python]
    # endregion METHOD___init__
    def _print_matrix_table(self, matrix_table: List[List[Cell]]) -> None:
        string = ""
        for i in range(len(matrix_table)):
            string += " ".join([str(cell.id_con) for cell in matrix_table[i]])
            string += "\n"
        self.logger.debug(f"{string}\nend table")

    # region METHOD__print_table_attr [DOMAIN(7): DocumentProcessing; CONCEPT(6): Method; TECH(6): Python]
    # endregion METHOD__print_matrix_table
    def _print_table_attr(self, matrix_cells: List[List[Cell]]) -> None:
        string = "Table:\n"
        for i in range(0, len(matrix_cells)):
            string += "\t".join([f"{cell.id_con}/{cell.is_attribute}/{cell.is_attribute_required}" for cell in matrix_cells[i]])
            string += "\n"
# endregion CLASS_BaseTableExtractor
        self.logger.debug(string)

    # endregion METHOD__print_table_attr


# region MODULE_CONTRACT [DOMAIN(8): DocumentProcessing; CONCEPT(7): Reader_base_table_extractor; TECH(6): Python, dedoc]
## @modulecontract
## @purpose Read and parse PDF documents, extracting lines with metadata, tables, and attachments into UnstructuredDocument.
## @scope Table recognition and extraction from document images.
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
## CLASS [6][BaseTableExtractor reader/processor] => BaseTableExtractor
## @usecases
## - [read]: System (Pipeline) → ParseDocument(PDF) → UnstructuredDocument
def _module_contract():
    pass
# endregion MODULE_CONTRACT
# GREP_SUMMARY: base_table_extractor, dedoc, reader, PDF, PdfReader, BaseReader, PDF, pdfminer, tabby, OCR, tables, image, txtlayer, columns, orientation, paragraphs, metadata, extraction, line, bbox, BaseTableExtractor
# STRUCTURE: ▶ Init ┌PDF file┐ → [BaseTableExtractor] ○ can_read? → ○ read → [__init__ → _print_matrix_table → _print_table_attr] → ⊕ UnstructuredDocument(lines, tables, attachments)
