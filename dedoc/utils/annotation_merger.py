# region MODULE_CONTRACT [DOMAIN(7): DocumentProcessing; CONCEPT(8): AnnotationMerging; TECH(6): IntervalOverlap, DefaultDict]
## @modulecontract
## @purpose To merge overlapping and adjacent text annotations (like bold, italic spans) into contiguous annotation regions, resolving contradictions by type. Critical for producing clean annotation output from fragmented reader results.
## @scope Annotation grouping, merging overlapping annotations, filtering contradicting annotations, delete previous merged cleanup.
## @input List of Annotation objects, source text string.
## @output Merged and filtered list of Annotation objects.
## @links [USES_API(6): re, collections.defaultdict]
## @invariants
## - merge_annotations returns an empty list for empty input.
## - Annotations with different name/value pairs are never merged into a single annotation.
## - Non-mergeable annotations are passed through unmodified.
## @rationale
## Q: Why handle spaces explicitly as Space objects?
## A: Whitespace between annotations can bridge mergeable spans. Explicit space tracking prevents over-merging across paragraph breaks.
## @changes
## LAST_CHANGE: [v1.0.0 – Added SEMANTIC TEMPLATE markup and LDD logging]
## @modulemap
## CLASS 5[Whitespace interval model] => Space
## CLASS 7[Grouped annotation container] => ExtendedAnnotation
## CLASS 9[Core annotation merging logic] => AnnotationMerger
## @usecases
## - [AnnotationMerger.merge_annotations]: Reader → NormalizeAnnotations → Clean annotation list
def _module_contract():
    pass
# endregion MODULE_CONTRACT
# GREP_SUMMARY: annotation, merge, overlap, interval, bold, italic, text span, grouping, contradiction filtering
# STRUCTURE: ▶ ┌Annotation, Space, ExtendedAnnotation data models┐ → ⚡ AnnotationMerger ┌annotations,text┐ → group by (name,value) → ⊕ space positions via regex → ◇ per-group: sort+merge overlapping → filter contradictions → ⎋ merged_annotations

import logging
import re
from collections import defaultdict
from typing import Dict, List, Optional, Union

from dedoc.data_structures.annotation import Annotation

logger = logging.getLogger(__name__)


# region CLASS_Space [DOMAIN(5): DataStructures; CONCEPT(4): IntervalModel; TECH(3): TypedContainer]
## @purpose To represent a whitespace interval in text, used as a bridge element between mergeable annotations.
class Space:

    def __init__(self, start: int, end: int) -> None:
        self.start = start
        self.end = end
# endregion CLASS_Space


# region CLASS_ExtendedAnnotation [DOMAIN(7): DataStructures; CONCEPT(6): AnnotationGrouping; TECH(5): IntervalMerge]
## @purpose To hold a group of annotations and spaces that form a contiguous merged region, tracking span boundaries and providing a final merge() method.
class ExtendedAnnotation:

    # region METHOD___init__ [DOMAIN(7): DataStructures; TECH(4): Initialization]
    ## @purpose To initialize an ExtendedAnnotation with optional pre-existing annotations and spaces, computing the start/end boundaries.
    ## @complexity 3
    def __init__(self, annotations: List[Annotation] = None, spaces: List[Space] = None) -> None:
        self.annotations = annotations if annotations is not None else []
        self.spaces = spaces if spaces is not None else []
        self.start = self.get_start()
        self.end = self.get_end()
    # endregion METHOD___init__

    # region METHOD_add [DOMAIN(7): DataStructures; TECH(5): IntervalUnion]
    ## @purpose To add either an Annotation or Space to the group, extending the start/end boundaries accordingly.
    ## @io Union[Annotation, Space] -> ExtendedAnnotation
    ## @complexity 3
    def add(self, annotation: Union[Annotation, Space]) -> "ExtendedAnnotation":
        self.start = min(annotation.start, self.start) if self.start is not None else annotation.start
        self.end = max(annotation.end, self.end) if self.end is not None else annotation.end
        if isinstance(annotation, Annotation):
            self.annotations.append(annotation)
        else:
            self.spaces.append(annotation)
        return self
    # endregion METHOD_add

    # region PROPERTY_name
    @property
    def name(self) -> str:
        return self.annotations[0].name
    # endregion PROPERTY_name

    # region PROPERTY_value
    @property
    def value(self) -> str:
        return self.annotations[0].value
    # endregion PROPERTY_value

    # region PROPERTY_extended
    @property
    def extended(self) -> List[Union[Annotation, Space]]:
        return self.annotations + self.spaces
    # endregion PROPERTY_extended

    # region METHOD_get_start [DOMAIN(5): DataStructures; TECH(3): BoundaryQuery]
    ## @purpose To compute the minimum start position across all contained annotations and spaces.
    ## @io None -> Optional[int]
    ## @complexity 2
    def get_start(self) -> Optional[int]:
        if len(self.extended) == 0:
            return None
        return min((annotation.start for annotation in self.extended))
    # endregion METHOD_get_start

    # region METHOD_get_end [DOMAIN(5): DataStructures; TECH(3): BoundaryQuery]
    ## @purpose To compute the maximum end position across all contained annotations and spaces.
    ## @io None -> Optional[int]
    ## @complexity 2
    def get_end(self) -> Optional[int]:
        if len(self.extended) == 0:
            return None
        return max((annotation.end for annotation in self.extended))
    # endregion METHOD_get_end

    # region METHOD_merge [DOMAIN(7): DataStructures; TECH(5): AnnotationReduction]
    ## @purpose To collapse the grouped annotations into a single merged Annotation spanning the full range, or None if no annotations present.
    ## @io None -> Optional[Annotation]
    ## @complexity 3
    def merge(self) -> Optional[Annotation]:
        if len(self.annotations) == 0:
            return None
        else:
            start = min((a.start for a in self.annotations))
            end = max((a.end for a in self.annotations))
            annotation = self.annotations[0]
            return Annotation(start=start, end=end, value=annotation.value, name=annotation.name)
    # endregion METHOD_merge
# endregion CLASS_ExtendedAnnotation


# region CLASS_AnnotationMerger [DOMAIN(9): DocumentProcessing; CONCEPT(8): AnnotationMerging; TECH(7): IntervalOverlap, DefaultDict]
## @purpose To merge overlapping and adjacent annotations of the same type/value into contiguous spans, filter out contradictions, and clean up stale merges.
class AnnotationMerger:
    spaces = re.compile(r"\s+")

    # region METHOD_merge_annotations [DOMAIN(9): DocumentProcessing; CONCEPT(8): AnnotationMerging; TECH(7): IntervalMerge]
    ## @purpose To merge annotations across the full document text: group by name+value, merge overlapping groups, then filter contradicting overlaps.
    ## @uses _group_annotations, _merge_one_group, __filter_contradicting_annotations
    ## @io (List[Annotation], str) -> List[Annotation]
    ## @complexity 7
    def merge_annotations(self, annotations: List[Annotation], text: str) -> List[Annotation]:
        if not annotations:
            return []

        logger.debug(f"[IMP:5][AnnotationMerger][INIT] Merging {len(annotations)} annotations")
        annotations_group_by_name_value = self._group_annotations(annotations).values()
        spaces = [Space(m.start(), m.end()) for m in self.spaces.finditer(text)]

        merged = []
        for annotation_group in annotations_group_by_name_value:
            group = self._merge_one_group(annotations=annotation_group, spaces=spaces)
            merged.extend(group)

        filtered = self.__filter_contradicting_annotations(merged, text)
        logger.debug(f"[IMP:6][AnnotationMerger][RESULT] Merged: {len(annotations)} -> {len(filtered)} annotations")
        return filtered
    # endregion METHOD_merge_annotations

    # region METHOD__merge_one_group [DOMAIN(8): AnnotationMerging; TECH(6): IntervalUnion]
    ## @purpose To merge one group of same-name/same-value annotations, interleaving with spaces to detect adjacency.
    ## @io (List[Annotation], List[Space]) -> List[Annotation]
    ## @complexity 6
    def _merge_one_group(self, annotations: List[Annotation], spaces: List[Space]) -> List[Annotation]:
        if len(annotations) <= 1 or not annotations[0].is_mergeable:
            return annotations
        self.__check_annotations_group(annotations)
        result = []
        sorted_annotations = sorted(annotations + spaces, key=lambda a: a.start)
        left = 0
        right = 1
        current_annotation = ExtendedAnnotation().add(sorted_annotations[left])
        while right < len(sorted_annotations):
            right_annotation = sorted_annotations[right]
            if current_annotation.end >= right_annotation.start:
                current_annotation.add(right_annotation)
            else:
                result.append(current_annotation)
                current_annotation = ExtendedAnnotation().add(right_annotation)
            right += 1
        result.append(current_annotation)
        result_annotations = (extended.merge() for extended in result)
        return [annotation for annotation in result_annotations if annotation is not None]
    # endregion METHOD__merge_one_group

    # region METHOD___check_annotations_group [DOMAIN(6): Validation; TECH(4): Assertion]
    ## @purpose To assert that all annotations in a group share the same name and value, enforcing the invariant required for correct merging.
    ## @io List[Annotation] -> None
    ## @complexity 3
    def __check_annotations_group(self, annotations: List[Annotation]) -> None:
        if len(annotations) > 0:
            first = annotations[0]
            first_name_value = first.name, first.value
            same_name_value = all((annotation.name, annotation.value) == first_name_value for annotation in annotations)
            assert same_name_value, "all group items must have the same name and value"
    # endregion METHOD___check_annotations_group

    # region METHOD__group_annotations [DOMAIN(6): Grouping; TECH(5): DefaultDict]
    ## @purpose To group annotations by (name, value) tuple into a dictionary for batch processing.
    ## @io List[Annotation] -> Dict[str, List[Annotation]]
    ## @complexity 3
    @staticmethod
    def _group_annotations(annotations: List[Annotation]) -> Dict[str, List[Annotation]]:
        annotations_group_by_value = defaultdict(list)
        for annotation in annotations:
            annotations_group_by_value[(annotation.name, annotation.value)].append(annotation)
        return annotations_group_by_value
    # endregion METHOD__group_annotations

    # region METHOD___filter_contradicting_annotations [DOMAIN(8): AnnotationMerging; TECH(6): IntervalFiltering]
    ## @purpose To filter out merged annotations that contradict each other by overlapping in position, keeping only the latest valid annotation per position.
    ## @io (List[Annotation], str) -> List[Annotation]
    ## @complexity 6
    def __filter_contradicting_annotations(self, annotations: List[Annotation], text: str) -> List[Annotation]:
        annotations_by_type = defaultdict(list)
        for annotation in annotations:
            annotations_by_type[annotation.name].append(annotation)

        filtered = []
        for annotation_list in annotations_by_type.values():
            if not annotation_list[0].is_mergeable:
                filtered.extend(annotation_list)
                continue

            sorted_annotations = sorted(annotation_list, key=lambda x: x.start)
            prev_end = 0
            for annotation in sorted_annotations:
                if annotation.start >= prev_end:
                    filtered.append(annotation)
                    prev_end = annotation.end
                elif self.spaces.match(text[filtered[-1].start:filtered[-1].end]):
                    filtered[-1] = annotation
                    prev_end = annotation.end

        return filtered
    # endregion METHOD___filter_contradicting_annotations

    # region METHOD_delete_previous_merged [DOMAIN(7): Cleanup; TECH(5): ListMutation]
    ## @purpose To remove previously merged annotations that have been superseded by a new larger merge.
    ## @io (List[Annotation], Annotation) -> List[Annotation]
    ## @complexity 4
    @staticmethod
    def delete_previous_merged(merged: List[Annotation], new_annotations: Annotation) -> List[Annotation]:
        deleted_list = []
        for annotation in merged:
            if annotation.start == new_annotations.start and \
                    annotation.name == new_annotations.name and \
                    annotation.value == new_annotations.value and \
                    annotation.end <= new_annotations.end:
                deleted_list.append(annotation)

        for annotation in deleted_list:
            merged.remove(annotation)

        return merged
    # endregion METHOD_delete_previous_merged
# endregion CLASS_AnnotationMerger
