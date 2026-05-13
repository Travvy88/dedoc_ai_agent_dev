import logging
from abc import ABC, abstractmethod
from typing import List, Optional

from dedoc.data_structures.annotation import Annotation
from dedoc.data_structures.line_with_meta import LineWithMeta
from dedoc.data_structures.unstructured_document import UnstructuredDocument

logger = logging.getLogger(__name__)


# region CLASS_AbstractStructureExtractor [DOMAIN(DocumentProcessing): ...; CONCEPT(AbstractInterface): ...; TECH(ABC): ...]
## @purpose AbstractStructureExtractor for document structure extraction pipeline
class AbstractStructureExtractor(ABC):
    """
    This class adds additional information to the given unstructured document (list of lines) received from some of the readers.
    Types of lines (paragraph_type) and their levels (hierarchy_level) in the document are added.

    The hierarchy level of the line shows the importance of the line in the document: the more important the line is, the less level value it has.
    Look at the class :class:`dedoc.data_structures.HierarchyLevel` for more information.

    The paragraph type of the line should be one of the predefined types for some certain document domain, e.g. header, list_item, raw_text, etc.
    Each concrete structure extractor defines the rules of structuring: the levels and possible types of the lines.
    """
    # region METHOD___init__ [DOMAIN(X): ...; CONCEPT(Y): ...; TECH(Z): ...]
    ## @purpose __init__ method
    ## @io Input -> Output
    ## @complexity 5
    def __init__(self, *, config: Optional[dict] = None) -> None:
        """
        :param config: configuration of the extractor, e.g. logger for logging
        """
        self.config = {} if config is None else config
        self.logger = self.config.get("logger", logging.getLogger())
        self.logger.debug(f"[IMP:4][AbstractStructureExtractor][__init___INIT] Starting")

    # endregion METHOD___init__
    # region METHOD_extract [DOMAIN(X): ...; CONCEPT(Y): ...; TECH(Z): ...]
    ## @purpose extract method
    ## @io Input -> Output
    ## @complexity 5
    @abstractmethod
    def extract(self, document: UnstructuredDocument, parameters: Optional[dict] = None) -> UnstructuredDocument:
        self.logger.debug(f"[IMP:4][AbstractStructureExtractor][extract_INIT] Starting")
        """
        This method extracts structure for the document content received from some reader:
        it finds lines types and their hierarchy levels and adds them to the lines' metadata.

        :param document: document content that has been received from some of the readers
        :param parameters: additional parameters for document parsing, see :ref:`structure_type_parameters` for more details
        :return: document content with added additional information about lines types and hierarchy levels
        """
        pass

    # endregion METHOD_extract
    # region METHOD__postprocess [DOMAIN(X): ...; CONCEPT(Y): ...; TECH(Z): ...]
    ## @purpose _postprocess method
    ## @io Input -> Output
    ## @complexity 5
    def _postprocess(self, lines: List[LineWithMeta], paragraph_type: List[str], regexps: List, excluding_regexps: List) -> List[LineWithMeta]:
        self.logger.debug(f"[IMP:4][AbstractStructureExtractor][_postprocess_INIT] Starting")
        """
        The function searches for which of regular expressions (for regexps parameters) the string matches.
        If there is match, then additional node is creating.
        To filter out garbage (extra letters, spaces, etc.),
        the excluding_regexps is applied after for the matched substring (for example: "1.П"->"1.", "4.7.\t"->"4.7.")

        :param lines: input lines
        :param paragraph_type: list of paragraph types
        :param regexps: list of regular pattern according to the list of paragraph types
        :param excluding_regexps: list of filtering garbage regular pattern according to list of paragraph types
        :return: new post-processed list of LineWithMeta
        """
        from copy import deepcopy
        from dedoc.data_structures.hierarchy_level import HierarchyLevel

        if self.config.get("labeling_mode", False):
            return lines

        result = []
        for line in lines:
            if line.metadata.hierarchy_level.is_raw_text() and len(line.line) == 0:  # skip empty raw text
                continue
            if line.metadata.hierarchy_level.line_type in paragraph_type:
                matched = False
                for num, regexp in enumerate(regexps):
                    match = regexp.match(line.line)

                    if match:
                        matched = True
                        start = match.start()
                        end = match.end()
                        if excluding_regexps[num]:
                            match_excluding = excluding_regexps[num].search(line.line[start:end])
                            end = match_excluding.start() if match_excluding else end

                        result.append(LineWithMeta(line=line.line[start:end],
                                                   metadata=line.metadata,
                                                   annotations=self._select_annotations(line.annotations, start, end),
                                                   uid=line.uid))
                        metadata = deepcopy(line.metadata)
                        metadata.hierarchy_level = HierarchyLevel.create_raw_text()

                        rest_text = line.line[end:]
                        if len(rest_text) > 0:
                            annotations = self._select_annotations(line.annotations, end, len(line.line))
                            result.append(LineWithMeta(line=rest_text, metadata=metadata, annotations=annotations, uid=line.uid + "_split"))
                        break
                if not matched:
                    result.append(line)
            else:
                result.append(line)

        return result

    # endregion METHOD__postprocess
    # region METHOD__select_annotations [DOMAIN(X): ...; CONCEPT(Y): ...; TECH(Z): ...]
    ## @purpose _select_annotations method
    ## @io Input -> Output
    ## @complexity 5
    @staticmethod
    def _select_annotations(annotations: List[Annotation], start: int, end: int) -> List[Annotation]:
        # BUG_FIX_CONTEXT: _select_annotations is @staticmethod — no `self`. Use module-level logger instead of self.logger.
        logger.debug(f"[IMP:4][AbstractStructureExtractor][_select_annotations_INIT] Starting")
        from dedoc.data_structures.concrete_annotations.attach_annotation import AttachAnnotation
        from dedoc.data_structures.concrete_annotations.table_annotation import TableAnnotation

        assert start <= end
        res = []
        for annotation in annotations:
            if annotation.name in [TableAnnotation.name, AttachAnnotation.name]:
                if start == 0:
                    new_annotation = Annotation(start=start, end=end, value=annotation.value, name=annotation.name)
                    res.append(new_annotation)
            elif annotation.end > start and annotation.start <= end:
                new_start = max(annotation.start, start) - start
                new_end = min(annotation.end, end) - start
                new_annotation = Annotation(start=new_start, end=new_end, value=annotation.value, name=annotation.name)
                res.append(new_annotation)
        return res

    # endregion METHOD__select_annotations
# endregion CLASS_AbstractStructureExtractor
# region MODULE_CONTRACT [DOMAIN(DocumentProcessing): ...; CONCEPT(AbstractInterface): ...; TECH(ABC): ...]
## @modulecontract
## @purpose Document structure extraction for structure_extractors/abstract_structure_extractor: line classification, hierarchy level assignment, pattern matching.
## @scope Structure extraction pipeline — structure_extractors/abstract_structure_extractor
## @input Document lines with reader metadata.
## @output Lines annotated with hierarchy levels and line type labels.
## @links [USES_API(8): dedoc.data_structures; READS_DATA_FROM(8): readers]
## @invariants
## - Output lines preserve input order.
## @rationale
## Q: Why semantic region markup and LDD logging?
## A: Enables agent navigation via grep/Doxygen XML and runtime trace analysis.
## @changes
## LAST_CHANGE: [v1.0.1 – Fix LDD logging: use module-level logger in @staticmethod _select_annotations, fix __init__ logger init order]
## @modulemap
## CLASS [Weight 7][Structure extraction] => AbstractStructureExtractor
## @usecases
## - Extract structure: Reader → StructureExtractor → HierarchyBuilder → AnnotatedDocument
def _module_contract():
    pass
# endregion MODULE_CONTRACT
# GREP_SUMMARY: structure extractors, abstract structure extractor
# STRUCTURE: ▶ structure_extractors/abstract_structure_extractor → ○ AbstractStructureExtractor.cls → ⎋ result