from typing import List, Optional

from dedoc.data_structures.line_with_meta import LineWithMeta
from dedoc.data_structures.unstructured_document import UnstructuredDocument
from dedoc.readers.base_reader import BaseReader


# region CLASS_DocxReader [DOMAIN(8): DocumentProcessing; CONCEPT(7): Reader; TECH(6): Python]
class DocxReader(BaseReader):
    """
    This class is used for parsing documents with .docx extension.
    Please use :class:`~dedoc.converters.DocxConverter` for getting docx file from similar formats.
    """

    # region METHOD___init__ [DOMAIN(7): DocumentProcessing; CONCEPT(6): Method; TECH(6): Python]
    def __init__(self, *, config: Optional[dict] = None) -> None:
        from dedoc.attachments_extractors.concrete_attachments_extractors.docx_attachments_extractor import DocxAttachmentsExtractor
        from dedoc.extensions import recognized_extensions, recognized_mimes

        super().__init__(config=config, recognized_extensions=recognized_extensions.docx_like_format, recognized_mimes=recognized_mimes.docx_like_format)
        self.attachment_extractor = DocxAttachmentsExtractor(config=self.config)

    # region METHOD_read [DOMAIN(7): DocumentProcessing; CONCEPT(6): Method; TECH(6): Python]
    # endregion METHOD___init__
    def read(self, file_path: str, parameters: Optional[dict] = None) -> UnstructuredDocument:
        """
        The method return document content with all document's lines, tables and attachments.
        This reader is able to add some additional information to the `tag_hierarchy_level` of :class:`~dedoc.data_structures.LineMetadata`.
        Look to the documentation of :meth:`~dedoc.readers.BaseReader.read` to get information about the method's parameters.
        """
        from dedoc.readers.docx_reader.data_structures.docx_document import DocxDocument
        from dedoc.utils.parameter_utils import get_param_with_attachments

        with_attachments = get_param_with_attachments(parameters)
        attachments = self.attachment_extractor.extract(file_path=file_path, parameters=parameters) if with_attachments else []

        docx_document = DocxDocument(path=file_path, attachments=attachments, logger=self.logger)
        lines = self.__fix_lines(docx_document.lines)
        return UnstructuredDocument(lines=lines, tables=docx_document.tables, attachments=attachments, warnings=[])

    # region METHOD___fix_lines [DOMAIN(7): DocumentProcessing; CONCEPT(6): Method; TECH(6): Python]
    # endregion METHOD_read
    def __fix_lines(self, lines: List[LineWithMeta]) -> List[LineWithMeta]:
        from dedoc.data_structures.hierarchy_level import HierarchyLevel

        for i, line in enumerate(lines[1:]):
            if lines[i].metadata.tag_hierarchy_level != line.metadata.tag_hierarchy_level \
                    or lines[i].metadata.tag_hierarchy_level.line_type != HierarchyLevel.unknown \
                    or lines[i].line.endswith("\n"):
                continue

            old_len = len(lines[i].line)
            lines[i].set_line(lines[i].line + "\n")

            for annotation in lines[i].annotations:
                if annotation.end == old_len:
                    annotation.end += 1

# endregion CLASS_DocxReader
        return lines

    # endregion METHOD___fix_lines


# region MODULE_CONTRACT [DOMAIN(8): DocumentProcessing; CONCEPT(7): Reader_docx_reader; TECH(6): Python, dedoc]
## @modulecontract
## @purpose Read and parse DOCX documents, extracting lines with metadata, tables, and attachments into UnstructuredDocument.
## @scope Document parsing pipeline: DOCX format reading.
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
## CLASS [6][DocxReader reader/processor] => DocxReader
## @usecases
## - [read]: System (Pipeline) → ParseDocument(DOCX) → UnstructuredDocument
def _module_contract():
    pass
# endregion MODULE_CONTRACT
# GREP_SUMMARY: docx_reader, dedoc, reader, DOCX, DocxReader, BaseReader, DOCX, Word, UnstructuredDocument, LineWithMeta, attachments, numbering, styles, properties, paragraph, footnote, DocxReader
# STRUCTURE: ▶ Init ┌DOCX file┐ → [DocxReader] ○ can_read? → ○ read → [__init__ → read → __fix_lines] → ⊕ UnstructuredDocument(lines, tables, attachments)
