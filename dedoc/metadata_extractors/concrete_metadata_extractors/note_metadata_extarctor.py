# region MODULE_CONTRACT [DOMAIN(8): DocumentProcessing, MetadataExtraction; CONCEPT(6): NoteFormat, PickleDeserialization; TECH(6): PythonPickle]
## @modulecontract
## @purpose To extract metadata from .note.pickle documents — a custom serialized format containing author, file size, and timestamps stored as a pickled dictionary.
## @scope Note (.note.pickle) file metadata extraction, pickle deserialization.
## @input file_path via extract(), config with logger.
## @output dict with keys: file_name, file_type ("note"), size, access_time, created_time, modified_time, author.
## @links [USES_API(6): pickle.load, BadFileFormatError]
## @invariants
## - can_extract checks for ".note.pickle" suffix (case-insensitive).
## - On pickle deserialization failure, raises BadFileFormatError.
## @rationale
## Q: Why override can_extract with a suffix check?
## A: .note.pickle files have no standard MIME type and no consistent extension registry — suffix matching is the most reliable detection method.
## @changes
## LAST_CHANGE: [v1.0.0 — Semantic template markup and LDD logging added.]
## @modulemap
## CLASS 7[Note metadata extractor from .note.pickle files] => NoteMetadataExtractor
## @usecases
## - [NoteMetadataExtractor]: MetadataExtractorComposition → DetectNotePickle → DeserializePickle → MetadataDict
def _module_contract():
    pass
# endregion MODULE_CONTRACT
# GREP_SUMMARY: note, pickle, metadata, author, deserialize, BadFileFormatError
# STRUCTURE: ▶ CLASS NoteMetadataExtractor(ABC): ◇ can_extract ┌.note.pickle suffix?┐ → ⚡ extract ┌pickle.load → dict┐ → ⚡ BadFileFormatError on failure

from typing import Optional

from dedoc.common.exceptions.bad_file_error import BadFileFormatError
from dedoc.metadata_extractors.abstract_metadata_extractor import AbstractMetadataExtractor


# region CLASS_NoteMetadataExtractor [DOMAIN(8): DocumentProcessing, MetadataExtraction; CONCEPT(6): NoteFormat, PickleDeserialization; TECH(6): PythonPickle]
## @purpose To extract metadata from .note.pickle files by deserializing a pickled dictionary containing author, size, and timestamp fields.
class NoteMetadataExtractor(AbstractMetadataExtractor):
    # region METHOD_init [DOMAIN(6): Configuration; CONCEPT(5): Constructor; TECH(4): PythonDefaults]
    ## @purpose To instantiate the extractor — no format-specific registrations needed since .note.pickle has no standard MIME/extension.
    ## @uses None
    ## @io Optional[dict] -> None
    ## @complexity 2
    def __init__(self, *, config: Optional[dict] = None) -> None:
        super().__init__(config=config)
        self.logger.debug("[IMP:4][NoteMetadataExtractor][INIT] Note metadata extractor initialized")
    # endregion METHOD_init

    # region METHOD_can_extract [DOMAIN(7): FormatMatching; CONCEPT(6): SuffixCheck; TECH(4): PythonStrings]
    ## @purpose To detect .note.pickle files by checking the converted filename suffix — no MIME or extension registry used.
    ## @uses AbstractMetadataExtractor._get_names
    ## @io str × Optional[str] × Optional[str] × Optional[dict] × Optional[str] × Optional[str] -> bool
    ## @complexity 4
    def can_extract(self,
                    file_path: str,
                    converted_filename: Optional[str] = None,
                    original_filename: Optional[str] = None,
                    parameters: Optional[dict] = None,
                    mime: Optional[str] = None,
                    extension: Optional[str] = None) -> bool:
        """
        Check if the document has .note.pickle extension.
        Look to the :meth:`~dedoc.metadata_extractors.AbstractMetadataExtractor.can_extract` documentation to get the information about parameters.
        """
        file_dir, file_name, converted_filename, original_filename = self._get_names(file_path, converted_filename, original_filename)
        matches = converted_filename.lower().endswith(".note.pickle")
        self.logger.debug(f"[IMP:5][NoteMetadataExtractor][CAN_EXTRACT] File={converted_filename}, is_note_pickle={matches}")
        return matches
    # endregion METHOD_can_extract

    # region METHOD_extract [DOMAIN(8): MetadataExtraction; CONCEPT(7): PickleDeserialization; TECH(6): PythonPickle]
    ## @purpose To deserialize a .note.pickle file and construct a metadata dictionary with author, file size, and timestamps.
    ## @uses pickle, os.path, BadFileFormatError
    ## @io str × Optional[str] × Optional[str] × Optional[dict] -> dict
    ## @complexity 6
    def extract(self,
                file_path: str,
                converted_filename: Optional[str] = None,
                original_filename: Optional[str] = None,
                parameters: Optional[dict] = None) -> dict:
        """
        Add the predefined list of metadata for the .note.pickle documents.
        Look to the :meth:`~dedoc.metadata_extractors.AbstractMetadataExtractor.extract` documentation to get the information about parameters.
        """
        import os
        import pickle

        file_dir, file_name, converted_filename, original_filename = self._get_names(file_path, converted_filename, original_filename)

        try:
            file_path_resolved = os.path.join(file_dir, converted_filename)
            self.logger.debug(f"[IMP:5][NoteMetadataExtractor][OPEN] Loading pickle file={os.path.basename(file_path_resolved)}")
            with open(file_path_resolved, "rb") as infile:
                note_dict = pickle.load(infile)

            meta_info = dict(file_name=original_filename,
                             file_type="note",
                             size=note_dict["size"],
                             access_time=note_dict["modified_time"],
                             created_time=note_dict["created_time"],
                             modified_time=note_dict["modified_time"],
                             author=note_dict["author"])
            self.logger.info(f"[IMP:9][NoteMetadataExtractor][RESULT] Metadata extracted: author={meta_info['author']}, size={meta_info['size']}")
            return meta_info
        except Exception:
            self.logger.warning(f"[IMP:9][NoteMetadataExtractor][BROKEN] Bad note file: {os.path.basename(file_path_resolved)}")
            raise BadFileFormatError(f"Bad note file:\n file_name = {os.path.basename(file_path_resolved)}. Seems note-format is broken")
    # endregion METHOD_extract
# endregion CLASS_NoteMetadataExtractor
