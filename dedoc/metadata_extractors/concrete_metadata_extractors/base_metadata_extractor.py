# region MODULE_CONTRACT [DOMAIN(8): DocumentProcessing, MetadataExtraction; CONCEPT(7): FileAttributes, FallbackExtractor; TECH(6): os.stat]
## @modulecontract
## @purpose To provide a universal fallback metadata extractor that works for ANY file format, returning OS-level file attributes (name, size, timestamps, MIME type) and optional base64 encoding.
## @scope Extracting basic file metadata for all file formats, base64-encoding of file content.
## @input file_path via extract(), optional parameters dict.
## @output dict with keys: file_name, temporary_file_name, file_type, size, access_time, created_time, modified_time, [base64_encode].
## @links [USES_API(7): AbstractMetadataExtractor, os.stat, dedoc.utils.get_file_mime_type]
## @invariants
## - can_extract ALWAYS returns True (universal extractor).
## - _get_base_meta_information ALWAYS calls os.stat and returns a dict with 7 fixed keys.
## @rationale
## Q: Why have a universal extractor that matches everything?
## A: Serves as the safety net in the extraction chain. Even if no format-specific extractor handles a file, BaseMetadataExtractor provides essential OS metadata.
## @changes
## LAST_CHANGE: [v1.0.0 — Semantic template markup and LDD logging added.]
## @modulemap
## CLASS 8[Universal metadata extractor for any file format] => BaseMetadataExtractor
## @usecases
## - [BaseMetadataExtractor]: MetadataExtractorComposition → ExtractAnyFile → ReturnOSAttributes → MetadataDict
def _module_contract():
    pass
# endregion MODULE_CONTRACT
# GREP_SUMMARY: base, fallback, universal, metadata, os.stat, file attributes, base64, any format
# STRUCTURE: ▶ CLASS BaseMetadataExtractor(ABC): ◇ can_extract → always True → ⚡ extract ┌file stat + base64?┐ → _get_base_meta_information ┌os.stat → dict┐

from typing import Optional

from dedoc.metadata_extractors.abstract_metadata_extractor import AbstractMetadataExtractor


# region CLASS_BaseMetadataExtractor [DOMAIN(8): DocumentProcessing, MetadataExtraction; CONCEPT(7): FallbackExtractor, FileAttributes; TECH(6): os.stat]
## @purpose To extract universal OS-level metadata from any file and optionally return its base64-encoded content — the safety net in the extraction chain.
class BaseMetadataExtractor(AbstractMetadataExtractor):
    # region METHOD_can_extract [DOMAIN(7): FormatMatching; CONCEPT(6): UniversalDispatch; TECH(4): Python]
    ## @purpose To unconditionally declare capability for any file — this is the universal fallback extractor.
    ## @uses None
    ## @io str × Optional[str] × Optional[str] × Optional[dict] × Optional[str] × Optional[str] -> bool
    ## @complexity 1
    def can_extract(self,
                    file_path: str,
                    converted_filename: Optional[str] = None,
                    original_filename: Optional[str] = None,
                    parameters: Optional[dict] = None,
                    mime: Optional[str] = None,
                    extension: Optional[str] = None) -> bool:
        """
        This extractor can handle any file so the method always returns True.
        Look to the :meth:`~dedoc.metadata_extractors.AbstractMetadataExtractor.can_extract` documentation to get the information about parameters.
        """
        self.logger.debug(f"[IMP:4][BaseMetadataExtractor][CAN_EXTRACT] Universal extractor — always returns True for file={original_filename or file_path}")
        return True
    # endregion METHOD_can_extract

    # region METHOD_extract [DOMAIN(8): MetadataExtraction; CONCEPT(7): FileAttributes, Base64Encode; TECH(6): os, base64]
    ## @purpose To collect OS-level file metadata and optionally encode the file content to base64 when the file is an attachment.
    ## @uses base64, os.path, AbstractMetadataExtractor._get_names
    ## @io str × Optional[str] × Optional[str] × Optional[dict] -> dict
    ## @complexity 6
    def extract(self,
                file_path: str,
                converted_filename: Optional[str] = None,
                original_filename: Optional[str] = None,
                parameters: Optional[dict] = None) -> dict:
        """
        Gets the basic meta-information about the file.
        Look to the :meth:`~dedoc.metadata_extractors.AbstractMetadataExtractor.extract` documentation to get the information about parameters.
        """
        from base64 import b64encode
        import os

        parameters = {} if parameters is None else parameters
        file_dir, file_name, converted_filename, original_filename = self._get_names(file_path, converted_filename, original_filename)
        meta_info = self._get_base_meta_information(file_dir, file_name, original_filename)
        self.logger.info(f"[IMP:7][BaseMetadataExtractor][EXTRACT] Base metadata collected for file={original_filename}, size={meta_info.get('size')} bytes")

        if parameters.get("is_attached", False) and str(parameters.get("return_base64", "false")).lower() == "true":
            full_path = os.path.join(file_dir, converted_filename)
            self.logger.debug(f"[IMP:6][BaseMetadataExtractor][BASE64_ENCODE] Encoding file={converted_filename} to base64")
            with open(full_path, "rb") as file:
                meta_info["base64_encode"] = b64encode(file.read()).decode("utf-8")
            self.logger.info(f"[IMP:7][BaseMetadataExtractor][BASE64_DONE] Base64 encoding complete for file={converted_filename}")

        return meta_info
    # endregion METHOD_extract

    # region METHOD_get_base_meta_information [DOMAIN(7): FileAttributes; CONCEPT(6): StatExtraction, MIMEDetection; TECH(6): os.stat]
    ## @purpose To call os.stat on the file and build a standardized metadata dictionary with file name, type, size, and timestamps.
    ## @uses os.stat, dedoc.utils.get_file_mime_type
    ## @io str × str × str -> dict
    ## @complexity 4
    @staticmethod
    def _get_base_meta_information(directory: str, filename: str, name_actual: str) -> dict:
        import os
        from dedoc.utils.utils import get_file_mime_type

        full_path = os.path.join(directory, filename)
        (mode, ino, dev, nlink, uid, gid, size, atime, mtime, ctime) = os.stat(full_path)
        meta = {
            "file_name": name_actual,
            "temporary_file_name": filename,
            "file_type": get_file_mime_type(full_path),
            "size": size,  # in bytes
            "access_time": atime,
            "created_time": ctime,
            "modified_time": mtime
        }
        return meta
    # endregion METHOD_get_base_meta_information
# endregion CLASS_BaseMetadataExtractor
