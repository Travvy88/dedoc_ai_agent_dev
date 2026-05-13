# region MODULE_CONTRACT [DOMAIN(8): DocumentProcessing, MetadataExtraction; CONCEPT(8): AbstractFactory, PluginArchitecture; TECH(7): PythonABC]
## @modulecontract
## @purpose To define the abstract base class for all metadata extractors, establishing the plugin contract (can_extract + extract) that every format-specific extractor must implement.
## @scope Abstract extractor interface, file-name resolution, format-matching logic.
## @input Constructor: config dict, recognized_extensions set, recognized_mimes set.
## @output Abstract contract consumed by MetadataExtractorComposition and concrete extractors.
## @links [USES_API(6): os.path, dedoc.utils.get_mime_extension]
## @invariants
## - AbstractMetadataExtractor is never instantiated directly (ABC).
## - can_extract checks BOTH extension AND mime before returning bool.
## - _get_names always returns a 4-tuple (dir, name, converted_name, original_name).
## @rationale
## Q: Why use Abstract Base Class with abstractmethod extract?
## A: Enforces Liskov substitution — every extractor in the composition pipeline exposes the same extract() signature, regardless of format.
## @changes
## LAST_CHANGE: [v1.0.0 — Semantic template markup and LDD logging added.]
## @modulemap
## CLASS 10[Abstract base for all metadata extractors] => AbstractMetadataExtractor
## @usecases
## - [AbstractMetadataExtractor]: MetadataExtractorComposition → IterateExtractors → can_extract? → extract
def _module_contract():
    pass
# endregion MODULE_CONTRACT
# GREP_SUMMARY: abstract, metadata, extractor, ABC, plugin, interface, can_extract, format-matching, MIME
# STRUCTURE: ▶ CLASS AbstractMetadataExtractor: ■ __init__ ┌config, extensions, mimes┐ → ◇ can_extract ┌file_path, mime, extension┐ → ⚡ extract(abstract) → ◇ _get_names ┌os.path.split → 4-tuple┐

from abc import ABC, abstractmethod
from typing import Optional, Set, Tuple


# region CLASS_AbstractMetadataExtractor [DOMAIN(8): DocumentProcessing, MetadataExtraction; CONCEPT(8): AbstractFactory, PluginArchitecture; TECH(7): PythonABC]
## @purpose To serve as the abstract contract for all metadata extractors — any format-specific subclass must implement extract() and may override can_extract().
class AbstractMetadataExtractor(ABC):
    # region METHOD_init [DOMAIN(7): Configuration; CONCEPT(6): Constructor; TECH(5): PythonDefaults]
    ## @purpose To initialize the extractor with format recognition rules (extensions, mimes) and a logger from configuration.
    ## @uses logging (stdlib)
    ## @io Optional[dict] × Optional[Set] × Optional[Set] -> None
    ## @complexity 3
    def __init__(self, *, config: Optional[dict] = None, recognized_extensions: Optional[Set[str]] = None, recognized_mimes: Optional[Set[str]] = None) -> None:
        import logging

        self.config = {} if config is None else config
        self.logger = self.config.get("logger", logging.getLogger())
        self._recognized_extensions = {} if recognized_extensions is None else recognized_extensions
        self._recognized_mimes = {} if recognized_mimes is None else recognized_mimes
        self.logger.debug(f"[IMP:4][AbstractMetadataExtractor][INIT] Extensions={len(self._recognized_extensions)} Types, MIMEs={len(self._recognized_mimes)} Types")
    # endregion METHOD_init

    # region METHOD_can_extract [DOMAIN(7): FormatMatching; CONCEPT(7): CapabilityCheck; TECH(6): os.path, MIME]
    ## @purpose To determine whether this extractor can handle a given file by checking its extension and MIME type against supported sets.
    ## @uses os.path, dedoc.utils.get_mime_extension
    ## @io str × Optional[str] × Optional[str] × Optional[dict] × Optional[str] × Optional[str] -> bool
    ## @complexity 5
    def can_extract(self,
                    file_path: str,
                    converted_filename: Optional[str] = None,
                    original_filename: Optional[str] = None,
                    parameters: Optional[dict] = None,
                    mime: Optional[str] = None,
                    extension: Optional[str] = None) -> bool:
        """
        Check if this extractor can handle the given file.

        :param file_path: path to the file to extract metadata. \
        If dedoc manager is used, the file gets a new name during processing - this name should be passed here (for example 23141.doc)
        :param converted_filename: name of the file after renaming and conversion (if dedoc manager is used, for example 23141.docx), \
        by default it's a name from the file_path. Converted file should be located in the same directory as the file before converting.
        :param original_filename: name of the file before renaming (if dedoc manager is used), by default it's a name from the file_path
        :param parameters: additional parameters for document parsing, see :ref:`parameters_description` for more details
        :param mime: MIME type of a file
        :param extension: file extension, for example .doc or .pdf
        :return: True if the extractor can handle the given file and False otherwise
        """
        import os
        from dedoc.utils.utils import get_mime_extension

        file_dir, file_name, converted_filename, original_filename = self._get_names(file_path, converted_filename, original_filename)
        converted_file_path = os.path.join(file_dir, converted_filename)
        mime, extension = get_mime_extension(file_path=converted_file_path, mime=mime, extension=extension)
        can_handle = extension.lower() in self._recognized_extensions or mime in self._recognized_mimes
        self.logger.debug(f"[IMP:5][AbstractMetadataExtractor][CAN_EXTRACT] File={file_name}, mime={mime}, extension={extension}, can_extract={can_handle}")
        return can_handle
    # endregion METHOD_can_extract

    # region METHOD_extract [DOMAIN(8): MetadataExtraction; CONCEPT(8): AbstractContract; TECH(6): PythonABC]
    ## @purpose To define the contract for metadata extraction — subclasses must implement this to return document-specific metadata.
    ## @uses None
    ## @io str × Optional[str] × Optional[str] × Optional[dict] -> dict
    ## @complexity 1
    @abstractmethod
    def extract(self,
                file_path: str,
                converted_filename: Optional[str] = None,
                original_filename: Optional[str] = None,
                parameters: Optional[dict] = None) -> dict:
        """
        Extract metadata from file if possible, i.e. method :meth:`can_extract` returned True.

        :param file_path: path to the file to extract metadata. \
        If dedoc manager is used, the file gets a new name during processing - this name should be passed here (for example 23141.doc)
        :param converted_filename: name of the file after renaming and conversion (if dedoc manager is used, for example 23141.docx), \
        by default it's a name from the file_path. Converted file should be located in the same directory as the file before converting.
        :param original_filename: name of the file before renaming (if dedoc manager is used), by default it's a name from the file_path
        :param parameters: additional parameters for document parsing, see :ref:`parameters_description` for more details
        :return: dict with metadata information about the document
        """
        pass
    # endregion METHOD_extract

    # region METHOD_get_names [DOMAIN(6): FileResolution; CONCEPT(5): NameNormalization; TECH(5): os.path]
    ## @purpose To resolve and normalize the file path into a consistent 4-tuple: (directory, raw_name, converted_name, original_name).
    ## @uses os.path
    ## @io str × Optional[str] × Optional[str] -> Tuple[str, str, str, str]
    ## @complexity 3
    def _get_names(self, file_path: str, converted_filename: Optional[str], original_filename: Optional[str]) -> Tuple[str, str, str, str]:
        import os

        file_dir, file_name = os.path.split(file_path)
        converted_filename = file_name if converted_filename is None else converted_filename
        original_filename = file_name if original_filename is None else original_filename
        self.logger.debug(f"[IMP:4][AbstractMetadataExtractor][GET_NAMES] dir={file_dir}, raw={file_name}, converted={converted_filename}, original={original_filename}")
        return file_dir, file_name, converted_filename, original_filename
    # endregion METHOD_get_names
# endregion CLASS_AbstractMetadataExtractor
