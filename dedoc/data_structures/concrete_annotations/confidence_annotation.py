import logging

from dedoc.data_structures.annotation import Annotation

logger = logging.getLogger(__name__)


# region CLASS_ConfidenceAnnotation [DOMAIN(4): DocumentProcessing; CONCEPT(5): TextAnnotation, OCR_Confidence; TECH(3): DataStructure]
## @purpose Mark OCR confidence level of recognized text inside the line.
class ConfidenceAnnotation(Annotation):
    """
    Confidence level of some recognized with OCR text inside the line.
    """
    name = "confidence"

    # region METHOD___init__ [DOMAIN(4): DocumentProcessing; CONCEPT(5): TextAnnotation; TECH(3): DataStructure]
    ## @purpose Initialize confidence annotation with validated float value in [0, 1].
    ## @uses Annotation.__init__
    ## @io (int, int, str) -> None
    ## @complexity 4
    def __init__(self, start: int, end: int, value: str) -> None:
        """
        :param start: start of the text
        :param end: end of the text (not included)
        :param value: confidence level in "percents" (float number from 0 to 1)
        """
        logger.debug(f"[IMP:4][ConfidenceAnnotation][INIT] start={start}, end={end}, value={value}")
        try:
            assert 0.0 <= float(value) <= 1.0
        except ValueError:
            raise ValueError("the value of confidence annotation should be float value")
        except AssertionError:
            raise ValueError("the value of confidence annotation should be in range [0, 1]")
        super().__init__(start=start, end=end, name=ConfidenceAnnotation.name, value=value, is_mergeable=False)
        logger.debug(f"[IMP:4][ConfidenceAnnotation][INIT] ConfidenceAnnotation created successfully")
    # endregion METHOD___init__
# endregion CLASS_ConfidenceAnnotation

# region MODULE_CONTRACT [DOMAIN(4): DocumentProcessing; CONCEPT(5): TextAnnotation, OCR_Confidence; TECH(3): DataStructure, Python]
## @modulecontract
## @purpose Provide OCR confidence annotation — records the confidence score of OCR-recognized text.
## @scope Text annotation for OCR confidence levels.
## @input Confidence float string in [0, 1].
## @output ConfidenceAnnotation instance with is_mergeable=False.
## @links [INHERITS(9): Annotation]
## @invariants
## - value in [0.0, 1.0]
## - is_mergeable is always False
## @rationale
## Q: Why is_mergeable=False?
## A: Each confidence score is unique to its OCR segment and cannot be meaningfully merged.
## @changes
## LAST_CHANGE: [v1.0.0 – Added semantic markup and LDD logging]
## @modulemap
## CLASS 10[OCR confidence annotation] => ConfidenceAnnotation
## @usecases
## - [ConfidenceAnnotation]: OCR_Reader → AttachConfidenceScore → ConfidenceAnnotationStored
def _module_contract():
    pass
# endregion MODULE_CONTRACT
# GREP_SUMMARY: confidence, OCR, annotation, text, document, score, recognition, float
# STRUCTURE: ▶ Init [start, end, value] → ◇ assert 0.0 <= float(value) <= 1.0 → ⊕ super().__init__(name="confidence", is_mergeable=False) → ⎋ ConfidenceAnnotation
