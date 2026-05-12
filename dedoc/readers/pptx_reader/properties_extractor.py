from dataclasses import dataclass
from typing import Dict, Optional

import logging

logger = logging.getLogger(__name__)

from bs4 import Tag


@dataclass
# region CLASS_Properties [DOMAIN(8): DocumentProcessing; CONCEPT(7): Reader; TECH(6): Python]
class Properties:
    bold: bool = False
    italic: bool = False
    underlined: bool = False
    superscript: bool = False
    subscript: bool = False
    strike: bool = False
    size: int = 0
    alignment: str = "left"
# endregion CLASS_Properties
    title: bool = False


# region CLASS_PropertiesExtractor [DOMAIN(8): DocumentProcessing; CONCEPT(7): Reader; TECH(6): Python]
class PropertiesExtractor:
    """
    This class allows to extract some text formatting properties (see class Properties)

    Properties hierarchy:

    - Run and paragraph properties (slide.xml)
    - Slide layout properties (slideLayout.xml) TODO
    - Master slide properties (slideMaster.xml) TODO
    - Presentation default properties (presentation.xml -> defaultTextStyle)
    """
    # region METHOD___init__ [DOMAIN(7): DocumentProcessing; CONCEPT(6): Method; TECH(6): Python]
    def __init__(self, file_path: str) -> None:
        self.alignment_mapping = dict(l="left", r="right", ctr="center", just="both", dist="both", justLow="both", thaiDist="both")
        self.lvl2default_properties = self.__get_default_properties_mapping(file_path)

    # region METHOD_get_properties [DOMAIN(7): DocumentProcessing; CONCEPT(6): Method; TECH(6): Python]
    # endregion METHOD___init__
    def get_properties(self, xml: Tag, level: int, properties: Optional[Properties] = None) -> Properties:
        """
        xml examples:
            <a:pPr indent="0" lvl="0" marL="0" rtl="0" algn="l">
            <a:rPr i="1" lang="ru" sz="1800">
            <a:rPr baseline="30000" lang="ru" sz="1800">
        """
        from copy import deepcopy

        properties = properties or self.lvl2default_properties.get(level, Properties())
        new_properties = deepcopy(properties)
        if not xml:
            return new_properties

        self.__update_properties(xml, new_properties)
        return new_properties

    # region METHOD___update_properties [DOMAIN(7): DocumentProcessing; CONCEPT(6): Method; TECH(6): Python]
    # endregion METHOD_get_properties
    def __update_properties(self, xml: Tag, properties: Properties) -> None:
        if int(xml.get("b", "0")):
            properties.bold = True
        if int(xml.get("i", "0")):
            properties.italic = True

        underlined = xml.get("u", "none").lower()
        if underlined != "none":
            properties.underlined = True

        strike = xml.get("strike", "nostrike").lower()
        if strike != "nostrike":
            properties.strike = True

        size = xml.get("sz")
        if size:
            properties.size = float(size) / 100

        baseline = xml.get("baseline")
        if baseline:
            if float(baseline) < 0:
                properties.subscript = True
            else:
                properties.superscript = True

        self.__update_alignment(xml, properties)

    # region METHOD___update_alignment [DOMAIN(7): DocumentProcessing; CONCEPT(6): Method; TECH(6): Python]
    # endregion METHOD___update_properties
    def __update_alignment(self, xml: Tag, properties: Properties) -> None:
        alignment = xml.get("algn")
        if alignment and alignment in self.alignment_mapping:
            properties.alignment = self.alignment_mapping[alignment]

    # region METHOD___get_default_properties_mapping [DOMAIN(7): DocumentProcessing; CONCEPT(6): Method; TECH(6): Python]
    # endregion METHOD___update_alignment
    def __get_default_properties_mapping(self, file_path: str) -> Dict[int, Properties]:
        from dedoc.utils.office_utils import get_bs_from_zip

        lvl2properties = {}

        presentation_xml = get_bs_from_zip(file_path, "ppt/presentation.xml", remove_spaces=True)
        default_style = presentation_xml.defaultTextStyle
        if not default_style:
            return lvl2properties

        # lvl1pPr - lvl9pPr
        for i in range(1, 10):
            level_xml = getattr(default_style, f"lvl{i}pPr")
            if level_xml:
                self.__update_level_properties(level_xml, lvl2properties)
        return lvl2properties

    # region METHOD___update_level_properties [DOMAIN(7): DocumentProcessing; CONCEPT(6): Method; TECH(6): Python]
    # endregion METHOD___get_default_properties_mapping
    def __update_level_properties(self, xml: Tag, lvl2properties: Dict[int, Properties]) -> None:
        """
        Example:
            <a:lvl1pPr lvl="0" marR="0" rtl="0" algn="l">
                <a:lnSpc><a:spcPct val="100000"/></a:lnSpc>
                <a:spcBef><a:spcPts val="0"/></a:spcBef>
                <a:spcAft><a:spcPts val="0"/></a:spcAft>
                <a:buClr><a:srgbClr val="000000"/></a:buClr>
                <a:buFont typeface="Arial"/>
                <a:defRPr b="0" i="0" sz="1400" u="none" cap="none" strike="noStrike">
                    <a:solidFill><a:srgbClr val="000000"/></a:solidFill>
                    <a:latin typeface="Arial"/>
                    <a:ea typeface="Arial"/>
                    <a:cs typeface="Arial"/>
                    <a:sym typeface="Arial"/>
                </a:defRPr>
            </a:lvl1pPr>
        """
        level = int(xml.get("lvl", "0")) + 1
        level_properties = lvl2properties.get(level, Properties())
        self.__update_alignment(xml, level_properties)
        if xml.defRPr:
            self.__update_properties(xml.defRPr, level_properties)

# endregion CLASS_PropertiesExtractor
        lvl2properties[level] = level_properties

    # endregion METHOD___update_level_properties


# region MODULE_CONTRACT [DOMAIN(8): DocumentProcessing; CONCEPT(7): Reader_properties_extractor; TECH(6): Python, dedoc]
## @modulecontract
## @purpose Read and parse PPTX documents, extracting lines with metadata, tables, and attachments into UnstructuredDocument.
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
## CLASS [5][Properties reader/processor] => Properties
## CLASS [12][PropertiesExtractor reader/processor] => PropertiesExtractor
## @usecases
## - [read]: System (Pipeline) → ParseDocument(PPTX) → UnstructuredDocument
def _module_contract():
    pass
# endregion MODULE_CONTRACT
# GREP_SUMMARY: properties_extractor, dedoc, reader, PPTX, PptxReader, BaseReader, PPTX, PowerPoint, slides, shapes, paragraphs, tables, numbering, properties, Properties, PropertiesExtractor
# STRUCTURE: ▶ Init ┌PPTX file┐ → [Properties] ○ can_read? → ○ read → [read → can_read] → ⊕ UnstructuredDocument(lines, tables, attachments)
