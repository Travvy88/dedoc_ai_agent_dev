# region MODULE_CONTRACT [DOMAIN(9): DocumentProcessing, FileMetadata; CONCEPT(7): DocumentProperties, FilesystemMetadata; TECH(7): Pydantic, BaseModel, Extra]
## @modulecontract
## @purpose Define the DocumentMetadata schema — a Pydantic model holding file-level metadata (name, size, timestamps, MIME type, UID) with support for extra attributes.
## @scope Document file metadata model.
## @input None (standalone model with extra attributes support).
## @output Pydantic BaseModel `DocumentMetadata` with uid, file_name, size, timestamps, file_type, plus arbitrary extra fields.
## @links [USES_API(7): pydantic.BaseModel, pydantic.Extra]
## @invariants
## - uid is always a non-empty unique string.
## - file_name is always present (original document name).
## - Extra fields are preserved and serialized.
## @rationale
## Q: Why Extra.allow?
## A: Different document formats carry different metadata (author, pages, etc.). Extra.allow prevents data loss while keeping the schema flexible.
## @changes
## LAST_CHANGE: [v1.0.0 – Initial creation with semantic markup]
## @modulemap
## CLASS 9[Document metadata with extra attributes support] => DocumentMetadata
## @usecases
## - [DocumentMetadata]: MetadataExtractor => PopulateMetadata => ReturnToAPI
def _module_contract():
    pass
# endregion MODULE_CONTRACT
# GREP_SUMMARY: metadata, document, file, name, size, timestamps, MIME, uid, extra, Pydantic, schema
# STRUCTURE: ▶ Pydantic BaseModel (Extra.allow) → DocumentMetadata ┌uid, file_name, size, timestamps, file_type, +extra┐ → ⎋ JSON

import logging

from pydantic import BaseModel, Extra, Field

logger = logging.getLogger(__name__)

# region CLASS_DocumentMetadata [DOMAIN(9): DocumentProcessing; CONCEPT(7): FileMetadata; TECH(7): PydanticBaseModel]
## @purpose Hold document file metadata (name, size, timestamps, MIME type) with open extension for format-specific attributes via Extra.allow.
## @io (uid, file_name, size, timestamps, file_type, **extra) -> JSON serializable model
class DocumentMetadata(BaseModel):
    """
    Document metadata like its name, size, author, etc.

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
    class Config:
        extra = Extra.allow

    uid: str = Field(description="Document unique identifier (useful for attached files)", example="doc_uid_auto_ba73d76a-326a-11ec-8092-417272234cb0")
    file_name: str = Field(description="Original document name before rename and conversion", example="example.odt")
    temporary_file_name: str = Field(description="File name during parsing (unique name after rename and conversion)", example="123.odt")
    size: int = Field(description="File size in bytes", example=20060)
    modified_time: int = Field(description="Modification time of the document in the UnixTime format", example=1590579805)
    created_time: int = Field(description="Creation time of the document in the UnixTime format", example=1590579805)
    access_time: int = Field(description="File access time in the UnixTime format", example=1590579805)
    file_type: str = Field(description="Mime type of the file", example="application/vnd.oasis.opendocument.text")
# endregion CLASS_DocumentMetadata
