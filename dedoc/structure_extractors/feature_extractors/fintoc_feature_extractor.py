import re
from collections import defaultdict
from typing import Dict, Iterator, List, Optional, Tuple

import pandas as pd
from Levenshtein import ratio

from dedoc.data_structures.line_with_meta import LineWithMeta
from dedoc.structure_extractors.feature_extractors.abstract_extractor import AbstractFeatureExtractor
from dedoc.structure_extractors.feature_extractors.list_features.list_features_extractor import ListFeaturesExtractor
from dedoc.structure_extractors.feature_extractors.list_features.prefix.any_letter_prefix import AnyLetterPrefix
from dedoc.structure_extractors.feature_extractors.list_features.prefix.bracket_prefix import BracketPrefix
from dedoc.structure_extractors.feature_extractors.list_features.prefix.bracket_roman_prefix import BracketRomanPrefix
from dedoc.structure_extractors.feature_extractors.list_features.prefix.bullet_prefix import BulletPrefix
from dedoc.structure_extractors.feature_extractors.list_features.prefix.dotted_prefix import DottedPrefix
from dedoc.structure_extractors.feature_extractors.list_features.prefix.empty_prefix import EmptyPrefix
from dedoc.structure_extractors.feature_extractors.list_features.prefix.letter_prefix import LetterPrefix
from dedoc.structure_extractors.feature_extractors.list_features.prefix.roman_prefix import RomanPrefix
from dedoc.structure_extractors.feature_extractors.paired_feature_extractor import PairedFeatureExtractor
from dedoc.structure_extractors.feature_extractors.toc_feature_extractor import TOCFeatureExtractor, TocItem
from dedoc.structure_extractors.feature_extractors.utils_feature_extractor import normalization_by_min_max
from dedoc.structure_extractors.hierarchy_level_builders.utils_reg import regexps_year

import logging
logger = logging.getLogger(__name__)


# region CLASS_FintocFeatureExtractor [DOMAIN(DocumentProcessing): ...; CONCEPT(FeatureEngineering): ...; TECH(Pandas): ...]
## @purpose FintocFeatureExtractor for document structure extraction pipeline
class FintocFeatureExtractor(AbstractFeatureExtractor):

    # region METHOD___init__ [DOMAIN(X): ...; CONCEPT(Y): ...; TECH(Z): ...]
    ## @purpose __init__ method
    ## @io Input -> Output
    ## @complexity 5
    def __init__(self) -> None:
        super().__init__()

        self.logger.debug(f"[IMP:4][FintocFeatureExtractor][__init___INIT] Starting")
        self.paired_feature_extractor = PairedFeatureExtractor()
        self.prefix_list = [BulletPrefix, AnyLetterPrefix, LetterPrefix, BracketPrefix, BracketRomanPrefix, DottedPrefix, RomanPrefix]
        self.list_feature_extractors = [
            ListFeaturesExtractor(window_size=10, prefix_list=self.prefix_list),
            ListFeaturesExtractor(window_size=25, prefix_list=self.prefix_list),
            ListFeaturesExtractor(window_size=100, prefix_list=self.prefix_list)
        ]
        self.prefix2number = {prefix.name: i for i, prefix in enumerate(self.prefix_list, start=1)}
        self.prefix2number[EmptyPrefix.name] = 0

    # endregion METHOD___init__
    # region METHOD_parameters [DOMAIN(X): ...; CONCEPT(Y): ...; TECH(Z): ...]
    ## @purpose parameters method
    ## @io Input -> Output
    ## @complexity 5
    def parameters(self) -> dict:
        self.logger.debug(f"[IMP:4][FintocFeatureExtractor][parameters_INIT] Starting")
        return {}

    # endregion METHOD_parameters
    # region METHOD_transform [DOMAIN(X): ...; CONCEPT(Y): ...; TECH(Z): ...]
    ## @purpose transform method
    ## @io Input -> Output
    ## @complexity 5
    def transform(self, documents: List[List[LineWithMeta]], toc_lines: Optional[List[List[TocItem]]] = None) -> pd.DataFrame:
        self.logger.debug(f"[IMP:4][FintocFeatureExtractor][transform_INIT] Starting")
        assert len(documents) > 0
        result_matrix = pd.concat([self.__process_document(document, d_toc_lines) for document, d_toc_lines in zip(documents, toc_lines)], ignore_index=True)
        result_matrix = pd.concat([result_matrix, self.paired_feature_extractor.transform(documents)], axis=1)
        features = sorted(result_matrix.columns)
        result_matrix = result_matrix[features].astype(float)
        return result_matrix[features]

    # endregion METHOD_transform
    # region METHOD___process_document [DOMAIN(X): ...; CONCEPT(Y): ...; TECH(Z): ...]
    ## @purpose __process_document method
    ## @io Input -> Output
    ## @complexity 5
    def __process_document(self, lines: List[LineWithMeta], toc: Optional[List[TocItem]] = None) -> pd.DataFrame:
        self.logger.debug(f"[IMP:4][FintocFeatureExtractor][__process_document_INIT] Starting")
        features_df = pd.DataFrame(self.__look_at_prev_line(document=lines, n=1))
        features_df["line_relative_length"] = self.__get_line_relative_length(lines)

        list_features = pd.concat([f_e.one_document(lines)[1] for f_e in self.list_feature_extractors], axis=1)

        page_ids = [line.metadata.page_id for line in lines]
        start_page, finish_page = (min(page_ids), max(page_ids)) if page_ids else (0, 0)

        total_lines = len(lines)
        one_line_features_dict = defaultdict(list)
        for line in lines:
            for item in self.__one_line_features(line, total_lines, start_page=start_page, finish_page=finish_page, toc=toc):
                feature_name, feature = item[0], item[1]
                one_line_features_dict[feature_name].append(feature)

        one_line_features_df = pd.DataFrame(one_line_features_dict)
        one_line_features_df["font_size"] = self._normalize_features(one_line_features_df.font_size)

        one_line_features_df = self.prev_next_line_features(one_line_features_df, 3, 3)
        result_matrix = pd.concat([one_line_features_df, features_df, list_features], axis=1)
        result_matrix["page_id"] = [line.metadata.page_id for line in lines]
        return result_matrix

    # endregion METHOD___process_document
    # region METHOD___look_at_prev_line [DOMAIN(X): ...; CONCEPT(Y): ...; TECH(Z): ...]
    ## @purpose __look_at_prev_line method
    ## @io Input -> Output
    ## @complexity 5
    def __look_at_prev_line(self, document: List[LineWithMeta], n: int = 1) -> Dict[str, List]:
        self.logger.debug(f"[IMP:4][FintocFeatureExtractor][__look_at_prev_line_INIT] Starting")
        """
        Look at previous line and compare with current line

        :param document: list of lines
        :param n: previous line number to look
        :return: dict of features
        """
        res = defaultdict(list)
        for line_id, _ in enumerate(document):
            if line_id >= n:
                prev_line = document[line_id - n]
                res["prev_line_ends"].append(prev_line.line.endswith((".", ";")))
                res["prev_ends_with_colon"].append(prev_line.line.endswith(":"))
                res["prev_is_space"].append(prev_line.line.lower().isspace())
            else:
                res["prev_line_ends"].append(False)
                res["prev_ends_with_colon"].append(False)
                res["prev_is_space"].append(False)
        return res

    # endregion METHOD___look_at_prev_line
    # region METHOD___get_line_relative_length [DOMAIN(X): ...; CONCEPT(Y): ...; TECH(Z): ...]
    ## @purpose __get_line_relative_length method
    ## @io Input -> Output
    ## @complexity 5
    def __get_line_relative_length(self, lines: List[LineWithMeta]) -> List[float]:
        self.logger.debug(f"[IMP:4][FintocFeatureExtractor][__get_line_relative_length_INIT] Starting")
        max_len = max([len(line.line) for line in lines])
        relative_lengths = [len(line.line) / max_len for line in lines]
        return relative_lengths

    # endregion METHOD___get_line_relative_length
    # region METHOD___one_line_features [DOMAIN(X): ...; CONCEPT(Y): ...; TECH(Z): ...]
    ## @purpose __one_line_features method
    ## @io Input -> Output
    ## @complexity 5
    def __one_line_features(self, line: LineWithMeta, total_lines: int, start_page: int, finish_page: int, toc: Optional[List[TocItem]]) -> Iterator[tuple]:
        self.logger.debug(f"[IMP:4][FintocFeatureExtractor][__one_line_features_INIT] Starting")
        yield "normalized_page_id", normalization_by_min_max(line.metadata.page_id, min_v=start_page, max_v=finish_page)
        yield "indentation", self._get_indentation(line)
        yield "spacing", self._get_spacing(line)
        yield "bold", self._get_bold(line)
        yield "italic", self._get_italic(line)
        yield from self._get_color(line)
        yield "font_size", self._get_size(line)

        yield "line_id", normalization_by_min_max(line.metadata.line_id, min_v=0, max_v=total_lines)
        yield "num_year_regexp", len(regexps_year.findall(line.line))
        yield "endswith_dot", line.line.endswith(".")
        yield "endswith_semicolon", line.line.endswith(";")
        yield "endswith_colon", line.line.endswith(":")
        yield "endswith_comma", line.line.endswith(",")
        yield "startswith_bracket", line.line.strip().startswith(("(", "{"))

        bracket_cnt = 0
        for char in line.line:
            if char == "(":
                bracket_cnt += 1
            elif char == ")":
                bracket_cnt = max(0, bracket_cnt - 1)
        yield "bracket_num", bracket_cnt

        probable_toc_title = re.sub(r"[\s:]", "", line.line).lower()
        yield "is_toc_title", probable_toc_title in TOCFeatureExtractor.titles
        yield from self.__find_in_toc(line, toc)

        line_length = len(line.line) + 1
        yield "supper_percent", sum((1 for letter in line.line if letter.isupper())) / line_length
        yield "letter_percent", sum((1 for letter in line.line if letter.isalpha())) / line_length
        yield "number_percent", sum((1 for letter in line.line if letter.isnumeric())) / line_length
        yield "words_number", len(line.line.split())

    # endregion METHOD___one_line_features
    # region METHOD___find_in_toc [DOMAIN(X): ...; CONCEPT(Y): ...; TECH(Z): ...]
    ## @purpose __find_in_toc method
    ## @io Input -> Output
    ## @complexity 5
    def __find_in_toc(self, line: LineWithMeta, toc: Optional[List[TocItem]]) -> Iterator[Tuple[str, int]]:
        self.logger.debug(f"[IMP:4][FintocFeatureExtractor][__find_in_toc_INIT] Starting")
        if toc is None:
            yield "is_toc", 0
            yield "in_toc", 0
            yield "toc_exists", 0
        else:
            is_toc, in_toc, toc_exists = 0, 0, int(len(toc) > 0)
            line_text = line.line.lower().strip()
            for item in toc:
                if ratio(line_text, item.line.line.lower()) < 0.8:
                    continue
                # toc entry found
                try:
                    is_toc = 0 if line.metadata.page_id + 1 == int(item.page) else 1
                    in_toc = 1 if line.metadata.page_id + 1 == int(item.page) else 0
                except TypeError:
                    pass
                break

            yield "is_toc", is_toc
            yield "in_toc", in_toc
            yield "toc_exists", toc_exists

    # endregion METHOD___find_in_toc
# endregion CLASS_FintocFeatureExtractor
# region MODULE_CONTRACT [DOMAIN(DocumentProcessing): ...; CONCEPT(FeatureEngineering): ...; TECH(Pandas): ...]
## @modulecontract
## @purpose Document structure extraction for structure_extractors/feature_extractors/fintoc_feature_extractor: line classification, hierarchy level assignment, pattern matching.
## @scope Structure extraction pipeline — structure_extractors/feature_extractors/fintoc_feature_extractor
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
## CLASS [Weight 7][Structure extraction] => FintocFeatureExtractor
## @usecases
## - Extract structure: Reader → StructureExtractor → HierarchyBuilder → AnnotatedDocument
def _module_contract():
    pass
# endregion MODULE_CONTRACT
# GREP_SUMMARY: structure extractors, feature extractors, fintoc feature extractor
# STRUCTURE: ▶ structure_extractors/feature_extractors/fintoc_feature_extractor → ○ FintocFeatureExtractor.cls → ⎋ result