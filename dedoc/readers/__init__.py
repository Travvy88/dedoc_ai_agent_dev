from .archive_reader.archive_reader import ArchiveReader
from .article_reader.article_reader import ArticleReader
from .base_reader import BaseReader
from .csv_reader.csv_reader import CSVReader
from .docx_reader.docx_reader import DocxReader
from .email_reader.email_reader import EmailReader
from .excel_reader.excel_reader import ExcelReader
from .html_reader.html_reader import HtmlReader
from .json_reader.json_reader import JsonReader
from .mhtml_reader.mhtml_reader import MhtmlReader
from .note_reader.note_reader import NoteReader
from .pdf_reader.pdf_auto_reader.pdf_auto_reader import PdfAutoReader
from .pdf_reader.pdf_base_reader import PdfBaseReader
from .pdf_reader.pdf_image_reader.pdf_image_reader import PdfImageReader
from .pdf_reader.pdf_txtlayer_reader.pdf_broken_encoding_reader import PdfBrokenEncodingReader
from .pdf_reader.pdf_txtlayer_reader.pdf_tabby_reader import PdfTabbyReader
from .pdf_reader.pdf_txtlayer_reader.pdf_txtlayer_reader import PdfTxtlayerReader
from .pptx_reader.pptx_reader import PptxReader
from .reader_composition import ReaderComposition
from .txt_reader.raw_text_reader import RawTextReader

import logging

logger = logging.getLogger(__name__)

__all__ = ['ArchiveReader', 'ArticleReader', 'BaseReader', 'CSVReader', 'DocxReader', 'EmailReader', 'ExcelReader', 'HtmlReader', 'JsonReader', 'MhtmlReader',
           'NoteReader', 'PptxReader', 'ReaderComposition', 'RawTextReader', 'PdfBaseReader', 'PdfImageReader', 'PdfTabbyReader', 'PdfTxtlayerReader',
           'PdfAutoReader', 'PdfBrokenEncodingReader']


# region MODULE_CONTRACT [DOMAIN(8): DocumentProcessing; CONCEPT(7): Reader___init__; TECH(6): Python, dedoc]
## @modulecontract
## @purpose Re-export symbols for the  reader subpackage of dedoc/readers/.
## @scope Symbol re-export.
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
## [10][Module entry point / symbol re-exports]
## @usecases
## - [read]: System (Pipeline) → ParseDocument(document) → UnstructuredDocument
def _module_contract():
    pass
# endregion MODULE_CONTRACT
# GREP_SUMMARY: __init__, dedoc, reader, document, reader, document, parsing, UnstructuredDocument, __init__
# STRUCTURE: ▶ imports → ⊕ symbol re-exports
