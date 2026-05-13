import logging
from typing import Dict, Optional, Union

from dedoc.api.schema.document_metadata import DocumentMetadata as ApiDocumentMetadata
from dedoc.data_structures.serializable import Serializable

logger = logging.getLogger(__name__)


# region CLASS_DocumentMetadata [DOMAIN(9): DocumentProcessing, DataStructures; CONCEPT(9): Document, Metadata; TECH(6): Python, API]
## @purpose Hold document-level metadata: file name, size, timestamps, MIME type, UID, and arbitrary additional attributes.
class DocumentMetadata(Serializable):
    """
    This class holds information about document metadata.

    :ivar file_name: original document name (before rename and conversion, so it can contain non-ascii symbols, spaces and so on)
    :ivar temporary_file_name: file name during parsing (unique name after rename and conversion)
    :ivar size: size of the original file in bytes
    :ivar modified_time: time of the last modification in unix time format (seconds since the epoch)
    :ivar created_time: time of the creation in unixtime
    :ivar access_time: time of the last access to the file in unixtime
    :ivar file_type: mime type of the file
    :ivar uid: document unique identifier (useful for attached files)

    :vartype file_name: str
    :vartype temporary_file_name: str
    :vartype size: int
    :vartype modified_time: int
    :vartype created_time: int
    :vartype access_time: int
    :vartype file_type: str
    :vartype uid: str

    Additional variables may be added with other file metadata.
    """

    # region METHOD___init__ [DOMAIN(9): DocumentProcessing; CONCEPT(9): Document; TECH(6): Python]
    ## @purpose Initialize document metadata with file info, optional UID, and extra kwargs as attributes.
    ## @uses uuid
    ## @io (str, str, int, int, int, int, str, Optional[str], **kwargs) -> None
    ## @complexity 4
    def __init__(self,
                 file_name: str,
                 temporary_file_name: str,
                 size: int,
                 modified_time: int,
                 created_time: int,
                 access_time: int,
                 file_type: str,
                 uid: Optional[str] = None,
                 **kwargs: Dict[str, Union[str, int, float]]) -> None:
        """
        :param uid: document unique identifier
        :param file_name: original document name
        :param temporary_file_name: file name during parsing
        :param size: size of the original file in bytes
        :param modified_time: time of the last modification in unix time format
        :param created_time: time of the creation in unixtime
        :param access_time: time of the last access to the file in unixtime
        :param file_type: mime type of the file
        """
        import uuid

        logger.debug(f"[IMP:4][DocumentMetadata][INIT] file_name={file_name}, file_type={file_type}, size={size}, uid={uid}")
        self.file_name: str = file_name
        self.temporary_file_name: str = temporary_file_name
        self.size: int = size
        self.modified_time: int = modified_time
        self.created_time: int = created_time
        self.access_time: int = access_time
        self.file_type: str = file_type
        for key, value in kwargs.items():
            self.add_attribute(key, value)
        self.uid: str = f"doc_uid_auto_{uuid.uuid1()}" if uid is None else uid
        logger.info(f"[IMP:9][DocumentMetadata][RESULT] DocumentMetadata created with uid={self.uid}, file_type={self.file_type}")
    # endregion METHOD___init__

    # region METHOD_add_attribute [DOMAIN(9): DocumentProcessing; CONCEPT(5): Extensibility; TECH(5): Python]
    ## @purpose Dynamically add an arbitrary attribute to the metadata.
    ## @io (str, Union[str,int,float]) -> None
    ## @complexity 1
    def add_attribute(self, key: str, value: Union[str, int, float]) -> None:
        setattr(self, key, value)
    # endregion METHOD_add_attribute

    # region METHOD_to_api_schema [DOMAIN(9): DocumentProcessing; CONCEPT(8): Serialization; TECH(6): API]
    ## @purpose Convert document metadata to API schema using vars().
    ## @uses ApiDocumentMetadata
    ## @io None -> ApiDocumentMetadata
    ## @complexity 2
    def to_api_schema(self) -> ApiDocumentMetadata:
        logger.debug(f"[IMP:4][DocumentMetadata][TO_API] Converting to API schema")
        return ApiDocumentMetadata(**vars(self))
    # endregion METHOD_to_api_schema
# endregion CLASS_DocumentMetadata

# region MODULE_CONTRACT [DOMAIN(9): DocumentProcessing, DataStructures; CONCEPT(9): Document, Metadata; TECH(6): Python, API]
## @modulecontract
## @purpose Define the DocumentMetadata data structure — holds file-level metadata and supports dynamic attribute addition.
## @scope Document metadata: file info, timestamps, UID generation, extensible attributes.
## @input File name, temp name, size, timestamps, MIME type, optional UID, extra kwargs.
## @output DocumentMetadata instance with auto-generated or provided UID.
## @links [INHERITS(5): Serializable, USES_API(8): ApiDocumentMetadata]
## @invariants
## - uid is always a non-empty string (auto-generated if not provided)
## @rationale
## Q: Why use **kwargs for extensibility?
## A: Different document formats have different metadata fields; kwargs enable format-specific extensions without schema changes.
## @changes
## LAST_CHANGE: [v1.0.0 – Added semantic markup and LDD logging]
## @modulemap
## CLASS 10[Document metadata container] => DocumentMetadata
## METHOD 5[Add dynamic attribute] => add_attribute
## METHOD 8[API schema conversion] => to_api_schema
## @usecases
## - [DocumentMetadata]: Reader → ExtractFileMetadata → DocumentMetadataStored
def _module_contract():
    pass
# endregion MODULE_CONTRACT
# GREP_SUMMARY: DocumentMetadata, metadata, document, file_name, size, timestamps, file_type, uid, API, serializable
# STRUCTURE: ▶ DocumentMetadata ┌file_name, temp_name, size, timestamps, file_type, uid?, **kwargs┐ → ◇ uid auto-gen (uuid.uuid1) → ⊕ add_attribute kwargs → ⊕ to_api_schema (vars) → ⎋ ApiDocumentMetadata
