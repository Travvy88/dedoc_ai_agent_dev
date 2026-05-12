from typing import List

from dedoc.data_structures.line_with_meta import LineWithMeta
from dedoc.data_structures.unstructured_document import UnstructuredDocument
from dedoc.readers.html_reader.html_tags import HtmlTags

import logging

logger = logging.getLogger(__name__)


# region CLASS_HtmlLinePostprocessing [DOMAIN(8): DocumentProcessing; CONCEPT(7): Reader; TECH(6): Python]
class HtmlLinePostprocessing:

    # region METHOD_postprocess [DOMAIN(7): DocumentProcessing; CONCEPT(6): Method; TECH(6): Python]
    def postprocess(self, document: UnstructuredDocument) -> UnstructuredDocument:
        lines = self.__lines_postprocessing(document.lines)
        document.lines = lines
        return document

    # region METHOD___lines_postprocessing [DOMAIN(7): DocumentProcessing; CONCEPT(6): Method; TECH(6): Python]
    # endregion METHOD_postprocess
    def __lines_postprocessing(self, lines: List[LineWithMeta]) -> List[LineWithMeta]:
        lines = self.__add_newlines(lines)
        lines = self.__fix_special_symbols(lines)
        for line_id, line in enumerate(lines):
            line.metadata.line_id = line_id
        return lines

    # region METHOD___add_newlines [DOMAIN(7): DocumentProcessing; CONCEPT(6): Method; TECH(6): Python]
    # endregion METHOD___lines_postprocessing
    def __add_newlines(self, lines: List[LineWithMeta]) -> List[LineWithMeta]:
        for line, next_line in zip(lines[:-1], lines[1:]):
            next_line_tag = getattr(next_line.metadata, "html_tag", None)
            if not line.line.endswith("\n") and next_line_tag in HtmlTags.paragraphs:
                line.set_line(line.line + "\n")
        return lines

    # region METHOD___fix_special_symbols [DOMAIN(7): DocumentProcessing; CONCEPT(6): Method; TECH(6): Python]
    # endregion METHOD___add_newlines
    def __fix_special_symbols(self, lines: List[LineWithMeta]) -> List[LineWithMeta]:
        """
        replace some special symbols to common symbols, e.q.
        "\xa0" -> " "
        @param lines:
        @return:
        """
        for line in lines:
            new_text = line.line.replace("\xa0", " ")
            line.set_line(new_text)
# endregion CLASS_HtmlLinePostprocessing
        return lines

    # endregion METHOD___fix_special_symbols


# region MODULE_CONTRACT [DOMAIN(8): DocumentProcessing; CONCEPT(7): Reader_html_line_postprocessing; TECH(6): Python, dedoc]
## @modulecontract
## @purpose Read and parse HTML documents, extracting lines with metadata, tables, and attachments into UnstructuredDocument.
## @scope Document parsing pipeline: HTML format reading.
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
## CLASS [8][HtmlLinePostprocessing reader/processor] => HtmlLinePostprocessing
## @usecases
## - [read]: System (Pipeline) → ParseDocument(HTML) → UnstructuredDocument
def _module_contract():
    pass
# endregion MODULE_CONTRACT
# GREP_SUMMARY: html_line_postprocessing, dedoc, reader, HTML, HtmlReader, BaseReader, HTML, tags, annotation, BeautifulSoup, line postprocessing, tag_hierarchy_level, HtmlLinePostprocessing
# STRUCTURE: ▶ Init ┌HTML file┐ → [HtmlLinePostprocessing] ○ can_read? → ○ read → [postprocess → __lines_postprocessing → __add_newlines] → ⊕ UnstructuredDocument(lines, tables, attachments)
