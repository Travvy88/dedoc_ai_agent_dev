import logging

from dedoc.data_structures.annotation import Annotation

logger = logging.getLogger(__name__)


# region CLASS_AttachAnnotation [DOMAIN(4): DocumentProcessing; CONCEPT(5): TextAnnotation, Attachment; TECH(3): DataStructure]
## @purpose Indicate the place of the attachment in the original document (e.g. where an image was placed in a docx document).
class AttachAnnotation(Annotation):
    """
    This annotation indicate the place of the attachment in the original document (for example, the place where image
    was placed in the docx document).
    The line containing this annotation is placed directly before the referred attachment.
    """
    name = "attachment"

    # region METHOD___init__ [DOMAIN(4): DocumentProcessing; CONCEPT(5): TextAnnotation; TECH(3): DataStructure]
    ## @purpose Initialize attachment annotation with attachment UID.
    ## @uses Annotation.__init__
    ## @io (str, int, int) -> None
    ## @complexity 2
    def __init__(self, attach_uid: str, start: int, end: int) -> None:
        """
        :param attach_uid: unique identifier of the attachment which is referenced inside this annotation
        :param start: start of the annotated text (usually zero)
        :param end: end of the annotated text (usually end of the line)
        """
        logger.debug(f"[IMP:4][AttachAnnotation][INIT] attach_uid={attach_uid}, start={start}, end={end}")
        super().__init__(start=start, end=end, name=AttachAnnotation.name, value=attach_uid, is_mergeable=False)
        logger.debug(f"[IMP:4][AttachAnnotation][INIT] AttachAnnotation created successfully")
    # endregion METHOD___init__
# endregion CLASS_AttachAnnotation

# region MODULE_CONTRACT [DOMAIN(4): DocumentProcessing; CONCEPT(5): TextAnnotation, Attachment; TECH(3): DataStructure, Python]
## @modulecontract
## @purpose Provide attachment placeholder annotation — marks where an attachment (image, etc.) was placed in the original document.
## @scope Text annotation for attachment references.
## @input Attachment UID string.
## @output AttachAnnotation instance with is_mergeable=False.
## @links [INHERITS(9): Annotation]
## @invariants
## - is_mergeable is always False
## @rationale
## Q: Why is_mergeable=False?
## A: Each attachment reference is a distinct entity that should not be merged with others.
## @changes
## LAST_CHANGE: [v1.0.0 – Added semantic markup and LDD logging]
## @modulemap
## CLASS 10[Attachment reference annotation] => AttachAnnotation
## @usecases
## - [AttachAnnotation]: Reader → MarkAttachmentPlace → AttachAnnotationStored
def _module_contract():
    pass
# endregion MODULE_CONTRACT
# GREP_SUMMARY: attachment, annotation, text, document, placeholder, image, docx, attach_uid
# STRUCTURE: ▶ Init [attach_uid, start, end] → ⊕ super().__init__(name="attachment", is_mergeable=False) → ⎋ AttachAnnotation
