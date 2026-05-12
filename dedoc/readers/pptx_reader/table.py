import hashlib

from bs4 import Tag

import logging

logger = logging.getLogger(__name__)

from dedoc.data_structures.cell_with_meta import CellWithMeta
from dedoc.data_structures.table import Table
from dedoc.data_structures.table_metadata import TableMetadata
from dedoc.readers.docx_reader.numbering_extractor import NumberingExtractor
from dedoc.readers.pptx_reader.properties_extractor import PropertiesExtractor
from dedoc.readers.pptx_reader.shape import PptxShape


# region CLASS_PptxTable [DOMAIN(8): DocumentProcessing; CONCEPT(7): Reader; TECH(6): Python]
class PptxTable:
    """
    This class corresponds to the table (tag <a:tbl>) in the slides xml files.
    """
    # region METHOD___init__ [DOMAIN(7): DocumentProcessing; CONCEPT(6): Method; TECH(6): Python]
    def __init__(self, xml: Tag, page_id: int, numbering_extractor: NumberingExtractor, properties_extractor: PropertiesExtractor) -> None:
        """
        Contains information about table properties.
        :param xml: BeautifulSoup tree with table properties
        """
        self.xml = xml
        self.page_id = page_id
        self.numbering_extractor = numbering_extractor
        self.properties_extractor = properties_extractor
        self.__uid = hashlib.md5(xml.encode()).hexdigest()

    # endregion METHOD___init__
    @property
    # region METHOD_uid [DOMAIN(7): DocumentProcessing; CONCEPT(6): Method; TECH(6): Python]
    def uid(self) -> str:
        return self.__uid

    # region METHOD_to_table [DOMAIN(7): DocumentProcessing; CONCEPT(6): Method; TECH(6): Python]
    # endregion METHOD_uid
    def to_table(self) -> Table:
        """
        Converts xml file with table to Table class
        """
        # tbl -- table; tr -- table row, tc -- table cell
        # delete tables inside tables
        for tbl in self.xml.find_all("a:tbl"):
            tbl.extract()

        rows = self.xml.find_all("a:tr")
        cell_list = []

        for row in rows:
            cells = row.find_all("a:tc")
            col_index = 0
            cell_row_list = []

            for cell in cells:
                if int(cell.get("vMerge", 0)):  # vertical merge
                    cell_with_meta = CellWithMeta(lines=cell_list[-1][col_index].lines, colspan=1, rowspan=1, invisible=True)
                elif int(cell.get("hMerge", 0)):  # horizontal merge
                    cell_with_meta = CellWithMeta(lines=cell_row_list[-1].lines, colspan=1, rowspan=1, invisible=True)
                else:
                    colspan = int(cell.get("gridSpan", 1))  # gridSpan attribute describes number of horizontally merged cells
                    rowspan = int(cell.get("rowSpan", 1))  # rowSpan attribute for vertically merged set of cells (or horizontally split cells)
                    lines = PptxShape(xml=cell, page_id=self.page_id, numbering_extractor=self.numbering_extractor, init_line_id=0,
                                      properties_extractor=self.properties_extractor).get_lines()
                    cell_with_meta = CellWithMeta(lines=lines, colspan=colspan, rowspan=rowspan, invisible=False)

                cell_row_list.append(cell_with_meta)
                col_index += 1

            cell_list.append(cell_row_list)

# endregion CLASS_PptxTable
        return Table(cells=cell_list, metadata=TableMetadata(page_id=self.page_id, uid=self.uid))

    # endregion METHOD_to_table


# region MODULE_CONTRACT [DOMAIN(8): DocumentProcessing; CONCEPT(7): Reader_table; TECH(6): Python, dedoc]
## @modulecontract
## @purpose Read and parse PPTX documents, extracting lines with metadata, tables, and attachments into UnstructuredDocument.
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
## CLASS [6][PptxTable reader/processor] => PptxTable
## @usecases
## - [read]: System (Pipeline) → ParseDocument(PPTX) → UnstructuredDocument
def _module_contract():
    pass
# endregion MODULE_CONTRACT
# GREP_SUMMARY: table, dedoc, reader, PPTX, PptxReader, BaseReader, PPTX, PowerPoint, slides, shapes, paragraphs, tables, numbering, properties, PptxTable
# STRUCTURE: ▶ Init ┌PPTX file┐ → [PptxTable] ○ can_read? → ○ read → [__init__ → uid → to_table] → ⊕ UnstructuredDocument(lines, tables, attachments)
