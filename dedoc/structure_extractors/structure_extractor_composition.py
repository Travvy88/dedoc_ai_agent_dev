from typing import Dict, Optional

from dedoc.data_structures.unstructured_document import UnstructuredDocument
from dedoc.structure_extractors.abstract_structure_extractor import AbstractStructureExtractor

import logging
logger = logging.getLogger(__name__)


# region CLASS_StructureExtractorComposition [DOMAIN(DocumentProcessing): ...; CONCEPT(Composition): ...; TECH(Python): ...]
## @purpose StructureExtractorComposition for document structure extraction pipeline
class StructureExtractorComposition(AbstractStructureExtractor):
    """
    This class allows to extract structure from any document according to the available list of structure extractors.
    The list of structure extractors and names of document types for them is set via the class constructor.
    Each document type defines some specific document domain, those structure is extracted via the corresponding structure extractor.
    """
    # region METHOD___init__ [DOMAIN(X): ...; CONCEPT(Y): ...; TECH(Z): ...]
    ## @purpose __init__ method
    ## @io Input -> Output
    ## @complexity 5
    def __init__(self, extractors: Dict[str, AbstractStructureExtractor], default_key: str, *, config: Optional[dict] = None) -> None:
        """
        :param extractors: mapping document_type -> structure extractor, defined for certain document domains
        :param default_key: the document_type of the structure extractor, that will be used by default if the wrong parameters are given. \
        default_key should exist as a key in the extractors' dictionary.
        """
        super().__init__(config=config)
        self.logger.debug(f"[IMP:4][StructureExtractorComposition][__init___INIT] Starting")
        assert default_key in extractors
        self.extractors = extractors
        self.default_extractor_key = default_key

    # endregion METHOD___init__
    # region METHOD_extract [DOMAIN(X): ...; CONCEPT(Y): ...; TECH(Z): ...]
    ## @purpose extract method
    ## @io Input -> Output
    ## @complexity 5
    def extract(self, document: UnstructuredDocument, parameters: Optional[dict] = None) -> UnstructuredDocument:
        self.logger.debug(f"[IMP:4][StructureExtractorComposition][extract_INIT] Starting")
        """
        Adds information about the document structure according to the document type received from parameters (the key `document_type`).
        If there isn't `document_type` key in parameters or this document_type isn't found in the supported types, the default extractor will be used.
        To get the information about the method's parameters look at the documentation of the class \
        :class:`~dedoc.structure_extractors.AbstractStructureExtractor`.
        """
        parameters = {} if parameters is None else parameters
        document_type = parameters.get("document_type", self.default_extractor_key)
        extractor = self.extractors.get(document_type, self.extractors[self.default_extractor_key])
        return extractor.extract(document, parameters)

    # endregion METHOD_extract
# endregion CLASS_StructureExtractorComposition
# region MODULE_CONTRACT [DOMAIN(DocumentProcessing): ...; CONCEPT(Composition): ...; TECH(Python): ...]
## @modulecontract
## @purpose Document structure extraction for structure_extractors/structure_extractor_composition: line classification, hierarchy level assignment, pattern matching.
## @scope Structure extraction pipeline — structure_extractors/structure_extractor_composition
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
## CLASS [Weight 7][Structure extraction] => StructureExtractorComposition
## @usecases
## - Extract structure: Reader → StructureExtractor → HierarchyBuilder → AnnotatedDocument
def _module_contract():
    pass
# endregion MODULE_CONTRACT
# GREP_SUMMARY: structure extractors, structure extractor composition
# STRUCTURE: ▶ structure_extractors/structure_extractor_composition → ○ StructureExtractorComposition.cls → ⎋ result