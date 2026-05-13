from typing import List, Optional

from dedoc.data_structures.line_with_meta import LineWithMeta
from dedoc.data_structures.unstructured_document import UnstructuredDocument
from dedoc.structure_extractors.abstract_structure_extractor import AbstractStructureExtractor

import logging
logger = logging.getLogger(__name__)


# region CLASS_ArticleStructureExtractor [DOMAIN(DocumentProcessing): ...; CONCEPT(DocumentStructureParser): ...; TECH(Python): ...]
## @purpose ArticleStructureExtractor for document structure extraction pipeline
class ArticleStructureExtractor(AbstractStructureExtractor):
    """
    This class corresponds to the `GROBID <https://grobid.readthedocs.io/en/latest/>`_ article structure extraction.

    This class saves all tag_hierarchy_levels received from the :class:`~dedoc.readers.ArticleReader` \
    without using the postprocessing step (without using regular expressions).

    You can find the description of this type of structure in the section :ref:`article_structure`.
    """
    document_type = "article"

    # region METHOD_extract [DOMAIN(X): ...; CONCEPT(Y): ...; TECH(Z): ...]
    ## @purpose extract method
    ## @io Input -> Output
    ## @complexity 5
    def extract(self, document: UnstructuredDocument, parameters: Optional[dict] = None) -> UnstructuredDocument:
        self.logger.debug(f"[IMP:4][ArticleStructureExtractor][extract_INIT] Starting")
        """
        Extract article structure from the given document and add additional information to the lines' metadata.
        To get the information about the method's parameters look at the documentation of the class \
        :class:`~dedoc.structure_extractors.AbstractStructureExtractor`.
        """
        from dedoc.data_structures.hierarchy_level import HierarchyLevel

        for line in document.lines:
            if line.metadata.tag_hierarchy_level is None or line.metadata.tag_hierarchy_level.is_unknown():
                line.metadata.tag_hierarchy_level = HierarchyLevel.create_raw_text()
            else:
                line.metadata.hierarchy_level = line.metadata.tag_hierarchy_level
            assert line.metadata.hierarchy_level is not None

        return document

    # endregion METHOD_extract
    # region METHOD__postprocess [DOMAIN(X): ...; CONCEPT(Y): ...; TECH(Z): ...]
    ## @purpose _postprocess method
    ## @io Input -> Output
    ## @complexity 5
    def _postprocess(self, lines: List[LineWithMeta], paragraph_type: List[str], regexps: List, excluding_regexps: List) -> List[LineWithMeta]:
        self.logger.debug(f"[IMP:4][ArticleStructureExtractor][_postprocess_INIT] Starting")
        return lines

    # endregion METHOD__postprocess
# endregion CLASS_ArticleStructureExtractor
# region MODULE_CONTRACT [DOMAIN(DocumentProcessing): ...; CONCEPT(DocumentStructureParser): ...; TECH(Python): ...]
## @modulecontract
## @purpose Document structure extraction for structure_extractors/concrete_structure_extractors/article_structure_extractor: line classification, hierarchy level assignment, pattern matching.
## @scope Structure extraction pipeline — structure_extractors/concrete_structure_extractors/article_structure_extractor
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
## CLASS [Weight 7][Structure extraction] => ArticleStructureExtractor
## @usecases
## - Extract structure: Reader → StructureExtractor → HierarchyBuilder → AnnotatedDocument
def _module_contract():
    pass
# endregion MODULE_CONTRACT
# GREP_SUMMARY: structure extractors, concrete structure extractors, article structure extractor
# STRUCTURE: ▶ structure_extractors/concrete_structure_extractors/article_structure_extractor → ○ ArticleStructureExtractor.cls → ⎋ result