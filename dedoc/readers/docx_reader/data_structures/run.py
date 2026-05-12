from typing import Optional

from bs4 import Tag

import logging

logger = logging.getLogger(__name__)

from dedoc.readers.docx_reader.data_structures.base_props import BaseProperties
from dedoc.readers.docx_reader.properties_extractor import change_caps


# region CLASS_Run [DOMAIN(8): DocumentProcessing; CONCEPT(7): Reader; TECH(6): Python]
class Run(BaseProperties):

    # region METHOD___init__ [DOMAIN(7): DocumentProcessing; CONCEPT(6): Method; TECH(6): Python]
    def __init__(self, properties: Optional[BaseProperties], styles_extractor: "StylesExtractor") -> None:  # noqa
        """
        Contains information about run properties.
        :param properties: Paragraph or Run for copying its properties
        :param styles_extractor: StylesExtractor
        """

        self.name2char = dict(tab="\t", br="\n", cr="\r")
        self.text = ""
        self.styles_extractor = styles_extractor
        super().__init__(properties)

    # region METHOD_get_text [DOMAIN(7): DocumentProcessing; CONCEPT(6): Method; TECH(6): Python]
    # endregion METHOD___init__
    def get_text(self, xml: Tag) -> None:
        """
        Makes the text of run.
        :param xml: BeautifulSoup tree with run properties
        """
        for tag in xml:
            tag_name = tag.name

            if tag_name in self.name2char:
                self.text += self.name2char[tag_name]
                continue

            if tag_name == "t" and tag.text:
                self.text += tag.text

            elif tag_name == "sym":
                try:
                    self.text += chr(int("0x" + tag["w:char"], 16))
                except KeyError:
                    pass

        change_caps(self, xml)
        if hasattr(self, "caps") and xml.caps:
            self.text = self.text.upper()

    # region METHOD___repr__ [DOMAIN(7): DocumentProcessing; CONCEPT(6): Method; TECH(6): Python]
    # endregion METHOD_get_text
    def __repr__(self) -> str:
        text = self.text[:30].replace("\n", r"\n")
        return f"Run({text})"

    # region METHOD___eq__ [DOMAIN(7): DocumentProcessing; CONCEPT(6): Method; TECH(6): Python]
    # endregion METHOD___repr__
    def __eq__(self, other: "Run") -> bool:
        if not isinstance(other, Run):
            return False

        size_eq = self.size == other.size
        font_eq = self.bold == other.bold and self.italic == other.italic and self.underlined == other.underlined
        script_eq = self.superscript == other.superscript and self.subscript == other.subscript
# endregion CLASS_Run
        return size_eq and font_eq and script_eq

    # endregion METHOD___eq__


# region MODULE_CONTRACT [DOMAIN(8): DocumentProcessing; CONCEPT(7): Reader_run; TECH(6): Python, dedoc]
## @modulecontract
## @purpose Read and parse DOCX documents, extracting lines with metadata, tables, and attachments into UnstructuredDocument.
## @scope Data model definitions.
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
## CLASS [8][Run reader/processor] => Run
## @usecases
## - [read]: System (Pipeline) → ParseDocument(DOCX) → UnstructuredDocument
def _module_contract():
    pass
# endregion MODULE_CONTRACT
# GREP_SUMMARY: run, dedoc, reader, DOCX, DocxReader, BaseReader, DOCX, Word, UnstructuredDocument, LineWithMeta, attachments, numbering, styles, properties, paragraph, footnote, Run
# STRUCTURE: ▶ Init ┌DOCX file┐ → [Run] ○ can_read? → ○ read → [__init__ → get_text → __repr__] → ⊕ UnstructuredDocument(lines, tables, attachments)
