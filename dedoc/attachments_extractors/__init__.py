# region MODULE_CONTRACT [DOMAIN(8): DocumentProcessing; CONCEPT(8): AttachmentExtraction; TECH(3): PythonPackage]
## @modulecontract
## @purpose Centralized import surface for all attachment extractors: exposes AbstractAttachmentsExtractor, all Office-format extractors, JSON and PDF extractors.
## @scope Package initialization, symbol re-export, public API surface.
## @input None
## @output Public symbols: AbstractAttachmentsExtractor, AbstractOfficeAttachmentsExtractor, DocxAttachmentsExtractor, ExcelAttachmentsExtractor, JsonAttachmentsExtractor, PDFAttachmentsExtractor, PptxAttachmentsExtractor
## @links [USES_API(9): AbstractAttachmentsExtractor, AbstractOfficeAttachmentsExtractor, DocxAttachmentsExtractor, ExcelAttachmentsExtractor, JsonAttachmentsExtractor, PDFAttachmentsExtractor, PptxAttachmentsExtractor]
## @invariants
## - __all__ ALWAYS contains all 7 public symbols.
## - Every concrete extractor listed in __all__ is importable from this package.
## @rationale
## Q: Why re-export everything here instead of importing from subpackages?
## A: Single import surface simplifies client code: `from dedoc.attachments_extractors import DocxAttachmentsExtractor`.
## @changes
## LAST_CHANGE: [v1.0.0 – Semantic markup added]
## @modulemap
## CLASS 10[Abstract base for attachment extraction] => AbstractAttachmentsExtractor
## CLASS 9[Abstract base for Office-format attachments (docx, xlsx, pptx)] => AbstractOfficeAttachmentsExtractor
## CLASS 8[Extracts attachments from .docx files] => DocxAttachmentsExtractor
## CLASS 8[Extracts attachments from .xlsx files] => ExcelAttachmentsExtractor
## CLASS 8[Extracts attachments from .json files] => JsonAttachmentsExtractor
## CLASS 8[Extracts attachments from .pdf files] => PDFAttachmentsExtractor
## CLASS 8[Extracts attachments from .pptx files] => PptxAttachmentsExtractor
## @usecases
## - [__init__]: CodeAgent (Import) => ImportExtractor => GetExtractorInstance
def _module_contract():
    pass
# endregion MODULE_CONTRACT
# GREP_SUMMARY: attachments, extractors, docx, xlsx, pptx, pdf, json, abstract, office, package_init
# STRUCTURE: ▶ Import ┌all extractor classes┐ → ○ __all__ ← [...7 symbols] → ⎋

from .abstract_attachment_extractor import AbstractAttachmentsExtractor
from .concrete_attachments_extractors.abstract_office_attachments_extractor import AbstractOfficeAttachmentsExtractor
from .concrete_attachments_extractors.docx_attachments_extractor import DocxAttachmentsExtractor
from .concrete_attachments_extractors.excel_attachments_extractor import ExcelAttachmentsExtractor
from .concrete_attachments_extractors.json_attachment_extractor import JsonAttachmentsExtractor
from .concrete_attachments_extractors.pdf_attachments_extractor import PDFAttachmentsExtractor
from .concrete_attachments_extractors.pptx_attachments_extractor import PptxAttachmentsExtractor

__all__ = ['AbstractAttachmentsExtractor', 'AbstractOfficeAttachmentsExtractor', 'DocxAttachmentsExtractor', 'ExcelAttachmentsExtractor',
           'JsonAttachmentsExtractor', 'PDFAttachmentsExtractor', 'PptxAttachmentsExtractor']
