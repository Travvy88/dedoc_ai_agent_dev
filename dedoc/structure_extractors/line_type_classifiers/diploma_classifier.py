from typing import List, Optional

from dedoc.data_structures.line_with_meta import LineWithMeta
from dedoc.structure_extractors.feature_extractors.diploma_feature_extractor import DiplomaFeatureExtractor
from dedoc.structure_extractors.feature_extractors.toc_feature_extractor import TocItem
from dedoc.structure_extractors.line_type_classifiers.abstract_pickled_classifier import AbstractPickledLineTypeClassifier

import logging
logger = logging.getLogger(__name__)


# region CLASS_DiplomaLineTypeClassifier [DOMAIN(DocumentProcessing): ...; CONCEPT(Classification): ...; TECH(XGBoost): ...]
## @purpose DiplomaLineTypeClassifier for document structure extraction pipeline
class DiplomaLineTypeClassifier(AbstractPickledLineTypeClassifier):

    # region METHOD___init__ [DOMAIN(X): ...; CONCEPT(Y): ...; TECH(Z): ...]
    ## @purpose __init__ method
    ## @io Input -> Output
    ## @complexity 5
    def __init__(self, path: str, *, config: dict) -> None:
        super().__init__(config=config)

        self.logger.debug(f"[IMP:4][DiplomaLineTypeClassifier][__init___INIT] Starting")
        self.classifier, feature_extractor_parameters = self.load("diploma", path)
        self.feature_extractor = DiplomaFeatureExtractor()

    # endregion METHOD___init__
    # region METHOD_predict [DOMAIN(X): ...; CONCEPT(Y): ...; TECH(Z): ...]
    ## @purpose predict method
    ## @io Input -> Output
    ## @complexity 5
    def predict(self, lines: List[LineWithMeta], toc_items: Optional[List[TocItem]] = None) -> List[str]:
        self.logger.debug(f"[IMP:4][DiplomaLineTypeClassifier][predict_INIT] Starting")
        if len(lines) == 0:
            return []

        features = self.feature_extractor.transform([lines], toc_items=[toc_items])
        labels_probability = self.classifier.predict_proba(features)

        title_id = list(self.classifier.classes_).index("title")
        raw_text_id = list(self.classifier.classes_).index("raw_text")
        toc_id = list(self.classifier.classes_).index("toc")
        labels_probability[:, toc_id] = 0  # actually we don't predict toc items

        # set empty lines as raw_text
        empty_line = [line.line.strip() == "" for line in lines]
        labels_probability[empty_line, :] = 0
        labels_probability[empty_line, raw_text_id] = 1

        # Work with a title
        labels = [self.classifier.classes_[i] for i in labels_probability.argmax(1)]
        first_non_title = 0
        for i, line in enumerate(lines):
            text_wo_spaces = "".join(line.line.lower().strip().split())
            match = self.feature_extractor.year_regexp.match(text_wo_spaces)

            if match is not None:
                first_non_title = i + 1
                break

            if labels[i] not in ("title", "raw_text", "other"):
                first_non_title = i
                break

        # set probability to one for title before the body or toc
        labels_probability[:first_non_title, :] = 0
        labels_probability[:first_non_title, title_id] = 1
        # zeros probability for title after body of document has begun
        labels_probability[first_non_title:, title_id] = 0

        labels = [self.classifier.classes_[i] for i in labels_probability.argmax(1)]
        assert len(labels) == len(lines)
        return labels

    # endregion METHOD_predict
# endregion CLASS_DiplomaLineTypeClassifier
# region MODULE_CONTRACT [DOMAIN(DocumentProcessing): ...; CONCEPT(Classification): ...; TECH(XGBoost): ...]
## @modulecontract
## @purpose Document structure extraction for structure_extractors/line_type_classifiers/diploma_classifier: line classification, hierarchy level assignment, pattern matching.
## @scope Structure extraction pipeline — structure_extractors/line_type_classifiers/diploma_classifier
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
## CLASS [Weight 7][Structure extraction] => DiplomaLineTypeClassifier
## @usecases
## - Extract structure: Reader → StructureExtractor → HierarchyBuilder → AnnotatedDocument
def _module_contract():
    pass
# endregion MODULE_CONTRACT
# GREP_SUMMARY: structure extractors, line type classifiers, diploma classifier
# STRUCTURE: ▶ structure_extractors/line_type_classifiers/diploma_classifier → ○ DiplomaLineTypeClassifier.cls → ⎋ result