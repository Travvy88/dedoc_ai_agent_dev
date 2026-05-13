from collections import defaultdict
from typing import List

import logging

logger = logging.getLogger(__name__)

from bs4 import Tag

from dedoc.data_structures.line_with_meta import LineWithMeta
from dedoc.readers.pptx_reader.numbering_extractor import NumberingExtractor
from dedoc.readers.pptx_reader.paragraph import PptxParagraph
from dedoc.readers.pptx_reader.properties_extractor import PropertiesExtractor


# region CLASS_PptxShape [DOMAIN(8): DocumentProcessing; CONCEPT(7): Reader; TECH(6): Python]
class PptxShape:
    """
    This class corresponds to one textual block of the presentation (tag <a:sp>).
    """
    # region METHOD___init__ [DOMAIN(7): DocumentProcessing; CONCEPT(6): Method; TECH(6): Python]
    def __init__(self, xml: Tag, page_id: int, init_line_id: int, numbering_extractor: NumberingExtractor, properties_extractor: PropertiesExtractor,
                 is_title: bool = False) -> None:
        self.xml = xml
        self.page_id = page_id
        self.init_line_id = init_line_id
        self.numbering_extractor = numbering_extractor
        self.properties_extractor = properties_extractor
        self.is_title = is_title

    # region METHOD_get_lines [DOMAIN(7): DocumentProcessing; CONCEPT(6): Method; TECH(6): Python]
    # endregion METHOD___init__
    def get_lines(self) -> List[LineWithMeta]:
        if not self.xml.get_text().strip():
            return []

        if self.xml.ph and "title" in self.xml.ph.get("type", "").lower():
            self.is_title = True

        lines = []
        numbering2shift = defaultdict(int)
        prev_list_level = None

        for line_id, paragraph_xml in enumerate(self.xml.find_all("a:p")):
            paragraph = PptxParagraph(paragraph_xml, self.numbering_extractor, self.properties_extractor)

            if paragraph.numbered_list_type:
                if prev_list_level and paragraph.level > prev_list_level:
                    numbering2shift[(paragraph.numbered_list_type, paragraph.level)] = 0

                shift = numbering2shift[(paragraph.numbered_list_type, paragraph.level)]
                numbering2shift[(paragraph.numbered_list_type, paragraph.level)] += 1
                prev_list_level = paragraph.level
            else:
                shift = 0

            lines.append(paragraph.get_line_with_meta(line_id=self.init_line_id + line_id, page_id=self.page_id, is_title=self.is_title, shift=shift))

# endregion CLASS_PptxShape
        return lines

    # endregion METHOD_get_lines


# region MODULE_CONTRACT [DOMAIN(8): DocumentProcessing; CONCEPT(7): Reader_shape; TECH(6): Python, dedoc]
## @modulecontract
## @purpose Read and parse PPTX documents, extracting lines with metadata, tables, and attachments into UnstructuredDocument.
## @scope Document parsing pipeline: PPTX format reading.
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
## CLASS [4][PptxShape reader/processor] => PptxShape
## @usecases
## - [read]: System (Pipeline) → ParseDocument(PPTX) → UnstructuredDocument
def _module_contract():
    pass
# endregion MODULE_CONTRACT
# GREP_SUMMARY: shape, dedoc, reader, PPTX, PptxReader, BaseReader, PPTX, PowerPoint, slides, shapes, paragraphs, tables, numbering, properties, PptxShape
# STRUCTURE: ▶ Init ┌PPTX file┐ → [PptxShape] ○ can_read? → ○ read → [__init__ → get_lines] → ⊕ UnstructuredDocument(lines, tables, attachments)
