from typing import List

import numpy as np

from dedoc.data_structures.concrete_annotations.size_annotation import SizeAnnotation
from dedoc.data_structures.line_with_meta import LineWithMeta
from dedoc.structure_extractors.feature_extractors.tz_feature_extractor import TzTextFeatures
from dedoc.structure_extractors.line_type_classifiers.abstract_pickled_classifier import AbstractPickledLineTypeClassifier

import logging
logger = logging.getLogger(__name__)


# region CLASS_TzLineTypeClassifier [DOMAIN(DocumentProcessing): ...; CONCEPT(Classification): ...; TECH(XGBoost): ...]
## @purpose TzLineTypeClassifier for document structure extraction pipeline
class TzLineTypeClassifier(AbstractPickledLineTypeClassifier):

    # region METHOD___init__ [DOMAIN(X): ...; CONCEPT(Y): ...; TECH(Z): ...]
    ## @purpose __init__ method
    ## @io Input -> Output
    ## @complexity 5
    def __init__(self, classifier_type: str, path: str, *, config: dict) -> None:
        super().__init__(config=config)

        self.logger.debug(f"[IMP:4][TzLineTypeClassifier][__init___INIT] Starting")
        self.classifier, feature_extractor_parameters = self.load(classifier_type, path)
        self.feature_extractor = TzTextFeatures(**feature_extractor_parameters)

    # endregion METHOD___init__
    # region METHOD_predict [DOMAIN(X): ...; CONCEPT(Y): ...; TECH(Z): ...]
    ## @purpose predict method
    ## @io Input -> Output
    ## @complexity 5
    def predict(self, lines: List[LineWithMeta]) -> List[str]:
        self.logger.debug(f"[IMP:4][TzLineTypeClassifier][predict_INIT] Starting")
        """
        get predictions from xgb classifier and patch them according to our prior knowledge. For example we know that
        title can not be interrupted with other structures. Empty line can not be item or toc item (but can be part of
        title or raw_text), there are can not be toc items after body has begun
        @param lines:
        @return:
        """
        if len(lines) == 0:
            return []

        features = self.feature_extractor.transform([lines])
        labels_probability = self.classifier.predict_proba(features)

        title_id = list(self.classifier.classes_).index("title")
        toc_id = list(self.classifier.classes_).index("toc")
        raw_text_id = list(self.classifier.classes_).index("raw_text")

        empty_line = [line.line.strip() == "" for line in lines]
        labels_probability[empty_line, :] = 0
        labels_probability[empty_line, raw_text_id] = 1

        labels = [self.classifier.classes_[i] for i in labels_probability.argmax(1)]
        first_non_title = min((i for i, label in enumerate(labels) if label not in ["title", "raw_text"]), default=0)
        # set probability to one for title before the body or toc
        labels_probability[:first_non_title, :] = 0
        labels_probability[:first_non_title, title_id] = 1
        # zeros probability for title after body of document has begun
        labels_probability[first_non_title:, title_id] = 0

        # work with probability for toc
        auto_toc_lines_mask = np.array([self.__is_auto_toc_line(line) for line in lines])
        if auto_toc_lines_mask.any():
            #  include line with contents header to the toc e.g. "содержание"
            first_auto_toc_ind = np.where(auto_toc_lines_mask)[0][0]
            first_toc_ind = min((i for i, label in enumerate(labels) if label == "toc"), default=-1)
            if first_toc_ind > 0:
                auto_toc_lines_mask[first_toc_ind:first_auto_toc_ind] = True
            # zero probability for non-toc elements in documents with auto toc
            labels_probability[np.logical_not(auto_toc_lines_mask), toc_id] = 0
            # toc elements are definitely toc
            labels_probability[auto_toc_lines_mask, toc_id] = 1
        else:
            # zeros probability for toc after body begun
            first_item = min((i for i, label in enumerate(labels) if label in ("item", "part")), default=0)
            labels_probability[first_item:, toc_id] = 0
        toc_lines = (line_id for line_id, line in enumerate(lines) if line.line.strip().lower() == "содержание")
        toc_start_id = min(toc_lines, default=-1)
        if toc_id > 0:
            labels_probability[:toc_start_id, toc_id] = 0
        labels = [self.classifier.classes_[i] for i in labels_probability.argmax(1)]

        predictions = self._postprocess_labels(lines=lines, predictions=labels)
        assert len(predictions) == len(lines)
        return predictions

    # endregion METHOD_predict
    # region METHOD___is_auto_toc_line [DOMAIN(X): ...; CONCEPT(Y): ...; TECH(Z): ...]
    ## @purpose __is_auto_toc_line method
    ## @io Input -> Output
    ## @complexity 5
    def __is_auto_toc_line(self, line: LineWithMeta) -> bool:
        self.logger.debug(f"[IMP:4][TzLineTypeClassifier][__is_auto_toc_line_INIT] Starting")
        annotations = line.annotations
        for annotation in annotations:
            if annotation.name == "style":
                return annotation.value.lower().startswith("toc") or annotation.value.lower().startswith("contents")
        return False

    # endregion METHOD___is_auto_toc_line
    # region METHOD__postprocess_labels [DOMAIN(X): ...; CONCEPT(Y): ...; TECH(Z): ...]
    ## @purpose _postprocess_labels method
    ## @io Input -> Output
    ## @complexity 5
    def _postprocess_labels(self, lines: List[LineWithMeta], predictions: List[str]) -> List[str]:
        self.logger.debug(f"[IMP:4][TzLineTypeClassifier][_postprocess_labels_INIT] Starting")
        assert len(lines) == len(predictions)
        sizes = [self._get_size(line) for line in lines]
        median_size = np.median(sizes)
        result = []
        for line, prediction in zip(lines, predictions):
            if self._get_size(line) >= median_size + 2 and prediction in ("item", "part", "named_item"):
                result.append("part")
            elif prediction == "part":
                result.append("named_item")
            else:
                result.append(prediction)
        return result

    # endregion METHOD__postprocess_labels
    # region METHOD__get_size [DOMAIN(X): ...; CONCEPT(Y): ...; TECH(Z): ...]
    ## @purpose _get_size method
    ## @io Input -> Output
    ## @complexity 5
    def _get_size(self, line: LineWithMeta) -> float:
        self.logger.debug(f"[IMP:4][TzLineTypeClassifier][_get_size_INIT] Starting")
        caps = 1 if line.line.isupper() and len(line.line.strip()) > 4 else 0
        for annotation in line.annotations:
            if annotation.name == SizeAnnotation.name:
                return float(annotation.value) + caps
        return 0 + caps

    # endregion METHOD__get_size
# endregion CLASS_TzLineTypeClassifier
# region MODULE_CONTRACT [DOMAIN(DocumentProcessing): ...; CONCEPT(Classification): ...; TECH(XGBoost): ...]
## @modulecontract
## @purpose Document structure extraction for structure_extractors/line_type_classifiers/tz_classifier: line classification, hierarchy level assignment, pattern matching.
## @scope Structure extraction pipeline — structure_extractors/line_type_classifiers/tz_classifier
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
## CLASS [Weight 7][Structure extraction] => TzLineTypeClassifier
## @usecases
## - Extract structure: Reader → StructureExtractor → HierarchyBuilder → AnnotatedDocument
def _module_contract():
    pass
# endregion MODULE_CONTRACT
# GREP_SUMMARY: structure extractors, line type classifiers, tz classifier
# STRUCTURE: ▶ structure_extractors/line_type_classifiers/tz_classifier → ○ TzLineTypeClassifier.cls → ⎋ result