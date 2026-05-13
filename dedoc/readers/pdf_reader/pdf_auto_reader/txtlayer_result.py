from dataclasses import dataclass
from typing import Optional

import logging

logger = logging.getLogger(__name__)

from dedoc.data_structures.unstructured_document import UnstructuredDocument


@dataclass
# region CLASS_TxtLayerResult [DOMAIN(8): DocumentProcessing; CONCEPT(7): Reader; TECH(6): Python]
class TxtLayerResult:
    """
    Class for saving information about textual layer correctness of the document chunk.
    - correct - if the document chunk contains correct textual layer or not
    - start - start page of the document chunk (numeration starts with 1)
    - end - end page of the document chunk (numeration starts with 1, end included)
    - document - UnstructuredDocument of document pages[start:end]
    """
    correct: bool
    start: int
    end: Optional[int]
# endregion CLASS_TxtLayerResult
    document: Optional[UnstructuredDocument] = None


# region MODULE_CONTRACT [DOMAIN(8): DocumentProcessing; CONCEPT(7): Reader_txtlayer_result; TECH(6): Python, dedoc]
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
## CLASS [5][TxtLayerResult reader/processor] => TxtLayerResult
## @usecases
## - [read]: System (Pipeline) → ParseDocument(PDF) → UnstructuredDocument
def _module_contract():
    pass
# endregion MODULE_CONTRACT
# GREP_SUMMARY: txtlayer_result, dedoc, reader, PDF, PdfReader, BaseReader, PDF, pdfminer, tabby, OCR, tables, image, txtlayer, columns, orientation, paragraphs, metadata, extraction, line, bbox, TxtLayerResult
# STRUCTURE: ▶ Init ┌PDF file┐ → [TxtLayerResult] ○ can_read? → ○ read → [read → can_read] → ⊕ UnstructuredDocument(lines, tables, attachments)
