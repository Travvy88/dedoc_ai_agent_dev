import re
from collections import Counter, defaultdict
from typing import Iterable, Iterator, List, Optional, Tuple

import pandas as pd

from dedoc.data_structures.line_with_meta import LineWithMeta
from dedoc.structure_extractors.feature_extractors.abstract_extractor import AbstractFeatureExtractor
from dedoc.structure_extractors.feature_extractors.list_features.list_features_extractor import ListFeaturesExtractor
from dedoc.structure_extractors.feature_extractors.list_features.prefix.bullet_prefix import BulletPrefix
from dedoc.structure_extractors.feature_extractors.toc_feature_extractor import TOCFeatureExtractor, TocItem
from dedoc.structure_extractors.feature_extractors.utils_feature_extractor import normalization_by_min_max
from dedoc.structure_extractors.hierarchy_level_builders.utils_reg import regexps_number, regexps_subitem_extended, regexps_year
from dedoc.utils.utils import flatten

import logging
logger = logging.getLogger(__name__)


# region CLASS_TzTextFeatures [DOMAIN(DocumentProcessing): ...; CONCEPT(FeatureEngineering): ...; TECH(Pandas): ...]
## @purpose TzTextFeatures for document structure extraction pipeline
class TzTextFeatures(AbstractFeatureExtractor):

    named_item_regexp = re.compile(r"^(под)?раздел\s*")
    toc_extractor = TOCFeatureExtractor()

    # region METHOD___init__ [DOMAIN(X): ...; CONCEPT(Y): ...; TECH(Z): ...]
    ## @purpose __init__ method
    ## @io Input -> Output
    ## @complexity 5
    def __init__(self, text_features_only: bool = False) -> None:
        super().__init__()

        self.logger.debug(f"[IMP:4][TzTextFeatures][__init___INIT] Starting")
        self.list_item_regexp = [
            regexps_subitem_extended,
            re.compile(r"^\s*[IVX]+"),  # roman numerals
            # https://stackoverflow.com/questions/267399/how-do-you-match-only-valid-
            # roman-numerals-with-a-regular-expression
            BulletPrefix.regexp,
            self.named_item_regexp
        ]
        self.end_regexp = [
            re.compile(r"\d+$")
        ]
        self.text_features_only = text_features_only
        self.list_feature_extractor = ListFeaturesExtractor()

    # endregion METHOD___init__
    # region METHOD_parameters [DOMAIN(X): ...; CONCEPT(Y): ...; TECH(Z): ...]
    ## @purpose parameters method
    ## @io Input -> Output
    ## @complexity 5
    def parameters(self) -> dict:
        self.logger.debug(f"[IMP:4][TzTextFeatures][parameters_INIT] Starting")
        return {"text_features_only": self.text_features_only}

    # endregion METHOD_parameters
    # region METHOD_transform [DOMAIN(X): ...; CONCEPT(Y): ...; TECH(Z): ...]
    ## @purpose transform method
    ## @io Input -> Output
    ## @complexity 5
    def transform(self, documents: List[List[LineWithMeta]], toc_lines: Optional[List[List[TocItem]]] = None) -> pd.DataFrame:
        self.logger.debug(f"[IMP:4][TzTextFeatures][transform_INIT] Starting")
        list_features = self.list_feature_extractor.transform(documents)
        result_matrix = pd.concat([self.__process_document(document) for document in documents], ignore_index=True)
        result_matrix["is_in_toc"] = list(flatten(self.toc_extractor.is_line_in_toc(document) for document in documents))
        result_matrix = pd.concat([result_matrix, list_features], axis=1)
        features = sorted(result_matrix.columns)
        cnt = Counter(features)
        assert cnt.most_common(1)[0][1] == 1, cnt.most_common(3)

        return result_matrix[features].astype(float)

    # endregion METHOD_transform
    # region METHOD___process_document [DOMAIN(X): ...; CONCEPT(Y): ...; TECH(Z): ...]
    ## @purpose __process_document method
    ## @io Input -> Output
    ## @complexity 5
    def __process_document(self, lines: List[LineWithMeta]) -> pd.DataFrame:
        self.logger.debug(f"[IMP:4][TzTextFeatures][__process_document_INIT] Starting")
        features_df = pd.DataFrame({
            "toc": self._before_special_line(lines, self.__find_toc),
            "tz": self._before_special_line(lines, self.__find_tz),
            "list_item": self._list_features(lines)
        })

        page_ids = [line.metadata.page_id for line in lines]
        if page_ids:
            start_page, finish_page = min(page_ids), max(page_ids)
        else:
            start_page, finish_page = 0, 0

        one_line_features_dict = defaultdict(list)
        for line in lines:
            for item in self._one_line_features(line, len(lines), start_page=start_page, finish_page=finish_page):
                feature_name, feature = item[0], item[1]
                one_line_features_dict[feature_name].append(feature)
        one_line_features_df = pd.DataFrame(one_line_features_dict)
        one_line_features_df["indentation"] = self._normalize_features(one_line_features_df.indentation)

        one_line_features_df = self.prev_next_line_features(one_line_features_df, 3, 3)

        result_matrix = pd.concat([one_line_features_df, features_df], axis=1)
        return result_matrix

    # endregion METHOD___process_document
    # region METHOD__one_line_features [DOMAIN(X): ...; CONCEPT(Y): ...; TECH(Z): ...]
    ## @purpose _one_line_features method
    ## @io Input -> Output
    ## @complexity 5
    def _one_line_features(self, line: LineWithMeta, total_lines: int, start_page: int, finish_page: int) -> Iterator[Tuple[str, int]]:
        self.logger.debug(f"[IMP:4][TzTextFeatures][_one_line_features_INIT] Starting")
        text = line.line.lower()

        yield from self._start_regexp(line.line, self.list_item_regexp)
        yield ("named_item_regexp", 1) if self.named_item_regexp.match(text) else ("named_item_regexp", 0)
        yield ("is_upper", 1) if line.line.strip().isupper() else ("is_upper", 0)
        yield ("is_lower", 1) if line.line.strip().islower() else ("is_lower", 0)
        yield "day_month_regexp", int("дней" in text) + int("месяцев" in text)
        yield "year_regexp", len(regexps_year.findall(text))

        number = regexps_number.match(text)
        number = number.group().strip() if number else ""
        if number.endswith((")", "}")):
            number = number[:-1]
        yield ("dot_number_regexp", 1) if number.endswith(".") else ("dot_number_regexp", 0)
        yield "dot_number_regexp_len", len(number.split("."))
        yield "dot_number_regexp_max", max([int(n) for n in number.split(".") if n if n.isnumeric()], default=-1)

        yield "text_length", len(text)
        yield "words_number", len(text.split())
        yield "is_toc_line", int(text.strip() == "содержание")
        yield ("is_tz_line", 1) if "техническое" in text and "задание" in text else ("is_tz_line", 0)
        yield "line_id", normalization_by_min_max(line.metadata.line_id, min_v=0, max_v=total_lines)

        yield "indentation", self._get_indentation(line)
        if not self.text_features_only:
            yield "font_size", self._get_size(line)
            yield "bold", self._get_bold(line)
            yield from self._get_alignment(line)
            yield from self._get_style(line)
            yield "page_id", normalization_by_min_max(line.metadata.page_id, min_v=start_page, max_v=finish_page)

    # endregion METHOD__one_line_features
    # region METHOD__get_alignment [DOMAIN(X): ...; CONCEPT(Y): ...; TECH(Z): ...]
    ## @purpose _get_alignment method
    ## @io Input -> Output
    ## @complexity 5
    def _get_alignment(self, line: LineWithMeta) -> Iterable[Tuple[str, float]]:
        self.logger.debug(f"[IMP:4][TzTextFeatures][_get_alignment_INIT] Starting")
        alignment = {annotation.value for annotation in line.annotations if annotation.name == "alignment"}
        yield "alignment_left", 1 if "left" in alignment else 0
        yield "alignment_center", 1 if "center" in alignment else 0
        yield "alignment_right", 1 if "right" in alignment else 0

    # endregion METHOD__get_alignment
    # region METHOD__get_style [DOMAIN(X): ...; CONCEPT(Y): ...; TECH(Z): ...]
    ## @purpose _get_style method
    ## @io Input -> Output
    ## @complexity 5
    def _get_style(self, line: LineWithMeta) -> Tuple[str, float]:
        self.logger.debug(f"[IMP:4][TzTextFeatures][_get_style_INIT] Starting")
        style = "".join((annotation.value.lower() for annotation in line.annotations if annotation.name == "style"))
        yield "style_heading", 1 if "heading" in style else 0
        yield "style_contents", 1 if "contents" in style else 0

    # endregion METHOD__get_style
    # region METHOD__end_regexp [DOMAIN(X): ...; CONCEPT(Y): ...; TECH(Z): ...]
    ## @purpose _end_regexp method
    ## @io Input -> Output
    ## @complexity 5
    def _end_regexp(self, line: str) -> Iterable[int]:
        self.logger.debug(f"[IMP:4][TzTextFeatures][_end_regexp_INIT] Starting")
        matches = 0
        for pattern in self.end_regexp:  # list patterns
            match = pattern.findall(line.lower().strip())
            if match is not None and len(match) > 0:
                matches += 1
                yield 1
            else:
                yield 0
        yield matches

    # endregion METHOD__end_regexp
    # region METHOD___find_toc [DOMAIN(X): ...; CONCEPT(Y): ...; TECH(Z): ...]
    ## @purpose __find_toc method
    ## @io Input -> Output
    ## @complexity 5
    def __find_toc(self, document: List[LineWithMeta]) -> Optional[Tuple[int, int, int]]:
        self.logger.debug(f"[IMP:4][TzTextFeatures][__find_toc_INIT] Starting")
        """
        find start of table of content, we assume that start of toc should contain only one word:
         "содержание" or "оглавление"
        @param document: document in form of list of lines
        @return: tuple (page id from metadata, line id from metadata, index of line in list
        if there is no special line we return None
        """
        for line_id, line in enumerate(document):
            if line.line.strip().lower() in ("содержание", "оглавление"):
                return line.metadata.page_id, line.metadata.line_id, line_id
        return None

    # endregion METHOD___find_toc
    # region METHOD___find_tz [DOMAIN(X): ...; CONCEPT(Y): ...; TECH(Z): ...]
    ## @purpose __find_tz method
    ## @io Input -> Output
    ## @complexity 5
    def __find_tz(self, document: List[LineWithMeta]) -> Optional[Tuple[int, int, int]]:
        self.logger.debug(f"[IMP:4][TzTextFeatures][__find_tz_INIT] Starting")
        for line_id, line in enumerate(document):
            text = "".join(filter(str.isalpha, line.line)).lower()
            if text == "техническоезадание" or text == "приложение":
                return line.metadata.page_id, line.metadata.line_id, line_id
        return None

    # endregion METHOD___find_tz
    # region METHOD___find_item [DOMAIN(X): ...; CONCEPT(Y): ...; TECH(Z): ...]
    ## @purpose __find_item method
    ## @io Input -> Output
    ## @complexity 5
    def __find_item(self, document: List[LineWithMeta]) -> Optional[Tuple[int, int, int]]:
        self.logger.debug(f"[IMP:4][TzTextFeatures][__find_item_INIT] Starting")
        for line_id, line in enumerate(document):
            text = "".join(filter(str.isalpha, line.line))
            if list(self._start_regexp(text, self.list_item_regexp))[-1] > 0:
                return line.metadata.page_id, line.metadata.line_id, line_id
        return None

    # endregion METHOD___find_item
# endregion CLASS_TzTextFeatures
# region MODULE_CONTRACT [DOMAIN(DocumentProcessing): ...; CONCEPT(FeatureEngineering): ...; TECH(Pandas): ...]
## @modulecontract
## @purpose Document structure extraction for structure_extractors/feature_extractors/tz_feature_extractor: line classification, hierarchy level assignment, pattern matching.
## @scope Structure extraction pipeline — structure_extractors/feature_extractors/tz_feature_extractor
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
## CLASS [Weight 7][Structure extraction] => TzTextFeatures
## @usecases
## - Extract structure: Reader → StructureExtractor → HierarchyBuilder → AnnotatedDocument
def _module_contract():
    pass
# endregion MODULE_CONTRACT
# GREP_SUMMARY: structure extractors, feature extractors, tz feature extractor
# STRUCTURE: ▶ structure_extractors/feature_extractors/tz_feature_extractor → ○ TzTextFeatures.cls → ⎋ result