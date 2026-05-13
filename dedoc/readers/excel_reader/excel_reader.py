from typing import Optional

from xlrd.sheet import Sheet

import logging

logger = logging.getLogger(__name__)

from dedoc.data_structures.table import Table
from dedoc.data_structures.unstructured_document import UnstructuredDocument
from dedoc.readers.base_reader import BaseReader


# region CLASS_ExcelReader [DOMAIN(8): DocumentProcessing; CONCEPT(7): Reader; TECH(6): Python]
class ExcelReader(BaseReader):
    """
    This class is used for parsing documents with .xlsx extension.
    Please use :class:`~dedoc.converters.ExcelConverter` for getting xlsx file from similar formats.
    """
    import xlrd
    xlrd.xlsx.ensure_elementtree_imported(False, None)
    xlrd.xlsx.Element_has_iter = True

    # region METHOD___init__ [DOMAIN(7): DocumentProcessing; CONCEPT(6): Method; TECH(6): Python]
    def __init__(self, *, config: Optional[dict] = None) -> None:
        from dedoc.attachments_extractors.concrete_attachments_extractors.excel_attachments_extractor import ExcelAttachmentsExtractor
        from dedoc.extensions import recognized_extensions, recognized_mimes
        super().__init__(config=config, recognized_extensions=recognized_extensions.excel_like_format, recognized_mimes=recognized_mimes.excel_like_format)
        self.attachment_extractor = ExcelAttachmentsExtractor(config=self.config)

    # region METHOD_read [DOMAIN(7): DocumentProcessing; CONCEPT(6): Method; TECH(6): Python]
    # endregion METHOD___init__
    def read(self, file_path: str, parameters: Optional[dict] = None) -> UnstructuredDocument:
        """
        This method extracts tables and attachments from the document, `lines` attribute remains empty.
        Look to the documentation of :meth:`~dedoc.readers.BaseReader.read` to get information about the method's parameters.
        """
        import xlrd
        from dedoc.utils.parameter_utils import get_param_with_attachments

        with xlrd.open_workbook(file_path) as book:
            sheets_num = book.nsheets
            tables = []
            for sheet_num in range(sheets_num):
                sheet = book.sheet_by_index(sheet_num)
                tables.append(self.__parse_sheet(sheet_num, sheet))
            if get_param_with_attachments(parameters):
                attachments = self.attachment_extractor.extract(file_path=file_path, parameters=parameters)
            else:
                attachments = []
            return UnstructuredDocument(lines=[], tables=tables, attachments=attachments, warnings=[])

    # region METHOD___parse_sheet [DOMAIN(7): DocumentProcessing; CONCEPT(6): Method; TECH(6): Python]
    # endregion METHOD_read
    def __parse_sheet(self, sheet_id: int, sheet: Sheet) -> Table:
        from dedoc.data_structures.line_with_meta import LineWithMeta
        from dedoc.data_structures.line_metadata import LineMetadata
        from dedoc.data_structures.cell_with_meta import CellWithMeta
        from dedoc.data_structures.table_metadata import TableMetadata

        n_rows = sheet.nrows
        n_cols = sheet.ncols
        res = []
        for row_id in range(n_rows):
            row = []
            for col_id in range(n_cols):
                value = str(sheet.cell_value(rowx=row_id, colx=col_id))
                row.append(CellWithMeta(lines=[LineWithMeta(line=value, metadata=LineMetadata(page_id=sheet_id, line_id=0))]))
            res.append(row)
        metadata = TableMetadata(page_id=sheet_id)
# endregion CLASS_ExcelReader
        return Table(cells=res, metadata=metadata)

    # endregion METHOD___parse_sheet


# region MODULE_CONTRACT [DOMAIN(8): DocumentProcessing; CONCEPT(7): Reader_excel_reader; TECH(6): Python, dedoc]
## @modulecontract
## @purpose Read and parse Excel (.xlsx) documents, extracting lines with metadata, tables, and attachments into UnstructuredDocument.
## @scope Document parsing pipeline: Excel (.xlsx) format reading.
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
## CLASS [6][ExcelReader reader/processor] => ExcelReader
## @usecases
## - [read]: System (Pipeline) → ParseDocument(Excel (.xlsx)) → UnstructuredDocument
def _module_contract():
    pass
# endregion MODULE_CONTRACT
# GREP_SUMMARY: excel_reader, dedoc, reader, Excel (.xlsx), ExcelReader, BaseReader, XLSX, xlrd, spreadsheet, Table, sheets, cells, ExcelReader
# STRUCTURE: ▶ Init ┌Excel (.xlsx) file┐ → [ExcelReader] ○ can_read? → ○ read → [__init__ → read → __parse_sheet] → ⊕ UnstructuredDocument(lines, tables, attachments)
