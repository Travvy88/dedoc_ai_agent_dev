from abc import ABC
from enum import Enum
from typing import Dict, Iterable, List, Optional

from dedoc.data_structures.line_with_meta import LineWithMeta
from dedoc.data_structures.unstructured_document import UnstructuredDocument
from dedoc.structure_extractors.abstract_structure_extractor import AbstractStructureExtractor

import logging
logger = logging.getLogger(__name__)


# region CLASS_LawDocType [DOMAIN(DocumentProcessing): ...; CONCEPT(DocumentStructureParser): ...; TECH(Python): ...]
## @purpose LawDocType for document structure extraction pipeline
class LawDocType(Enum):
    decree = "постановление"
    order = "приказ"
    bylaw = "распоряжение"
    definition = "определение"
    directive = "директива"
    code = "кодекс"
    law = "закон"
    constitution = "конституция"
    edict = "указ"
    state = "положение"
    instruction = "инструкция"
    federal_law = "федеральный закон"

    # region METHOD_doc_types [DOMAIN(X): ...; CONCEPT(Y): ...; TECH(Z): ...]
    ## @purpose doc_types method
    ## @io Input -> Output
    ## @complexity 5
    @staticmethod
    def doc_types() -> List[str]:
        # BUG_FIX_CONTEXT: self.logger не существует в @staticmethod — заменён на модульный logger.
        logger.debug(f"[IMP:4][LawDocType][doc_types_INIT] Starting")
        # order is important
        return [
            LawDocType.definition,
            LawDocType.order,
            LawDocType.bylaw,
            LawDocType.code,
            LawDocType.federal_law,
            LawDocType.edict,
            LawDocType.law,
            LawDocType.decree,
            LawDocType.directive,
            LawDocType.constitution,
            LawDocType.state,
            LawDocType.instruction
        ]

    # endregion METHOD_doc_types
    # region METHOD_foiv_types [DOMAIN(X): ...; CONCEPT(Y): ...; TECH(Z): ...]
    ## @purpose foiv_types method
    ## @io Input -> Output
    ## @complexity 5
    @staticmethod
    def foiv_types() -> List["LawDocType"]:
        # BUG_FIX_CONTEXT: self.logger не существует в @staticmethod — заменён на модульный logger.
        logger.debug(f"[IMP:4][LawDocType][foiv_types_INIT] Starting")
        return [LawDocType.order, LawDocType.state, LawDocType.instruction]


    # endregion METHOD_foiv_types
# endregion CLASS_LawDocType
# region CLASS_ClassifyingLawStructureExtractor [DOMAIN(DocumentProcessing): ...; CONCEPT(DocumentStructureParser): ...; TECH(Python): ...]
## @purpose ClassifyingLawStructureExtractor for document structure extraction pipeline
class ClassifyingLawStructureExtractor(AbstractStructureExtractor, ABC):
    """
    This class is used to dynamically classify laws into two types: laws and foiv.
    The specific extractors are called according to the classifying results.
    """
    document_type = "law"

    # region METHOD___init__ [DOMAIN(X): ...; CONCEPT(Y): ...; TECH(Z): ...]
    ## @purpose __init__ method
    ## @io Input -> Output
    ## @complexity 5
    def __init__(self, extractors: Dict[str, AbstractStructureExtractor], *, config: Optional[dict] = None) -> None:
        """
        :param extractors: mapping law_type -> structure extractor, defined for certain law types
        :param config: configuration of the extractor, e.g. logger for logging
        """
        super().__init__(config=config)

        self.logger.debug(f"[IMP:4][ClassifyingLawStructureExtractor][__init___INIT] Starting")
        self.extractors = extractors

        self.hat_batch_size = 3
        self.hat_batch_count = 7

        self.main_templates = dict()
        federal_law_ws = self.__add_whitespace_match("федеральный закон")
        self.main_templates[LawDocType.federal_law] = {rf"\b{federal_law_ws}\b"}

        decree_ws = self.__add_whitespace_match("постановление")
        self.main_templates[LawDocType.decree] = {rf"\b{decree_ws}\b"}

        # Hot fix for tesseract common error
        order_char_map = {"з": "[з3]"}
        order_ws = self.__add_whitespace_match("приказ", char_map=order_char_map)
        self.main_templates[LawDocType.order] = {rf"\b{order_ws}\b"}

        bylaw_ws = self.__add_whitespace_match("распоряжение")
        self.main_templates[LawDocType.bylaw] = {rf"\b{bylaw_ws}\b"}

        law_ws = self.__add_whitespace_match("закон")
        self.main_templates[LawDocType.law] = {rf"\b{law_ws}\b"}

        edict_ws = self.__add_whitespace_match("указ")
        self.main_templates[LawDocType.edict] = {rf"\b{edict_ws}\b"}

        definition_ws = self.__add_whitespace_match("определение")
        self.main_templates[LawDocType.definition] = {rf"\b{definition_ws}\b"}

        directive_ws = self.__add_whitespace_match("директива")
        self.main_templates[LawDocType.directive] = {rf"\b{directive_ws}\b"}  # TODO no data

        code_ws = self.__add_whitespace_match("кодекс")
        self.main_templates[LawDocType.code] = {rf"\b{code_ws}\b"}

        constitution_ws = self.__add_whitespace_match("конституция")
        self.main_templates[LawDocType.constitution] = {rf"\b{constitution_ws}\b"}

        state_ws = self.__add_whitespace_match("положение")
        self.main_templates[LawDocType.state] = {rf"\b{state_ws}\b"}

        instruction_ws = self.__add_whitespace_match("инструкция")
        self.main_templates[LawDocType.instruction] = {rf"\b{instruction_ws}\b"}

    # endregion METHOD___init__
    # region METHOD_extract [DOMAIN(X): ...; CONCEPT(Y): ...; TECH(Z): ...]
    ## @purpose extract method
    ## @io Input -> Output
    ## @complexity 5
    def extract(self, document: UnstructuredDocument, parameters: Optional[dict] = None) -> UnstructuredDocument:
        self.logger.debug(f"[IMP:4][ClassifyingLawStructureExtractor][extract_INIT] Starting")
        """
        Classify law kind and extract structure according to the specific law format.
        To get the information about the method's parameters look at the documentation of the class \
        :class:`~dedoc.structure_extractors.AbstractStructureExtractor`.
        """
        parameters = {} if parameters is None else parameters
        selected_extractor = self._predict_extractor(lines=document.lines)
        result = selected_extractor.extract(document, parameters)
        warning = f"Use {selected_extractor.document_type} classifier"
        result.warnings = result.warnings + [warning]
        return result

    # endregion METHOD_extract
    # region METHOD__predict_extractor [DOMAIN(X): ...; CONCEPT(Y): ...; TECH(Z): ...]
    ## @purpose _predict_extractor method
    ## @io Input -> Output
    ## @complexity 5
    def _predict_extractor(self, lines: List[LineWithMeta]) -> AbstractStructureExtractor:
        self.logger.debug(f"[IMP:4][ClassifyingLawStructureExtractor][_predict_extractor_INIT] Starting")
        raw_lines = [line.line for line in lines]
        doc_type = self.__type_detect(lines=raw_lines)
        extractor = self.__get_extractor_by_type(doc_type=doc_type)
        return extractor

    # endregion METHOD__predict_extractor
    # region METHOD___type_detect [DOMAIN(X): ...; CONCEPT(Y): ...; TECH(Z): ...]
    ## @purpose __type_detect method
    ## @io Input -> Output
    ## @complexity 5
    def __type_detect(self, lines: List[str]) -> Optional[LawDocType]:
        self.logger.debug(f"[IMP:4][ClassifyingLawStructureExtractor][__type_detect_INIT] Starting")
        """
        Search for type N in first lines.
        Roud robin type search for each line batch.
        """
        import re

        first_lines = self.__create_line_batches(lines, batch_size=self.hat_batch_size, batch_count=self.hat_batch_count)

        # Hack for ЗАКОН ... КОДЕКС ...
        law_matched = False

        for batch in first_lines:
            for doc_type in LawDocType.doc_types():
                for template in self.main_templates[doc_type]:
                    for line in batch:
                        # - for ЯМАЛО-НЕНЕЦКИЙ, \.№ for ПОСТАНОВЛЕНИЕ от 1.1.2000 № 34
                        # / for Приказ № 47/823 от 17.12.2013 г.
                        if re.fullmatch(r"[\s\w-]*" + template + r"[()/\.№\s\w-]*", line, re.IGNORECASE):
                            if doc_type is LawDocType.law:
                                law_matched = True
                            else:
                                return doc_type
        if law_matched:
            return LawDocType.law

        return None

    # endregion METHOD___type_detect
    # region METHOD___get_extractor_by_type [DOMAIN(X): ...; CONCEPT(Y): ...; TECH(Z): ...]
    ## @purpose __get_extractor_by_type method
    ## @io Input -> Output
    ## @complexity 5
    def __get_extractor_by_type(self, doc_type: Optional[LawDocType]) -> AbstractStructureExtractor:
        self.logger.debug(f"[IMP:4][ClassifyingLawStructureExtractor][__get_extractor_by_type_INIT] Starting")
        from dedoc.structure_extractors.concrete_structure_extractors.foiv_law_structure_extractor import FoivLawStructureExtractor
        from dedoc.structure_extractors.concrete_structure_extractors.law_structure_excractor import LawStructureExtractor

        if doc_type is None:
            self.logger.info(f"Dynamic document type not found, using base: {LawStructureExtractor.document_type}")
            return self.extractors[LawStructureExtractor.document_type]
        elif doc_type in LawDocType.foiv_types():
            if FoivLawStructureExtractor.document_type in self.extractors:
                self.logger.info(f"Dynamic document type predicted: {FoivLawStructureExtractor.document_type}")
                return self.extractors[FoivLawStructureExtractor.document_type]
            else:
                self.logger.warning(f"No classifier for predicted dynamic document type {FoivLawStructureExtractor.document_type}, "
                                    f"using {LawStructureExtractor.document_type}")
                return self.extractors[LawStructureExtractor.document_type]
        else:
            self.logger.info(f"Dynamic document type predicted: {LawStructureExtractor.document_type}")
            return self.extractors[LawStructureExtractor.document_type]

    # endregion METHOD___get_extractor_by_type
    # region METHOD___add_whitespace_match [DOMAIN(X): ...; CONCEPT(Y): ...; TECH(Z): ...]
    ## @purpose __add_whitespace_match method
    ## @io Input -> Output
    ## @complexity 5
    def __add_whitespace_match(self, pattern: Iterable, char_map: dict = None) -> str:
        self.logger.debug(f"[IMP:4][ClassifyingLawStructureExtractor][__add_whitespace_match_INIT] Starting")
        if char_map is not None:
            # convert some chars to seq of chars: [з3]
            robust_word = (char_map.get(pattern[i:i + 1], pattern[i:i + 1])
                           for i in range(0, len(pattern), 1))
            return r"\s*".join(robust_word)
        else:
            return r"\s*".join(pattern[i:i + 1] for i in range(0, len(pattern), 1))

    # endregion METHOD___add_whitespace_match
    # region METHOD___create_line_batches [DOMAIN(X): ...; CONCEPT(Y): ...; TECH(Z): ...]
    ## @purpose __create_line_batches method
    ## @io Input -> Output
    ## @complexity 5
    def __create_line_batches(self, lines: List[str], batch_size: int, batch_count: int) -> List[List[str]]:
        self.logger.debug(f"[IMP:4][ClassifyingLawStructureExtractor][__create_line_batches_INIT] Starting")
        """
        Pack lines into batch_count batches of size batch_size.
        """
        batch_lines = []
        cur_batch = []
        cur_batches_count = 0
        cur_batch_size = 0
        for line in lines:
            if line.strip():
                line = self.__text_clean(line).strip()
                if cur_batch_size < batch_size:
                    cur_batch.append(line)
                    cur_batch_size += 1
                else:
                    batch_lines.append(cur_batch)
                    cur_batch = [line]
                    cur_batch_size = 1
                    cur_batches_count += 1
            if cur_batches_count > batch_count:
                break
        return batch_lines

    # endregion METHOD___create_line_batches
    # region METHOD___text_clean [DOMAIN(X): ...; CONCEPT(Y): ...; TECH(Z): ...]
    ## @purpose __text_clean method
    ## @io Input -> Output
    ## @complexity 5
    def __text_clean(self, text: str) -> str:
        self.logger.debug(f"[IMP:4][ClassifyingLawStructureExtractor][__text_clean_INIT] Starting")
        from collections import OrderedDict

        bad_characters = OrderedDict({"\u0438\u0306": "й", "\u0439\u0306": "й", "\u0418\u0306": "Й", "\u0419\u0306": "Й"})
        for bad_c, good_c in bad_characters.items():
            text = text.replace(bad_c, good_c)
        return text

    # endregion METHOD___text_clean
# endregion CLASS_ClassifyingLawStructureExtractor
# region MODULE_CONTRACT [DOMAIN(DocumentProcessing): ...; CONCEPT(DocumentStructureParser): ...; TECH(Python): ...]
## @modulecontract
## @purpose Document structure extraction for structure_extractors/concrete_structure_extractors/classifying_law_structure_extractor: line classification, hierarchy level assignment, pattern matching.
## @scope Structure extraction pipeline — structure_extractors/concrete_structure_extractors/classifying_law_structure_extractor
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
## CLASS [Weight 7][Structure extraction] => LawDocType
## CLASS [Weight 7][Structure extraction] => ClassifyingLawStructureExtractor
## @usecases
## - Extract structure: Reader → StructureExtractor → HierarchyBuilder → AnnotatedDocument
def _module_contract():
    pass
# endregion MODULE_CONTRACT
# GREP_SUMMARY: structure extractors, concrete structure extractors, classifying law structure extractor
# STRUCTURE: ▶ structure_extractors/concrete_structure_extractors/classifying_law_structure_extractor → ○ LawDocType.cls ⊕ ClassifyingLawStructureExtractor.cls → ⎋ result