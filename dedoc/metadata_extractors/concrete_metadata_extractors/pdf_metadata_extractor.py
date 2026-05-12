# region MODULE_CONTRACT [DOMAIN(8): DocumentProcessing, MetadataExtraction; CONCEPT(7): PDFFormat, DocumentInfo; TECH(7): pypdf]
## @modulecontract
## @purpose To extract metadata from PDF documents — reads document info dictionary (author, title, subject, producer, creation/modification dates) via pypdf and merges with base file metadata.
## @scope PDF metadata: document information dictionary, producer, creator, author, title, dates.
## @input file_path via extract(), config with recognized PDF formats.
## @output dict merging BaseMetadataExtractor fields + PDF document info fields (producer, creator, author, title, subject, keywords, creation_date, modification_date).
## @links [USES_API(8): BaseMetadataExtractor, pypdf.PdfReader, dedoc.utils.convert_datetime]
## @invariants
## - _get_pdf_info NEVER raises — on PdfReadError or general Exception returns {"broken_pdf": True} (unless debug_mode is on).
## - __prettify_metadata filters out empty-string values and unmapped keys.
## @rationale
## Q: Why use pypdf instead of PyPDF2 or pdfplumber?
## A: pypdf is the actively maintained successor to PyPDF2 and provides a clean metadata dictionary via PdfReader.metadata with minimal overhead.
## @changes
## LAST_CHANGE: [v1.0.0 — Semantic template markup and LDD logging added.]
## @modulemap
## CLASS 8[PDF metadata extractor with document info] => PdfMetadataExtractor
## @usecases
## - [PdfMetadataExtractor]: MetadataExtractorComposition → ExtractPDF → MergeBaseAndPdfInfo → MetadataDict
def _module_contract():
    pass
# endregion MODULE_CONTRACT
# GREP_SUMMARY: pdf, metadata, pypdf, document info, producer, author, title, creation date, PdfReader
# STRUCTURE: ▶ CLASS PdfMetadataExtractor(ABC): ■ __init__ ┌pdf_keys + base_extractor┐ → ⚡ extract ┌base ⊕ pdf_fields┐ → _get_pdf_info ┌PdfReader.metadata → prettify┐ → __prettify_metadata ┌filter empty + convert dates┐

from typing import Optional

from dedoc.metadata_extractors.abstract_metadata_extractor import AbstractMetadataExtractor
from dedoc.metadata_extractors.concrete_metadata_extractors.base_metadata_extractor import BaseMetadataExtractor


# region CLASS_PdfMetadataExtractor [DOMAIN(8): DocumentProcessing, MetadataExtraction; CONCEPT(7): PDFFormat, DocumentInfo; TECH(7): pypdf]
## @purpose To extract PDF document metadata (author, title, dates, etc.) via pypdf and merge with base OS file metadata.
class PdfMetadataExtractor(AbstractMetadataExtractor):
    # region METHOD_init [DOMAIN(7): Configuration; CONCEPT(6): Constructor, KeyMapping; TECH(6): PythonDicts]
    ## @purpose To register PDF-format extensions/MIMEs, define PDF metadata key mappings, and instantiate a BaseMetadataExtractor delegate.
    ## @uses dedoc.extensions, BaseMetadataExtractor
    ## @io Optional[dict] -> None
    ## @complexity 4
    def __init__(self, *, config: Optional[dict] = None) -> None:
        from dedoc.extensions import recognized_extensions, recognized_mimes
        super().__init__(config=config, recognized_extensions=recognized_extensions.pdf_like_format, recognized_mimes=recognized_mimes.pdf_like_format)
        self.base_extractor = BaseMetadataExtractor(config=config)
        self.keys = {
            "/Producer": "producer",
            "/Creator": "creator",
            "/Author": "author",
            "/Title": "title",
            "/Subject": "subject",
            "/Keywords": "keywords"
        }
        self.keys_date = {
            "/CreationDate": "creation_date",
            "/ModDate": "modification_date",
        }
        self.logger.debug(f"[IMP:4][PdfMetadataExtractor][INIT] PDF keys: {len(self.keys)} string fields, {len(self.keys_date)} date fields")
    # endregion METHOD_init

    # region METHOD_extract [DOMAIN(8): MetadataExtraction; CONCEPT(7): DataMerge; TECH(6): PythonDicts]
    ## @purpose To combine base OS file metadata with PDF document info metadata into a single result dictionary.
    ## @uses BaseMetadataExtractor.extract, _get_pdf_info
    ## @io str × Optional[str] × Optional[str] × Optional[dict] -> dict
    ## @complexity 5
    def extract(self,
                file_path: str,
                converted_filename: Optional[str] = None,
                original_filename: Optional[str] = None,
                parameters: Optional[dict] = None) -> dict:
        """
        Add the predefined list of metadata for the pdf documents.
        Look to the :meth:`~dedoc.metadata_extractors.AbstractMetadataExtractor.extract` documentation to get the information about parameters.
        """
        import os

        file_dir, file_name, converted_filename, original_filename = self._get_names(file_path, converted_filename, original_filename)
        base_fields = self.base_extractor.extract(
            file_path=file_path, converted_filename=converted_filename, original_filename=original_filename, parameters=parameters
        )
        self.logger.debug(f"[IMP:5][PdfMetadataExtractor][BASE_DONE] Base fields: {sorted(base_fields.keys())}")

        pdf_fields = self._get_pdf_info(os.path.join(file_dir, converted_filename))
        self.logger.info(f"[IMP:8][PdfMetadataExtractor][PDF_DONE] PDF fields extracted: {len(pdf_fields)} keys")

        result = {**base_fields, **pdf_fields}
        self.logger.info(f"[IMP:9][PdfMetadataExtractor][RESULT] Total metadata fields: {len(result)}")
        return result
    # endregion METHOD_extract

    # region METHOD_get_pdf_info [DOMAIN(8): PDFParsing; CONCEPT(7): DocumentInfoExtraction; TECH(7): pypdf]
    ## @purpose To open a PDF file with pypdf, read the document info metadata dictionary, and prettify the keys via __prettify_metadata.
    ## @uses pypdf.PdfReader, pypdf.errors.PdfReadError
    ## @io str -> dict
    ## @complexity 6
    def _get_pdf_info(self, path: str) -> dict:
        import os
        from pypdf import PdfReader
        from pypdf.errors import PdfReadError

        try:
            self.logger.debug(f"[IMP:5][PdfMetadataExtractor][OPEN_PDF] Opening PDF: {os.path.basename(path)}")
            with open(path, "rb") as file:
                document = PdfReader(file)
                document_info = document.metadata if document.metadata is not None else {}
                result = self.__prettify_metadata(document_info)
            self.logger.info(f"[IMP:8][PdfMetadataExtractor][PDF_INFO] Metadata fields after prettify: {len(result)}")
            return result
        except PdfReadError:
            self.logger.warning(f"[IMP:9][PdfMetadataExtractor][PDF_READ_ERROR] PdfReadError for file={os.path.basename(path)}")
            return {"broken_pdf": True}
        except Exception as e:
            self.logger.warning(f"[IMP:9][PdfMetadataExtractor][GENERAL_ERROR] Exception extracting PDF metadata: {path} {e}")
            if self.config.get("debug_mode", False):
                raise e
            return {"broken_pdf": True}
    # endregion METHOD_get_pdf_info

    # region METHOD_prettify_metadata [DOMAIN(6): DataNormalization; CONCEPT(6): KeyMapping, DateConversion; TECH(5): PythonDicts]
    ## @purpose To normalize raw PDF metadata keys to human-readable field names and convert date strings to internal format via convert_datetime.
    ## @uses dedoc.utils.convert_datetime
    ## @io dict -> dict
    ## @complexity 5
    def __prettify_metadata(self, document_info: dict) -> dict:
        from dedoc.utils.utils import convert_datetime

        result = {}
        for key, value in document_info.items():
            if isinstance(value, str) and len(value) > 0:
                if key in self.keys:
                    result[self.keys[key]] = value
                elif key in self.keys_date:
                    try:
                        date = convert_datetime(value)
                    except Exception:
                        date = None
                    if date is not None:
                        result[self.keys_date[key]] = date
        return result
    # endregion METHOD_prettify_metadata
# endregion CLASS_PdfMetadataExtractor
