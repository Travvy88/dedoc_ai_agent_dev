from typing import Optional

from dedoc.data_structures.unstructured_document import UnstructuredDocument
from dedoc.structure_extractors.abstract_structure_extractor import AbstractStructureExtractor

import logging
logger = logging.getLogger(__name__)


# region CLASS_TzStructureExtractor [DOMAIN(DocumentProcessing): ...; CONCEPT(DocumentStructureParser): ...; TECH(Python): ...]
## @purpose TzStructureExtractor for document structure extraction pipeline
class TzStructureExtractor(AbstractStructureExtractor):
    """
    This class is used for extraction structure from technical tasks.

    You can find the description of this type of structure in the section :ref:`tz_structure`.
    """
    document_type = "tz"

    # region METHOD___init__ [DOMAIN(X): ...; CONCEPT(Y): ...; TECH(Z): ...]
    ## @purpose __init__ method
    ## @io Input -> Output
    ## @complexity 5
    def __init__(self, *, config: Optional[dict] = None) -> None:
        """
        :param config: some configuration for document parsing
        """
        super().__init__(config=config)

        self.logger.debug(f"[IMP:4][TzStructureExtractor][__init___INIT] Starting")
        import os
        from dedoc.config import get_config
        from dedoc.structure_extractors.hierarchy_level_builders.header_builder.header_hierarchy_level_builder import HeaderHierarchyLevelBuilder
        from dedoc.structure_extractors.hierarchy_level_builders.toc_builder.toc_builder import TocBuilder
        from dedoc.structure_extractors.hierarchy_level_builders.tz_builder.body_builder import TzBodyBuilder
        from dedoc.structure_extractors.line_type_classifiers.tz_classifier import TzLineTypeClassifier

        self.header_builder = HeaderHierarchyLevelBuilder()
        self.body_builder = TzBodyBuilder()
        self.toc_builder = TocBuilder()
        path = os.path.join(get_config()["resources_path"], "line_type_classifiers")
        self.classifier = TzLineTypeClassifier(classifier_type="tz", path=os.path.join(path, "tz_classifier.zip"), config=self.config)
        self.txt_classifier = TzLineTypeClassifier(classifier_type="tz_txt", path=os.path.join(path, "tz_txt_classifier.zip"), config=self.config)

    # endregion METHOD___init__
    # region METHOD_extract [DOMAIN(X): ...; CONCEPT(Y): ...; TECH(Z): ...]
    ## @purpose extract method
    ## @io Input -> Output
    ## @complexity 5
    def extract(self, document: UnstructuredDocument, parameters: Optional[dict] = None) -> UnstructuredDocument:
        self.logger.debug(f"[IMP:4][TzStructureExtractor][extract_INIT] Starting")
        """
        Extract technical task structure from the given document and add additional information to the lines' metadata.
        To get the information about the method's parameters look at the documentation of the class \
        :class:`~dedoc.structure_extractors.AbstractStructureExtractor`.
        """
        from dedoc.extensions import recognized_mimes
        from dedoc.structure_extractors.hierarchy_level_builders.utils_reg import regexps_ends_of_number, regexps_number, regexps_subitem
        from dedoc.structure_extractors.feature_extractors.list_features.prefix.bullet_prefix import BulletPrefix

        if document.metadata.get("file_type") in recognized_mimes.txt_like_format:
            predictions = self.txt_classifier.predict(document.lines)
        else:
            predictions = self.classifier.predict(document.lines)
        header_lines, toc_lines, body_lines = [], [], []

        last_toc_line = max((line_id for line_id, prediction in enumerate(predictions) if prediction in ("toc", "title")), default=0)
        is_toc_begun = False
        is_body_begun = False
        for line_id, (line, prediction) in enumerate(zip(document.lines, predictions)):
            if prediction in ("part", "item") or is_body_begun:
                body_lines.append((line, prediction))
                is_body_begun = True
            elif line_id > last_toc_line:
                is_body_begun = True
                body_lines.append((line, prediction))
            elif (prediction == "toc" and not is_body_begun) or (not is_body_begun and is_toc_begun):
                toc_lines.append((line, prediction))
                is_toc_begun = True
            elif line.line.lower().strip() in ("содержание", "оглавление") and not is_toc_begun:
                is_toc_begun = True
                toc_lines.append((line, "toc"))
            else:
                header_lines.append((line, prediction))

        header_lines = self.header_builder.get_lines_with_hierarchy(lines_with_labels=header_lines, init_hl_depth=0)
        toc_lines = self.toc_builder.get_lines_with_hierarchy(lines_with_labels=toc_lines, init_hl_depth=1)
        body_lines = self.body_builder.get_lines_with_hierarchy(lines_with_labels=body_lines, init_hl_depth=1)

        document.lines = self._postprocess(lines=header_lines + toc_lines + body_lines,
                                           paragraph_type=["item"],
                                           regexps=[BulletPrefix.regexp, regexps_number, regexps_subitem],
                                           excluding_regexps=[None, regexps_ends_of_number, regexps_ends_of_number])
        return document

    # endregion METHOD_extract
# endregion CLASS_TzStructureExtractor
# region MODULE_CONTRACT [DOMAIN(DocumentProcessing): ...; CONCEPT(DocumentStructureParser): ...; TECH(Python): ...]
## @modulecontract
## @purpose Document structure extraction for structure_extractors/concrete_structure_extractors/tz_structure_extractor: line classification, hierarchy level assignment, pattern matching.
## @scope Structure extraction pipeline — structure_extractors/concrete_structure_extractors/tz_structure_extractor
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
## CLASS [Weight 7][Structure extraction] => TzStructureExtractor
## @usecases
## - Extract structure: Reader → StructureExtractor → HierarchyBuilder → AnnotatedDocument
def _module_contract():
    pass
# endregion MODULE_CONTRACT
# GREP_SUMMARY: structure extractors, concrete structure extractors, tz structure extractor
# STRUCTURE: ▶ structure_extractors/concrete_structure_extractors/tz_structure_extractor → ○ TzStructureExtractor.cls → ⎋ result