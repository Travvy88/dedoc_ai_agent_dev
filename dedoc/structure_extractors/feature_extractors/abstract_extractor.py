import json
from abc import ABC, abstractmethod
from typing import Iterable, List, Optional, Pattern, Tuple

import numpy as np
import pandas as pd
from scipy.stats._multivariate import method

from dedoc.data_structures.concrete_annotations.bold_annotation import BoldAnnotation
from dedoc.data_structures.concrete_annotations.color_annotation import ColorAnnotation
from dedoc.data_structures.concrete_annotations.indentation_annotation import IndentationAnnotation
from dedoc.data_structures.concrete_annotations.italic_annotation import ItalicAnnotation
from dedoc.data_structures.concrete_annotations.size_annotation import SizeAnnotation
from dedoc.data_structures.concrete_annotations.spacing_annotation import SpacingAnnotation
from dedoc.data_structures.concrete_annotations.underlined_annotation import UnderlinedAnnotation
from dedoc.data_structures.line_with_meta import LineWithMeta
from dedoc.structure_extractors.feature_extractors.char_features import not_chars
from dedoc.structure_extractors.feature_extractors.toc_feature_extractor import TocItem
from dedoc.structure_extractors.hierarchy_level_builders.utils_reg import regexps_ends_of_number, regexps_number
from dedoc.utils.utils import list_get

import logging
logger = logging.getLogger(__name__)


# region CLASS_AbstractFeatureExtractor [DOMAIN(DocumentProcessing): ...; CONCEPT(FeatureEngineering): ...; TECH(Pandas): ...]
## @purpose AbstractFeatureExtractor for document structure extraction pipeline
class AbstractFeatureExtractor(ABC):

    # region METHOD___init__ [DOMAIN(X): ...; CONCEPT(Y): ...; TECH(Z): ...]
    ## @purpose Initialize base feature extractor with logger
    ## @io Optional[dict] -> None
    ## @complexity 1
    def __init__(self, *, config: Optional[dict] = None):
        self.logger = (config or {}).get("logger", logging.getLogger(__name__)) if config else logging.getLogger(__name__)
    # endregion METHOD___init__

    # region METHOD_parameters [DOMAIN(X): ...; CONCEPT(Y): ...; TECH(Z): ...]
    ## @purpose parameters method
    ## @io Input -> Output
    ## @complexity 5
    @abstractmethod
    def parameters(self) -> dict:
        self.logger.debug(f"[IMP:4][AbstractFeatureExtractor][parameters_INIT] Starting")
        """
        Returns the dictionary with parameters for the `__init__` method of the feature extractor.
        """
        pass

    # endregion METHOD_parameters
    # region METHOD_transform [DOMAIN(X): ...; CONCEPT(Y): ...; TECH(Z): ...]
    ## @purpose transform method
    ## @io Input -> Output
    ## @complexity 5
    @abstractmethod
    def transform(self, documents: List[List[LineWithMeta]], toc_lines: Optional[List[List[TocItem]]] = None) -> pd.DataFrame:
        self.logger.debug(f"[IMP:4][AbstractFeatureExtractor][transform_INIT] Starting")
        """
        Extract a list of float features for each document line.

        :param documents: list of documents in form of list of lines
        :param toc_lines:
        :returns: matrix of features extracted for the document
        """
        pass

    # endregion METHOD_transform
    # region METHOD_prev_next_line_features [DOMAIN(X): ...; CONCEPT(Y): ...; TECH(Z): ...]
    ## @purpose prev_next_line_features method
    ## @io Input -> Output
    ## @complexity 5
    def prev_next_line_features(self, matrix: pd.DataFrame, n_prev: int, n_next: int) -> pd.DataFrame:
        self.logger.debug(f"[IMP:4][AbstractFeatureExtractor][prev_next_line_features_INIT] Starting")
        """
        Add features of previous and next lines to the input feature matrix.
        For each document line, `n_prev` features of previous lines and `n_next` features of next lines will be added.
        For lines that don't have previous/next lines, zeros are added as features

        :param matrix: matrix where rows are lines, columns are features
        :param n_prev: the number of previous lines, those features is needed to add to the current line's features
        :param n_next: the number of next lines, those features is needed to add to the current line's features
        :return: feature matrix with added features
        """
        feature_names = matrix.columns
        prev_line_features = [
            pd.DataFrame(data=self._prev_line_features(matrix.values, i), columns=self.__create_features_name(feature_names, "prev", i))
            for i in range(1, n_prev + 1)
        ]
        next_line_features = [
            pd.DataFrame(data=self._next_line_features(matrix.values, i), columns=self.__create_features_name(feature_names, "next", i))
            for i in range(1, n_next + 1)
        ]

        matrices = [matrix] + prev_line_features + next_line_features
        result_matrix = pd.concat(matrices, axis=1)
        return result_matrix

    # endregion METHOD_prev_next_line_features
    # region METHOD__prev_line_features [DOMAIN(X): ...; CONCEPT(Y): ...; TECH(Z): ...]
    ## @purpose _prev_line_features method
    ## @io Input -> Output
    ## @complexity 5
    @staticmethod
    def _prev_line_features(feature_matrix: np.ndarray, n: int) -> np.ndarray:
        # BUG_FIX_CONTEXT: self.logger недоступен в @staticmethod; заменён на модульный logger
        logger.debug(f"[IMP:4][AbstractFeatureExtractor][_prev_line_features_INIT] Starting")
        """
        :param feature_matrix: matrix where rows are lines, columns are features
        :param n: the number of previous lines, those features is needed to add to the current line's features
        :return: feature matrix where lines were shifted on n lines downwards (feature matrix for n previous lines, for the first n lines zeros are added)
        """
        if n > feature_matrix.shape[0]:
            return np.zeros(feature_matrix.shape)
        return np.vstack((np.zeros((n, feature_matrix.shape[1])), feature_matrix[:-n, :]))

    # endregion METHOD__prev_line_features
    # region METHOD__next_line_features [DOMAIN(X): ...; CONCEPT(Y): ...; TECH(Z): ...]
    ## @purpose _next_line_features method
    ## @io Input -> Output
    ## @complexity 5
    @staticmethod
    def _next_line_features(feature_matrix: np.ndarray, n: int) -> np.ndarray:
        # BUG_FIX_CONTEXT: self.logger недоступен в @staticmethod; заменён на модульный logger
        logger.debug(f"[IMP:4][AbstractFeatureExtractor][_next_line_features_INIT] Starting")
        """
        :param feature_matrix: matrix where rows are lines, columns are features
        :param n: the number of next lines, those features is needed to add to the current line's features
        :return: feature matrix where lines were shifted on n lines upwards (feature matrix for n next lines, for the last n lines zeros are added)
        """
        if n > feature_matrix.shape[0]:
            return np.zeros(feature_matrix.shape)
        return np.vstack((feature_matrix[n:, :], np.zeros((n, feature_matrix.shape[1]))))

    # endregion METHOD__next_line_features
    # region METHOD___create_features_name [DOMAIN(X): ...; CONCEPT(Y): ...; TECH(Z): ...]
    ## @purpose __create_features_name method
    ## @io Input -> Output
    ## @complexity 5
    def __create_features_name(self, old_names: pd.Index, which: str, num: int) -> List[str]:
        self.logger.debug(f"[IMP:4][AbstractFeatureExtractor][__create_features_name_INIT] Starting")
        return [f"{old_name}_{which}_{num}" for old_name in old_names]

    # endregion METHOD___create_features_name
    # region METHOD__start_regexp [DOMAIN(X): ...; CONCEPT(Y): ...; TECH(Z): ...]
    ## @purpose _start_regexp method
    ## @io Input -> Output
    ## @complexity 5
    def _start_regexp(self, line: str, regexps: List[Pattern], suffix: Optional[str] = None) -> Iterable[Tuple[str, float]]:
        self.logger.debug(f"[IMP:4][AbstractFeatureExtractor][_start_regexp_INIT] Starting")
        """
        Apply regular expressions to the given line, calculate the length of the match and number of matches in the line

        :param line: document line
        :param regexps: list of regular expressions that will be applied to the line
        :param suffix: the additional info for feature naming
        :return: feature name + value, values are length of the match and number of matches
        """
        matches = 0
        text = line.strip()
        for i, pattern in enumerate(regexps):  # list patterns
            feature_name = f"start_regexp_{i}" if suffix is None else f"start_regexp_{i}_{suffix}"

            match = pattern.match(text)
            if match is not None and match.end() > 0:
                matches += 1
                yield feature_name, match.end() - match.start()
            else:
                yield feature_name, 0

        if suffix is None:
            yield "start_regexp_num_matches", matches
        else:
            yield f"start_regexp_num_matches_{suffix}", matches

    # endregion METHOD__start_regexp
    # region METHOD__get_size [DOMAIN(X): ...; CONCEPT(Y): ...; TECH(Z): ...]
    ## @purpose _get_size method
    ## @io Input -> Output
    ## @complexity 5
    @staticmethod
    def _get_size(line: LineWithMeta) -> float:
        # BUG_FIX_CONTEXT: self.logger недоступен в @staticmethod; заменён на модульный logger
        logger.debug(f"[IMP:4][AbstractFeatureExtractor][_get_size_INIT] Starting")
        """
        :param line: document line
        :return: font size value
        """
        sizes = [annotation for annotation in line.annotations if annotation.name == SizeAnnotation.name]  # font size
        return float(sizes[0].value) if len(sizes) > 0 else 0.

    # endregion METHOD__get_size
    # region METHOD__get_bold [DOMAIN(X): ...; CONCEPT(Y): ...; TECH(Z): ...]
    ## @purpose _get_bold method
    ## @io Input -> Output
    ## @complexity 5
    @staticmethod
    def _get_bold(line: LineWithMeta) -> float:
        # BUG_FIX_CONTEXT: self.logger недоступен в @staticmethod; заменён на модульный logger
        logger.debug(f"[IMP:4][AbstractFeatureExtractor][_get_bold_INIT] Starting")
        """
        :param line: document line
        :return: indicator if there are some parts of the line bold
        """
        bold = [annotation for annotation in line.annotations if annotation.name == BoldAnnotation.name and annotation.value == "True"]
        return 1. if len(bold) > 0 else 0

    # endregion METHOD__get_bold
    # region METHOD__get_bold_percent [DOMAIN(X): ...; CONCEPT(Y): ...; TECH(Z): ...]
    ## @purpose _get_bold_percent method
    ## @io Input -> Output
    ## @complexity 5
    @staticmethod
    def _get_bold_percent(line: LineWithMeta) -> float:
        # BUG_FIX_CONTEXT: self.logger недоступен в @staticmethod; заменён на модульный logger
        logger.debug(f"[IMP:4][AbstractFeatureExtractor][_get_bold_percent_INIT] Starting")
        """
        :param line: document line
        :return: the percent of bold characters in a line
        """
        bold_character_number = sum([
            annotation.end - annotation.start for annotation in line.annotations if annotation.name == BoldAnnotation.name and annotation.value == "True"
        ])
        if len(line.line.strip()) == 0:
            return 0
        return min(bold_character_number / len(line.line.strip()), 1.0)

    # endregion METHOD__get_bold_percent
    # region METHOD__is_first_bold [DOMAIN(X): ...; CONCEPT(Y): ...; TECH(Z): ...]
    ## @purpose _is_first_bold method
    ## @io Input -> Output
    ## @complexity 5
    @staticmethod
    def _is_first_bold(line: LineWithMeta) -> float:
        # BUG_FIX_CONTEXT: self.logger недоступен в @staticmethod; заменён на модульный logger
        logger.debug(f"[IMP:4][AbstractFeatureExtractor][_is_first_bold_INIT] Starting")
        """
        :param line: document line
        :return: indicator if the beginning of the line is bold
        """
        for annotation in line.annotations:
            if annotation.name == BoldAnnotation.name and annotation.value == "True" and annotation.start == 0:
                return 1.
        return 0

    # endregion METHOD__is_first_bold
    # region METHOD__get_italic [DOMAIN(X): ...; CONCEPT(Y): ...; TECH(Z): ...]
    ## @purpose _get_italic method
    ## @io Input -> Output
    ## @complexity 5
    @staticmethod
    def _get_italic(line: LineWithMeta) -> float:
        # BUG_FIX_CONTEXT: self.logger недоступен в @staticmethod; заменён на модульный logger
        logger.debug(f"[IMP:4][AbstractFeatureExtractor][_get_italic_INIT] Starting")
        """
        :param line: document line
        :return: indicator if there are some parts of the line italic
        """
        italic = [annotation for annotation in line.annotations if annotation.name == ItalicAnnotation.name]
        return 1. if len(italic) > 0 else 0

    # endregion METHOD__get_italic
    # region METHOD__get_underlined [DOMAIN(X): ...; CONCEPT(Y): ...; TECH(Z): ...]
    ## @purpose _get_underlined method
    ## @io Input -> Output
    ## @complexity 5
    @staticmethod
    def _get_underlined(line: LineWithMeta) -> float:
        # BUG_FIX_CONTEXT: self.logger недоступен в @staticmethod; заменён на модульный logger
        logger.debug(f"[IMP:4][AbstractFeatureExtractor][_get_underlined_INIT] Starting")
        """
        :param line: document line
        :return: indicator if there are some parts of the line underlined
        """
        underlined = [annotation for annotation in line.annotations if annotation.name == UnderlinedAnnotation.name]
        return 1. if len(underlined) > 0 else 0

    # endregion METHOD__get_underlined
    # region METHOD__get_percent_upper_letters [DOMAIN(X): ...; CONCEPT(Y): ...; TECH(Z): ...]
    ## @purpose _get_percent_upper_letters method
    ## @io Input -> Output
    ## @complexity 5
    def _get_percent_upper_letters(self, line: LineWithMeta) -> float:
        self.logger.debug(f"[IMP:4][AbstractFeatureExtractor][_get_percent_upper_letters_INIT] Starting")
        count_upper = 0
        count_chars = 0
        for symbol in line.line.strip():
            if not symbol.isspace() and symbol not in not_chars:
                if symbol.isupper():
                    count_upper += 1
                count_chars += 1
        return min(count_upper / count_chars if count_chars != 0 else 0.0, 1.0)

    # endregion METHOD__get_percent_upper_letters
    # region METHOD__get_before_toc [DOMAIN(X): ...; CONCEPT(Y): ...; TECH(Z): ...]
    ## @purpose _get_before_toc method
    ## @io Input -> Output
    ## @complexity 5
    def _get_before_toc(self, line: LineWithMeta, toc_items: List[TocItem]) -> bool:
        self.logger.debug(f"[IMP:4][AbstractFeatureExtractor][_get_before_toc_INIT] Starting")
        if toc_items:
            return line.metadata.line_id < toc_items[0].line.metadata.line_id
        else:
            return False

    # endregion METHOD__get_before_toc
    # region METHOD__get_color [DOMAIN(X): ...; CONCEPT(Y): ...; TECH(Z): ...]
    ## @purpose _get_color method
    ## @io Input -> Output
    ## @complexity 5
    @staticmethod
    def _get_color(line: LineWithMeta) -> Iterable[Tuple[str, float]]:
        # BUG_FIX_CONTEXT: self.logger недоступен в @staticmethod; заменён на модульный logger
        logger.debug(f"[IMP:4][AbstractFeatureExtractor][_get_color_INIT] Starting")
        """
        :param line: document line
        :return: color values (R,G,B+color dispersion) with features names
        """
        color = [annotation for annotation in line.annotations if annotation.name == ColorAnnotation.name]
        if len(color) == 0:
            value = {}
        else:
            value = json.loads(color[0].value)
        red = value.get("red", 0)
        green = value.get("green", 0)
        blue = value.get("blue", 0)
        yield "red", red
        yield "green", green
        yield "blue", blue
        mean = (red + green + blue) / 3
        yield "color_dispersion", sum([(c - mean) ** 2 for c in (red, green, blue)]) / 2

    # endregion METHOD__get_color
    # region METHOD__get_spacing [DOMAIN(X): ...; CONCEPT(Y): ...; TECH(Z): ...]
    ## @purpose _get_spacing method
    ## @io Input -> Output
    ## @complexity 5
    @staticmethod
    def _get_spacing(line: LineWithMeta) -> float:
        # BUG_FIX_CONTEXT: self.logger недоступен в @staticmethod; заменён на модульный logger
        logger.debug(f"[IMP:4][AbstractFeatureExtractor][_get_spacing_INIT] Starting")
        """
        :param line: document line
        :return: spacing value (distance between two lines)
        """
        spacing = [annotation for annotation in line.annotations if annotation.name == SpacingAnnotation.name]
        return float(spacing[0].value) if len(spacing) > 0 else -1

    # endregion METHOD__get_spacing
    # region METHOD__get_indentation [DOMAIN(X): ...; CONCEPT(Y): ...; TECH(Z): ...]
    ## @purpose _get_indentation method
    ## @io Input -> Output
    ## @complexity 5
    @staticmethod
    def _get_indentation(line: LineWithMeta) -> float:
        # BUG_FIX_CONTEXT: self.logger недоступен в @staticmethod; заменён на модульный logger
        logger.debug(f"[IMP:4][AbstractFeatureExtractor][_get_indentation_INIT] Starting")
        """
        :param line: document line
        :return: indentation value (distance between line and document margin)
        """
        indentation = [annotation for annotation in line.annotations if isinstance(annotation, IndentationAnnotation)]
        return float(indentation[0].value) if len(indentation) > 0 else 0

    # endregion METHOD__get_indentation
    # region METHOD__can_be_prev_element [DOMAIN(X): ...; CONCEPT(Y): ...; TECH(Z): ...]
    ## @purpose _can_be_prev_element method
    ## @io Input -> Output
    ## @complexity 5
    @staticmethod
    def _can_be_prev_element(this_item: Optional[str], prev_item: Optional[str]) -> bool:
        # BUG_FIX_CONTEXT: self.logger недоступен в @staticmethod; заменён на модульный logger
        logger.debug(f"[IMP:4][AbstractFeatureExtractor][_can_be_prev_element_INIT] Starting")
        """
        Check if `prev_item` can be the previous element of `this_item` in the correct list
        For example, "2" can be previous element of "3", "2.1." can be previous element of "2.1.1"
        If `prev_item` is None then `this_item` is the first item in the list and should be 1

        :param this_item: text of the current list item
        :param this_item: text of the previous list item
        :return: True if `prev_item` can be the previous element of `this_item`
        """
        if this_item is None:
            return False
        this_item_list = [i for i in this_item.split(".") if len(i) > 0]
        if this_item_list == ["1"]:
            return True
        if prev_item is None:
            return False
        prev_item_list = [i for i in prev_item.split(".") if len(i) > 0]
        if len(prev_item_list) > len(this_item_list):
            return False
        if len(prev_item_list) < len(this_item_list) - 1:
            return False
        this_item_prefix = this_item_list[:-1]
        prev_item_prefix = prev_item_list[:-1]
        if len(prev_item_list) == len(this_item_list) - 1:
            return prev_item_list == this_item_prefix and this_item_list[-1] == "1"
        if len(prev_item_list) == len(this_item_list):
            return prev_item_prefix == this_item_prefix and int(this_item_list[-1]) - int(prev_item_list[-1]) == 1
        raise Exception(f"Unexpected case where this_item = {this_item} prev_item = {prev_item}")

    # endregion METHOD__can_be_prev_element
    # region METHOD__before_special_line [DOMAIN(X): ...; CONCEPT(Y): ...; TECH(Z): ...]
    ## @purpose _before_special_line method
    ## @io Input -> Output
    ## @complexity 5
    def _before_special_line(self, document: List[LineWithMeta], find_special_line: method) -> List[float]:
        self.logger.debug(f"[IMP:4][AbstractFeatureExtractor][_before_special_line_INIT] Starting")
        """
        Find "distance" to the closest special line in the document.
        If line is located before the special line, then distance is negative, if line is after special line then distance is positive,
        for special line distance is 0.
        If there is no special line in the document then distance is 0 for every line.

        :param document: document in form of list of lines
        :param find_special_line: function that finds some special line, see `__find_toc` for example
        :return: list of distances from given line to first special line
        """
        result = []
        special_line_position = find_special_line(document)
        if special_line_position is None:
            result.extend([0. for _ in document])
        else:
            special_line_id = special_line_position[-1]
            for line_id in range(len(document)):
                result.append(line_id - special_line_id)
        return result

    # endregion METHOD__before_special_line
    # region METHOD__list_features [DOMAIN(X): ...; CONCEPT(Y): ...; TECH(Z): ...]
    ## @purpose _list_features method
    ## @io Input -> Output
    ## @complexity 5
    def _list_features(self, lines: List[LineWithMeta], list_item_regexp: Pattern = regexps_number, end_regexp: Pattern = regexps_ends_of_number) \
            -> List[float]:
        self.logger.debug(f"[IMP:4][AbstractFeatureExtractor][_list_features_INIT] Starting")
        """
        For each line, the indicator is computed if the line is a list item.
        The indicator is obtained using regular expressions and checking, if list items form the correct list.

        :param lines: list of document lines
        :param list_item_regexp: regular expression for a list item
        :param end_regexp: regular expression for a text after the list item
        :return: list of indicators if a line is a list item
        """
        previous_ids = [-1]
        texts = [line.line.strip().strip() for line in lines]
        matches = map(list_item_regexp.match, texts)
        numbers = [(line_id, match.group().strip()) for line_id, match in enumerate(matches) if match]

        for num, (line_id, number) in enumerate(numbers):
            searched = end_regexp.search(number)
            if searched is not None:
                numbers[num] = (line_id, number[:searched.start()])
            if number.endswith((")", "}", ".")):
                numbers[num] = (line_id, number[:-1])

        if len(numbers) == 0:
            return [0 for _ in lines]
        line_ids, numbers = zip(*numbers)

        result_numbers = []
        for i in range(len(numbers)):
            one_item = []
            this_item = numbers[i]
            for k in previous_ids:
                prev_item = list_get(numbers, i + k)
                one_item.append(1 if self._can_be_prev_element(this_item=this_item, prev_item=prev_item) else -1)
            one_item = max(one_item)
            result_numbers.append(one_item)
        result = [0 for _ in lines]
        for line_id, one_item in zip(line_ids, result_numbers):
            result[line_id] = one_item
        return result

    # endregion METHOD__list_features
    # region METHOD__get_features_quantile [DOMAIN(X): ...; CONCEPT(Y): ...; TECH(Z): ...]
    ## @purpose _get_features_quantile method
    ## @io Input -> Output
    ## @complexity 5
    @staticmethod
    def _get_features_quantile(feature_column: pd.Series) -> pd.Series:
        # BUG_FIX_CONTEXT: self.logger недоступен в @staticmethod; заменён на модульный logger
        logger.debug(f"[IMP:4][AbstractFeatureExtractor][_get_features_quantile_INIT] Starting")
        """
        :param feature_column: column with one feature
        :return: column with feature's quantiles
        """
        feature_column = feature_column.fillna(feature_column.min() - 1)
        feature_column_s = np.sort(feature_column)
        feature_quantiles = np.searchsorted(feature_column_s, feature_column, "left")
        feature_quantiles += np.searchsorted(feature_column_s, feature_column, "right")
        feature_quantiles = feature_quantiles / 2 / feature_column.shape[0]
        return pd.Series(feature_quantiles)

    # endregion METHOD__get_features_quantile
    # region METHOD__normalize_features [DOMAIN(X): ...; CONCEPT(Y): ...; TECH(Z): ...]
    ## @purpose _normalize_features method
    ## @io Input -> Output
    ## @complexity 5
    @staticmethod
    def _normalize_features(feature_column: pd.Series) -> pd.Series:
        # BUG_FIX_CONTEXT: self.logger недоступен в @staticmethod; заменён на модульный logger
        logger.debug(f"[IMP:4][AbstractFeatureExtractor][_normalize_features_INIT] Starting")
        """
        new_feature = (feature - mean) / (max - min) if max = min else 0

        :param feature_column: column with one feature
        :return: normalized feature vector  [-1; 1]
        """
        feature_mean, feature_min, feature_max = feature_column.mean(), feature_column.min(), feature_column.max()
        new_feature_column = (feature_column - feature_mean) / (feature_max - feature_min) if feature_max - feature_min != 0.0 else 0.0
        return new_feature_column

    # endregion METHOD__normalize_features
# endregion CLASS_AbstractFeatureExtractor
# region MODULE_CONTRACT [DOMAIN(DocumentProcessing): ...; CONCEPT(FeatureEngineering): ...; TECH(Pandas): ...]
## @modulecontract
## @purpose Document structure extraction for structure_extractors/feature_extractors/abstract_extractor: line classification, hierarchy level assignment, pattern matching.
## @scope Structure extraction pipeline — structure_extractors/feature_extractors/abstract_extractor
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
## CLASS [Weight 7][Structure extraction] => AbstractFeatureExtractor
## @usecases
## - Extract structure: Reader → StructureExtractor → HierarchyBuilder → AnnotatedDocument
def _module_contract():
    pass
# endregion MODULE_CONTRACT
# GREP_SUMMARY: structure extractors, feature extractors, abstract extractor
# STRUCTURE: ▶ structure_extractors/feature_extractors/abstract_extractor → ○ AbstractFeatureExtractor.cls → ⎋ result