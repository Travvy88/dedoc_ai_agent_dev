# region MODULE_CONTRACT [DOMAIN(8): DocumentProcessing; CONCEPT(7): PDF; TECH(7): pypdf, pdf2image]
## @modulecontract
## @purpose To provide PDF-specific utilities for page counting and page-to-image conversion, enabling the Dedoc pipeline to extract visual representations of PDF pages.
## @scope PDF page count retrieval, PDF page image rendering.
## @input File path to PDF document, page index.
## @output Page count (int), page image (PIL.Image).
## @links [USES_API(8): pypdf, pdf2image]
## @invariants
## - get_pdf_page_count returns None (not raises) on unreadable PDFs.
## - get_page_image returns None if no images rendered for the given page.
## @rationale
## Q: Why use pypdf instead of PyPDF2?
## A: pypdf is the actively maintained successor with better error handling.
## @changes
## LAST_CHANGE: [v1.0.0 – Added SEMANTIC TEMPLATE markup and LDD logging]
## @modulemap
## FUNC 7[PDF page count] => get_pdf_page_count
## FUNC 8[PDF page to PIL image] => get_page_image
## @usecases
## - [get_pdf_page_count]: Reader → AssessDocumentLength → Page count reported
## - [get_page_image]: StructureExtractor → ExtractVisualFeatures → Page image rendered
def _module_contract():
    pass
# endregion MODULE_CONTRACT
# GREP_SUMMARY: PDF, page count, page image, pypdf, pdf2image, PIL, rendering
# STRUCTURE: ▶ ┌Library imports┐ → ⚡ get_pdf_page_count: ┌path┐ → 〈PdfReader → len(pages)〉 ∨ None → ⎋ count; ⚡ get_page_image: ┌path, page_id┐ → 〈convert_from_path → images[0]〉 ∨ None → ⎋ Image

import logging
from typing import Optional

from PIL.Image import Image

logger = logging.getLogger(__name__)


# region FUNC_get_pdf_page_count [DOMAIN(8): DocumentProcessing; CONCEPT(7): PDF; TECH(7): pypdf]
## @purpose To determine the number of pages in a PDF file, returning None on failure rather than raising an exception for graceful error handling.
## @uses pypdf.PdfReader
## @io str -> Optional[int]
## @complexity 4
def get_pdf_page_count(path: str) -> Optional[int]:
    from pypdf import PdfReader
    try:
        reader = PdfReader(path)
        count = len(reader.pages)
        logger.info(f"[IMP:7][get_pdf_page_count][RESULT] PDF {path}: {count} pages")
        return count
    except Exception:
        logger.warning(f"[IMP:8][get_pdf_page_count][FAIL] Cannot read page count for {path}")
        return None
# endregion FUNC_get_pdf_page_count


# region FUNC_get_page_image [DOMAIN(8): DocumentProcessing; CONCEPT(8): PDF; TECH(7): pdf2image]
## @purpose To render a specific PDF page as a PIL Image, used for visual feature extraction in document structure analysis.
## @uses pdf2image.convert_from_path
## @io (str, int) -> Optional[Image]
## @complexity 5
def get_page_image(path: str, page_id: int) -> Optional[Image]:
    from pdf2image import convert_from_path

    logger.debug(f"[IMP:5][get_page_image][RENDER] Rendering page {page_id} from {path}")
    images = convert_from_path(path, first_page=page_id + 1, last_page=page_id + 1)
    if len(images) > 0:
        logger.debug(f"[IMP:5][get_page_image][DONE] Page {page_id} rendered successfully")
        return images[0]
    logger.warning(f"[IMP:7][get_page_image][EMPTY] No image for page {page_id} in {path}")
    return None
# endregion FUNC_get_page_image
