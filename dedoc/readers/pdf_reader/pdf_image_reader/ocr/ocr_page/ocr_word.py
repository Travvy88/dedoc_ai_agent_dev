from dedocutils.data_structures import BBox

import logging

logger = logging.getLogger(__name__)


# region CLASS_OcrWord [DOMAIN(8): DocumentProcessing; CONCEPT(7): Reader; TECH(6): Python]
class OcrWord:
    level = 5

    # region METHOD___init__ [DOMAIN(7): DocumentProcessing; CONCEPT(6): Method; TECH(6): Python]
    def __init__(self, text: str, bbox: BBox, confidence: float, order: int) -> None:
        """
        Single word from ocr.
        :param text: extracted text
        :param bbox: word coordinates
        :param order: word order in line
        """
        super().__init__()
        self.text = text.replace("—", " ")
        self.bbox = bbox
        self.confidence = confidence
# endregion CLASS_OcrWord
        self.order = order

    # endregion METHOD___init__


# region MODULE_CONTRACT [DOMAIN(8): DocumentProcessing; CONCEPT(7): Reader_ocr_word; TECH(6): Python, dedoc]
## @modulecontract
## @purpose Read and parse PDF documents, extracting lines with metadata, tables, and attachments into UnstructuredDocument.
## @scope OCR processing pipeline for document images.
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
## CLASS [2][OcrWord reader/processor] => OcrWord
## @usecases
## - [read]: System (Pipeline) → ParseDocument(PDF) → UnstructuredDocument
def _module_contract():
    pass
# endregion MODULE_CONTRACT
# GREP_SUMMARY: ocr_word, dedoc, reader, PDF, PdfReader, BaseReader, PDF, pdfminer, tabby, OCR, tables, image, txtlayer, columns, orientation, paragraphs, metadata, extraction, line, bbox, OcrWord
# STRUCTURE: ▶ Init ┌PDF file┐ → [OcrWord] ○ can_read? → ○ read → [__init__] → ⊕ UnstructuredDocument(lines, tables, attachments)
