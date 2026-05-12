# region MODULE_CONTRACT [DOMAIN(8): DocumentProcessing; CONCEPT(7): OfficeFormats; TECH(6): zipfile, BeautifulSoup]
## @modulecontract
## @purpose To extract and parse XML content from Office Open XML format files (docx, pptx, xlsx) via zipfile + BeautifulSoup, serving as a shared utility for Office format readers.
## @scope ZIP archive XML extraction, whitespace normalization, BeautifulSoup tree construction.
## @input Path to office format file, internal XML path.
## @output BeautifulSoup XML tree or None if the file is not found inside the archive.
## @links [USES_API(7): zipfile, BeautifulSoup]
## @links_to_spec REQ-OFFICE-001
## @invariants
## - Returns None for missing internal XML paths without raising.
## - Raises BadFileFormatError on corrupted ZIP archives.
## @rationale
## Q: Why remove whitespace between XML tags?
## A: Office XML files often contain formatting whitespace that interferes with BeautifulSoup parsing. Pre-cleaning yields cleaner parse trees.
## @changes
## LAST_CHANGE: [v1.0.0 – Added SEMANTIC TEMPLATE markup and LDD logging]
## @modulemap
## FUNC 8[XML extraction from Office ZIP] => get_bs_from_zip
## @usecases
## - [get_bs_from_zip]: DocxReader → ExtractDocumentXML → BeautifulSoup tree for parsing
def _module_contract():
    pass
# endregion MODULE_CONTRACT
# GREP_SUMMARY: Office, docx, pptx, xlsx, zipfile, XML, BeautifulSoup, extraction
# STRUCTURE: ▶ ┌zip_path, xml_path┐ → ○ ZipFile.open(xml_path) → re.sub whitespace → BeautifulSoup(content,"xml") ∨ (KeyError → None, BadZipFile → raise BadFileFormatError) → ⎋ BeautifulSoup|None

import logging
import os
import re
import zipfile
from typing import Optional

from bs4 import BeautifulSoup

from dedoc.common.exceptions.bad_file_error import BadFileFormatError

logger = logging.getLogger(__name__)


# region FUNC_get_bs_from_zip [DOMAIN(8): DocumentProcessing; CONCEPT(7): OfficeFormats; TECH(7): zipfile, BeautifulSoup]
## @purpose To extract a specific XML file from an Office Open XML archive and parse it into a BeautifulSoup tree, with optional inter-tag whitespace removal for pptx.
## @uses zipfile, re, BeautifulSoup, BadFileFormatError
## @io (str, str, bool) -> Optional[BeautifulSoup]
## @complexity 6
def get_bs_from_zip(zip_path: str, xml_path: str, remove_spaces: bool = False) -> Optional[BeautifulSoup]:
    logger.debug(f"[IMP:5][get_bs_from_zip][INIT] Extracting {xml_path} from {zip_path}")
    try:
        with zipfile.ZipFile(zip_path) as document:
            content = document.read(xml_path)
            content = re.sub(br"\n[\t ]*", b"", content)

            if remove_spaces:
                content = re.sub(br"(?<!<a:t)>\s+<", b"><", content)

            soup = BeautifulSoup(content, "xml")
            logger.info(f"[IMP:7][get_bs_from_zip][SUCCESS] Parsed {xml_path} from {os.path.basename(zip_path)}")
            return soup
    except KeyError:
        logger.debug(f"[IMP:5][get_bs_from_zip][MISSING] {xml_path} not found in {zip_path}")
        return None
    except zipfile.BadZipFile:
        logger.error(f"[IMP:9][get_bs_from_zip][CORRUPT] Bad office file: {os.path.basename(zip_path)}")
        raise BadFileFormatError(f"Bad office file:\n file_name = {os.path.basename(zip_path)}. Seems file is broken")
# endregion FUNC_get_bs_from_zip
