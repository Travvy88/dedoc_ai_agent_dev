import hashlib
import logging
import time
from typing import List

from bs4 import Tag

from dedoc.readers.docx_reader.data_structures.paragraph import Paragraph
from dedoc.readers.docx_reader.footnote_extractor import FootnoteExtractor
from dedoc.readers.docx_reader.numbering_extractor import NumberingExtractor
from dedoc.readers.docx_reader.styles_extractor import StylesExtractor


# region CLASS_Counter [DOMAIN(8): DocumentProcessing; CONCEPT(7): Reader; TECH(6): Python]
class Counter:

    # region METHOD___init__ [DOMAIN(7): DocumentProcessing; CONCEPT(6): Method; TECH(6): Python]
    def __init__(self, body: Tag, logger: logging.Logger) -> None:
        self.logger = logger
        self.total_paragraph_number = sum([len(p.find_all("w:p")) for p in body if p.name != "p" and p.name != "tbl" and isinstance(p, Tag)])
        self.total_paragraph_number += len([p for p in body if p.name == "p" and isinstance(p, Tag)])
        self.current_paragraph_number = 0
        self.checkpoint_time = time.time()

    # region METHOD_inc [DOMAIN(7): DocumentProcessing; CONCEPT(6): Method; TECH(6): Python]
    # endregion METHOD___init__
    def inc(self) -> None:
        self.current_paragraph_number += 1
        current_time = time.time()
        if current_time - self.checkpoint_time > 3:
            self.logger.info(f"Processed {self.current_paragraph_number} paragraphs from {self.total_paragraph_number}")
# endregion CLASS_Counter
            self.checkpoint_time = current_time


# region CLASS_ParagraphMaker [DOMAIN(8): DocumentProcessing; CONCEPT(7): Reader; TECH(6): Python]
    # endregion METHOD_inc
class ParagraphMaker:

    # region METHOD___init__ [DOMAIN(7): DocumentProcessing; CONCEPT(6): Method; TECH(6): Python]
    def __init__(self,
                 path_hash: str,
                 counter: Counter,
                 styles_extractor: StylesExtractor,
                 numbering_extractor: NumberingExtractor,
                 footnote_extractor: FootnoteExtractor,
                 endnote_extractor: FootnoteExtractor) -> None:
        self.counter = counter
        self.path_hash = path_hash
        self.styles_extractor = styles_extractor
        self.numbering_extractor = numbering_extractor
        self.footnote_extractor = footnote_extractor
        self.endnote_extractor = endnote_extractor
        self.uids_set = set()

    # region METHOD_make_paragraph [DOMAIN(7): DocumentProcessing; CONCEPT(6): Method; TECH(6): Python]
    # endregion METHOD___init__
    def make_paragraph(self, paragraph_xml: Tag, paragraph_list: List[Paragraph]) -> Paragraph:
        uid = self.__get_paragraph_uid(paragraph_xml=paragraph_xml)
        paragraph = Paragraph(xml=paragraph_xml,
                              styles_extractor=self.styles_extractor,
                              numbering_extractor=self.numbering_extractor,
                              footnote_extractor=self.footnote_extractor,
                              endnote_extractor=self.endnote_extractor,
                              uid=uid)
        prev_paragraph = None if len(paragraph_list) == 0 else paragraph_list[-1]
        paragraph.spacing = paragraph.spacing_before if prev_paragraph is None else max(prev_paragraph.spacing_after, paragraph.spacing_before)
        self.counter.inc()
        return paragraph

    # region METHOD___get_paragraph_uid [DOMAIN(7): DocumentProcessing; CONCEPT(6): Method; TECH(6): Python]
    # endregion METHOD_make_paragraph
    def __get_paragraph_uid(self, paragraph_xml: Tag) -> str:
        xml_hash = hashlib.md5(paragraph_xml.encode()).hexdigest()
        raw_uid = f"{self.path_hash}_{xml_hash}"
        uid = raw_uid
        n = 0
        while uid in self.uids_set:
            n += 1
            uid = f"{raw_uid}_{n}"
        self.uids_set.add(uid)
# endregion CLASS_ParagraphMaker
        return uid

    # endregion METHOD___get_paragraph_uid


# region MODULE_CONTRACT [DOMAIN(8): DocumentProcessing; CONCEPT(7): Reader_utils; TECH(6): Python, dedoc]
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
## CLASS [4][Counter reader/processor] => Counter
## CLASS [6][ParagraphMaker reader/processor] => ParagraphMaker
## @usecases
## - [read]: System (Pipeline) → ParseDocument(DOCX) → UnstructuredDocument
def _module_contract():
    pass
# endregion MODULE_CONTRACT
# GREP_SUMMARY: utils, dedoc, reader, DOCX, DocxReader, BaseReader, DOCX, Word, UnstructuredDocument, LineWithMeta, attachments, numbering, styles, properties, paragraph, footnote, Counter, ParagraphMaker
# STRUCTURE: ▶ Init ┌DOCX file┐ → [Counter] ○ can_read? → ○ read → [__init__ → inc] → ⊕ UnstructuredDocument(lines, tables, attachments)
