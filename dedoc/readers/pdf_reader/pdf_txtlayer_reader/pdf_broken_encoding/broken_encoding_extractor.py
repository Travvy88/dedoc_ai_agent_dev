from pathlib import Path
from typing import Optional

import logging

logger = logging.getLogger(__name__)

from dedoc.readers.pdf_reader.data_classes.page_with_bboxes import PageWithBBox
from dedoc.readers.pdf_reader.pdf_base_reader import ParametersForParseDoc
from dedoc.readers.pdf_reader.pdf_txtlayer_reader.pdf_broken_encoding.pdf_layout_corrector import PDFLayoutCorrector
from dedoc.readers.pdf_reader.pdf_txtlayer_reader.pdfminer_reader.pdfminer_extractor import PdfminerExtractor


# region CLASS_BrokenEncodingExtractor [DOMAIN(8): DocumentProcessing; CONCEPT(7): Reader; TECH(6): Python]
class BrokenEncodingExtractor(PdfminerExtractor):

    # region METHOD___init__ [DOMAIN(7): DocumentProcessing; CONCEPT(6): Method; TECH(6): Python]
    def __init__(self, *, config: dict) -> None:
        super().__init__(config=config)
        self.layout_corrector = PDFLayoutCorrector()
        self.cache = {}

    # region METHOD_extract_text_layer [DOMAIN(7): DocumentProcessing; CONCEPT(6): Method; TECH(6): Python]
    # endregion METHOD___init__
    def extract_text_layer(self, path: str, page_number: int, parameters: ParametersForParseDoc) -> Optional[PageWithBBox]:
        if path in self.cache:  # TODO think how to do it more properly
            pages, layouts = self.cache[path]
        else:
            pages, layouts = self.layout_corrector.get_correct_layout(Path(path))
            self.cache = {path: (pages, layouts)}

        for page_num, (page, layout) in enumerate(zip(pages, layouts)):
            if page_num != page_number:
                continue
# endregion CLASS_BrokenEncodingExtractor
            return self._handle_page(page=page, page_number=page_number, path=path, parameters=parameters, layout=layout)

    # endregion METHOD_extract_text_layer


# region MODULE_CONTRACT [DOMAIN(8): DocumentProcessing; CONCEPT(7): Reader_broken_encoding_extractor; TECH(6): Python, dedoc]
## @modulecontract
## @purpose Read and parse PDF documents, extracting lines with metadata, tables, and attachments into UnstructuredDocument.
## @scope Feature and metadata extraction from documents.
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
## CLASS [4][BrokenEncodingExtractor reader/processor] => BrokenEncodingExtractor
## @usecases
## - [read]: System (Pipeline) → ParseDocument(PDF) → UnstructuredDocument
def _module_contract():
    pass
# endregion MODULE_CONTRACT
# GREP_SUMMARY: broken_encoding_extractor, dedoc, reader, PDF, PdfReader, BaseReader, PDF, pdfminer, tabby, OCR, tables, image, txtlayer, columns, orientation, paragraphs, metadata, extraction, line, bbox, BrokenEncodingExtractor
# STRUCTURE: ▶ Init ┌PDF file┐ → [BrokenEncodingExtractor] ○ can_read? → ○ read → [__init__ → extract_text_layer] → ⊕ UnstructuredDocument(lines, tables, attachments)
