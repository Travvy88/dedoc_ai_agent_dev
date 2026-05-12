import logging

from dedoc.data_structures.annotation import Annotation

logger = logging.getLogger(__name__)


# region CLASS_ReferenceAnnotation [DOMAIN(4): DocumentProcessing; CONCEPT(5): TextAnnotation, Reference; TECH(3): DataStructure]
## @purpose Point to a place in the document text that is a link to another line (e.g. bibliography reference).
class ReferenceAnnotation(Annotation):
    """
    This annotation points to a place in the document text that is a link to another line in the document (for example, another textual line).

    Example of usage for document_type="article" with the example of link on the bibliography_item :class:`~dedoc.data_structures.LineWithMeta`.

        LineWithMeta:

        .. code-block:: python

            LineWithMeta(   # the line with the reference annotation
                line="As for the PRF, we use the tree-based construction from Goldreich, Goldwasser and Micali [18]",
                metadata=LineMetadata(page_id=0, line_id=32),
                annotations=[ReferenceAnnotation(start=90, end=92, value="97cfac39-f0e3-11ee-b81c-b88584b4e4a1"), ...]
            )

        other LineWithMeta:

        .. code-block:: python

            LineWithMeta(   # The line referenced by the previous one
                line="some your text (can be empty)",
                metadata=LineMetadata(
                    page_id=10,
                    line_id=189,
                    tag_hierarchy_level=HierarchyLevel(level1=2, level2=0, paragraph_type="bibliography_item")),
                    uid="97cfac39-f0e3-11ee-b81c-b88584b4e4a1"
                ),
                annotations=[]
            )
    """
    name = "reference"

    # region METHOD___init__ [DOMAIN(4): DocumentProcessing; CONCEPT(5): TextAnnotation; TECH(3): DataStructure]
    ## @purpose Initialize reference annotation with target line UID.
    ## @uses Annotation.__init__
    ## @io (str, int, int) -> None
    ## @complexity 2
    def __init__(self, value: str, start: int, end: int) -> None:
        """
        :param value: unique identifier of the line to which this annotation refers
        :param start: start of the annotated text with a link
        :param end: end of the annotated text with a link
        """
        logger.debug(f"[IMP:4][ReferenceAnnotation][INIT] value={value}, start={start}, end={end}")
        super().__init__(start=start, end=end, name=ReferenceAnnotation.name, value=value, is_mergeable=False)
        logger.debug(f"[IMP:4][ReferenceAnnotation][INIT] ReferenceAnnotation created successfully")
    # endregion METHOD___init__
# endregion CLASS_ReferenceAnnotation

# region MODULE_CONTRACT [DOMAIN(4): DocumentProcessing; CONCEPT(5): TextAnnotation, Reference, Bibliography; TECH(3): DataStructure, Python]
## @modulecontract
## @purpose Provide cross-reference annotation — links a text span to another document line by its UID.
## @scope Text annotation for cross-references and bibliography links.
## @input Target line UID string.
## @output ReferenceAnnotation instance with is_mergeable=False.
## @links [INHERITS(9): Annotation]
## @invariants
## - is_mergeable is always False
## @rationale
## Q: Why use UID-based references rather than positional?
## A: UIDs survive line reordering and merging, unlike positional indices.
## @changes
## LAST_CHANGE: [v1.0.0 – Added semantic markup and LDD logging]
## @modulemap
## CLASS 10[Reference text annotation] => ReferenceAnnotation
## @usecases
## - [ReferenceAnnotation]: StructureExtractor → LinkBibliographyRef → ReferenceAnnotationStored
def _module_contract():
    pass
# endregion MODULE_CONTRACT
# GREP_SUMMARY: reference, annotation, text, document, bibliography, link, cross-reference, uid
# STRUCTURE: ▶ Init [value, start, end] → ⊕ super().__init__(name="reference", is_mergeable=False) → ⎋ ReferenceAnnotation
