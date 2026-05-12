import json
import logging
import os
import tempfile
import zipfile
from abc import ABC
from typing import Optional, Tuple

from xgboost import XGBClassifier

from dedoc.download_models import download_from_hub
from dedoc.structure_extractors.line_type_classifiers.abstract_line_type_classifier import AbstractLineTypeClassifier
from dedoc.utils.parameter_utils import get_param_gpu_available


# region CLASS_AbstractPickledLineTypeClassifier [DOMAIN(DocumentProcessing): ...; CONCEPT(Classification): ...; TECH(XGBoost): ...]
## @purpose AbstractPickledLineTypeClassifier for document structure extraction pipeline
class AbstractPickledLineTypeClassifier(AbstractLineTypeClassifier, ABC):
    """
    Abstract class for lines classification with functionality of loading and saving a classifier.
    """

    # region METHOD___init__ [DOMAIN(X): ...; CONCEPT(Y): ...; TECH(Z): ...]
    ## @purpose __init__ method
    ## @io Input -> Output
    ## @complexity 5
    def __init__(self, *, config: Optional[dict] = None) -> None:
        super().__init__(config=config)
        self.logger = self.config.get("logger", logging.getLogger())
        self.logger.debug(f"[IMP:4][AbstractPickledLineTypeClassifier][__init___INIT] Starting")

    # endregion METHOD___init__
    # region METHOD_load [DOMAIN(X): ...; CONCEPT(Y): ...; TECH(Z): ...]
    ## @purpose load method
    ## @io Input -> Output
    ## @complexity 5
    def load(self, classifier_type: str, path: str) -> Tuple[XGBClassifier, dict]:
        self.logger.debug(f"[IMP:4][AbstractPickledLineTypeClassifier][load_INIT] Starting")
        """
        Load the pickled classifier with parameters for a feature extractor.

        :param classifier_type: name of the classifier to load from huggingface in case `path` does not exist
            (https://huggingface.co/dedoc/line_type_classifiers)
        :param path: path from where to load the pickled classifier
        :return: loaded XGBClassifier and parameters for a feature extractor
        """
        if not os.path.isfile(path):
            out_dir, out_name = os.path.split(path)
            download_from_hub(out_dir=out_dir, out_name=out_name, repo_name="line_type_classifiers", hub_name=f"{classifier_type}.zip")

        with tempfile.TemporaryDirectory() as tmpdir:
            with zipfile.ZipFile(path) as archive:
                archive.extractall(tmpdir)

            with open(os.path.join(tmpdir, "parameters.json")) as parameters_file:
                feature_extractor_parameters = json.load(parameters_file)
            classifier = XGBClassifier()
            classifier.load_model(os.path.join(tmpdir, "classifier.json"))

        if get_param_gpu_available(self.config, self.logger):
            gpu_params = dict(predictor="gpu_predictor", tree_method="auto", gpu_id=0)
            classifier.set_params(**gpu_params)
            classifier.get_booster().set_param(gpu_params)

        return classifier, feature_extractor_parameters

    # endregion METHOD_load
    # region METHOD_save [DOMAIN(X): ...; CONCEPT(Y): ...; TECH(Z): ...]
    ## @purpose save method
    ## @io Input -> Output
    ## @complexity 5
    @staticmethod
    def save(path_out: str, classifier: XGBClassifier, parameters: dict) -> str:
        self.logger.debug(f"[IMP:4][AbstractPickledLineTypeClassifier][save_INIT] Starting")
        """
        Save the classifier (with initialization parameters for a feature extractor) into the `.zip` file with path=`path_out`

        * classifier -> classifier.json
        * parameters -> parameters.json

        :param path_out: path (with file name) where to save the object
        :param classifier: classifier to save
        :param parameters: feature extractor parameters to save
        :return: the resulting path of the saved file
        """
        with tempfile.TemporaryDirectory() as tmpdir:
            clf_path = os.path.join(tmpdir, "classifier.json")
            params_path = os.path.join(tmpdir, "parameters.json")
            classifier.save_model(clf_path)
            with open(params_path, "w") as out_file:
                json.dump(parameters, out_file)

            with zipfile.ZipFile(path_out, "w") as archive:
                archive.write(clf_path, os.path.basename(clf_path))
                archive.write(params_path, os.path.basename(params_path))
        return path_out

    # endregion METHOD_save
# endregion CLASS_AbstractPickledLineTypeClassifier
# region MODULE_CONTRACT [DOMAIN(DocumentProcessing): ...; CONCEPT(Classification): ...; TECH(XGBoost): ...]
## @modulecontract
## @purpose Document structure extraction for structure_extractors/line_type_classifiers/abstract_pickled_classifier: line classification, hierarchy level assignment, pattern matching.
## @scope Structure extraction pipeline — structure_extractors/line_type_classifiers/abstract_pickled_classifier
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
## CLASS [Weight 7][Structure extraction] => AbstractPickledLineTypeClassifier
## @usecases
## - Extract structure: Reader → StructureExtractor → HierarchyBuilder → AnnotatedDocument
def _module_contract():
    pass
# endregion MODULE_CONTRACT
# GREP_SUMMARY: structure extractors, line type classifiers, abstract pickled classifier
# STRUCTURE: ▶ structure_extractors/line_type_classifiers/abstract_pickled_classifier → ○ AbstractPickledLineTypeClassifier.cls → ⎋ result