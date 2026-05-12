from abc import ABC, abstractmethod
from typing import Optional, Set

from dedoc.data_structures.unstructured_document import UnstructuredDocument


# region CLASS_BaseReader [DOMAIN(8): DocumentProcessing; CONCEPT(7): Reader; TECH(6): Python]
class BaseReader(ABC):
    """
    This class is a base class for reading documents of any formats.
    It allows to check if the specific reader can read the document of some format and
    to get document's text with metadata, tables and attachments.

    The metadata (or annotations) of the text are various and may include text boldness and color, footnotes or links to tables.
    Some of the readers can also extract information about line type and hierarchy level (for example, list item) -
    this information is stored in the `tag_hierarchy_level` attribute of the class :class:`~dedoc.data_structures.LineMetadata`.
    """
    # region METHOD___init__ [DOMAIN(7): DocumentProcessing; CONCEPT(6): Method; TECH(6): Python]
    def __init__(self, *, config: Optional[dict] = None, recognized_extensions: Optional[Set[str]] = None, recognized_mimes: Optional[Set[str]] = None) -> None:
        """
        :param config: configuration of the reader, e.g. logger for logging
        :param recognized_extensions: set of supported files extensions with a dot, for example {.doc, .pdf}
        :param recognized_mimes: set of supported MIME types of files
        """
        import logging

        self.config = {} if config is None else config
        self.logger = self.config.get("logger", logging.getLogger())
        self._recognized_extensions = {} if recognized_extensions is None else recognized_extensions
        self._recognized_mimes = {} if recognized_mimes is None else recognized_mimes
    # endregion METHOD___init__

    # region METHOD_can_read [DOMAIN(7): DocumentProcessing; CONCEPT(6): Method; TECH(6): Python]
    def can_read(self, file_path: Optional[str] = None, mime: Optional[str] = None, extension: Optional[str] = None, parameters: Optional[dict] = None) -> bool:
        """
        Check if this reader can handle the given file.
        You should provide at least one of the following parameters: file_path, extension, mime.

        :param file_path: path to the file in the file system
        :param mime: MIME type of a file
        :param extension: file extension, for example .doc or .pdf
        :param parameters: dict with additional parameters for document reader, see :ref:`parameters_description` for more details

        :return: True if this reader can handle the file, False otherwise
        """
        from dedoc.utils.utils import get_mime_extension

        mime, extension = get_mime_extension(file_path=file_path, mime=mime, extension=extension)
        return extension.lower() in self._recognized_extensions or mime in self._recognized_mimes

    # endregion METHOD_can_read

    # region METHOD_read [DOMAIN(7): DocumentProcessing; CONCEPT(6): Method; TECH(6): Python]
    @abstractmethod
    def read(self, file_path: str, parameters: Optional[dict] = None) -> UnstructuredDocument:
        """
        Read file from disk and extract text with annotations, tables and attachments from the document.
        The given file should have appropriate extension and mime type, so it should be checked by the method
        :meth:`~dedoc.readers.BaseReader.can_read`, which should return True beforehand.

        :param file_path: path to the file in the file system
        :param parameters: dict with additional parameters for document reader, see :ref:`parameters_description` for more details

        :return: intermediate representation of the document with lines, tables and attachments
        """
        pass
    # endregion METHOD_read

    # region METHOD__postprocess [DOMAIN(7): DocumentProcessing; CONCEPT(6): Method; TECH(6): Python]
    def _postprocess(self, document: UnstructuredDocument) -> UnstructuredDocument:
        """
        Perform document postprocessing.
        """
        return document
    # endregion METHOD__postprocess
# endregion CLASS_BaseReader


# region MODULE_CONTRACT [DOMAIN(8): DocumentProcessing; CONCEPT(7): Reader_base_reader; TECH(6): Python, dedoc]
## @modulecontract
## @purpose Define abstract base class for all document readers — the contract every format-specific reader must fulfill.
## @scope Document parsing pipeline: base (interface) format reading.
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
## CLASS [8][BaseReader reader/processor] => BaseReader
## @usecases
## - [read]: System (Pipeline) → ParseDocument(base (interface)) → UnstructuredDocument
def _module_contract():
    pass
# endregion MODULE_CONTRACT
# GREP_SUMMARY: base_reader, dedoc, reader, base (interface), BaseReader, ABC, abstract, UnstructuredDocument, reader, interface, document parsing, MIME, extension detection, abstract base, BaseReader
# STRUCTURE: ▶ Init ┌base (interface) file┐ → [BaseReader] ○ can_read? → ○ read → [__init__ → can_read → read] → ⊕ UnstructuredDocument(lines, tables, attachments)
