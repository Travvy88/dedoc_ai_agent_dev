import logging
from typing import List, Optional

from dedoc.data_structures.attached_file import AttachedFile
from dedoc.data_structures.line_with_meta import LineWithMeta
from dedoc.data_structures.table import Table

logger = logging.getLogger(__name__)


# region CLASS_UnstructuredDocument [DOMAIN(9): DocumentProcessing, DataStructures; CONCEPT(10): Document, RawOutput; TECH(6): Python]
## @purpose Hold raw (pre-structure-extraction) document content — flat line list, tables, attachments, metadata dict, and warnings from a reader.
class UnstructuredDocument:
    """
    This class holds information about raw document content: its text, tables and attachments, that have been procured using one of the readers.
    Text is represented as a flat list of lines, hierarchy level of each line isn't defined (only tag hierarchy level may exist).

    :ivar lines: list of textual lines with metadata returned by a reader
    :ivar tables: list of document tables returned by a reader
    :ivar attachments: list of document attached files
    :ivar metadata: information about the document (like in :class:`~dedoc.data_structures.DocumentMetadata`)
    :ivar warnings: list of warnings, obtained in the process of the document parsing

    :vartype lines: List[LineWithMeta]
    :vartype tables: List[Table]
    :vartype attachments: List[AttachedFile]
    :vartype metadata: dict
    :vartype warnings: List[str]
    """

    # region METHOD___init__ [DOMAIN(9): DocumentProcessing; CONCEPT(10): Document; TECH(6): Python]
    ## @purpose Initialize unstructured document with tables, lines, attachments, warnings, and metadata dict.
    ## @io (List[Table], List[LineWithMeta], List[AttachedFile], Optional[List[str]], Optional[dict]) -> None
    ## @complexity 2
    def __init__(self,
                 tables: List[Table],
                 lines: List[LineWithMeta],
                 attachments: List[AttachedFile],
                 warnings: Optional[List[str]] = None,
                 metadata: Optional[dict] = None) -> None:
        """
        :param tables: list of document tables
        :param lines: list of raw document lines
        :param attachments: list of documents attachments
        :param warnings: list of warnings, obtained in the process of the document parsing
        :param metadata: additional data
        """
        logger.debug(f"[IMP:4][UnstructuredDocument][INIT] tables={len(tables)}, lines={len(lines)}, attachments={len(attachments)}, warnings={len(warnings) if warnings else 0}")
        self.tables: List[Table] = tables
        self.lines: List[LineWithMeta] = lines
        self.attachments: List[AttachedFile] = attachments
        self.warnings: List[str] = warnings if warnings else []
        self.metadata: dict = metadata if metadata is not None else {}
        logger.info(f"[IMP:9][UnstructuredDocument][RESULT] UnstructuredDocument created: {len(self.lines)} lines, {len(self.tables)} tables, {len(self.attachments)} attachments")
    # endregion METHOD___init__

    # region METHOD_get_text [DOMAIN(9): DocumentProcessing; CONCEPT(7): TextExtraction; TECH(5): Python]
    ## @purpose Join all lines to get the full raw text of the document.
    ## @uses LineWithMeta.join
    ## @io None -> str
    ## @complexity 2
    def get_text(self) -> str:
        logger.debug(f"[IMP:4][UnstructuredDocument][GET_TEXT] Joining {len(self.lines)} lines")
        result = LineWithMeta.join(self.lines).line
        logger.debug(f"[IMP:4][UnstructuredDocument][GET_TEXT] Result text len={len(result)}")
        return result
    # endregion METHOD_get_text
# endregion CLASS_UnstructuredDocument

# region MODULE_CONTRACT [DOMAIN(9): DocumentProcessing, DataStructures; CONCEPT(10): Document, RawOutput; TECH(6): Python]
## @modulecontract
## @purpose Define the UnstructuredDocument data structure — the intermediate output of document readers containing flat lines, tables, and attachments before structure extraction.
## @scope Raw document content: flat line list, tables, attachments, metadata, warnings.
## @input Tables, lines, attachments, optional warnings and metadata.
## @output UnstructuredDocument instance consumed by structure extractors.
## @links [READS_DATA_FROM(9): LineWithMeta, Table, AttachedFile]
## @invariants
## - warnings is never None (defaults to empty list)
## - metadata is never None (defaults to empty dict)
## @rationale
## Q: Why a separate "unstructured" phase?
## A: Readers output flat line lists with format-specific tags; structure extractors then assign hierarchy levels and build the document tree. This separation enables independent reader and extractor development.
## @changes
## LAST_CHANGE: [v1.0.0 – Added semantic markup and LDD logging]
## @modulemap
## CLASS 10[Unstructured document container] => UnstructuredDocument
## METHOD 5[Get full raw text] => get_text
## @usecases
## - [UnstructuredDocument]: Reader → ReturnRawDocument → UnstructuredDocumentProduced
## - [UnstructuredDocument]: StructureExtractor → BuildDocumentTree → ParsedDocumentCreated
def _module_contract():
    pass
# endregion MODULE_CONTRACT
# GREP_SUMMARY: UnstructuredDocument, document, raw, lines, tables, attachments, metadata, warnings, reader, flat, text
# STRUCTURE: ▶ UnstructuredDocument ┌tables[], lines[], attachments[], warnings?, metadata?┐ → ⊕ get_text (LineWithMeta.join) → ⎋ raw text string
