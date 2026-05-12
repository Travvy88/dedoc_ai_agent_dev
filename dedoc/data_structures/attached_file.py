import logging

logger = logging.getLogger(__name__)


# region CLASS_AttachedFile [DOMAIN(9): DocumentProcessing, DataStructures; CONCEPT(8): Attachment, FileMetadata; TECH(5): Python]
## @purpose Hold information about files attached to the parsed document: original name, disk path, content analysis flag, and UID.
class AttachedFile:
    """
    Holds information about files, attached to the parsed document.

    :ivar original_name: original name of the attached file if it was possible to extract it
    :ivar tmp_file_path: path to the attached file on disk - its name is different from original_name
    :ivar need_content_analysis: does the attached file need parsing (enable recursive parsing in :class:`~dedoc.DedocManager`)
    :ivar uid: unique identifier of the attached file

    :vartype original_name: str
    :vartype tmp_file_path: str
    :vartype need_content_analysis: bool
    :vartype uid: str
    """

    # region METHOD___init__ [DOMAIN(9): DocumentProcessing; CONCEPT(8): Attachment; TECH(5): Python]
    ## @purpose Initialize attached file metadata with original name, temp path, content analysis flag, and UID.
    ## @io (str, str, bool, str) -> None
    ## @complexity 2
    def __init__(self, original_name: str, tmp_file_path: str, need_content_analysis: bool, uid: str) -> None:
        """
        :param original_name: original name of the attached file
        :param tmp_file_path: path to the attachment file
        :param need_content_analysis: indicator should we parse the attachment's content or simply save it without parsing
        :param uid: unique identifier of the attachment
        """
        logger.debug(f"[IMP:4][AttachedFile][INIT] original_name={original_name}, uid={uid}, need_content_analysis={need_content_analysis}")
        self.original_name: str = original_name
        self.tmp_file_path: str = tmp_file_path
        self.need_content_analysis: bool = need_content_analysis
        self.uid: str = uid
        logger.debug(f"[IMP:4][AttachedFile][INIT] AttachedFile created for uid={uid}")
    # endregion METHOD___init__

    # region METHOD_get_filename_in_path [DOMAIN(9): DocumentProcessing; CONCEPT(5): Attachment; TECH(5): Python]
    ## @purpose Return the path to the attached file on disk.
    ## @io None -> str
    ## @complexity 1
    def get_filename_in_path(self) -> str:
        return self.tmp_file_path
    # endregion METHOD_get_filename_in_path

    # region METHOD_get_original_filename [DOMAIN(9): DocumentProcessing; CONCEPT(5): Attachment; TECH(5): Python]
    ## @purpose Return the original file name before rename.
    ## @io None -> str
    ## @complexity 1
    def get_original_filename(self) -> str:
        return self.original_name
    # endregion METHOD_get_original_filename
# endregion CLASS_AttachedFile

# region MODULE_CONTRACT [DOMAIN(9): DocumentProcessing, DataStructures; CONCEPT(8): Attachment, FileMetadata; TECH(5): Python]
## @modulecontract
## @purpose Define the AttachedFile data structure — holds metadata about files embedded in the parsed document.
## @scope Attached file metadata storage and access.
## @input Original name, temp path, analysis flag, UID.
## @output AttachedFile instance.
## @links [USED_BY(9): UnstructuredDocument]
## @invariants
## - uid is always a non-empty string
## - original_name may differ from tmp_file_path basename
## @rationale
## Q: Why separate original_name from tmp_file_path?
## A: During processing, files are renamed for uniqueness; the original name is preserved for user presentation.
## @changes
## LAST_CHANGE: [v1.0.0 – Added semantic markup and LDD logging]
## @modulemap
## CLASS 10[Attached file metadata] => AttachedFile
## METHOD 6[Get disk path] => get_filename_in_path
## METHOD 6[Get original name] => get_original_filename
## @usecases
## - [AttachedFile]: Reader → ExtractAttachment → AttachedFileStored
def _module_contract():
    pass
# endregion MODULE_CONTRACT
# GREP_SUMMARY: AttachedFile, attachment, file, metadata, document, original_name, tmp_file_path, uid, need_content_analysis
# STRUCTURE: ▶ AttachedFile ┌original_name, tmp_file_path, need_content_analysis, uid┐ → ⊕ get_filename_in_path → ⊕ get_original_filename → ⎋ file metadata
