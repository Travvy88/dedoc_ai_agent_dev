from typing import Optional

from dedoc.data_structures.unstructured_document import UnstructuredDocument
from dedoc.readers.pdf_reader.pdf_txtlayer_reader.pdf_txtlayer_reader import PdfTxtlayerReader

import logging

logger = logging.getLogger(__name__)


# region CLASS_PdfBrokenEncodingReader [DOMAIN(8): DocumentProcessing; CONCEPT(7): Reader; TECH(6): Python]
class PdfBrokenEncodingReader(PdfTxtlayerReader):
    """
    This class allows to extract content (text, tables, attachments) from the .pdf documents with a textual layer with broken encoding
    (copyable documents, but copied text is incorrect) with complex background.
    It uses a pdfminer library for text extraction and CNN for font's glyphs prediction.
    Currently, only Russian and English languages are supported.

    For more information, look to `pdf_with_text_layer` option description in :ref:`pdf_handling_parameters`.
    """

    # region METHOD___init__ [DOMAIN(7): DocumentProcessing; CONCEPT(6): Method; TECH(6): Python]
    def __init__(self, *, config: Optional[dict] = None) -> None:
        super().__init__(config=config)
        from dedoc.readers.pdf_reader.pdf_txtlayer_reader.pdf_broken_encoding.broken_encoding_extractor import BrokenEncodingExtractor

        self.extractor_layer = BrokenEncodingExtractor(config=self.config)
        self.reader_key = "bad_encoding"

    # region METHOD_can_read [DOMAIN(7): DocumentProcessing; CONCEPT(6): Method; TECH(6): Python]
    # endregion METHOD___init__
    def can_read(self, file_path: Optional[str] = None, mime: Optional[str] = None, extension: Optional[str] = None, parameters: Optional[dict] = None) -> bool:
        """
        Check if the document extension is suitable for this reader (PDF format is supported only).
        This method returns `True` only when the key `pdf_with_text_layer` with value `bad_encoding` is set in the dictionary `parameters`.

        You can look to :ref:`pdf_handling_parameters` to get more information about `parameters` dictionary possible arguments.

        Look to the documentation of :meth:`~dedoc.readers.BaseReader.can_read` to get information about the method's parameters.
        """
        return super().can_read(file_path=file_path, mime=mime, extension=extension, parameters=parameters)

    # region METHOD__postprocess [DOMAIN(7): DocumentProcessing; CONCEPT(6): Method; TECH(6): Python]
    # endregion METHOD_can_read
    def _postprocess(self, document: UnstructuredDocument) -> UnstructuredDocument:
        """
        Perform document postprocessing.
        """
        self.extractor_layer.cache = {}
# endregion CLASS_PdfBrokenEncodingReader
        return document

    # endregion METHOD__postprocess


# region MODULE_CONTRACT [DOMAIN(8): DocumentProcessing; CONCEPT(7): Reader_pdf_broken_encoding_reader; TECH(6): Python, dedoc]
## @modulecontract
## @purpose Read and parse PDF documents, extracting lines with metadata, tables, and attachments into UnstructuredDocument.
## @scope Document parsing pipeline: PDF format reading.
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
## CLASS [6][PdfBrokenEncodingReader reader/processor] => PdfBrokenEncodingReader
## @usecases
## - [read]: System (Pipeline) → ParseDocument(PDF) → UnstructuredDocument
def _module_contract():
    pass
# endregion MODULE_CONTRACT
# GREP_SUMMARY: pdf_broken_encoding_reader, dedoc, reader, PDF, PdfReader, BaseReader, PDF, pdfminer, tabby, OCR, tables, image, txtlayer, columns, orientation, paragraphs, metadata, extraction, line, bbox, PdfBrokenEncodingReader
# STRUCTURE: ▶ Init ┌PDF file┐ → [PdfBrokenEncodingReader] ○ can_read? → ○ read → [__init__ → can_read → _postprocess] → ⊕ UnstructuredDocument(lines, tables, attachments)
