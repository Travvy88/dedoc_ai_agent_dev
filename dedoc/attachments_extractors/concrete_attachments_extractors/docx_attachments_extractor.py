# region MODULE_CONTRACT [DOMAIN(8): DocumentProcessing; CONCEPT(8): AttachmentExtraction; TECH(8): docx, OpenXML, ZIP, BeautifulSoup]
## @modulecontract
## @purpose Extract attachments from .docx files: OLE objects from word/ folder, plus diagram extraction (each diagram paragraph becomes a separate .docx attachment via BeautifulSoup reconstruction).
## @scope docx attachment extraction: ZIP traversal, diagram isolation via BeautifulSoup XML parsing, OLE stream handling via base class.
## @input File path to .docx document; optional parameters dict.
## @output List of AttachedFile objects (images, OLE objects from word/; reconstructed diagram .docx files).
## @links [USES_API(9): AbstractOfficeAttachmentsExtractor._get_attachments, AbstractAttachmentsExtractor._content2attach_file]
## @links [USES_API(8): BeautifulSoup (bs4), zipfile.ZipFile, hashlib]
## @links [USES_API(7): dedoc.utils.parameter_utils.get_param_need_content_analysis]
## @links [USES_API(6): BadFileFormatError (dedoc.common.exceptions)]
## @invariants
## - extract ALWAYS returns a List[AttachedFile] (may be empty).
## - BadZipFile is caught and re-raised as BadFileFormatError with a descriptive message.
## - Diagram extraction is attempted first; word/ attachments are added second.
## @rationale
## Q: Why extract diagrams as separate .docx files?
## A: Docx diagram paragraphs contain embedded drawing data. Reconstructing each diagram paragraph as its own .docx allows downstream parsers to handle each diagram independently, providing better document structure.
## Q: Why read word/document.xml first, falling back to word/document2.xml?
## A: Some docx variants (older templates) use document2.xml as the main body. The fallback ensures compatibility.
## @changes
## LAST_CHANGE: [v1.0.0 – Semantic markup + LDD logging added]
## @modulemap
## CLASS 9[Extracts attachments from .docx files] => DocxAttachmentsExtractor
## METHOD 5[Constructor: registers recognized docx extensions/mimes] => __init__
## METHOD 9[Main extraction: diagrams + word/ attachments] => extract
## METHOD 8[Extracts diagram paragraphs as individual .docx files] => __extract_diagrams
## @usecases
## - [extract]: DedocManager => ExtractDocxAttachments => List[AttachedFile]
def _module_contract():
    pass
# endregion MODULE_CONTRACT
# GREP_SUMMARY: docx, word, attachments, extractor, diagrams, BeautifulSoup, XML, ZIP, OLE, document.xml, document2.xml, BadFileFormatError
# STRUCTURE: ▶ Init ┌recognized docx extensions/mimes┐ → ⚡ extract(file_path) → ○ try: ZipFile → ◇ __extract_diagrams(zfile) → ⊕ diagram attachments → ◇ _get_attachments(attachments_dir="word") → ⊕ word/ attachments → ∑ ↔ catch BadZipFile→BadFileFormatError → ⎋ List[AttachedFile]; ◇ __extract_diagrams → ⚡ read document.xml → BeautifulSoup → ○ ∀paragraph with <pict>: extract→rebuild .docx→⊕ attachment → ⎋

from typing import List, Optional
from zipfile import BadZipFile, ZipFile

from dedoc.attachments_extractors.concrete_attachments_extractors.abstract_office_attachments_extractor import AbstractOfficeAttachmentsExtractor
from dedoc.common.exceptions.bad_file_error import BadFileFormatError
from dedoc.data_structures.attached_file import AttachedFile

import logging

logger = logging.getLogger(__name__)


# region CLASS_DocxAttachmentsExtractor [DOMAIN(8): DocumentProcessing; CONCEPT(8): AttachmentExtraction; TECH(8): docx, OpenXML]
## @purpose Extract attachments from .docx files: OLE objects and reconstructed diagram paragraphs.
class DocxAttachmentsExtractor(AbstractOfficeAttachmentsExtractor):
    # region METHOD___init__ [DOMAIN(8): DocumentProcessing; CONCEPT(5): Initialization; TECH(4): PythonConfig]
    ## @purpose Initialize the docx extractor with recognized docx-like file extensions and MIME types.
    ## @uses dedoc.extensions.recognized_extensions, dedoc.extensions.recognized_mimes
    ## @io Optional[dict] -> None
    ## @complexity 2
    def __init__(self, *, config: Optional[dict] = None) -> None:
        from dedoc.extensions import recognized_extensions, recognized_mimes
        super().__init__(config=config, recognized_extensions=recognized_extensions.docx_like_format, recognized_mimes=recognized_mimes.docx_like_format)
        logger.debug(f"[IMP:4][DocxAttachmentsExtractor][INIT] Initialized with docx-like format recognition")
    # endregion METHOD___init__

    # region METHOD_extract [DOMAIN(9): DocumentProcessing; CONCEPT(9): AttachmentExtraction; TECH(8): zipfile, docx]
    ## @purpose Extract all attachments from a .docx file: first extract diagram paragraphs as separate .docx files, then collect word/ media and OLE objects.
    ## @uses __extract_diagrams, AbstractOfficeAttachmentsExtractor._get_attachments, AbstractAttachmentsExtractor._content2attach_file
    ## @io str, Optional[dict] -> List[AttachedFile]
    ## @complexity 7
    def extract(self, file_path: str, parameters: Optional[dict] = None) -> List[AttachedFile]:
        import os
        from dedoc.utils.parameter_utils import get_param_need_content_analysis

        parameters = {} if parameters is None else parameters
        tmpdir, filename = os.path.split(file_path)
        result = []
        logger.debug(f"[IMP:6][DocxAttachmentsExtractor][EXTRACT] Extracting from docx: {filename}")
        try:
            with ZipFile(os.path.join(tmpdir, filename), "r") as zfile:
                diagram_attachments = self.__extract_diagrams(zfile)
                logger.info(f"[IMP:7][DocxAttachmentsExtractor][EXTRACT] Extracted {len(diagram_attachments)} diagram attachments")
                need_content_analysis = get_param_need_content_analysis(parameters)
                result += self._content2attach_file(content=diagram_attachments, tmpdir=tmpdir, need_content_analysis=need_content_analysis,
                                                    parameters=parameters)

            result += self._get_attachments(tmpdir=tmpdir, filename=filename, parameters=parameters, attachments_dir="word")
            logger.info(f"[IMP:9][DocxAttachmentsExtractor][EXTRACT] Total attachments extracted from {filename}: {len(result)}")

        except BadZipFile:
            logger.critical(f"[IMP:10][DocxAttachmentsExtractor][EXTRACT] BadZipFile for {filename}")
            raise BadFileFormatError(f"Bad docx file:\n file_name = {filename}. Seems docx is broken")
        return result
    # endregion METHOD_extract

    # region METHOD___extract_diagrams [DOMAIN(8): DocumentProcessing; CONCEPT(8): DiagramExtraction; TECH(8): BeautifulSoup, XML, zipfile]
    ## @purpose Parse docx XML to isolate diagram paragraphs (containing <pict> elements), reconstruct each as a standalone .docx file with the full zip context.
    ## @uses BeautifulSoup (bs4), hashlib.md5, tempfile.TemporaryDirectory, zipfile.ZipFile
    ## @io ZipFile -> List[Tuple[str, bytes]]
    ## @complexity 9
    def __extract_diagrams(self, document: ZipFile) -> List[tuple]:
        import hashlib
        import os
        import re
        import tempfile
        from bs4 import BeautifulSoup, Tag

        result = []
        logger.debug(f"[IMP:6][DocxAttachmentsExtractor][EXTRACT_DIAGRAMS] Starting diagram extraction")
        try:
            content = document.read("word/document.xml")
        except KeyError:
            content = document.read("word/document2.xml")
            logger.debug(f"[IMP:5][DocxAttachmentsExtractor][EXTRACT_DIAGRAMS] Fallback to document2.xml")

        content = re.sub(br"\n[\t ]*", b"", content)
        bs = BeautifulSoup(content, "xml")

        paragraphs = [p for p in bs.body]
        diagram_paragraphs = []
        for paragraph in paragraphs:
            if not isinstance(paragraph, Tag):
                continue

            extracted = paragraph.extract()
            if extracted.pict:
                diagram_paragraphs.append(extracted)
        if not diagram_paragraphs:
            logger.debug(f"[IMP:5][DocxAttachmentsExtractor][EXTRACT_DIAGRAMS] No diagram paragraphs found")
            return result

        logger.info(f"[IMP:7][DocxAttachmentsExtractor][EXTRACT_DIAGRAMS] Found {len(diagram_paragraphs)} diagram paragraphs")

        with tempfile.TemporaryDirectory() as tmpdir:
            document.extractall(tmpdir)
            namelist = document.namelist()

            for p in diagram_paragraphs:
                bs.body.insert(1, p)
                doc_text = str(bs)
                paragraph = p.extract()
                uid = hashlib.md5(paragraph.encode()).hexdigest()

                with open(f"{tmpdir}/word/document.xml", "w") as f:
                    f.write(doc_text)
                diagram_name = f"{uid}.docx"
                with ZipFile(os.path.join(tmpdir, diagram_name), mode="w") as new_d:
                    for filename in namelist:
                        new_d.write(os.path.join(tmpdir, filename), arcname=filename)
                with open(os.path.join(tmpdir, diagram_name), "rb") as f:
                    result.append((diagram_name, f.read()))
                logger.debug(f"[IMP:5][DocxAttachmentsExtractor][EXTRACT_DIAGRAMS] Reconstructed diagram: {diagram_name}")

        logger.info(f"[IMP:9][DocxAttachmentsExtractor][EXTRACT_DIAGRAMS] Total diagram .docx files constructed: {len(result)}")
        return result
    # endregion METHOD___extract_diagrams
# endregion CLASS_DocxAttachmentsExtractor
