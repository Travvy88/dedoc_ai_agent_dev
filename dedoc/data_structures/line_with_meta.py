import logging
from typing import List, Optional, Sized, Union

from dedoc.api.schema.line_with_meta import LineWithMeta as ApiLineWithMeta
from dedoc.data_structures.annotation import Annotation
from dedoc.data_structures.line_metadata import LineMetadata
from dedoc.data_structures.serializable import Serializable

logger = logging.getLogger(__name__)


# region CLASS_LineWithMeta [DOMAIN(9): DocumentProcessing, DataStructures; CONCEPT(10): Line, Metadata; TECH(7): Python, API, AnnotationMerger]
## @purpose Structural unit of document — a line (or paragraph) of text with metadata and annotations. Supports slicing, joining, and splitting with annotation consistency.
class LineWithMeta(Sized, Serializable):
    """
    Structural unit of document - line (or paragraph) of text and its metadata.
    One LineWithMeta should not contain text from different logical parts of the document
    (for example, document title and raw text of the document should not be in the same line).
    Still the logical part of the document may be represented by more than one line (for example, document title may consist of many lines).
    """

    # region METHOD___init__ [DOMAIN(9): DocumentProcessing; CONCEPT(10): Line; TECH(7): Python]
    ## @purpose Initialize line with raw text, optional metadata, annotations, and auto-generated UID.
    ## @uses uuid.uuid1
    ## @io (str, Optional[LineMetadata], Optional[List[Annotation]], Optional[str]) -> None
    ## @complexity 3
    def __init__(self, line: str, metadata: Optional[LineMetadata] = None, annotations: Optional[List[Annotation]] = None, uid: str = None) -> None:
        """
        :param line: raw text of the document line
        :param metadata: metadata (related to the entire line, as line or page number, its hierarchy level)
        :param annotations: metadata that refers to some part of the text, for example, font size, font type, etc.
        :param uid: unique identifier of the line
        """
        from uuid import uuid1

        logger.debug(f"[IMP:4][LineWithMeta][INIT] line_len={len(line)}, annotations_count={len(annotations) if annotations else 0}, uid={uid}")
        self._line = line
        self._metadata = LineMetadata(page_id=0, line_id=None) if metadata is None else metadata
        self._annotations = [] if annotations is None else annotations
        self._uid = str(uuid1()) if uid is None else uid
        logger.debug(f"[IMP:4][LineWithMeta][INIT] LineWithMeta created: uid={self._uid}, len={len(line)}")
    # endregion METHOD___init__

    # region METHOD___len__ [DOMAIN(9): DocumentProcessing; CONCEPT(5): Size; TECH(5): Python]
    ## @purpose Return length of the raw text line.
    ## @io None -> int
    ## @complexity 1
    def __len__(self) -> int:
        return len(self._line)
    # endregion METHOD___len__

    # region METHOD_join [DOMAIN(9): DocumentProcessing; CONCEPT(9): LineMerging; TECH(6): Python]
    ## @purpose Join list of LineWithMeta with a delimiter, keeping annotations consistent via deepcopy and concatenation.
    ## @uses deepcopy
    ## @io (List[LineWithMeta], str) -> LineWithMeta
    ## @complexity 5
    @staticmethod
    def join(lines: List["LineWithMeta"], delimiter: str = "\n") -> "LineWithMeta":
        """
        Join list of lines with the given delimiter, keep annotations consistent.
        This method is similar to the python built-it join method for strings.

        :param lines: list of lines to join
        :param delimiter: delimiter to insert between lines
        :return: merged line
        """
        from copy import deepcopy

        logger.debug(f"[IMP:4][LineWithMeta][JOIN] Joining {len(lines)} lines with delimiter_len={len(delimiter)}")

        if len(lines) == 0:
            return LineWithMeta("")

        common_line = deepcopy(lines[0])

        for next_line in lines[1:]:
            common_line += delimiter
            common_line += next_line

        logger.debug(f"[IMP:4][LineWithMeta][JOIN] Joined result len={len(common_line)}")
        return common_line
    # endregion METHOD_join

    # region METHOD___lt__ [DOMAIN(9): DocumentProcessing; CONCEPT(5): Ordering; TECH(5): Python]
    ## @purpose Compare lines by raw text for ordering.
    ## @io (LineWithMeta) -> bool
    ## @complexity 1
    def __lt__(self, other: "LineWithMeta") -> bool:
        return self.line < other.line
    # endregion METHOD___lt__

    # region METHOD_split [DOMAIN(9): DocumentProcessing; CONCEPT(9): LineSplitting; TECH(7): Python, regex]
    ## @purpose Split this line by separator, keeping annotations consistent using regex boundary detection.
    ## @uses re
    ## @io str -> List[LineWithMeta]
    ## @complexity 6
    def split(self, sep: str) -> List["LineWithMeta"]:
        """
        Split this line into a list of lines, keep annotations consistent.
        This method does not remove any text from the line.

        :param sep: separator for splitting
        :return: list of split lines
        """
        import re

        logger.debug(f"[IMP:4][LineWithMeta][SPLIT] Splitting line len={len(self)} by sep_len={len(sep)}")

        if not sep:
            raise ValueError("empty separator")
        borders = set()
        for group in re.finditer(sep, self.line):
            borders.add(group.end())
        borders.add(0)
        borders.add(len(self.line))
        borders = sorted(borders)
        if len(borders) <= 2:
            return [self]
        result = []
        for start, end in zip(borders[:-1], borders[1:]):
            result.append(self[start:end])
        logger.debug(f"[IMP:4][LineWithMeta][SPLIT] Split into {len(result)} parts")
        return result
    # endregion METHOD_split

    # region METHOD___getitem__ [DOMAIN(9): DocumentProcessing; CONCEPT(7): LineSlicing; TECH(6): Python]
    ## @purpose Slice line with annotation consistency. Supports int index and slice (start:stop).
    ## @uses __extract_annotations_by_slice
    ## @io (Union[slice, int]) -> LineWithMeta
    ## @complexity 6
    def __getitem__(self, index: Union[slice, int]) -> "LineWithMeta":
        if isinstance(index, int):
            if len(self) == 0 or index >= len(self) or index < -len(self):
                raise IndexError("Get item on empty line")
            index %= len(self)
            return self[index: index + 1]
        if isinstance(index, slice):
            start = index.start if index.start else 0
            stop = index.stop if index.stop is not None else len(self)
            step = 1 if index.step is None else index.step
            if start < 0 or stop < 0 or step != 1:
                raise NotImplementedError()
            if start > len(self) or 0 < len(self) == start:
                raise IndexError("start > len(line)")

            annotations = self.__extract_annotations_by_slice(start, stop)
            return LineWithMeta(line=self.line[start: stop], metadata=self.metadata, annotations=annotations)
        else:
            raise TypeError("line indices must be integers")
    # endregion METHOD___getitem__

    # region METHOD___extract_annotations_by_slice [DOMAIN(9): DocumentProcessing; CONCEPT(8): AnnotationSlicing; TECH(6): Python]
    ## @purpose Extract annotations that overlap with the given slice, adjusting their start/end positions.
    ## @io (int, int) -> List[Annotation]
    ## @complexity 4
    def __extract_annotations_by_slice(self, start: int, stop: int) -> List[Annotation]:
        """
        Extract annotations for given slice.
        """
        assert start >= 0
        assert stop >= 0
        annotations = []
        for annotation in self.annotations:
            if start < annotation.end and stop > annotation.start:
                annotations.append(Annotation(
                    start=max(annotation.start, start) - start,
                    end=min(annotation.end, stop) - start,
                    name=annotation.name,
                    value=annotation.value))
        return annotations
    # endregion METHOD___extract_annotations_by_slice

    # region METHOD_line [DOMAIN(9): DocumentProcessing; CONCEPT(5): Property; TECH(5): Python]
    ## @purpose Get raw text of the document line.
    ## @io None -> str
    ## @complexity 1
    @property
    def line(self) -> str:
        """
        Raw text of the document line
        """
        return self._line
    # endregion METHOD_line

    # region METHOD_metadata [DOMAIN(9): DocumentProcessing; CONCEPT(5): Property; TECH(5): Python]
    ## @purpose Get line metadata (page ID, line ID, hierarchy level).
    ## @io None -> LineMetadata
    ## @complexity 1
    @property
    def metadata(self) -> LineMetadata:
        """
        Line metadata related to the entire line, as line or page number, hierarchy level
        """
        return self._metadata
    # endregion METHOD_metadata

    # region METHOD_annotations [DOMAIN(9): DocumentProcessing; CONCEPT(5): Property; TECH(5): Python]
    ## @purpose Get list of annotations (font size, font type, etc.).
    ## @io None -> List[Annotation]
    ## @complexity 1
    @property
    def annotations(self) -> List[Annotation]:
        """
        Metadata that refers to some part of the text, for example, font size, font type, etc.
        """
        return self._annotations
    # endregion METHOD_annotations

    # region METHOD_uid [DOMAIN(9): DocumentProcessing; CONCEPT(5): Property; TECH(5): Python]
    ## @purpose Get unique identifier of the line.
    ## @io None -> str
    ## @complexity 1
    @property
    def uid(self) -> str:
        """
        Unique identifier of the line
        """
        return self._uid
    # endregion METHOD_uid

    # region METHOD_set_line [DOMAIN(9): DocumentProcessing; CONCEPT(5): Mutation; TECH(5): Python]
    ## @purpose Set raw text of the line.
    ## @io str -> None
    ## @complexity 1
    def set_line(self, line: str) -> None:
        logger.debug(f"[IMP:4][LineWithMeta][SET_LINE] Changing line text, new_len={len(line)}")
        self._line = line
    # endregion METHOD_set_line

    # region METHOD_set_metadata [DOMAIN(9): DocumentProcessing; CONCEPT(5): Mutation; TECH(5): Python]
    ## @purpose Set line metadata.
    ## @io LineMetadata -> None
    ## @complexity 1
    def set_metadata(self, metadata: LineMetadata) -> None:
        logger.debug(f"[IMP:4][LineWithMeta][SET_METADATA] Changing metadata, new_page_id={metadata.page_id}")
        self._metadata = metadata
    # endregion METHOD_set_metadata

    # region METHOD___repr__ [DOMAIN(9): DocumentProcessing; CONCEPT(5): Display; TECH(5): Python]
    ## @purpose Return repr with truncated text and hierarchy level info.
    ## @io None -> str
    ## @complexity 2
    def __repr__(self) -> str:
        text = self.line if len(self.line) < 65 else self.line[:62] + "..."
        tag_hl = "None" if self.metadata.tag_hierarchy_level is None else \
            f"{self.metadata.tag_hierarchy_level.level_1, self.metadata.tag_hierarchy_level.level_2, self.metadata.tag_hierarchy_level.line_type}"
        hl = "None" if self.metadata.hierarchy_level is None else \
            f"{self.metadata.hierarchy_level.level_1, self.metadata.hierarchy_level.level_2, self.metadata.hierarchy_level.line_type}"
        return f"LineWithMeta({text.strip()}, tagHL={tag_hl}, HL={hl})"
    # endregion METHOD___repr__

    # region METHOD___add__ [DOMAIN(9): DocumentProcessing; CONCEPT(8): LineConcatenation; TECH(7): Python, AnnotationMerger]
    ## @purpose Concatenate two LineWithMeta or a LineWithMeta with a string, merging annotations.
    ## @uses AnnotationMerger
    ## @io (Union[LineWithMeta, str]) -> LineWithMeta
    ## @complexity 6
    def __add__(self, other: Union["LineWithMeta", str]) -> "LineWithMeta":
        from dedoc.utils.annotation_merger import AnnotationMerger

        assert isinstance(other, (LineWithMeta, str))
        if len(other) == 0:
            return self
        if isinstance(other, str):
            line = self.line + other
            return LineWithMeta(line=line, metadata=self._metadata, annotations=self.annotations, uid=self.uid)
        line = self.line + other.line
        shift = len(self)
        other_annotations = []
        for annotation in other.annotations:
            new_annotation = Annotation(start=annotation.start + shift, end=annotation.end + shift, name=annotation.name, value=annotation.value)
            other_annotations.append(new_annotation)
        annotations = AnnotationMerger().merge_annotations(self.annotations + other_annotations, text=line)
        return LineWithMeta(line=line, metadata=self._metadata, annotations=annotations, uid=self.uid)
    # endregion METHOD___add__

    # region METHOD_to_api_schema [DOMAIN(9): DocumentProcessing; CONCEPT(8): Serialization; TECH(6): API]
    ## @purpose Convert line with metadata to API schema, serializing annotations.
    ## @uses ApiLineWithMeta
    ## @io None -> ApiLineWithMeta
    ## @complexity 3
    def to_api_schema(self) -> ApiLineWithMeta:
        logger.debug(f"[IMP:4][LineWithMeta][TO_API] Converting to API schema")
        annotations = [annotation.to_api_schema() for annotation in self.annotations]
        return ApiLineWithMeta(text=self._line, annotations=annotations)
    # endregion METHOD_to_api_schema

    # region METHOD_shift [DOMAIN(9): DocumentProcessing; CONCEPT(7): CoordinateTransform; TECH(6): Python, BBox]
    ## @purpose Shift bounding box annotations by given deltas and update relative coordinates.
    ## @uses BBoxAnnotation, json
    ## @io (int, int, int, int) -> None
    ## @complexity 5
    def shift(self, shift_x: int, shift_y: int, image_width: int, image_height: int) -> None:
        import json
        from dedoc.data_structures.concrete_annotations.bbox_annotation import BBoxAnnotation

        logger.debug(f"[IMP:4][LineWithMeta][SHIFT] shift_x={shift_x}, shift_y={shift_y}, image_w={image_width}, image_h={image_height}")
        for annotation in self.annotations:
            if annotation.name == "bounding box":
                bbox, page_width, page_height = BBoxAnnotation.get_bbox_from_value(annotation.value)
                bbox.shift(shift_x, shift_y)
                annotation.value = json.dumps(bbox.to_relative_dict(image_width, image_height))
        logger.debug(f"[IMP:4][LineWithMeta][SHIFT] Applied shift to bounding box annotations")
    # endregion METHOD_shift
# endregion CLASS_LineWithMeta

# region MODULE_CONTRACT [DOMAIN(9): DocumentProcessing, DataStructures; CONCEPT(10): Line, Metadata, Annotations; TECH(7): Python, API, AnnotationMerger, BBox]
## @modulecontract
## @purpose Define the LineWithMeta data structure — the fundamental building block of document text with rich metadata and annotation-aware slicing/joining/splitting.
## @scope Text line with metadata: slicing, joining, splitting, concatenation, annotation merging, coordinate shifting.
## @input Raw text string, optional LineMetadata, optional Annotation list, optional UID.
## @output LineWithMeta instances with annotation-consistent operations.
## @links [INHERITS(5): Serializable, Sized, USES_API(8): ApiLineWithMeta, READS_DATA_FROM(9): LineMetadata, Annotation, AnnotationMerger, BBoxAnnotation]
## @invariants
## - UID is always auto-generated if not provided
## - annotations list is never None (defaults to empty list)
## - metadata is never None (defaults to page_id=0, line_id=None)
## @rationale
## Q: Why implement slicing/joining with annotation awareness?
## A: Annotations reference character positions; slicing without adjusting annotations would produce incorrect metadata. This class guarantees annotation integrity across all text operations.
## @changes
## LAST_CHANGE: [v1.0.0 – Added semantic markup and LDD logging]
## @modulemap
## CLASS 10[Document line with metadata and annotations] => LineWithMeta
## METHOD 6[Constructor] => __init__
## METHOD 8[Join lines] => join
## METHOD 7[Split line] => split
## METHOD 7[Slice line] => __getitem__
## METHOD 8[Concatenate] => __add__
## METHOD 6[Shift bbox] => shift
## METHOD 8[API schema] => to_api_schema
## @usecases
## - [LineWithMeta]: Reader → CreateLineWithMeta → LineStored
## - [LineWithMeta]: StructureExtractor → SliceLine → AnnotationConsistentSlice
def _module_contract():
    pass
# endregion MODULE_CONTRACT
# GREP_SUMMARY: LineWithMeta, line, text, metadata, annotations, document, join, split, slice, concatenate, shift, bbox, API, serializable
# STRUCTURE: ▶ LineWithMeta ┌line(_line), metadata(_metadata), annotations(_annotations), uid(_uid)┐ → ◇ join (deepcopy + __add__) → ◇ split (re.finditer borders) → ◇ __getitem__ (int/slice + annotation extraction) → ◇ __add__ (AnnotationMerger) → ⊕ shift (BBoxAnnotation) → ⊕ to_api_schema → ⎋ ApiLineWithMeta
