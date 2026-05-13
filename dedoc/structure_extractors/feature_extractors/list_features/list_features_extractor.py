from collections import defaultdict
from typing import Dict, List, Optional, Tuple

import numpy as np
import pandas as pd

from dedoc.data_structures.line_with_meta import LineWithMeta
from dedoc.structure_extractors.feature_extractors.abstract_extractor import AbstractFeatureExtractor
from dedoc.structure_extractors.feature_extractors.list_features.list_utils import get_prefix
from dedoc.structure_extractors.feature_extractors.list_features.prefix.bracket_prefix import BracketPrefix
from dedoc.structure_extractors.feature_extractors.list_features.prefix.bullet_prefix import BulletPrefix
from dedoc.structure_extractors.feature_extractors.list_features.prefix.dotted_prefix import DottedPrefix
from dedoc.structure_extractors.feature_extractors.list_features.prefix.letter_prefix import LetterPrefix
from dedoc.structure_extractors.feature_extractors.list_features.prefix.prefix import LinePrefix

import logging
logger = logging.getLogger(__name__)


# region CLASS_Window [DOMAIN(DocumentProcessing): ...; CONCEPT(FeatureEngineering): ...; TECH(Pandas): ...]
## @purpose Window for document structure extraction pipeline
class Window:
    # region METHOD___init__ [DOMAIN(X): ...; CONCEPT(Y): ...; TECH(Z): ...]
    ## @purpose __init__ method
    ## @io Input -> Output
    ## @complexity 5
    def __init__(self, indent_std: float, prefix_before: List[LinePrefix], prefix_after: List[LinePrefix]) -> None:
        self.logger = logging.getLogger(__name__)
        self.logger.debug(f"[IMP:4][Window][__init___INIT] Starting")
        self.indent_std = indent_std
        self.prefix_before = prefix_before
        self.prefix_after = prefix_after


    # endregion METHOD___init__
# endregion CLASS_Window
# region CLASS_ListFeaturesExtractor [DOMAIN(DocumentProcessing): ...; CONCEPT(FeatureEngineering): ...; TECH(Pandas): ...]
## @purpose ListFeaturesExtractor for document structure extraction pipeline
class ListFeaturesExtractor(AbstractFeatureExtractor):
    """
    Extracts features for list items:
        - indentation of items is analysed (same/different)
        - prefixes of items are analysed, if items can be predecessors of others

    The analysis is executed in a window of a fixed size (size of window = number of neighbor lines)
    """

    # region METHOD___init__ [DOMAIN(X): ...; CONCEPT(Y): ...; TECH(Z): ...]
    ## @purpose __init__ method
    ## @io Input -> Output
    ## @complexity 5
    def __init__(self, window_size: int = 25, prefix_list: Optional[List[LinePrefix]] = None) -> None:
        super().__init__()

        self.logger.debug(f"[IMP:4][ListFeaturesExtractor][__init___INIT] Starting")
        self.window_size = window_size
        self.prefix_list = prefix_list if prefix_list is not None else [BulletPrefix, LetterPrefix, BracketPrefix, DottedPrefix]

    # endregion METHOD___init__
    # region METHOD_parameters [DOMAIN(X): ...; CONCEPT(Y): ...; TECH(Z): ...]
    ## @purpose parameters method
    ## @io Input -> Output
    ## @complexity 5
    def parameters(self) -> dict:
        self.logger.debug(f"[IMP:4][ListFeaturesExtractor][parameters_INIT] Starting")
        return {"window_size": self.window_size}

    # endregion METHOD_parameters
    # region METHOD_fit [DOMAIN(X): ...; CONCEPT(Y): ...; TECH(Z): ...]
    ## @purpose fit method
    ## @io Input -> Output
    ## @complexity 5
    def fit(self, documents: List[List[LineWithMeta]], y: Optional[List[str]] = None) -> "AbstractFeatureExtractor":
        self.logger.debug(f"[IMP:4][ListFeaturesExtractor][fit_INIT] Starting")
        return self

    # endregion METHOD_fit
    # region METHOD_transform [DOMAIN(X): ...; CONCEPT(Y): ...; TECH(Z): ...]
    ## @purpose transform method
    ## @io Input -> Output
    ## @complexity 5
    def transform(self, documents: List[List[LineWithMeta]], y: Optional[List[str]] = None) -> pd.DataFrame:
        self.logger.debug(f"[IMP:4][ListFeaturesExtractor][transform_INIT] Starting")
        features = [self.one_document(doc)[1] for doc in documents]
        return pd.concat(features, axis=0, ignore_index=True)

    # endregion METHOD_transform
    # region METHOD_one_document [DOMAIN(X): ...; CONCEPT(Y): ...; TECH(Z): ...]
    ## @purpose one_document method
    ## @io Input -> Output
    ## @complexity 5
    def one_document(self, doc: List[LineWithMeta]) -> Tuple[List[LinePrefix], pd.DataFrame]:
        self.logger.debug(f"[IMP:4][ListFeaturesExtractor][one_document_INIT] Starting")
        prefixes = [self._get_prefix(line) for line in doc]
        indents = np.array([prefix.indent for prefix in prefixes])
        res = []
        doc_size = len(prefixes)
        for line_id, (_line, prefix) in enumerate(zip(doc, prefixes)):
            window = self._get_window(indents=indents, prefixes=prefixes, line_id=line_id, doc_size=doc_size)
            features = self._one_line_features(window=window, prefix=prefix)
            res.append(features)
        features_dict = defaultdict(list)
        for features in res:
            for feature_name, feature_value in features.items():
                features_dict[feature_name].append(feature_value)
        return prefixes, pd.DataFrame(features_dict)

    # endregion METHOD_one_document
    # region METHOD__one_line_features [DOMAIN(X): ...; CONCEPT(Y): ...; TECH(Z): ...]
    ## @purpose _one_line_features method
    ## @io Input -> Output
    ## @complexity 5
    def _one_line_features(self, prefix: LinePrefix, window: Window) -> Dict[str, float]:
        self.logger.debug(f"[IMP:4][ListFeaturesExtractor][_one_line_features_INIT] Starting")
        predecessor_num = 0
        predecessor_num_same_indent = 0
        same_indent = 0
        same_prefix = 0
        for prefix_other in window.prefix_before + window.prefix_after:
            is_predecessor = prefix.predecessor(prefix_other) or prefix.successor(prefix_other)
            is_same_indent = self._same_indent(this_indent=prefix.indent, other_indent=prefix_other.indent, std=window.indent_std)
            predecessor_num += is_predecessor
            same_indent += is_same_indent
            predecessor_num_same_indent += (is_same_indent and is_predecessor)
            same_prefix += (prefix_other.name == prefix.name)

        window_size = len(window.prefix_before) + len(window.prefix_after) + 1
        same_indent /= window_size
        predecessor_num_same_indent /= window_size
        predecessor_num /= window_size
        return {
            f"same_indent_{self.window_size}": same_indent,
            f"predecessor_num_same_indent_{self.window_size}": predecessor_num_same_indent,
            f"predecessor_num_{self.window_size}": predecessor_num
        }

    # endregion METHOD__one_line_features
    # region METHOD__same_indent [DOMAIN(X): ...; CONCEPT(Y): ...; TECH(Z): ...]
    ## @purpose _same_indent method
    ## @io Input -> Output
    ## @complexity 5
    def _same_indent(self, this_indent: float, other_indent: float, std: float) -> bool:
        self.logger.debug(f"[IMP:4][ListFeaturesExtractor][_same_indent_INIT] Starting")
        eps = 1
        return abs(this_indent - other_indent) <= 0.1 * std + eps

    # endregion METHOD__same_indent
    # region METHOD__get_prefix [DOMAIN(X): ...; CONCEPT(Y): ...; TECH(Z): ...]
    ## @purpose _get_prefix method
    ## @io Input -> Output
    ## @complexity 5
    def _get_prefix(self, line: LineWithMeta) -> LinePrefix:
        self.logger.debug(f"[IMP:4][ListFeaturesExtractor][_get_prefix_INIT] Starting")
        return get_prefix(self.prefix_list, line)

    # endregion METHOD__get_prefix
    # region METHOD__get_window [DOMAIN(X): ...; CONCEPT(Y): ...; TECH(Z): ...]
    ## @purpose _get_window method
    ## @io Input -> Output
    ## @complexity 5
    def _get_window(self, indents: np.ndarray, prefixes: List[LinePrefix], line_id: int, doc_size: int) -> Window:
        self.logger.debug(f"[IMP:4][ListFeaturesExtractor][_get_window_INIT] Starting")
        assert line_id < doc_size
        left = max(line_id - self.window_size, 0)
        right = min(line_id + self.window_size, doc_size)
        indents = indents[left: right]
        prefix_before = prefixes[left: line_id]
        prefix_after = prefixes[line_id + 1: right]
        return Window(indent_std=indents.std(), prefix_before=prefix_before, prefix_after=prefix_after)

    # endregion METHOD__get_window
# endregion CLASS_ListFeaturesExtractor
# region MODULE_CONTRACT [DOMAIN(DocumentProcessing): ...; CONCEPT(FeatureEngineering): ...; TECH(Pandas): ...]
## @modulecontract
## @purpose Document structure extraction for structure_extractors/feature_extractors/list_features/list_features_extractor: line classification, hierarchy level assignment, pattern matching.
## @scope Structure extraction pipeline — structure_extractors/feature_extractors/list_features/list_features_extractor
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
## CLASS [Weight 7][Structure extraction] => Window
## CLASS [Weight 7][Structure extraction] => ListFeaturesExtractor
## @usecases
## - Extract structure: Reader → StructureExtractor → HierarchyBuilder → AnnotatedDocument
def _module_contract():
    pass
# endregion MODULE_CONTRACT
# GREP_SUMMARY: structure extractors, feature extractors, list features, list features extractor
# STRUCTURE: ▶ structure_extractors/feature_extractors/list_features/list_features_extractor → ○ Window.cls ⊕ ListFeaturesExtractor.cls → ⎋ result