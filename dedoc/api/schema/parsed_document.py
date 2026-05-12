# region MODULE_CONTRACT [DOMAIN(9): DocumentProcessing, APIModel; CONCEPT(8): ParsingResult, DocumentAggregate; TECH(7): Pydantic, BaseModel]
## @modulecontract
## @purpose Define the ParsedDocument schema — the top-level API response model aggregating document content, metadata, attachments, warnings, and version info.
## @scope Root API response model — full document parsing result.
## @input None (standalone model, references DocumentContent, DocumentMetadata, self for attachments).
## @output Pydantic BaseModel `ParsedDocument` with content, metadata, version, warnings, attachments.
## @links [USES_API(7): pydantic.BaseModel; READS_DATA_FROM(8): DocumentContent, DocumentMetadata]
## @invariants
## - content is always present (may have empty tables and root-only structure).
## - attachments list may be empty if with_attachments=False.
## - version matches dedoc.version.__version__.
## @rationale
## Q: Why self-referential for attachments?
## A: Attached files are parsed into ParsedDocument themselves, forming a recursive structure that matches the nested nature of document attachments.
## @changes
## LAST_CHANGE: [v1.0.0 – Initial creation with semantic markup]
## @modulemap
## CLASS 10[Top-level API response — content + metadata + attachments] => ParsedDocument
## @usecases
## - [ParsedDocument]: ApiEndpoint => SerializeParsingResult => ReturnJSONToClient
def _module_contract():
    pass
# endregion MODULE_CONTRACT
# GREP_SUMMARY: parsed, document, content, metadata, attachments, warnings, version, API, response, Pydantic, schema
# STRUCTURE: ▶ Pydantic BaseModel → ParsedDocument ┌content:DocumentContent, metadata:DocumentMetadata, version:str, warnings:List[str], attachments:List[ParsedDocument]┐ → ⎋ JSON

import logging
from typing import List

from pydantic import BaseModel, Field

from dedoc.api.schema.document_content import DocumentContent
from dedoc.api.schema.document_metadata import DocumentMetadata

logger = logging.getLogger(__name__)

# region CLASS_ParsedDocument [DOMAIN(9): DocumentProcessing; CONCEPT(8): APIResponse; TECH(7): PydanticBaseModel]
## @purpose Top-level API response model: aggregates document content, metadata, nested attachments, warnings, and version into a single JSON-serializable entity.
## @io (content, metadata, version, warnings, attachments) -> JSON serializable model
class ParsedDocument(BaseModel):
    """
    Holds information about the document content, metadata and attachments.

    :ivar content: document text (hierarchy of nodes) and tables
    :ivar attachments: result of analysis of attached files (empty if with_attachments=False)
    :ivar metadata: document metadata such as size, creation date and so on.
    :ivar warnings: list of warnings and possible errors, arising in the process of document parsing
    :ivar version: version of the program that parsed this document

    :vartype content: DocumentContent
    :vartype attachments: List[ParsedDocument]
    :vartype metadata: DocumentMetadata
    :vartype warnings: List[str]
    :vartype version: str
    """
    content: DocumentContent = Field(description="Document text and tables")
    metadata: DocumentMetadata = Field(description="Document metadata such as size, creation date and so on")
    version: str = Field(description="Version of the program that parsed this document", example="0.9.1")
    warnings: List[str] = Field(description="List of warnings and possible errors, arising in the process of document parsing")
    attachments: List["ParsedDocument"] = Field(description="Result of analysis of attached files - list of `ParsedDocument`")
# endregion CLASS_ParsedDocument
