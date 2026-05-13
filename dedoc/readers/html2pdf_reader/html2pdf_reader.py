from typing import Dict, Optional, Tuple

from bs4 import BeautifulSoup

from dedoc.data_structures.table import Table
from dedoc.data_structures.unstructured_document import UnstructuredDocument
from dedoc.readers.html_reader.html_reader import HtmlReader


# region CLASS_Html2PdfReader [DOMAIN(8): DocumentProcessing; CONCEPT(7): Reader; TECH(6): Python]
class Html2PdfReader(HtmlReader):

    # region METHOD___init__ [DOMAIN(7): DocumentProcessing; CONCEPT(6): Method; TECH(6): Python]
    def __init__(self, *, config: Optional[dict] = None) -> None:
        super().__init__(config=config)
        from dedoc.readers.pdf_reader.pdf_txtlayer_reader.pdf_txtlayer_reader import PdfTxtlayerReader
        self.pdf_reader = PdfTxtlayerReader(config=self.config)

    # region METHOD_read [DOMAIN(7): DocumentProcessing; CONCEPT(6): Method; TECH(6): Python]
    # endregion METHOD___init__
    def read(self, file_path: str, parameters: Optional[dict] = None) -> UnstructuredDocument:
        import os
        from copy import deepcopy
        from tempfile import TemporaryDirectory
        from weasyprint import HTML

        parameters = {} if parameters is None else parameters
        with TemporaryDirectory() as tmp_dir:
            modified_path, tables = self._modify_html(file_path, tmp_dir)
            converted_path = os.path.join(tmp_dir, os.path.basename(file_path).replace(".html", ".pdf"))
            HTML(filename=modified_path).write_pdf(converted_path)
            self.logger.info(f"Convert {modified_path} to {converted_path}")
            parameters_new = deepcopy(parameters)
            parameters_new["pdf_with_text_layer"] = "true"
            unstructured_document = self.pdf_reader.read(file_path=converted_path, parameters=parameters_new)

        return self._add_tables(document=unstructured_document, tables=tables)

    # region METHOD__add_tables [DOMAIN(7): DocumentProcessing; CONCEPT(6): Method; TECH(6): Python]
    # endregion METHOD_read
    def _add_tables(self, document: UnstructuredDocument, tables: Dict[str, Table]) -> UnstructuredDocument:
        from dedoc.data_structures.concrete_annotations.table_annotation import TableAnnotation

        lines = []
        tables_result = []
        previous_line = None
        line_id = 0
        for line in document.lines:
            table_uid = line.line.strip()
            if table_uid not in tables:
                previous_line = line
                line.metadata.page_id = line_id
                line_id += 1
                lines.append(line)
            elif previous_line is not None:
                table_annotation = TableAnnotation(value=table_uid, start=0, end=len(line.line))
                previous_line.annotations.append(table_annotation)
                tables_result.append(tables[table_uid])
        return UnstructuredDocument(lines=lines, tables=tables_result, attachments=document.attachments)

    # region METHOD__handle_tables [DOMAIN(7): DocumentProcessing; CONCEPT(6): Method; TECH(6): Python]
    # endregion METHOD__add_tables
    def _handle_tables(self, soup: BeautifulSoup, path_hash: str) -> dict:
        from uuid import uuid1

        tables = {}
        for table_tag in soup.find_all("table"):
            table_uid = f"table_{uuid1()}"
            table = self._read_table(table_tag, path_hash)
            table.metadata.uid = table_uid
            tables[table_uid] = table
            table_tag.replace_with(table_uid)

        return tables

    # region METHOD__handle_super_elements [DOMAIN(7): DocumentProcessing; CONCEPT(6): Method; TECH(6): Python]
    # endregion METHOD__handle_tables
    def _handle_super_elements(self, soup: BeautifulSoup) -> None:
        """
        Function finds super-elements in the html (html present as BeautifulSoup's object)
        (For example:
         html-code: <span>1</span><span style="font-size:6pt; vertical-align:super">1</span><span>) lalala</span>)
         view: "1 ^1 ) lalala"

         and converts into
         html-code: <span>1.1) lalala</span>
         view: "1.1) lalala"
        """
        import re

        supers = soup.find_all(["span", "p"], {"style": re.compile("vertical-align:super")})

        for super_element in supers:
            if super_element.previous and super_element.previousSibling:
                super_element.previous.replaceWith(super_element.previous + "." + super_element.contents[0])
                if super_element.next and super_element.nextSibling:
                    super_element.previousSibling.replaceWith(super_element.previous + super_element.nextSibling.string)
                    super_element.nextSibling.decompose()
                super_element.decompose()

    # region METHOD__modify_html [DOMAIN(7): DocumentProcessing; CONCEPT(6): Method; TECH(6): Python]
    # endregion METHOD__handle_super_elements
    def _modify_html(self, path: str, tmp_dir: str) -> Tuple[str, dict]:
        import os
        from dedoc.utils.utils import calculate_file_hash

        with open(path, encoding="utf-8") as f:
            soup = BeautifulSoup(f.read(), "html.parser")

        tables = self._handle_tables(soup, path_hash=calculate_file_hash(path=path))
        self._handle_super_elements(soup)

        path_out = os.path.join(tmp_dir, os.path.basename(path))

        with open(path_out, "wb") as f_output:
            f_output.write(soup.prettify("utf-8"))
# endregion CLASS_Html2PdfReader
        return path_out, tables

    # endregion METHOD__modify_html


# region MODULE_CONTRACT [DOMAIN(8): DocumentProcessing; CONCEPT(7): Reader_html2pdf_reader; TECH(6): Python, dedoc]
## @modulecontract
## @purpose Read and parse HTML → PDF documents, extracting lines with metadata, tables, and attachments into UnstructuredDocument.
## @scope Document parsing pipeline: HTML → PDF format reading.
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
## CLASS [12][Html2PdfReader reader/processor] => Html2PdfReader
## @usecases
## - [read]: System (Pipeline) → ParseDocument(HTML → PDF) → UnstructuredDocument
def _module_contract():
    pass
# endregion MODULE_CONTRACT
# GREP_SUMMARY: html2pdf_reader, dedoc, reader, HTML → PDF, Html2PdfReader, BaseReader, HTML, PDF, conversion, wkhtmltopdf, pdfkit, Html2PdfReader
# STRUCTURE: ▶ Init ┌HTML → PDF file┐ → [Html2PdfReader] ○ can_read? → ○ read → [__init__ → read → _add_tables] → ⊕ UnstructuredDocument(lines, tables, attachments)
