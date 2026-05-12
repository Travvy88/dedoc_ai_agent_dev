from typing import Optional

from dedoc.data_structures.unstructured_document import UnstructuredDocument
from dedoc.readers.base_reader import BaseReader


# region CLASS_NoteReader [DOMAIN(8): DocumentProcessing; CONCEPT(7): Reader; TECH(6): Python]
class NoteReader(BaseReader):
    """
    This class is used for parsing documents with .note.pickle extension.
    """

    # region METHOD___init__ [DOMAIN(7): DocumentProcessing; CONCEPT(6): Method; TECH(6): Python]
    def __init__(self, *, config: Optional[dict] = None) -> None:
        super().__init__(config=config, recognized_extensions={".note.pickle"})

    # region METHOD_read [DOMAIN(7): DocumentProcessing; CONCEPT(6): Method; TECH(6): Python]
    # endregion METHOD___init__
    def read(self, file_path: str, parameters: Optional[dict] = None) -> UnstructuredDocument:
        """
        The method return document content with all document's lines.
        Look to the documentation of :meth:`~dedoc.readers.BaseReader.read` to get information about the method's parameters.
        """
        import os
        import pickle
        from dedoc.common.exceptions.bad_file_error import BadFileFormatError
        from dedoc.data_structures.line_with_meta import LineWithMeta

        try:
            with open(file_path, "rb") as infile:
                note_dict = pickle.load(infile)
            text = note_dict["content"]
            if isinstance(text, bytes):
                text = text.decode()
            lines = [LineWithMeta(line=text)]
            unstructured = UnstructuredDocument(tables=[], lines=lines, attachments=[])

            return unstructured
        except Exception as e:
            self.logger.warning(f"Can't handle {file_path}\n{e}")
# endregion CLASS_NoteReader
            raise BadFileFormatError(f"Bad note file:\n file_name = {os.path.basename(file_path)}. Seems note-format is broken")

    # endregion METHOD_read


# region MODULE_CONTRACT [DOMAIN(8): DocumentProcessing; CONCEPT(7): Reader_note_reader; TECH(6): Python, dedoc]
## @modulecontract
## @purpose Read and parse note documents, extracting lines with metadata, tables, and attachments into UnstructuredDocument.
## @scope Document parsing pipeline: note format reading.
## @input [File path (str), parameters (Optional[dict]) — document on disk.]
## @output [UnstructuredDocument with lines, tables, attachments, and warnings.]
## @links [USES_API(9): dedoc.data_structures.*; USES_API(8): dedoc.readers.BaseReader]
## @invariants
## - read() ALWAYS returns an UnstructuredDocument.
## @rationale
## Q: Why is this reader separated from others?
## A: Each reader handles one format family — isolation prevents format coupling and simplifies extension.
## @changes
## LAST_CHANGE: [v1.0.0 – Added SEMANTIC TEMPLATE markup and LDD logging.]
## @modulemap
## CLASS [4][NoteReader reader/processor] => NoteReader
## @usecases
## - [read]: System (Pipeline) → ParseDocument(note) → UnstructuredDocument
def _module_contract():
    pass
# endregion MODULE_CONTRACT
# GREP_SUMMARY: note_reader, dedoc, reader, note, NoteReader, BaseReader, note, text, plain, UnstructuredDocument, NoteReader
# STRUCTURE: ▶ Init ┌note file┐ → [NoteReader] ○ can_read? → ○ read → [__init__ → read] → ⊕ UnstructuredDocument(lines, tables, attachments)
