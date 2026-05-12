from typing import List, Optional, Tuple

from dedoc.data_structures.line_metadata import LineMetadata
from dedoc.data_structures.line_with_meta import LineWithMeta
from dedoc.data_structures.unstructured_document import UnstructuredDocument
from dedoc.structure_extractors.abstract_structure_extractor import AbstractStructureExtractor

import logging
logger = logging.getLogger(__name__)


# region CLASS_DiplomaStructureExtractor [DOMAIN(DocumentProcessing): ...; CONCEPT(DocumentStructureParser): ...; TECH(Python): ...]
## @purpose DiplomaStructureExtractor for document structure extraction pipeline
class DiplomaStructureExtractor(AbstractStructureExtractor):
    """
    This class is used for extraction structure from russian diplomas, master dissertations, thesis, etc.

    You can find the description of this type of structure in the section :ref:`diploma_structure`.
    """
    document_type = "diploma"

    # region METHOD___init__ [DOMAIN(X): ...; CONCEPT(Y): ...; TECH(Z): ...]
    ## @purpose __init__ method
    ## @io Input -> Output
    ## @complexity 5
    def __init__(self, *, config: Optional[dict] = None) -> None:
        """
        :param config: some configuration for document parsing
        """
        super().__init__(config=config)

        self.logger.debug(f"[IMP:4][DiplomaStructureExtractor][__init___INIT] Starting")
        import os
        import re
        from dedoc.config import get_config
        from dedoc.structure_extractors.hierarchy_level_builders.diploma_builder.body_builder import DiplomaBodyBuilder
        from dedoc.structure_extractors.hierarchy_level_builders.header_builder.header_hierarchy_level_builder import HeaderHierarchyLevelBuilder
        from dedoc.structure_extractors.hierarchy_level_builders.toc_builder.toc_builder import TocBuilder
        from dedoc.structure_extractors.line_type_classifiers.diploma_classifier import DiplomaLineTypeClassifier

        self.header_builder = HeaderHierarchyLevelBuilder()
        self.toc_builder = TocBuilder()
        self.body_builder = DiplomaBodyBuilder()
        path = os.path.join(get_config()["resources_path"], "line_type_classifiers")
        self.classifier = DiplomaLineTypeClassifier(path=os.path.join(path, "diploma_classifier.zip"), config=self.config)
        self.footnote_start_regexp = re.compile(r"^\d+ ")

    # endregion METHOD___init__
    # region METHOD_extract [DOMAIN(X): ...; CONCEPT(Y): ...; TECH(Z): ...]
    ## @purpose extract method
    ## @io Input -> Output
    ## @complexity 5
    def extract(self, document: UnstructuredDocument, parameters: Optional[dict] = None) -> UnstructuredDocument:
        self.logger.debug(f"[IMP:4][DiplomaStructureExtractor][extract_INIT] Starting")
        """
        Extract diploma structure from the given document and add additional information to the lines' metadata.
        To get the information about the method's parameters look at the documentation of the class \
        :class:`~dedoc.structure_extractors.AbstractStructureExtractor`.
        """
        # preprocess lines
        lines = self._replace_toc_lines(document.lines)
        lines = self._replace_footnote_lines(lines)
        self._add_page_id_lines(lines)

        # exclude found toc from predicting
        toc_items = self.classifier.feature_extractor.toc_extractor.get_toc(lines, by_tag="toc")
        lines_for_predict = [line for line in lines if line.metadata.tag_hierarchy_level.line_type not in ("toc", "page_id", "footnote")]
        predictions = self.classifier.predict(lines_for_predict, toc_items=toc_items)
        assert len(predictions) == len(lines_for_predict)
        for line, prediction in zip(lines_for_predict, predictions):
            line.metadata.tag_hierarchy_level.line_type = prediction

        header_lines = [(line, "title") for line in lines if line.metadata.tag_hierarchy_level.line_type == "title"]
        body_lines = [
            (line, line.metadata.tag_hierarchy_level.line_type) for line in lines if line.metadata.tag_hierarchy_level.line_type not in ("title", "toc")
        ]
        toc_lines = [(item.line, "toc") for item in toc_items]

        # build structure
        header_lines = self.header_builder.get_lines_with_hierarchy(lines_with_labels=header_lines, init_hl_depth=0)
        toc_lines = self.toc_builder.get_lines_with_hierarchy(lines_with_labels=toc_lines, init_hl_depth=1)
        body_lines = self.body_builder.get_lines_with_hierarchy(lines_with_labels=body_lines, init_hl_depth=1)
        lines = header_lines + toc_lines + body_lines

        document.lines = sorted(lines, key=lambda x: (x.metadata.page_id, x.metadata.line_id))

        return document

    # endregion METHOD_extract
    # region METHOD__replace_toc_lines [DOMAIN(X): ...; CONCEPT(Y): ...; TECH(Z): ...]
    ## @purpose _replace_toc_lines method
    ## @io Input -> Output
    ## @complexity 5
    def _replace_toc_lines(self, lines: List[LineWithMeta]) -> Tuple[List[LineWithMeta]]:
        self.logger.debug(f"[IMP:4][DiplomaStructureExtractor][_replace_toc_lines_INIT] Starting")
        toc_items = self.classifier.feature_extractor.toc_extractor.get_toc(lines)
        if len(toc_items) == 0:
            return lines

        toc_lines = [toc_item.line for toc_item in toc_items]
        min_toc_line_id = min(line.metadata.line_id for line in toc_lines)
        max_toc_line_id = max(line.metadata.line_id for line in toc_lines)

        lines_wo_toc = []
        toc_title = None
        for line in lines:
            if line.metadata.line_id < min_toc_line_id and line.line.strip().lower() in self.classifier.feature_extractor.toc_extractor.titles:
                toc_title = line
                toc_title.metadata.tag_hierarchy_level.line_type = "toc"
            elif not (min_toc_line_id <= line.metadata.line_id <= max_toc_line_id):
                lines_wo_toc.append(line)

        toc_lines = [toc_title] if toc_title else []
        for item in toc_items:
            tg = item.line.metadata.tag_hierarchy_level
            tg.line_type = "toc"
            metadata = LineMetadata(item.line.metadata.page_id, item.line.metadata.line_id, tg, item.line.metadata.hierarchy_level, tocitem_page=item.page)
            item.line.set_metadata(metadata)
            toc_lines.append(item.line)

        lines = lines_wo_toc + toc_lines
        lines = sorted(lines, key=lambda x: (x.metadata.page_id, x.metadata.line_id))
        return lines

    # endregion METHOD__replace_toc_lines
    # region METHOD__replace_footnote_lines [DOMAIN(X): ...; CONCEPT(Y): ...; TECH(Z): ...]
    ## @purpose _replace_footnote_lines method
    ## @io Input -> Output
    ## @complexity 5
    def _replace_footnote_lines(self, lines: List[LineWithMeta]) -> List[LineWithMeta]:
        self.logger.debug(f"[IMP:4][DiplomaStructureExtractor][_replace_footnote_lines_INIT] Starting")
        fixed_lines = []
        current_footnote = None
        for line in lines:
            # usual case of simple line
            if line.metadata.tag_hierarchy_level.line_type != "footnote" and current_footnote is None:
                fixed_lines.append(line)

            # simple line, previous was a footnote
            elif line.metadata.tag_hierarchy_level.line_type != "footnote":
                current_footnote.metadata.tag_hierarchy_level.line_type = "footnote"
                fixed_lines.append(current_footnote)
                fixed_lines.append(line)
                current_footnote = None

            # first footnote
            elif current_footnote is None:
                current_footnote = line

            # new footnote after previous one
            elif self.footnote_start_regexp.match(line.line):
                current_footnote.metadata.tag_hierarchy_level.line_type = "footnote"
                fixed_lines.append(current_footnote)
                current_footnote = line

            # footnote continuation
            else:
                current_footnote += line

        if current_footnote is not None:
            current_footnote.metadata.tag_hierarchy_level.line_type = "footnote"
            fixed_lines.append(current_footnote)
        return fixed_lines

    # endregion METHOD__replace_footnote_lines
    # region METHOD__add_page_id_lines [DOMAIN(X): ...; CONCEPT(Y): ...; TECH(Z): ...]
    ## @purpose _add_page_id_lines method
    ## @io Input -> Output
    ## @complexity 5
    def _add_page_id_lines(self, lines: List[LineWithMeta]) -> None:
        self.logger.debug(f"[IMP:4][DiplomaStructureExtractor][_add_page_id_lines_INIT] Starting")
        for i in range(1, len(lines) - 1):
            line = lines[i]
            if (lines[i - 1].metadata.page_id < line.metadata.page_id or line.metadata.page_id < lines[i + 1].metadata.page_id) \
                    and line.line.strip().isdigit():
                line.metadata.tag_hierarchy_level.line_type = "page_id"

    # endregion METHOD__add_page_id_lines
# endregion CLASS_DiplomaStructureExtractor
# region MODULE_CONTRACT [DOMAIN(DocumentProcessing): ...; CONCEPT(DocumentStructureParser): ...; TECH(Python): ...]
## @modulecontract
## @purpose Document structure extraction for structure_extractors/concrete_structure_extractors/diploma_structure_extractor: line classification, hierarchy level assignment, pattern matching.
## @scope Structure extraction pipeline — structure_extractors/concrete_structure_extractors/diploma_structure_extractor
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
## CLASS [Weight 7][Structure extraction] => DiplomaStructureExtractor
## @usecases
## - Extract structure: Reader → StructureExtractor → HierarchyBuilder → AnnotatedDocument
def _module_contract():
    pass
# endregion MODULE_CONTRACT
# GREP_SUMMARY: structure extractors, concrete structure extractors, diploma structure extractor
# STRUCTURE: ▶ structure_extractors/concrete_structure_extractors/diploma_structure_extractor → ○ DiplomaStructureExtractor.cls → ⎋ result