from typing import List, Optional, Tuple

from dedoc.data_structures.unstructured_document import UnstructuredDocument
from dedoc.readers.base_reader import BaseReader

import logging

logger = logging.getLogger(__name__)


# region CLASS_CSVReader [DOMAIN(8): DocumentProcessing; CONCEPT(7): Reader; TECH(6): Python]
class CSVReader(BaseReader):
    """
    This class allows to parse files with the following extensions: .csv, .tsv.
    """

    # region METHOD___init__ [DOMAIN(7): DocumentProcessing; CONCEPT(6): Method; TECH(6): Python]
    def __init__(self, *, config: Optional[dict] = None) -> None:
        from dedoc.extensions import recognized_extensions, recognized_mimes
        super().__init__(config=config, recognized_extensions=recognized_extensions.csv_like_format, recognized_mimes=recognized_mimes.csv_like_format)
        self.default_separator = ","

    # region METHOD_read [DOMAIN(7): DocumentProcessing; CONCEPT(6): Method; TECH(6): Python]
    # endregion METHOD___init__
    def read(self, file_path: str, parameters: Optional[dict] = None) -> UnstructuredDocument:
        """
        The method will place all extracted content inside tables of the :class:`~dedoc.data_structures.UnstructuredDocument`.
        The lines and attachments remain empty.
        Look to the documentation of :meth:`~dedoc.readers.BaseReader.read` to get information about the method's parameters.
        """
        import pandas as pd
        from dedoc.data_structures.line_metadata import LineMetadata
        from dedoc.data_structures.line_with_meta import LineWithMeta
        from dedoc.data_structures.cell_with_meta import CellWithMeta
        from dedoc.data_structures.table import Table
        from dedoc.data_structures.table_metadata import TableMetadata

        parameters = {} if parameters is None else parameters
        delimiter = parameters.get("delimiter")
        if delimiter is None:
            delimiter = "\t" if file_path.endswith(".tsv") else self.default_separator
        encoding, encoding_warning = self.__get_encoding(file_path, parameters)
        df = pd.read_csv(file_path, sep=delimiter, header=None, encoding=encoding, dtype="string", keep_default_na=False)
        table_metadata = TableMetadata(page_id=0)
        cells_with_meta = []
        line_id = 0
        for ind in df.index:
            row_lines = []
            for cell in df.loc[ind]:
                row_lines.append(CellWithMeta(lines=[LineWithMeta(line=cell, metadata=LineMetadata(page_id=0, line_id=line_id))]))
                line_id += 1
            cells_with_meta.append(row_lines)

        tables = [Table(cells=cells_with_meta, metadata=table_metadata)]
        warnings = [f"delimiter is '{delimiter}'"]
        warnings.extend(encoding_warning)
        return UnstructuredDocument(lines=[], tables=tables, attachments=[], warnings=warnings)

    # region METHOD___get_encoding [DOMAIN(7): DocumentProcessing; CONCEPT(6): Method; TECH(6): Python]
    # endregion METHOD_read
    def __get_encoding(self, path: str, parameters: dict) -> Tuple[str, List[str]]:
        from dedoc.utils.utils import get_encoding

        if parameters.get("encoding"):
            return parameters["encoding"], []
        else:
            encoding = get_encoding(path, "utf-8")
# endregion CLASS_CSVReader
            return encoding, [f"encoding is {encoding}"]

    # endregion METHOD___get_encoding


# region MODULE_CONTRACT [DOMAIN(8): DocumentProcessing; CONCEPT(7): Reader_csv_reader; TECH(6): Python, dedoc]
## @modulecontract
## @purpose Read and parse CSV/TSV documents, extracting lines with metadata, tables, and attachments into UnstructuredDocument.
## @scope Document parsing pipeline: CSV/TSV format reading.
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
## CLASS [6][CSVReader reader/processor] => CSVReader
## @usecases
## - [read]: System (Pipeline) → ParseDocument(CSV/TSV) → UnstructuredDocument
def _module_contract():
    pass
# endregion MODULE_CONTRACT
# GREP_SUMMARY: csv_reader, dedoc, reader, CSV/TSV, CSVReader, BaseReader, CSV, TSV, delimiter, pandas, UnstructuredDocument, Table, spreadsheet, CSVReader
# STRUCTURE: ▶ Init ┌CSV/TSV file┐ → [CSVReader] ○ can_read? → ○ read → [__init__ → read → __get_encoding] → ⊕ UnstructuredDocument(lines, tables, attachments)
