import logging
import re
from enum import Enum
from typing import List, Optional

from bs4 import BeautifulSoup, Tag

from dedoc.readers.docx_reader.data_structures.base_props import BaseProperties
from dedoc.readers.docx_reader.data_structures.run import Run
from dedoc.readers.docx_reader.properties_extractor import change_paragraph_properties, change_run_properties


# region CLASS_StyleType [DOMAIN(8): DocumentProcessing; CONCEPT(7): Reader; TECH(6): Python]
class StyleType(Enum):
    CHARACTER = "character"
    PARAGRAPH = "paragraph"
# endregion CLASS_StyleType
    NUMBERING = "numbering"


# region CLASS_StylesExtractor [DOMAIN(8): DocumentProcessing; CONCEPT(7): Reader; TECH(6): Python]
class StylesExtractor:

    # region METHOD___init__ [DOMAIN(7): DocumentProcessing; CONCEPT(6): Method; TECH(6): Python]
    def __init__(self, xml: Optional[BeautifulSoup], logger: logging.Logger) -> None:
        """
        :param xml: BeautifulSoup tree with styles
        :param logger: logger
        """
        if not xml or not xml.styles:
            raise Exception("Corrupted XML file with styles")

        self.logger = logger
        self.styles = xml.styles
        self.numbering_extractor = None

        # extract information from docDefaults
        # docDefaults: rPrDefault + pPrDefault
        self.doc_defaults = self.styles.docDefaults
        self.default_style = self.styles.find_all("w:style", attrs={"w:default": "1", "w:type": "paragraph"})
        self.default_style = self.default_style[0] if self.default_style else None

        self.__styles_cache = {}
        self.__styles_hierarchy_cache = {}
        self.style_regexp = re.compile(r"heading\s*(\d+)")

    # region METHOD_parse [DOMAIN(7): DocumentProcessing; CONCEPT(6): Method; TECH(6): Python]
    # endregion METHOD___init__
    def parse(self, style_id: Optional[str], old_properties: BaseProperties, style_type: StyleType) -> None:
        """
        Change old_properties according to style's properties.
        If style_id is None find default style else find style with given style_id and
        :param style_id: styleId for style
        :param old_properties: properties for saving style properties
        :param style_type: "paragraph", "character" or "numbering" ("numbering" is auxiliary, it will be changed as "paragraph")
        """

        if self.doc_defaults:
            change_paragraph_properties(old_properties, self.doc_defaults)
        if self.default_style:
            change_paragraph_properties(old_properties, self.default_style)

        # if styleId == None set default style
        if not style_id:
            return

        # it is used for prevent recursion because of style and numbering linking
        if style_type == StyleType.NUMBERING:
            ignore_num = True
            style_type = StyleType.PARAGRAPH
        else:
            ignore_num = False

        style = self.__find_style(style_id, style_type)
        if not style:
            return

        if hasattr(old_properties, "style_name"):
            name = style.find("w:name")
            old_properties.style_name = name["w:val"] if name else style_id
            old_properties.style_level = self.__get_heading_level(old_properties.style_name)

        styles = self.__get_styles_hierarchy(style, style_id, style_type)
        self.__apply_styles(old_properties, styles)

        # information in numPr for styles
        if style.numPr and self.numbering_extractor and hasattr(old_properties, "xml") and not old_properties.xml.numPr and not ignore_num:
            try:
                numbering_run = Run(old_properties, self)
                self.numbering_extractor.parse(style, old_properties, numbering_run)
                if hasattr(old_properties, "runs"):
                    old_properties.runs.append(numbering_run)
            except KeyError as error:
                self.logger.info(error)

    # region METHOD___get_styles_hierarchy [DOMAIN(7): DocumentProcessing; CONCEPT(6): Method; TECH(6): Python]
    # endregion METHOD_parse
    def __get_styles_hierarchy(self, style: Tag, style_id: str, style_type: StyleType) -> List[Tag]:
        """
        Make the list with styles hierarchy.
        :param style: the first style in the hierarchy
        :returns: the list with styles hierarchy
        """
        key = (style_id, style_type.value)
        if key in self.__styles_hierarchy_cache:
            return self.__styles_hierarchy_cache[key]

        styles = [style]
        current_style = style
        while current_style and current_style.basedOn:
            try:
                parent_style_id = current_style.basedOn["w:val"]
                current_style = self.__find_style(parent_style_id, style_type)
                if current_style:
                    styles.append(current_style)
            except KeyError:
                pass

        styles = styles[::-1]
        self.__styles_hierarchy_cache[key] = styles
        return styles

    # region METHOD___apply_styles [DOMAIN(7): DocumentProcessing; CONCEPT(6): Method; TECH(6): Python]
    # endregion METHOD___get_styles_hierarchy
    def __apply_styles(self, old_properties: BaseProperties, styles: List[Tag]) -> None:
        """
        Applies all styles to old_properties according to the hierarchy:
        defaults -> paragraph -> numbering -> character
        :param old_properties: properties for changing
        :param styles: styles in order to apply
        """
        for current_style in styles:
            if current_style.pPr:
                change_paragraph_properties(old_properties, current_style.pPr)
            if current_style.rPr:
                change_run_properties(old_properties, current_style.rPr)

    # region METHOD___find_style [DOMAIN(7): DocumentProcessing; CONCEPT(6): Method; TECH(6): Python]
    # endregion METHOD___apply_styles
    def __find_style(self, style_id: str, style_type: StyleType) -> Optional[Tag]:
        """
        Finds style tree with given style_id and style_type.
        :param style_id: styleId for given style
        :param style_type: "paragraph" or "character"
        :return: None if there isn't such style else BeautifulSoup tree with style
        """
        key = (style_id, style_type.value)
        if key in self.__styles_cache:
            return self.__styles_cache[key]

        styles = self.styles.find_all("w:style", attrs={"w:styleId": style_id, "w:type": style_type.value})
        if not styles:
            return None

        result = styles[0]
        self.__styles_cache[key] = result
        return result

    # region METHOD___get_heading_level [DOMAIN(7): DocumentProcessing; CONCEPT(6): Method; TECH(6): Python]
    # endregion METHOD___find_style
    def __get_heading_level(self, style_name: str) -> Optional[int]:
        """
        :param style_name: name of the style
        :returns: level if style name begins with heading else None
        """
        if style_name.lower().strip() == "title":
            return 1
        match = self.style_regexp.match(style_name.lower())  # e.g. Heading 1
# endregion CLASS_StylesExtractor
        return int(match.groups()[0]) + 1 if match else None

    # endregion METHOD___get_heading_level


# region MODULE_CONTRACT [DOMAIN(8): DocumentProcessing; CONCEPT(7): Reader_styles_extractor; TECH(6): Python, dedoc]
## @modulecontract
## @purpose Read and parse DOCX documents, extracting lines with metadata, tables, and attachments into UnstructuredDocument.
## @scope Feature and metadata extraction from documents.
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
## CLASS [5][StyleType reader/processor] => StyleType
## CLASS [12][StylesExtractor reader/processor] => StylesExtractor
## @usecases
## - [read]: System (Pipeline) → ParseDocument(DOCX) → UnstructuredDocument
def _module_contract():
    pass
# endregion MODULE_CONTRACT
# GREP_SUMMARY: styles_extractor, dedoc, reader, DOCX, DocxReader, BaseReader, DOCX, Word, UnstructuredDocument, LineWithMeta, attachments, numbering, styles, properties, paragraph, footnote, StyleType, StylesExtractor
# STRUCTURE: ▶ Init ┌DOCX file┐ → [StyleType] ○ can_read? → ○ read → [read → can_read] → ⊕ UnstructuredDocument(lines, tables, attachments)
