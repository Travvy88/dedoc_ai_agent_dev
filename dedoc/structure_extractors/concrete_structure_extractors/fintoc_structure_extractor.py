from typing import Dict, List, Optional, Tuple, Union

from pandas import DataFrame

from dedoc.data_structures.line_with_meta import LineWithMeta
from dedoc.data_structures.unstructured_document import UnstructuredDocument
from dedoc.structure_extractors.abstract_structure_extractor import AbstractStructureExtractor

import logging
logger = logging.getLogger(__name__)


# region CLASS_FintocStructureExtractor [DOMAIN(DocumentProcessing): ...; CONCEPT(DocumentStructureParser): ...; TECH(Python): ...]
## @purpose FintocStructureExtractor for document structure extraction pipeline
class FintocStructureExtractor(AbstractStructureExtractor):
    """
    This class is an implementation of the TOC extractor for the `FinTOC 2022 Shared task <https://wp.lancs.ac.uk/cfie/fintoc2022/>`_.
    The code is a modification of the winner's solution (ISP RAS team).

    This structure extractor is used for English, French and Spanish financial prospects in PDF format (with a textual layer).
    It is recommended to use :class:`~dedoc.readers.PdfTxtlayerReader` to obtain document lines.
    You can find the more detailed description of this type of structure in the section :ref:`fintoc_structure`.
    """
    document_type = "fintoc"

    # region METHOD___init__ [DOMAIN(X): ...; CONCEPT(Y): ...; TECH(Z): ...]
    ## @purpose __init__ method
    ## @io Input -> Output
    ## @complexity 5
    def __init__(self, *, config: Optional[dict] = None) -> None:
        super().__init__(config=config)

        self.logger.debug(f"[IMP:4][FintocStructureExtractor][__init___INIT] Starting")
        import os
        import re
        from dedoc.config import get_config
        from dedoc.readers.pdf_reader.pdf_txtlayer_reader.pdf_txtlayer_reader import PdfTxtlayerReader  # to exclude circular imports
        from dedoc.structure_extractors.feature_extractors.fintoc_feature_extractor import FintocFeatureExtractor
        from dedoc.structure_extractors.feature_extractors.toc_feature_extractor import TOCFeatureExtractor
        from dedoc.structure_extractors.line_type_classifiers.fintoc_classifier import FintocClassifier

        self.pdf_reader = PdfTxtlayerReader(config=self.config)
        self.toc_extractor = TOCFeatureExtractor()
        self.features_extractor = FintocFeatureExtractor()
        self.languages = ("en", "fr", "sp")
        path = os.path.join(get_config()["resources_path"], "fintoc_classifiers")
        self.classifiers = {language: FintocClassifier(language=language, weights_dir_path=path) for language in self.languages}
        self.toc_item_regexp = re.compile(r'"([^"]+)" (\d+)')
        self.empty_string_regexp = re.compile(r"^\s*\n$")

    # endregion METHOD___init__
    # region METHOD_extract [DOMAIN(X): ...; CONCEPT(Y): ...; TECH(Z): ...]
    ## @purpose extract method
    ## @io Input -> Output
    ## @complexity 5
    def extract(self, document: UnstructuredDocument, parameters: Optional[dict] = None, file_path: Optional[str] = None) -> UnstructuredDocument:
        self.logger.debug(f"[IMP:4][FintocStructureExtractor][extract_INIT] Starting")
        """
        According to the `FinTOC 2022 <https://wp.lancs.ac.uk/cfie/fintoc2022/>`_ title detection task, lines are classified as titles and non-titles.
        The information about titles is saved in ``line.metadata.hierarchy_level`` (:class:`~dedoc.data_structures.HierarchyLevel` class):

            - Title lines have ``HierarchyLevel.header`` type, and their depth (``HierarchyLevel.level_2``) is similar to \
            the depth of TOC item from the FinTOC 2022 TOC generation task.
            - Non-title lines have ``HierarchyLevel.raw_text`` type, and their depth isn't obtained.

        :param document: document content that has been received from some of the readers (:class:`~dedoc.readers.PdfTxtlayerReader` is recommended).
        :param parameters: for this structure extractor, "language" parameter is used for setting document's language, e.g. ``parameters={"language": "en"}``. \
        The following options are supported:

            * "en", "eng" - English (default);
            * "fr", "fra" - French;
            * "sp", "spa" - Spanish.
        :param file_path: path to the file on disk.
        :return: document content with added additional information about title/non-title lines and hierarchy levels of titles.
        """
        from dedoc.data_structures.hierarchy_level import HierarchyLevel

        parameters = {} if parameters is None else parameters
        language = self.__get_param_language(parameters=parameters)

        features, documents = self.get_features(documents_dict={file_path: document.lines})
        predictions = self.classifiers[language].predict(features)
        lines: List[LineWithMeta] = documents[0]
        assert len(lines) == len(predictions)

        for line, prediction in zip(lines, predictions):
            if prediction > 0:
                line.metadata.hierarchy_level = HierarchyLevel(level_1=1, level_2=prediction, line_type=HierarchyLevel.header, can_be_multiline=True)
            else:
                line.metadata.hierarchy_level = HierarchyLevel.create_raw_text()
        document.lines = lines

        return document

    # endregion METHOD_extract
    # region METHOD___get_param_language [DOMAIN(X): ...; CONCEPT(Y): ...; TECH(Z): ...]
    ## @purpose __get_param_language method
    ## @io Input -> Output
    ## @complexity 5
    def __get_param_language(self, parameters: dict) -> str:
        self.logger.debug(f"[IMP:4][FintocStructureExtractor][__get_param_language_INIT] Starting")
        language = parameters.get("language", "en")

        if language in ("en", "eng", "rus+eng"):
            return "en"

        if language in ("fr", "fra"):
            return "fr"

        if language in ("sp", "spa"):
            return "sp"

        if language not in self.languages:
            self.logger.warning(f"Language {language} is not supported by this extractor. Use default language (en)")
        return "en"

    # endregion METHOD___get_param_language
    # region METHOD_get_features [DOMAIN(X): ...; CONCEPT(Y): ...; TECH(Z): ...]
    ## @purpose get_features method
    ## @io Input -> Output
    ## @complexity 5
    def get_features(self, documents_dict: Dict[str, List[LineWithMeta]]) -> Tuple[DataFrame, List[List[LineWithMeta]]]:
        self.logger.debug(f"[IMP:4][FintocStructureExtractor][get_features_INIT] Starting")
        toc_lines, documents = [], []
        for file_path, document_lines in documents_dict.items():
            toc_lines.append(self.__get_toc(file_path=file_path))
            documents.append(self.__filter_lines(document_lines))
        features = self.features_extractor.transform(documents=documents, toc_lines=toc_lines)
        return features, documents

    # endregion METHOD_get_features
    # region METHOD___filter_lines [DOMAIN(X): ...; CONCEPT(Y): ...; TECH(Z): ...]
    ## @purpose __filter_lines method
    ## @io Input -> Output
    ## @complexity 5
    def __filter_lines(self, lines: List[LineWithMeta]) -> List[LineWithMeta]:
        self.logger.debug(f"[IMP:4][FintocStructureExtractor][__filter_lines_INIT] Starting")
        special_unicode_symbols = [u"\uf0b7", u"\uf0d8", u"\uf084", u"\uf0a7", u"\uf0f0", u"\x83"]

        lines = [line for line in lines if not self.empty_string_regexp.match(line.line)]
        for line in lines:
            for ch in special_unicode_symbols:
                line.set_line(line.line.replace(ch, ""))

        return lines

    # endregion METHOD___filter_lines
    # region METHOD___get_toc [DOMAIN(X): ...; CONCEPT(Y): ...; TECH(Z): ...]
    ## @purpose __get_toc method
    ## @io Input -> Output
    ## @complexity 5
    def __get_toc(self, file_path: Optional[str]) -> List[Dict[str, Union[LineWithMeta, str]]]:
        self.logger.debug(f"[IMP:4][FintocStructureExtractor][__get_toc_INIT] Starting")
        """
        Try to get TOC from PDF automatically. If TOC wasn't extracted automatically, it is extracted using regular expressions.
        """
        import os

        if file_path is None or not file_path.lower().endswith(".pdf"):
            return []

        toc = self.__get_automatic_toc(path=file_path)
        if len(toc) > 0:
            self.logger.info(f"Got automatic TOC from {os.path.basename(file_path)}")
            return toc

        parameters = {"is_one_column_document": "True", "need_header_footer_analysis": "True", "pages": ":10"}
        lines = self.pdf_reader.read(file_path=file_path, parameters=parameters).lines
        return self.toc_extractor.get_toc(lines)

    # endregion METHOD___get_toc
    # region METHOD___get_automatic_toc [DOMAIN(X): ...; CONCEPT(Y): ...; TECH(Z): ...]
    ## @purpose __get_automatic_toc method
    ## @io Input -> Output
    ## @complexity 5
    def __get_automatic_toc(self, path: str) -> List[Dict[str, Union[LineWithMeta, str]]]:
        self.logger.debug(f"[IMP:4][FintocStructureExtractor][__get_automatic_toc_INIT] Starting")
        import os

        result = []
        with os.popen(f'pdftocio -p "{path}"') as out:
            toc = out.readlines()

        for line in toc:
            match = self.toc_item_regexp.match(line.strip())
            if match:
                result.append({"line": LineWithMeta(match.group(1)), "page": match.group(2)})

        return result

    # endregion METHOD___get_automatic_toc
# endregion CLASS_FintocStructureExtractor
# region MODULE_CONTRACT [DOMAIN(DocumentProcessing): ...; CONCEPT(DocumentStructureParser): ...; TECH(Python): ...]
## @modulecontract
## @purpose Document structure extraction for structure_extractors/concrete_structure_extractors/fintoc_structure_extractor: line classification, hierarchy level assignment, pattern matching.
## @scope Structure extraction pipeline — structure_extractors/concrete_structure_extractors/fintoc_structure_extractor
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
## CLASS [Weight 7][Structure extraction] => FintocStructureExtractor
## @usecases
## - Extract structure: Reader → StructureExtractor → HierarchyBuilder → AnnotatedDocument
def _module_contract():
    pass
# endregion MODULE_CONTRACT
# GREP_SUMMARY: structure extractors, concrete structure extractors, fintoc structure extractor
# STRUCTURE: ▶ structure_extractors/concrete_structure_extractors/fintoc_structure_extractor → ○ FintocStructureExtractor.cls → ⎋ result