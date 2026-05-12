import json
from typing import List, Optional

import numpy as np
import pandas as pd
from scipy.stats._multivariate import method

from dedoc.data_structures.concrete_annotations.bbox_annotation import BBoxAnnotation
from dedoc.data_structures.concrete_annotations.size_annotation import SizeAnnotation
from dedoc.data_structures.line_with_meta import LineWithMeta
from dedoc.structure_extractors.feature_extractors.abstract_extractor import AbstractFeatureExtractor
from dedoc.structure_extractors.feature_extractors.toc_feature_extractor import TocItem
from dedoc.utils.utils import flatten

import logging
logger = logging.getLogger(__name__)


# region CLASS_PairedFeatureExtractor [DOMAIN(DocumentProcessing): ...; CONCEPT(FeatureEngineering): ...; TECH(Pandas): ...]
## @purpose PairedFeatureExtractor for document structure extraction pipeline
class PairedFeatureExtractor(AbstractFeatureExtractor):
    """
    This class is used as an auxiliary feature extractor to the main extractor.
    It allows to add "raw" features related to the lines importance.
    Based on one line property (size, indentation) it computes a raw line's depth inside the document tree.

    Example:
        For lines
            line1 (size=16)
            line2 (size=14)
            line3 (size=12)
            line4 (size=12)
            line5 (size=14)
            line6 (size=12)
        We will obtain a feature vector (raw_depth_size)
            [0, 1, 2, 2, 1, 2]
    """

    # region METHOD_parameters [DOMAIN(X): ...; CONCEPT(Y): ...; TECH(Z): ...]
    ## @purpose parameters method
    ## @io Input -> Output
    ## @complexity 5
    def parameters(self) -> dict:
        self.logger.debug(f"[IMP:4][PairedFeatureExtractor][parameters_INIT] Starting")
        return {}

    # endregion METHOD_parameters
    # region METHOD_transform [DOMAIN(X): ...; CONCEPT(Y): ...; TECH(Z): ...]
    ## @purpose transform method
    ## @io Input -> Output
    ## @complexity 5
    def transform(self, documents: List[List[LineWithMeta]], toc_lines: Optional[List[List[TocItem]]] = None) -> pd.DataFrame:
        self.logger.debug(f"[IMP:4][PairedFeatureExtractor][transform_INIT] Starting")
        df = pd.DataFrame()
        df["raw_depth_size"] = list(flatten([self._handle_one_document(document, self.__get_size) for document in documents]))
        df["raw_depth_indentation"] = list(flatten([self._handle_one_document(document, self._get_indentation) for document in documents]))
        return df

    # endregion METHOD_transform
    # region METHOD__handle_one_document [DOMAIN(X): ...; CONCEPT(Y): ...; TECH(Z): ...]
    ## @purpose _handle_one_document method
    ## @io Input -> Output
    ## @complexity 5
    def _handle_one_document(self, document: List[LineWithMeta], get_feature: method) -> List[int]:
        self.logger.debug(f"[IMP:4][PairedFeatureExtractor][_handle_one_document_INIT] Starting")
        if len(document) == 0:
            return []
        if len(document) == 1:
            return [0]

        features = [get_feature(line) for line in document]
        std = np.std(features)
        result = []
        stack = []

        for line in document:
            while len(stack) > 0 and self.__compare_lines(stack[-1], line, get_feature, std) <= 0:
                stack.pop()
            result.append(len(stack))
            stack.append(line)

        return result

    # endregion METHOD__handle_one_document
    # region METHOD___get_size [DOMAIN(X): ...; CONCEPT(Y): ...; TECH(Z): ...]
    ## @purpose __get_size method
    ## @io Input -> Output
    ## @complexity 5
    def __get_size(self, line: LineWithMeta) -> float:
        self.logger.debug(f"[IMP:4][PairedFeatureExtractor][__get_size_INIT] Starting")
        annotations = line.annotations
        size_annotation = [annotation for annotation in annotations if annotation.name == SizeAnnotation.name]
        if len(size_annotation) > 0:
            return float(size_annotation[0].value)

        bbox_annotation = [annotation for annotation in annotations if annotation.name == BBoxAnnotation.name]
        if len(bbox_annotation) > 0:
            bbox = json.loads(bbox_annotation[0].value)
            return bbox["height"]

        return 0

    # endregion METHOD___get_size
    # region METHOD___compare_lines [DOMAIN(X): ...; CONCEPT(Y): ...; TECH(Z): ...]
    ## @purpose __compare_lines method
    ## @io Input -> Output
    ## @complexity 5
    def __compare_lines(self, first_line: LineWithMeta, second_line: LineWithMeta, get_feature: method, threshold: float = 0) -> int:
        self.logger.debug(f"[IMP:4][PairedFeatureExtractor][__compare_lines_INIT] Starting")
        first_feature = get_feature(first_line)
        second_feature = get_feature(second_line)

        if first_feature > second_feature + threshold:
            return 1

        if second_feature > first_feature + threshold:
            return -1

        return 0

    # endregion METHOD___compare_lines
# endregion CLASS_PairedFeatureExtractor
# region MODULE_CONTRACT [DOMAIN(DocumentProcessing): ...; CONCEPT(FeatureEngineering): ...; TECH(Pandas): ...]
## @modulecontract
## @purpose Document structure extraction for structure_extractors/feature_extractors/paired_feature_extractor: line classification, hierarchy level assignment, pattern matching.
## @scope Structure extraction pipeline — structure_extractors/feature_extractors/paired_feature_extractor
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
## CLASS [Weight 7][Structure extraction] => PairedFeatureExtractor
## @usecases
## - Extract structure: Reader → StructureExtractor → HierarchyBuilder → AnnotatedDocument
def _module_contract():
    pass
# endregion MODULE_CONTRACT
# GREP_SUMMARY: structure extractors, feature extractors, paired feature extractor
# STRUCTURE: ▶ structure_extractors/feature_extractors/paired_feature_extractor → ○ PairedFeatureExtractor.cls → ⎋ result