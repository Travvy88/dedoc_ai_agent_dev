import logging
import os
from typing import Dict, List, Optional, Union

import numpy as np
import pandas as pd
import xgbfir
from xgboost import XGBClassifier

from dedoc.download_models import download_from_hub


# region CLASS_FintocClassifier [DOMAIN(DocumentProcessing): ...; CONCEPT(Classification): ...; TECH(XGBoost): ...]
## @purpose FintocClassifier for document structure extraction pipeline
class FintocClassifier:
    """
    Classifier of financial documents for the FinTOC 2022 Shared task (https://wp.lancs.ac.uk/cfie/fintoc2022/).
    Lines are classified in two stages:
        1. Binary classification title/not title (title detection task)
        2. Classification of title lines into title depth classes (1-6) (TOC generation task)

    More important lines have a lesser depth.
    As a result:
        1. For non-title lines, classifier returns -1.
        2. For title lines, classifier returns their depth (from 1 to 6).
    """

    # region METHOD___init__ [DOMAIN(X): ...; CONCEPT(Y): ...; TECH(Z): ...]
    ## @purpose __init__ method
    ## @io Input -> Output
    ## @complexity 5
    def __init__(self, language: str, weights_dir_path: Optional[str] = None) -> None:
        self.logger = logging.getLogger(__name__)
        self.logger.debug(f"[IMP:4][FintocClassifier][__init___INIT] Starting")
        """
        :param language: language of data ("en", "fr", "sp")
        :param weights_dir_path: path to directory with trained models weights
        """
        self.weights_dir_path = weights_dir_path
        self.language = language
        self.classifiers = {"binary": None, "target": None}

    # endregion METHOD___init__
    # region METHOD_predict [DOMAIN(X): ...; CONCEPT(Y): ...; TECH(Z): ...]
    ## @purpose predict method
    ## @io Input -> Output
    ## @complexity 5
    def predict(self, features: pd.DataFrame) -> List[int]:
        self.logger.debug(f"[IMP:4][FintocClassifier][predict_INIT] Starting")
        """
        Two-staged classification: title/not title and depth classification for titles.
        For non-title lines, classifier returns -1, for title lines, classifier returns their depth (from 1 to 6).
        """
        binary_predictions = self.binary_classifier.predict(features)
        # binary_predictions = [True, False, ...], target predictions are predicted only for True items
        target_predictions = self.target_classifier.predict(features[binary_predictions])
        result = np.ones_like(binary_predictions) * -1
        result[binary_predictions] = target_predictions
        # return list [1, 2, 3, -1, -1, ...], where positive values mean headers depth, -1 mean non-header lines
        return list(result)

    # endregion METHOD_predict
    # region METHOD_fit [DOMAIN(X): ...; CONCEPT(Y): ...; TECH(Z): ...]
    ## @purpose fit method
    ## @io Input -> Output
    ## @complexity 5
    def fit(self,
            binary_classifier_parameters: Dict[str, Union[int, float, str]],
            target_classifier_parameters: Dict[str, Union[int, float, str]],
            features: pd.DataFrame,
            features_names: List[str]) -> None:
        self.logger.debug(f"[IMP:4][FintocClassifier][fit_INIT] Starting")
        self.classifiers["binary"] = XGBClassifier(**binary_classifier_parameters)
        self.classifiers["target"] = XGBClassifier(**target_classifier_parameters)
        self.binary_classifier.fit(features[features_names], features.label != -1)
        self.target_classifier.fit(features[features_names][features.label != -1], features.label[features.label != -1])

    # endregion METHOD_fit
    # region METHOD_save [DOMAIN(X): ...; CONCEPT(Y): ...; TECH(Z): ...]
    ## @purpose save method
    ## @io Input -> Output
    ## @complexity 5
    def save(self, classifiers_dir_path: str, features_importances_dir_path: str, logger: logging.Logger, features_names: List[str], reader: str) -> None:
        self.logger.debug(f"[IMP:4][FintocClassifier][save_INIT] Starting")
        os.makedirs(classifiers_dir_path, exist_ok=True)
        for classifier_type in ("binary", "target"):
            self.classifiers[classifier_type].save_model(os.path.join(classifiers_dir_path, f"{classifier_type}_classifier_{self.language}_{reader}.json"))
        logger.info(f"Classifiers were saved in {classifiers_dir_path} directory")

        os.makedirs(features_importances_dir_path, exist_ok=True)
        for classifier_type in ("binary", "target"):
            xgbfir.saveXgbFI(self.classifiers[classifier_type], feature_names=features_names,
                             OutputXlsxFile=os.path.join(features_importances_dir_path, f"feature_importances_{classifier_type}_{self.language}_{reader}.xlsx"))
        logger.info(f"Features importances were saved in {features_importances_dir_path} directory")

    # endregion METHOD_save
    # region METHOD_binary_classifier [DOMAIN(X): ...; CONCEPT(Y): ...; TECH(Z): ...]
    ## @purpose binary_classifier method
    ## @io Input -> Output
    ## @complexity 5
    @property
    def binary_classifier(self) -> XGBClassifier:
        self.logger.debug(f"[IMP:4][FintocClassifier][binary_classifier_INIT] Starting")
        return self.__lazy_load_weights("binary")

    # endregion METHOD_binary_classifier
    # region METHOD_target_classifier [DOMAIN(X): ...; CONCEPT(Y): ...; TECH(Z): ...]
    ## @purpose target_classifier method
    ## @io Input -> Output
    ## @complexity 5
    @property
    def target_classifier(self) -> XGBClassifier:
        self.logger.debug(f"[IMP:4][FintocClassifier][target_classifier_INIT] Starting")
        return self.__lazy_load_weights("target")

    # endregion METHOD_target_classifier
    # region METHOD___lazy_load_weights [DOMAIN(X): ...; CONCEPT(Y): ...; TECH(Z): ...]
    ## @purpose __lazy_load_weights method
    ## @io Input -> Output
    ## @complexity 5
    def __lazy_load_weights(self, classifier_type: str) -> XGBClassifier:
        self.logger.debug(f"[IMP:4][FintocClassifier][__lazy_load_weights_INIT] Starting")
        if self.classifiers[classifier_type] is None:
            assert self.weights_dir_path is not None
            file_name = f"{classifier_type}_classifier_{self.language}.json"
            classifier_path = os.path.join(self.weights_dir_path, file_name)
            if not os.path.isfile(classifier_path):
                download_from_hub(out_dir=self.weights_dir_path,
                                  out_name=file_name,
                                  repo_name="fintoc_classifiers",
                                  hub_name=f"{classifier_type}_classifier_{self.language}_txt_layer.json")

            classifier = XGBClassifier()
            classifier.load_model(classifier_path)
            self.classifiers[classifier_type] = classifier

        return self.classifiers[classifier_type]

    # endregion METHOD___lazy_load_weights
# endregion CLASS_FintocClassifier
# region MODULE_CONTRACT [DOMAIN(DocumentProcessing): ...; CONCEPT(Classification): ...; TECH(XGBoost): ...]
## @modulecontract
## @purpose Document structure extraction for structure_extractors/line_type_classifiers/fintoc_classifier: line classification, hierarchy level assignment, pattern matching.
## @scope Structure extraction pipeline — structure_extractors/line_type_classifiers/fintoc_classifier
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
## CLASS [Weight 7][Structure extraction] => FintocClassifier
## @usecases
## - Extract structure: Reader → StructureExtractor → HierarchyBuilder → AnnotatedDocument
def _module_contract():
    pass
# endregion MODULE_CONTRACT
# GREP_SUMMARY: structure extractors, line type classifiers, fintoc classifier
# STRUCTURE: ▶ structure_extractors/line_type_classifiers/fintoc_classifier → ○ FintocClassifier.cls → ⎋ result