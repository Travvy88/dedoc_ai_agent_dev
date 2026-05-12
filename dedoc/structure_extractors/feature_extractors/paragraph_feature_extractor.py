from collections import defaultdict, deque
from typing import Iterator, List, Optional, Tuple

import pandas as pd
from _operator import attrgetter
from dedocutils.data_structures import BBox
from pandas import DataFrame

from dedoc.data_structures.concrete_annotations.bbox_annotation import BBoxAnnotation
from dedoc.data_structures.line_with_meta import LineWithMeta
from dedoc.readers.pdf_reader.data_classes.line_with_location import LineWithLocation
from dedoc.structure_extractors.feature_extractors.abstract_extractor import AbstractFeatureExtractor
from dedoc.structure_extractors.feature_extractors.list_features.list_features_extractor import ListFeaturesExtractor
from dedoc.structure_extractors.feature_extractors.toc_feature_extractor import TocItem
from dedoc.utils.utils import list_get

import logging
logger = logging.getLogger(__name__)


# region CLASS_ParagraphFeatureExtractor [DOMAIN(DocumentProcessing): ...; CONCEPT(FeatureEngineering): ...; TECH(Pandas): ...]
## @purpose ParagraphFeatureExtractor for document structure extraction pipeline
class ParagraphFeatureExtractor(AbstractFeatureExtractor):

    # region METHOD___init__ [DOMAIN(X): ...; CONCEPT(Y): ...; TECH(Z): ...]
    ## @purpose __init__ method
    ## @io Input -> Output
    ## @complexity 5
    def __init__(self, *, config: dict = None) -> None:  # noqa
        super().__init__()
        self.logger.debug(f"[IMP:4][ParagraphFeatureExtractor][__init___INIT] Starting")
        self.config = config if config is not None else {}
        self.list_feature_extractor = ListFeaturesExtractor()

    # endregion METHOD___init__
    # region METHOD_parameters [DOMAIN(X): ...; CONCEPT(Y): ...; TECH(Z): ...]
    ## @purpose parameters method
    ## @io Input -> Output
    ## @complexity 5
    def parameters(self) -> dict:
        self.logger.debug(f"[IMP:4][ParagraphFeatureExtractor][parameters_INIT] Starting")
        return {}

    # endregion METHOD_parameters
    # region METHOD___process_document [DOMAIN(X): ...; CONCEPT(Y): ...; TECH(Z): ...]
    ## @purpose __process_document method
    ## @io Input -> Output
    ## @complexity 5
    def __process_document(self, document: List[LineWithMeta]) -> pd.DataFrame:
        self.logger.debug(f"[IMP:4][ParagraphFeatureExtractor][__process_document_INIT] Starting")
        _, list_features_df = self.list_feature_extractor.one_document(document)
        list_features_df["list_item"] = self._list_features(document)

        one_line_features_dict = defaultdict(list)
        for line_id, line in enumerate(document):
            prev_line = list_get(document, line_id - 1)
            next_line = list_get(document, line_id + 1)

            for feature_name, feature in self._one_line_features(line, prev_line, next_line):
                one_line_features_dict[feature_name].append(feature)

        one_doc_features_df = pd.DataFrame(one_line_features_dict)
        one_doc_features_df = self.__normalize_features(one_doc_features_df)

        # result_matrix = self.prev_next_line_features(one_doc_features_df, 1, 1)
        result_matrix = pd.concat([one_doc_features_df, list_features_df], axis=1)

        return result_matrix

    # endregion METHOD___process_document
    # region METHOD___normalize_features [DOMAIN(X): ...; CONCEPT(Y): ...; TECH(Z): ...]
    ## @purpose __normalize_features method
    ## @io Input -> Output
    ## @complexity 5
    def __normalize_features(self, features_df: DataFrame) -> DataFrame:
        self.logger.debug(f"[IMP:4][ParagraphFeatureExtractor][__normalize_features_INIT] Starting")
        normalize_columns = (
            "distance_prev", "distance_next", "height", "height_next", "height_prev", "indent", "indent_right", "indent_prev_right", "indent_next",
            "indent_prev"
        )
        for column in normalize_columns:
            if column in features_df.columns:
                features_df[column] = self._get_features_quantile(features_df[column])

        return features_df

    # endregion METHOD___normalize_features
    # region METHOD_transform [DOMAIN(X): ...; CONCEPT(Y): ...; TECH(Z): ...]
    ## @purpose transform method
    ## @io Input -> Output
    ## @complexity 5
    def transform(self, documents: List[List[LineWithMeta]], toc_lines: Optional[List[List[TocItem]]] = None) -> pd.DataFrame:
        self.logger.debug(f"[IMP:4][ParagraphFeatureExtractor][transform_INIT] Starting")
        result_matrix = pd.concat([self.__process_document(document) for document in documents], ignore_index=True)
        features = sorted(result_matrix.columns)
        return result_matrix[features].astype(float)

    # endregion METHOD_transform
    # region METHOD__one_line_features [DOMAIN(X): ...; CONCEPT(Y): ...; TECH(Z): ...]
    ## @purpose _one_line_features method
    ## @io Input -> Output
    ## @complexity 5
    def _one_line_features(self, line: LineWithMeta, prev_line: Optional[LineWithMeta], next_line: Optional[LineWithMeta]) -> Iterator[Tuple[str, int]]:
        self.logger.debug(f"[IMP:4][ParagraphFeatureExtractor][_one_line_features_INIT] Starting")
        bbox, page_width = self._get_bbox(line)
        prev_line_bbox, _ = self._get_bbox(prev_line)
        next_line_bbox, _ = self._get_bbox(next_line)
        prev_indent_queue = deque([], maxlen=5)
        if bbox is not None:
            prev_indent_queue.append(bbox.x_top_left)

        yield "indent", bbox.x_top_left if bbox else None
        yield "indent_prev", self._relative_indent(bbox, prev_line_bbox) if bbox else None
        yield "indent_next", self._relative_indent(next_line_bbox, bbox) if bbox else None
        yield "indent_right", bbox.x_bottom_right if bbox else None
        yield "indent_prev_right", self._relative_indent(bbox, prev_line_bbox, left=False) if bbox else None

        yield "intersection_next", self._intersection(next_line_bbox, bbox) if bbox else None
        yield "intersection_prev", self._intersection(prev_line_bbox, bbox) if bbox else None
        yield "prev_text_lens", len(prev_line.line) if prev_line else None
        yield "text_lens", len(line.line)

        if prev_line:
            yield "upper_letters_percent_prev", self._get_percent_upper_letters(line)
        else:
            yield "upper_letters_percent_prev", None

        caps = self._get_percent_upper_letters(line)
        yield "upper_letters_percent", caps
        yield "is_capitalized", int(caps == 1.0)

        bold = self._get_bold_percent(line)
        yield "is_bold_changed", int(bold == 1.0) != int(self._get_bold_percent(prev_line) == 1.0) if prev_line else None
        yield "is_bold_changed_next", int(self._get_bold_percent(line) == 1.0) != int(self._get_bold_percent(next_line) == 1.0) if next_line else None

        if prev_line:
            _, _, _, color_dispersion_cur = list(self._get_color(prev_line))
            _, _, _, color_dispersion_prev = list(self._get_color(line))
            yield "color_dispersion_diff", abs(color_dispersion_cur[1] - color_dispersion_prev[1])
        else:
            yield "color_dispersion_diff", None

        yield "distance_prev", bbox.y_top_left - prev_line_bbox.y_bottom_right if prev_line_bbox and bbox else None
        yield "distance_next", next_line_bbox.y_top_left - bbox.y_bottom_right if next_line_bbox and bbox else None

        yield "height", bbox.height if bbox else None
        yield "height_next", bbox.height / (next_line_bbox.height + 1) if (next_line_bbox and bbox) else None
        yield "height_prev", bbox.height / (prev_line_bbox.height + 1) if (prev_line_bbox and bbox) else None

    # endregion METHOD__one_line_features
    # region METHOD__relative_indent [DOMAIN(X): ...; CONCEPT(Y): ...; TECH(Z): ...]
    ## @purpose _relative_indent method
    ## @io Input -> Output
    ## @complexity 5
    def _relative_indent(self, this_bbox: Optional[BBox], prev_bbox: Optional[BBox], left: bool = True) -> Optional[float]:
        self.logger.debug(f"[IMP:4][ParagraphFeatureExtractor][_relative_indent_INIT] Starting")
        if this_bbox is None or prev_bbox is None:
            return None
        elif left:
            return this_bbox.x_top_left - prev_bbox.x_top_left
        else:
            return this_bbox.x_bottom_right - prev_bbox.x_bottom_right

    # endregion METHOD__relative_indent
    # region METHOD__relative_indent_new [DOMAIN(X): ...; CONCEPT(Y): ...; TECH(Z): ...]
    ## @purpose _relative_indent_new method
    ## @io Input -> Output
    ## @complexity 5
    def _relative_indent_new(self, this_bbox: Optional[BBox], prev_bbox: Optional[BBox], page_width: Optional[int], left: bool = True) -> Optional[float]:
        self.logger.debug(f"[IMP:4][ParagraphFeatureExtractor][_relative_indent_new_INIT] Starting")
        if this_bbox is None or prev_bbox is None or page_width is None:
            return None
        elif left:
            return min(this_bbox.x_top_left - prev_bbox.x_top_left / page_width, 1.0)
        else:
            return min(this_bbox.x_bottom_right - prev_bbox.x_bottom_right / page_width, 1.0)

    # endregion METHOD__relative_indent_new
    # region METHOD__diff_left_right_indent [DOMAIN(X): ...; CONCEPT(Y): ...; TECH(Z): ...]
    ## @purpose _diff_left_right_indent method
    ## @io Input -> Output
    ## @complexity 5
    def _diff_left_right_indent(self, this_box: Optional[BBox], page_width: Optional[int]) -> Optional[float]:
        self.logger.debug(f"[IMP:4][ParagraphFeatureExtractor][_diff_left_right_indent_INIT] Starting")
        if this_box is None or page_width is None:
            return None
        left = this_box.x_top_left
        right = page_width - this_box.x_bottom_right
        diff = abs(left - right) / page_width
        return diff

    # endregion METHOD__diff_left_right_indent
    # region METHOD__intersection [DOMAIN(X): ...; CONCEPT(Y): ...; TECH(Z): ...]
    ## @purpose _intersection method
    ## @io Input -> Output
    ## @complexity 5
    def _intersection(self, this_bbox: Optional[BBox], that_bbox: Optional[BBox]) -> Optional[float]:
        self.logger.debug(f"[IMP:4][ParagraphFeatureExtractor][_intersection_INIT] Starting")
        if this_bbox is None or that_bbox is None:
            return None
        if this_bbox.x_top_left >= that_bbox.x_bottom_right or that_bbox.x_top_left >= this_bbox.x_bottom_right:
            return 0
        union_left = min(this_bbox.x_top_left, that_bbox.x_top_left)
        union_right = max(this_bbox.x_bottom_right, that_bbox.x_bottom_right)

        intersection_left = max(this_bbox.x_top_left, that_bbox.x_top_left)
        intersection_right = min(this_bbox.x_bottom_right, that_bbox.x_bottom_right)
        if union_left <= union_right:
            return 0
        else:
            return (intersection_right - intersection_left) / (union_right - union_left)

    # endregion METHOD__intersection
    # region METHOD__get_bbox [DOMAIN(X): ...; CONCEPT(Y): ...; TECH(Z): ...]
    ## @purpose _get_bbox method
    ## @io Input -> Output
    ## @complexity 5
    def _get_bbox(self, line: Optional[LineWithMeta]) -> Tuple[Optional[BBox], Optional[int]]:
        self.logger.debug(f"[IMP:4][ParagraphFeatureExtractor][_get_bbox_INIT] Starting")
        if line is None:
            return None, None
        if isinstance(line, LineWithLocation):
            return line.location.bbox, None

        bboxes_w_h = [BBoxAnnotation.get_bbox_from_value(bbox.value) for bbox in line.annotations if bbox.name == BBoxAnnotation.name]
        bboxes, pages_width, _ = zip(*bboxes_w_h)
        page_width = pages_width[0] if len(pages_width) > 0 and pages_width[0] > 1 else None
        if len(bboxes) > 1:
            line_bbox = BBox.from_two_points(
                top_left=(min(bboxes, key=attrgetter("x_top_left")).x_top_left, min(bboxes, key=attrgetter("y_top_left")).y_top_left),
                bottom_right=(max(bboxes, key=attrgetter("x_bottom_right")).x_bottom_right, max(bboxes, key=attrgetter("y_bottom_right")).y_bottom_right)
            )
            return line_bbox, page_width
        else:
            return bboxes[0], page_width

    # endregion METHOD__get_bbox
# endregion CLASS_ParagraphFeatureExtractor
# region MODULE_CONTRACT [DOMAIN(DocumentProcessing): ...; CONCEPT(FeatureEngineering): ...; TECH(Pandas): ...]
## @modulecontract
## @purpose Document structure extraction for structure_extractors/feature_extractors/paragraph_feature_extractor: line classification, hierarchy level assignment, pattern matching.
## @scope Structure extraction pipeline — structure_extractors/feature_extractors/paragraph_feature_extractor
## @input Document lines with reader metadata.
## @output Lines annotated with hierarchy levels and line type labels.
## @links [USES_API(8): dedoc.data_structures; READS_DATA_FROM(8): readers]
## @invariants
## - Output lines preserve input order.
## @rationale
## Q: Why semantic region markup and LDD logging?
## A: Enables agent navigation via grep/Doxygen XML and runtime trace analysis.
## @changes
## LAST_CHANGE: [v1.0.0 – Added semantic template markup and LDD logging]
## @modulemap
## CLASS [Weight 7][Structure extraction] => ParagraphFeatureExtractor
## @usecases
## - Extract structure: Reader → StructureExtractor → HierarchyBuilder → AnnotatedDocument
def _module_contract():
    pass
# endregion MODULE_CONTRACT
# GREP_SUMMARY: structure extractors, feature extractors, paragraph feature extractor
# STRUCTURE: ▶ structure_extractors/feature_extractors/paragraph_feature_extractor → ○ ParagraphFeatureExtractor.cls → ⎋ result