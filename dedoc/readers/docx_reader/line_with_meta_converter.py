from dedoc.data_structures.concrete_annotations.alignment_annotation import AlignmentAnnotation
from dedoc.data_structures.concrete_annotations.bold_annotation import BoldAnnotation
from dedoc.data_structures.concrete_annotations.indentation_annotation import IndentationAnnotation
from dedoc.data_structures.concrete_annotations.italic_annotation import ItalicAnnotation
from dedoc.data_structures.concrete_annotations.linked_text_annotation import LinkedTextAnnotation
from dedoc.data_structures.concrete_annotations.size_annotation import SizeAnnotation
from dedoc.data_structures.concrete_annotations.spacing_annotation import SpacingAnnotation
from dedoc.data_structures.concrete_annotations.strike_annotation import StrikeAnnotation
from dedoc.data_structures.concrete_annotations.style_annotation import StyleAnnotation
from dedoc.data_structures.concrete_annotations.subscript_annotation import SubscriptAnnotation
from dedoc.data_structures.concrete_annotations.superscript_annotation import SuperscriptAnnotation
from dedoc.data_structures.concrete_annotations.underlined_annotation import UnderlinedAnnotation
from dedoc.data_structures.hierarchy_level import HierarchyLevel
from dedoc.data_structures.line_metadata import LineMetadata
from dedoc.data_structures.line_with_meta import LineWithMeta
from dedoc.readers.docx_reader.data_structures.paragraph import Paragraph
from dedoc.utils.annotation_merger import AnnotationMerger

import logging

logger = logging.getLogger(__name__)


# region CLASS_LineWithMetaConverter [DOMAIN(8): DocumentProcessing; CONCEPT(7): Reader; TECH(6): Python]
class LineWithMetaConverter:

    # region METHOD___init__ [DOMAIN(7): DocumentProcessing; CONCEPT(6): Method; TECH(6): Python]
    def __init__(self, paragraph: Paragraph, paragraph_id: int) -> None:
        """
        Converts custom DOCX Paragraph to LineWithMeta class.
        :param paragraph: Paragraph for converting its properties to the unified representation.
        """
        annotations = [BoldAnnotation, ItalicAnnotation, UnderlinedAnnotation, StrikeAnnotation, SuperscriptAnnotation, SubscriptAnnotation]
        self.dict2annotation = {annotation.name: annotation for annotation in annotations}
        self.annotation_merger = AnnotationMerger()

        self.paragraph = paragraph
        self.line = self.__parse(paragraph, paragraph_id)

    # region METHOD___parse [DOMAIN(7): DocumentProcessing; CONCEPT(6): Method; TECH(6): Python]
    # endregion METHOD___init__
    def __parse(self, paragraph: Paragraph, paragraph_id: int) -> LineWithMeta:
        annotations = [
            IndentationAnnotation(start=0, end=len(paragraph.text), value=str(paragraph.indentation)),
            AlignmentAnnotation(start=0, end=len(paragraph.text), value=paragraph.jc),
            SpacingAnnotation(start=0, end=len(paragraph.text), value=str(paragraph.spacing))
        ]
        for footnote in paragraph.footnotes:
            annotations.append(LinkedTextAnnotation(start=0, end=len(paragraph.text), value=footnote))

        if paragraph.style_name is not None:
            annotations.append(StyleAnnotation(start=0, end=len(paragraph.text), value=paragraph.style_name))

        assert len(paragraph.runs) == len(paragraph.runs_ids)

        for run, (start, end) in zip(paragraph.runs, paragraph.runs_ids):
            annotations.append(SizeAnnotation(start=start, end=end, value=str(run.size / 2)))
            for property_name in ["bold", "italic", "underlined", "strike", "superscript", "subscript"]:
                property_value = getattr(run, property_name)
                if property_value:
                    annotations.append(self.dict2annotation[property_name](start=start, end=end, value=str(property_value)))
        annotations = self.annotation_merger.merge_annotations(annotations, paragraph.text)

        metadata = LineMetadata(page_id=0, line_id=paragraph_id, tag_hierarchy_level=self.__get_tag(paragraph))
        return LineWithMeta(line=paragraph.text, metadata=metadata, annotations=annotations, uid=paragraph.uid)

    # region METHOD___get_tag [DOMAIN(7): DocumentProcessing; CONCEPT(6): Method; TECH(6): Python]
    # endregion METHOD___parse
    def __get_tag(self, paragraph: Paragraph) -> HierarchyLevel:
        # TODO toc, toc_item, bullet_list
        if paragraph.style_level is not None:
            return HierarchyLevel(1, paragraph.style_level, False, HierarchyLevel.header)

        if paragraph.list_level is not None:
            return HierarchyLevel(2, paragraph.list_level, False, HierarchyLevel.list_item)

# endregion CLASS_LineWithMetaConverter
        return HierarchyLevel.create_unknown()

    # endregion METHOD___get_tag


# region MODULE_CONTRACT [DOMAIN(8): DocumentProcessing; CONCEPT(7): Reader_line_with_meta_converter; TECH(6): Python, dedoc]
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
## CLASS [6][LineWithMetaConverter reader/processor] => LineWithMetaConverter
## @usecases
## - [read]: System (Pipeline) → ParseDocument(DOCX) → UnstructuredDocument
def _module_contract():
    pass
# endregion MODULE_CONTRACT
# GREP_SUMMARY: line_with_meta_converter, dedoc, reader, DOCX, DocxReader, BaseReader, DOCX, Word, UnstructuredDocument, LineWithMeta, attachments, numbering, styles, properties, paragraph, footnote, LineWithMetaConverter
# STRUCTURE: ▶ Init ┌DOCX file┐ → [LineWithMetaConverter] ○ can_read? → ○ read → [__init__ → __parse → __get_tag] → ⊕ UnstructuredDocument(lines, tables, attachments)
