import logging
from typing import List, Optional

from dedoc.api.schema.parsed_document import ParsedDocument as ApiParsedDocument
from dedoc.data_structures.document_content import DocumentContent
from dedoc.data_structures.document_metadata import DocumentMetadata
from dedoc.data_structures.serializable import Serializable

logger = logging.getLogger(__name__)


# region CLASS_ParsedDocument [DOMAIN(9): DocumentProcessing, DataStructures; CONCEPT(10): Document, Aggregation; TECH(6): Python, API]
## @purpose Top-level container for a fully parsed document — holds content (text tree + tables), metadata, attachments (recursive ParsedDocument list), and warnings.
class ParsedDocument(Serializable):
    """
    This class holds information about the document content, metadata and attachments.

    :ivar content: document text (hierarchy of nodes) and tables
    :ivar attachments: result of analysis of attached files (empty if with_attachments=False)
    :ivar metadata: document metadata such as size, creation date and so on.
    :ivar warnings: list of warnings and possible errors, arising in the process of document parsing

    :vartype content: DocumentContent
    :vartype attachments: List[ParsedDocument]
    :vartype metadata: DocumentMetadata
    :vartype warnings: List[str]
    """

    # region METHOD___init__ [DOMAIN(9): DocumentProcessing; CONCEPT(10): Document; TECH(6): Python]
    ## @purpose Initialize parsed document with metadata, content, warnings, and optional recursive attachments.
    ## @io (DocumentMetadata, DocumentContent, Optional[List[str]], Optional[List[ParsedDocument]]) -> None
    ## @complexity 2
    def __init__(self,
                 metadata: DocumentMetadata,
                 content: DocumentContent,
                 warnings: Optional[List[str]] = None,
                 attachments: Optional[List["ParsedDocument"]] = None) -> None:
        """
        :param metadata: document metadata such as size, creation date and so on.
        :param content: text and tables
        :param attachments: result of analysis of attached files
        :param warnings: list of warnings and possible errors, arising in the process of document parsing
        """
        logger.debug(f"[IMP:4][ParsedDocument][INIT] attachments_count={len(attachments) if attachments else 0}, warnings_count={len(warnings) if warnings else 0}")
        self.metadata: DocumentMetadata = metadata
        self.content: DocumentContent = content
        self.attachments: List["ParsedDocument"] = [] if attachments is None else attachments
        self.warnings: List[str] = warnings if warnings is not None else []
        logger.info(f"[IMP:9][ParsedDocument][RESULT] ParsedDocument created with {len(self.attachments)} attachments, {len(self.warnings)} warnings")
    # endregion METHOD___init__

    # region METHOD_add_attachments [DOMAIN(9): DocumentProcessing; CONCEPT(6): Mutation; TECH(5): Python]
    ## @purpose Add list of parsed documents as attachments to this document.
    ## @io List[ParsedDocument] -> None
    ## @complexity 2
    def add_attachments(self, new_attachment: List["ParsedDocument"]) -> None:
        logger.debug(f"[IMP:4][ParsedDocument][ADD_ATTACH] Adding {len(new_attachment)} attachments")
        if self.attachments is None:
            self.attachments = []
        self.attachments.extend(new_attachment)
        logger.debug(f"[IMP:4][ParsedDocument][ADD_ATTACH] Total attachments: {len(self.attachments)}")
    # endregion METHOD_add_attachments

    # region METHOD_set_metadata [DOMAIN(9): DocumentProcessing; CONCEPT(5): Mutation; TECH(5): Python]
    ## @purpose Replace document metadata.
    ## @io DocumentMetadata -> None
    ## @complexity 1
    def set_metadata(self, metadata: DocumentMetadata) -> None:
        logger.debug(f"[IMP:4][ParsedDocument][SET_METADATA] Updating metadata, uid={metadata.uid}")
        self.metadata = metadata
    # endregion METHOD_set_metadata

    # region METHOD_to_api_schema [DOMAIN(9): DocumentProcessing; CONCEPT(8): Serialization; TECH(6): API]
    ## @purpose Convert parsed document to API schema, recursively serializing content, metadata, and attachments.
    ## @uses ApiParsedDocument, dedoc.version
    ## @io None -> ApiParsedDocument
    ## @complexity 4
    def to_api_schema(self) -> ApiParsedDocument:
        import dedoc.version

        logger.debug(f"[IMP:4][ParsedDocument][TO_API] Converting to API schema, version={dedoc.version.__version__}")
        content = self.content.to_api_schema()
        metadata = self.metadata.to_api_schema()
        attachments = [attachment.to_api_schema() for attachment in self.attachments] if self.attachments is not None else []
        return ApiParsedDocument(content=content, metadata=metadata, version=dedoc.version.__version__, warnings=self.warnings, attachments=attachments)
    # endregion METHOD_to_api_schema
# endregion CLASS_ParsedDocument

# region MODULE_CONTRACT [DOMAIN(9): DocumentProcessing, DataStructures; CONCEPT(10): Document, Aggregation; TECH(6): Python, API]
## @modulecontract
## @purpose Define the ParsedDocument data structure — the top-level aggregation of content, metadata, attachments, and warnings for a completely parsed document.
## @scope Complete document container: text tree + tables (DocumentContent), metadata, recursive attachments, warnings.
## @input DocumentMetadata, DocumentContent, optional warnings and attachments.
## @output ParsedDocument instance convertible to API schema.
## @links [INHERITS(5): Serializable, USES_API(8): ApiParsedDocument, READS_DATA_FROM(9): DocumentContent, DocumentMetadata]
## @invariants
## - attachments is never None (defaults to empty list)
## - warnings is never None (defaults to empty list)
## @rationale
## Q: Why do attachments contain ParsedDocument recursively?
## A: Attached files (e.g. embedded PDFs) may themselves be parsed into documents, requiring recursive parsing. This enables full document hierarchy.
## @changes
## LAST_CHANGE: [v1.0.0 – Added semantic markup and LDD logging]
## @modulemap
## CLASS 10[Complete parsed document] => ParsedDocument
## METHOD 6[Constructor] => __init__
## METHOD 5[Add attachments] => add_attachments
## METHOD 4[Set metadata] => set_metadata
## METHOD 8[API schema conversion] => to_api_schema
## @usecases
## - [ParsedDocument]: DedocManager → ParseDocument → ParsedDocumentReturned
## - [ParsedDocument]: AttachmentHandler → RecursiveParse → NestedParsedDocuments
def _module_contract():
    pass
# endregion MODULE_CONTRACT
# GREP_SUMMARY: ParsedDocument, document, content, metadata, attachments, warnings, version, API, serializable, recursive
# STRUCTURE: ▶ ParsedDocument ┌metadata, content(DocumentContent), warnings?, attachments?(recursive[])┐ → ⊕ add_attachments → ⊕ set_metadata → ⊕ to_api_schema (recursive: content + metadata + attachments + version) → ⎋ ApiParsedDocument
