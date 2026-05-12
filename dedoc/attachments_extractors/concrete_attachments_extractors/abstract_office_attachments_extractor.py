# region MODULE_CONTRACT [DOMAIN(8): DocumentProcessing; CONCEPT(9): AttachmentExtraction; TECH(8): OpenXML, OLE, zipfile]
## @modulecontract
## @purpose Provide the abstract foundation for Microsoft Office OpenXML format (docx, xlsx, pptx) attachment extractors: OLE stream parsing, zip-based media/embedding extraction.
## @scope Office-format attachment extraction: ZIP archive traversal, OLE binary stream parsing (Ole10Native, CONTENTS for PDF), media/embedding folder filtering.
## @input File path, binary OLE stream content, zip archive entries.
## @output List of AttachedFile objects (images, PDFs, OLE-native files) extracted from the Office archive.
## @links [USES_API(9): olefile.OleFileIO, charset_normalizer.from_bytes]
## @links [USES_API(8): AbstractAttachmentsExtractor._content2attach_file]
## @links [USES_API(7): dedoc.utils.parameter_utils.get_param_need_content_analysis]
## @invariants
## - _get_attachments ALWAYS returns List[AttachedFile] (may be empty).
## - .emf and .wmf files are always skipped (Windows metafile, not useful downstream).
## - .bin OLE files are parsed for embedded PDF or Ole10Native streams.
## @rationale
## Q: Why abstract instead of concrete?
## A: docx, xlsx, and pptx share identical ZIP+OLE attachment extraction logic; differences are only in the media folder path (word/, xl/, ppt/) passed by subclasses.
## Q: Why manual OLE binary parsing instead of a library?
## A: The Ole10Native binary format is simple (fixed-offset structure); a specialized library adds dependency weight without benefit.
## @changes
## LAST_CHANGE: [v1.0.0 – Semantic markup + LDD logging added]
## @modulemap
## CLASS 9[Abstract base for Office-format attachment extractors] => AbstractOfficeAttachmentsExtractor
## METHOD 5[Constructor: delegates to AbstractAttachmentsExtractor] => __init__
## METHOD 8[Parses Ole10Native binary stream to (filename, bytes)] => __parse_ole_contents
## METHOD 9[Main extraction: traverses ZIP, collects media/embeddings, parses OLE] => _get_attachments
## @usecases
## - [_get_attachments]: DocxAttachmentsExtractor => ExtractOfficeAttachments => List[AttachedFile]
def _module_contract():
    pass
# endregion MODULE_CONTRACT
# GREP_SUMMARY: office, abstract, attachments, OLE, Ole10Native, zipfile, OpenXML, docx, xlsx, pptx, media, embeddings, parse_ole
# STRUCTURE: ▶ Init ┌AbstractAttachmentsExtractor base┐ → ⚡ _get_attachments(tmpdir, filename, attachments_dir) → ○ zipfile read → ◇ filter media/embeddings: 〈.emf/.wmf?skip｜.bin?→OLE parse→PDF/Ole10Native｜read zip bytes〉 → ⊕ content list → ◇ _content2attach_file → ∑ List[AttachedFile] → ⎋

from abc import ABC
from typing import List, Optional, Set, Tuple

from dedoc.attachments_extractors.abstract_attachment_extractor import AbstractAttachmentsExtractor
from dedoc.data_structures.attached_file import AttachedFile

import logging

logger = logging.getLogger(__name__)


# region CLASS_AbstractOfficeAttachmentsExtractor [DOMAIN(8): DocumentProcessing; CONCEPT(9): AttachmentExtraction; TECH(8): OpenXML, OLE]
## @purpose Abstract base class for Office-format (docx, xlsx, pptx) attachment extraction: OLE binary parsing and ZIP-based media collection.
class AbstractOfficeAttachmentsExtractor(AbstractAttachmentsExtractor, ABC):
    # region METHOD___init__ [DOMAIN(8): DocumentProcessing; CONCEPT(5): Initialization; TECH(4): PythonConfig]
    ## @purpose Initialize with config and recognized extensions/mimes, delegating to the parent AbstractAttachmentsExtractor.
    ## @io Optional[dict], Optional[Set[str]], Optional[Set[str]] -> None
    ## @complexity 2
    def __init__(self, *, config: Optional[dict] = None, recognized_extensions: Optional[Set[str]] = None, recognized_mimes: Optional[Set[str]] = None) -> None:
        super().__init__(config=config, recognized_extensions=recognized_extensions, recognized_mimes=recognized_mimes)
        logger.debug(f"[IMP:4][AbstractOfficeAttachmentsExtractor][INIT] Office extractor initialized")
    # endregion METHOD___init__

    # region METHOD___parse_ole_contents [DOMAIN(8): BinaryParsing; CONCEPT(8): OLEParsing; TECH(7): BinaryStream, charset_normalizer]
    ## @purpose Parse the Ole10Native binary stream into the original filename and file contents.
    ## @uses charset_normalizer.from_bytes
    ## @io bytes -> Tuple[str, bytes]
    ## @complexity 8
    def __parse_ole_contents(self, stream: bytes) -> Tuple[str, bytes]:
        from charset_normalizer import from_bytes

        # original filename in ANSI starts at byte 7 and is null terminated
        stream = stream[6:]

        last_name_pos = 0
        for ord_chr in stream:
            if ord_chr == 0:
                break
            last_name_pos += 1

        filename_binary = stream[:last_name_pos]
        dammit = from_bytes(filename_binary)
        filename = filename_binary.decode(encoding=dammit.best().encoding)
        logger.debug(f"[IMP:5][AbstractOfficeAttachmentsExtractor][PARSE_OLE] Decoded filename: {filename}")

        stream = stream[len(filename) + 1:]
        filesize = 0
        # original filepath in ANSI is next and is null terminated
        for ord_chr in stream:
            if ord_chr == 0:
                break
            filesize += 1

        # next 4 bytes are unused
        stream = stream[filesize + 1 + 4:]
        # size of the temporary file path in ANSI in little endian
        temporary_filepath_size = 0
        temporary_filepath_size |= stream[0] << 0
        temporary_filepath_size |= stream[1] << 8
        temporary_filepath_size |= stream[2] << 16
        temporary_filepath_size |= stream[3] << 24
        stream = stream[4 + temporary_filepath_size:]
        size = 0  # size of the contents in little endian
        size |= stream[0] << 0
        size |= stream[1] << 8
        size |= stream[2] << 16
        size |= stream[3] << 24
        stream = stream[4:]
        contents = stream[:size]  # contents
        logger.debug(f"[IMP:5][AbstractOfficeAttachmentsExtractor][PARSE_OLE] Parsed contents size: {size} bytes")
        return filename, contents
    # endregion METHOD___parse_ole_contents

    # region METHOD__get_attachments [DOMAIN(9): DocumentProcessing; CONCEPT(9): AttachmentExtraction; TECH(8): zipfile, olefile]
    ## @purpose Extract all attachments from an Office-format ZIP archive: collect media/embeddings from the specified folder, parse .bin OLE files for embedded PDF or Ole10Native content.
    ## @uses olefile.OleFileIO, AbstractAttachmentsExtractor._content2attach_file
    ## @io str, str, dict, str -> List[AttachedFile]
    ## @complexity 8
    def _get_attachments(self, tmpdir: str, filename: str, parameters: dict, attachments_dir: str) -> List[AttachedFile]:
        import olefile
        import os
        import zipfile
        from dedoc.utils.parameter_utils import get_param_need_content_analysis

        result = []

        logger.debug(f"[IMP:6][AbstractOfficeAttachmentsExtractor][GET_ATTACHMENTS] Extracting from {filename}, attachments_dir={attachments_dir}")

        with zipfile.ZipFile(os.path.join(tmpdir, filename), "r") as zfile:
            files = zfile.namelist()
            attachments = [file for file in files if file.startswith((f"{attachments_dir}/media/", f"{attachments_dir}/embeddings/"))]
            logger.info(f"[IMP:7][AbstractOfficeAttachmentsExtractor][GET_ATTACHMENTS] Found {len(attachments)} candidate attachments in {attachments_dir}/")

            for attachment in attachments:
                original_name = os.path.split(attachment)[-1]

                # these are windows metafile extensions
                if original_name.endswith((".emf", "wmf")):
                    logger.debug(f"[IMP:3][AbstractOfficeAttachmentsExtractor][GET_ATTACHMENTS] Skipping metafile: {original_name}")
                    continue

                if not original_name.endswith(".bin"):
                    result.append((original_name, zfile.read(attachment)))
                    logger.debug(f"[IMP:5][AbstractOfficeAttachmentsExtractor][GET_ATTACHMENTS] Collected: {original_name}")
                else:
                    with zfile.open(attachment) as f:
                        ole = olefile.OleFileIO(f.read())

                    # extracting PDF-files
                    if ole.exists("CONTENTS"):
                        data = ole.openstream("CONTENTS").read()
                        if data[0:5] == b"%PDF-":
                            extracted_name = f"{os.path.splitext(original_name)[-2]}.pdf"
                            result.append((extracted_name, data))
                            logger.info(f"[IMP:8][AbstractOfficeAttachmentsExtractor][GET_ATTACHMENTS] Extracted PDF from OLE: {extracted_name}")

                    # extracting files in other formats
                    elif ole.exists("\x01Ole10Native"):
                        original_name, contents = self.__parse_ole_contents(ole.openstream("\x01Ole10Native").read())
                        result.append((original_name, contents))
                        logger.info(f"[IMP:8][AbstractOfficeAttachmentsExtractor][GET_ATTACHMENTS] Extracted Ole10Native: {original_name}")

                    # TODO process any ole files except \x01Ole10Native and PDF (looks like impossible task)

            need_content_analysis = get_param_need_content_analysis(parameters)
            attachments = self._content2attach_file(content=result, tmpdir=tmpdir, need_content_analysis=need_content_analysis, parameters=parameters)
            logger.info(f"[IMP:9][AbstractOfficeAttachmentsExtractor][GET_ATTACHMENTS] Total attachments from {filename}: {len(attachments)}")
            return attachments
    # endregion METHOD__get_attachments
# endregion CLASS_AbstractOfficeAttachmentsExtractor
