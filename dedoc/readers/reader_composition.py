from typing import List, Optional

from dedoc.common.exceptions.bad_file_error import BadFileFormatError
from dedoc.data_structures.unstructured_document import UnstructuredDocument
from dedoc.readers.base_reader import BaseReader

import logging

logger = logging.getLogger(__name__)


# region CLASS_ReaderComposition [DOMAIN(8): DocumentProcessing; CONCEPT(7): Reader; TECH(6): Python]
class ReaderComposition(object):
    """
    This class allows to read any document of the predefined list of formats according to the available list of readers.
    The list of readers is set via the class constructor.
    The first suitable reader is used for parsing (the one whose method :meth:`~dedoc.readers.BaseReader.can_read` returns True), \
    so the order of the given readers is important.
    """
    # region METHOD___init__ [DOMAIN(7): DocumentProcessing; CONCEPT(6): Method; TECH(6): Python]
    def __init__(self, readers: List[BaseReader]) -> None:
        """
        :param readers: the list of readers for documents of different formats that will be used for parsing
        """
        self.readers = readers
    # endregion METHOD___init__

    # region METHOD_read [DOMAIN(7): DocumentProcessing; CONCEPT(6): Method; TECH(6): Python]
    def read(self, file_path: str, parameters: Optional[dict] = None, extension: Optional[str] = None, mime: Optional[str] = None) -> UnstructuredDocument:
        """
        Get intermediate representation for the document of any format which one of the available readers can parse.
        If there is no suitable reader for the given document, the BadFileFormatException will be raised.

        :param file_path: path of the file to be parsed
        :param parameters: dict with additional parameters for document readers, see :ref:`parameters_description` for more details
        :param extension: file extension, for example .doc or .pdf
        :param mime: MIME type of file
        :return: intermediate representation of the document with lines, tables and attachments
        """
        import os
        from dedoc.utils.utils import get_mime_extension

        mime, extension = get_mime_extension(file_path=file_path, mime=mime, extension=extension)

        for reader in self.readers:
            if reader.can_read(file_path=file_path, mime=mime, extension=extension, parameters=parameters):
                unstructured_document = reader.read(file_path=file_path, parameters=parameters)
                return unstructured_document

        file_name = os.path.basename(file_path)
        raise BadFileFormatError(
            msg=f"No one can read file: name = {file_name}, extension = {extension}, mime = {mime}",
            msg_api=f"Unsupported file format {mime} of the input file {file_name}"
        )
    # endregion METHOD_read
# endregion CLASS_ReaderComposition


# region MODULE_CONTRACT [DOMAIN(8): DocumentProcessing; CONCEPT(7): Reader_reader_composition; TECH(6): Python, dedoc]
## @modulecontract
## @purpose Compose multiple readers into a single entry point that routes documents to the first capable reader.
## @scope Document parsing pipeline: composition (multiplexer) format reading.
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
## CLASS [4][ReaderComposition reader/processor] => ReaderComposition
## @usecases
## - [read]: System (Pipeline) → ParseDocument(composition (multiplexer)) → UnstructuredDocument
def _module_contract():
    pass
# endregion MODULE_CONTRACT
# GREP_SUMMARY: reader_composition, dedoc, reader, composition (multiplexer), reader, document, parsing, UnstructuredDocument, ReaderComposition
# STRUCTURE: ▶ Init ┌composition (multiplexer) file┐ → [ReaderComposition] ○ can_read? → ○ read → [__init__ → read] → ⊕ UnstructuredDocument(lines, tables, attachments)
