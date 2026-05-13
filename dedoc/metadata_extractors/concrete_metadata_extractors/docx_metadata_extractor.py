# region MODULE_CONTRACT [DOMAIN(8): DocumentProcessing, MetadataExtraction; CONCEPT(7): DOCXFormat, CoreProperties; TECH(7): python-docx]
## @modulecontract
## @purpose To extract rich metadata from DOCX documents — reads core properties (author, dates, keywords, etc.) via python-docx and merges them with base OS metadata.
## @scope DOCX file metadata: core properties, subject, keywords, author, dates.
## @input file_path via extract(), config with recognized formats.
## @output dict merging BaseMetadataExtractor fields + DOCX-specific core properties (document_subject, keywords, category, comments, author, last_modified_by, created_date, modified_date, last_printed_date).
## @links [USES_API(8): BaseMetadataExtractor, python-docx Document.core_properties]
## @invariants
## - extract() ALWAYS returns a dict with base metadata merged.
## - On PackageNotFoundError, returns {"broken_docx": True} instead of raising.
## @rationale
## Q: Why use BaseMetadataExtractor as a delegate instead of inheritance?
## A: Composition allows combining base file metadata with format-specific properties without coupling the DOCX extractor to os.stat internals.
## @changes
## LAST_CHANGE: [v1.0.0 — Semantic template markup and LDD logging added.]
## @modulemap
## CLASS 8[DOCX metadata extractor with core properties] => DocxMetadataExtractor
## @usecases
## - [DocxMetadataExtractor]: MetadataExtractorComposition → ExtractDOCX → MergeBaseAndDocx → MetadataDict
def _module_contract():
    pass
# endregion MODULE_CONTRACT
# GREP_SUMMARY: docx, word, metadata, core properties, author, keywords, python-docx, dates, OOXML
# STRUCTURE: ▶ CLASS DocxMetadataExtractor(ABC): ■ __init__ ┌docx_ext + mimes + base_extractor┐ → ⚡ extract ┌base_fields ⊕ docx_fields┐ → _get_docx_fields ┌python-docx Document.core_properties → dict┐ → __convert_date ┌datetime → int ts┐

from datetime import datetime
from typing import Optional

from dedoc.metadata_extractors.abstract_metadata_extractor import AbstractMetadataExtractor
from dedoc.metadata_extractors.concrete_metadata_extractors.base_metadata_extractor import BaseMetadataExtractor


# region CLASS_DocxMetadataExtractor [DOMAIN(8): DocumentProcessing, MetadataExtraction; CONCEPT(7): DOCXFormat, CoreProperties; TECH(7): python-docx]
## @purpose To extract DOCX-specific metadata by reading OOXML core properties (author, dates, keywords, etc.) and merging with base file metadata.
class DocxMetadataExtractor(AbstractMetadataExtractor):
    # region METHOD_init [DOMAIN(7): Configuration; CONCEPT(6): Constructor; TECH(5): PythonDefaults]
    ## @purpose To register the format (DOCX extensions and MIMEs) and instantiate a BaseMetadataExtractor delegate for base-level metadata.
    ## @uses dedoc.extensions, BaseMetadataExtractor
    ## @io Optional[dict] -> None
    ## @complexity 4
    def __init__(self, *, config: Optional[dict] = None) -> None:
        from dedoc.extensions import recognized_extensions, recognized_mimes

        super().__init__(config=config, recognized_extensions=recognized_extensions.docx_like_format, recognized_mimes=recognized_mimes.docx_like_format)
        self.base_extractor = BaseMetadataExtractor(config=config)
        self.logger.debug(f"[IMP:4][DocxMetadataExtractor][INIT] DOCX extractor initialized with base_extractor delegate")
    # endregion METHOD_init

    # region METHOD_extract [DOMAIN(8): MetadataExtraction; CONCEPT(7): DataMerge; TECH(6): PythonDicts]
    ## @purpose To collect base OS metadata and DOCX-specific core properties, merging them into a single result dictionary.
    ## @uses BaseMetadataExtractor.extract, _get_docx_fields
    ## @io str × Optional[str] × Optional[str] × Optional[dict] -> dict
    ## @complexity 5
    def extract(self,
                file_path: str,
                converted_filename: Optional[str] = None,
                original_filename: Optional[str] = None,
                parameters: Optional[dict] = None) -> dict:
        """
        Add the predefined list of metadata for the docx documents.
        Look to the :meth:`~dedoc.metadata_extractors.AbstractMetadataExtractor.extract` documentation to get the information about parameters.
        """
        import os

        parameters = {} if parameters is None else parameters
        file_dir, file_name, converted_filename, original_filename = self._get_names(file_path, converted_filename, original_filename)

        base_fields = self.base_extractor.extract(
            file_path=file_path, converted_filename=converted_filename, original_filename=original_filename, parameters=parameters
        )
        self.logger.debug(f"[IMP:5][DocxMetadataExtractor][BASE_DONE] Base fields collected: {sorted(base_fields.keys())}")

        docx_fields = self._get_docx_fields(os.path.join(file_dir, converted_filename))
        self.logger.info(f"[IMP:8][DocxMetadataExtractor][DOCX_DONE] DOCX fields collected: {sorted(docx_fields.keys())}")

        result = {**base_fields, **docx_fields}
        self.logger.info(f"[IMP:9][DocxMetadataExtractor][RESULT] Total metadata fields: {len(result)}")
        return result
    # endregion METHOD_extract

    # region METHOD_convert_date [DOMAIN(5): DateTime; CONCEPT(5): TimestampConversion; TECH(4): PythonDatetime]
    ## @purpose To convert an optional datetime to a Unix timestamp integer — None-safe helper for core property date fields.
    ## @uses datetime.timestamp
    ## @io Optional[datetime] -> Optional[int]
    ## @complexity 2
    def __convert_date(self, date: Optional[datetime]) -> Optional[int]:
        return None if date is None else int(date.timestamp())
    # endregion METHOD_convert_date

    # region METHOD_get_docx_fields [DOMAIN(8): DocumentProcessing; CONCEPT(7): CorePropertiesExtraction; TECH(7): python-docx]
    ## @purpose To open a DOCX document with python-docx and extract all standard core properties (subject, author, dates, etc.) into a dictionary.
    ## @uses docx.Document, docx.opc.exceptions.PackageNotFoundError
    ## @io str -> dict
    ## @complexity 6
    def _get_docx_fields(self, file_path: str) -> dict:
        import docx
        from docx.opc.exceptions import PackageNotFoundError
        import os

        self.logger.debug(f"[IMP:5][DocxMetadataExtractor][OPEN_DOCX] Opening file={os.path.basename(file_path)}")
        assert os.path.isfile(file_path)
        try:
            doc = docx.Document(file_path)
            properties = doc.core_properties
            parameters = {
                "document_subject": properties.subject,
                "keywords": properties.keywords,
                "category": properties.category,
                "comments": properties.comments,
                "author": properties.author,
                "last_modified_by": properties.last_modified_by,
                "created_date": self.__convert_date(properties.created),
                "modified_date": self.__convert_date(properties.modified),
                "last_printed_date": self.__convert_date(properties.last_printed),
            }
            self.logger.info(f"[IMP:8][DocxMetadataExtractor][CORE_PROPS] Author={parameters.get('author')}, created={parameters.get('created_date')}")
            return parameters
        except PackageNotFoundError:
            self.logger.warning(f"[IMP:9][DocxMetadataExtractor][BROKEN] PackageNotFoundError for file={os.path.basename(file_path)}")
            return {"broken_docx": True}
    # endregion METHOD_get_docx_fields
# endregion CLASS_DocxMetadataExtractor
