import re
from collections import defaultdict
from typing import Iterator, List, Optional, Tuple

import pandas as pd
from Levenshtein import ratio

from dedoc.data_structures.line_with_meta import LineWithMeta
from dedoc.structure_extractors.feature_extractors.abstract_extractor import AbstractFeatureExtractor
from dedoc.structure_extractors.feature_extractors.list_features.list_features_extractor import ListFeaturesExtractor
from dedoc.structure_extractors.feature_extractors.list_features.list_utils import get_prefix
from dedoc.structure_extractors.feature_extractors.list_features.prefix.dotted_prefix import DottedPrefix
from dedoc.structure_extractors.feature_extractors.toc_feature_extractor import TOCFeatureExtractor, TocItem
from dedoc.structure_extractors.feature_extractors.utils_feature_extractor import normalization_by_min_max
from dedoc.structure_extractors.hierarchy_level_builders.utils_reg import regexps_digits_with_dots, regexps_item

import logging
logger = logging.getLogger(__name__)


# region CLASS_DiplomaFeatureExtractor [DOMAIN(DocumentProcessing): ...; CONCEPT(FeatureEngineering): ...; TECH(Pandas): ...]
## @purpose DiplomaFeatureExtractor for document structure extraction pipeline
class DiplomaFeatureExtractor(AbstractFeatureExtractor):

    # region METHOD___init__ [DOMAIN(X): ...; CONCEPT(Y): ...; TECH(Z): ...]
    ## @purpose __init__ method
    ## @io Input -> Output
    ## @complexity 5
    def __init__(self) -> None:
        super().__init__()

        self.logger.debug(f"[IMP:4][DiplomaFeatureExtractor][__init___INIT] Starting")
        self.named_item_keywords = ("аннотация", "abstract", "введение", "заключение", "библиографическийсписок", "списоклитературы")
        self.named_item_start = ("приложени", "глава")
        self.raw_text_keywords = ("рисунок", "таблица")
        self.titles = ("бакалаврскаяработа", "магистерскаядиссертация", "выпускнаяквалификационнаяработа", "бакалаврскаяработа", "курсоваяработа", "(подпись)")
        self.title_keywords = ("автор:", "руководитель:", "научныйруководитель:")
        self.year_regexp = re.compile(r".*20\d\dг\.$")
        self.digits_with_dots_regexp = regexps_digits_with_dots
        self.only_digits_regexp = re.compile(r"^\s*\d+\s")

        self.start_regexps = [
            regexps_item,  # list like 1.
            self.digits_with_dots_regexp,  # lists like 1.1.1. or 1.1.1
            self.only_digits_regexp,  # digits and space after them
        ]
        self.list_feature_extractor = ListFeaturesExtractor()
        self.toc_extractor = TOCFeatureExtractor()

    # endregion METHOD___init__
    # region METHOD_parameters [DOMAIN(X): ...; CONCEPT(Y): ...; TECH(Z): ...]
    ## @purpose parameters method
    ## @io Input -> Output
    ## @complexity 5
    def parameters(self) -> dict:
        self.logger.debug(f"[IMP:4][DiplomaFeatureExtractor][parameters_INIT] Starting")
        return {}

    # endregion METHOD_parameters
    # region METHOD_transform [DOMAIN(X): ...; CONCEPT(Y): ...; TECH(Z): ...]
    ## @purpose transform method
    ## @io Input -> Output
    ## @complexity 5
    def transform(self, documents: List[List[LineWithMeta]], toc_items: Optional[List[List[TocItem]]] = None) -> pd.DataFrame:
        self.logger.debug(f"[IMP:4][DiplomaFeatureExtractor][transform_INIT] Starting")
        if not toc_items:
            toc_items = [self.toc_extractor.get_toc(doc_lines) for doc_lines in documents]
        assert len(toc_items) == len(documents)

        result_matrix = pd.concat([self.__process_document(document, d_toc_lines) for document, d_toc_lines in zip(documents, toc_items)], ignore_index=True)
        features = sorted(result_matrix.columns)
        return result_matrix[features].astype(float)

    # endregion METHOD_transform
    # region METHOD__get_similarity_with_tocitems [DOMAIN(X): ...; CONCEPT(Y): ...; TECH(Z): ...]
    ## @purpose _get_similarity_with_tocitems method
    ## @io Input -> Output
    ## @complexity 5
    def _get_similarity_with_tocitems(self, line: str, toc_items: List[TocItem], max_compare_symbols: int = 45) -> float:
        self.logger.debug(f"[IMP:4][DiplomaFeatureExtractor][_get_similarity_with_tocitems_INIT] Starting")
        return max(ratio(item.line.line.strip()[:max_compare_symbols], line.strip()[:max_compare_symbols]) for item in toc_items)

    # endregion METHOD__get_similarity_with_tocitems
    # region METHOD___process_document [DOMAIN(X): ...; CONCEPT(Y): ...; TECH(Z): ...]
    ## @purpose __process_document method
    ## @io Input -> Output
    ## @complexity 5
    def __process_document(self, lines: List[LineWithMeta], toc_items: List[TocItem]) -> pd.DataFrame:
        self.logger.debug(f"[IMP:4][DiplomaFeatureExtractor][__process_document_INIT] Starting")
        toc_items = [] if toc_items is None else toc_items
        _, features_df = self.list_feature_extractor.one_document(lines)
        features_df["list_item"] = self._list_features(lines)

        filtered_toc_items = [item.filter_toc_line(item) for item in toc_items]

        one_line_features_dict = defaultdict(list)
        for num, line in enumerate(lines):
            for item in self._one_line_features(line, len(lines), num, filtered_toc_items):
                feature_name, feature = item[0], item[1]
                one_line_features_dict[feature_name].append(feature)
        one_line_features_df = pd.DataFrame(one_line_features_dict)
        one_line_features_df["indentation"] = self._normalize_features(one_line_features_df.indentation)
        one_line_features_df["font_size"] = self._normalize_features(one_line_features_df.font_size)
        one_line_features_df = self.prev_next_line_features(one_line_features_df, 3, 3)

        result_matrix = pd.concat([one_line_features_df, features_df], axis=1)
        return result_matrix

    # endregion METHOD___process_document
    # region METHOD__one_line_features [DOMAIN(X): ...; CONCEPT(Y): ...; TECH(Z): ...]
    ## @purpose _one_line_features method
    ## @io Input -> Output
    ## @complexity 5
    def _one_line_features(self, line: LineWithMeta, total_lines: int, line_num: int, toc_items: List[TocItem]) -> Iterator[Tuple[str, int]]:
        self.logger.debug(f"[IMP:4][DiplomaFeatureExtractor][_one_line_features_INIT] Starting")
        yield "indentation", self._get_indentation(line)
        yield "font_size", self._get_size(line)
        yield "bold", self._get_bold(line)
        bold_percent = self._get_bold_percent(line)
        yield "bold_percent", bold_percent
        yield "fully_bold", int(bold_percent == 1.)
        yield "italic", self._get_italic(line)
        yield "underlined", self._get_underlined(line)
        yield "upper_letters_percent", (self._get_percent_upper_letters(line) == 1.0)

        is_toc = hasattr(line, "label") and line.label == "toc"
        yield "is_toc", int(is_toc)
        yield "is_in_toc", self._get_similarity_with_tocitems(line.line, toc_items) if toc_items and not is_toc else 0.0
        yield "before_toc", int(self._get_before_toc(line, toc_items))

        text = line.line.lower()
        text_wo_spaces = "".join(text.strip().split())
        yield "is_title", int(text_wo_spaces in self.titles)
        yield "is_title_keyword", int(text_wo_spaces in self.title_keywords)
        yield "is_named_item", int(text_wo_spaces in self.named_item_keywords)
        yield "named_item_start", int(text_wo_spaces.startswith(self.named_item_start))
        yield "is_raw_text", len([word for word in self.raw_text_keywords if word in text_wo_spaces])

        yield from self._start_regexp(line.line, self.start_regexps)
        yield "brackets_number", sum(c in "()" for c in text_wo_spaces)

        yield "is_lower", int(line.line.strip().islower())

        prefix = get_prefix([DottedPrefix], line)
        yield ("dotted_depth", len(prefix.numbers)) if prefix.name == DottedPrefix.name else ("dotted_depth", 0)

        yield "text_length", len(text.strip())
        yield "words_number", len(text.strip().split())
        yield "line_id", normalization_by_min_max(line_num, min_v=0, max_v=total_lines)
        # TODO work with page number (if it will be added to docx correctly)

    # endregion METHOD__one_line_features
# endregion CLASS_DiplomaFeatureExtractor
# region MODULE_CONTRACT [DOMAIN(DocumentProcessing): ...; CONCEPT(FeatureEngineering): ...; TECH(Pandas): ...]
## @modulecontract
## @purpose Document structure extraction for structure_extractors/feature_extractors/diploma_feature_extractor: line classification, hierarchy level assignment, pattern matching.
## @scope Structure extraction pipeline — structure_extractors/feature_extractors/diploma_feature_extractor
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
## CLASS [Weight 7][Structure extraction] => DiplomaFeatureExtractor
## @usecases
## - Extract structure: Reader → StructureExtractor → HierarchyBuilder → AnnotatedDocument
def _module_contract():
    pass
# endregion MODULE_CONTRACT
# GREP_SUMMARY: structure extractors, feature extractors, diploma feature extractor
# STRUCTURE: ▶ structure_extractors/feature_extractors/diploma_feature_extractor → ○ DiplomaFeatureExtractor.cls → ⎋ result