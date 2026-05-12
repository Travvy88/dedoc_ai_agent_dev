import cv2
import numpy as np

import logging

logger = logging.getLogger(__name__)


# region CLASS_ValleyEmphasisBinarizer [DOMAIN(8): DocumentProcessing; CONCEPT(7): Reader; TECH(6): Python]
class ValleyEmphasisBinarizer:
    # region METHOD___init__ [DOMAIN(7): DocumentProcessing; CONCEPT(6): Method; TECH(6): Python]
    def __init__(self, n: int = 5) -> None:
        self.n = n

    # region METHOD_binarize [DOMAIN(7): DocumentProcessing; CONCEPT(6): Method; TECH(6): Python]
    # endregion METHOD___init__
    def binarize(self, image: np.ndarray) -> np.ndarray:
        if image.shape[-1] == 3:
            image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        threshold = self.__get_threshold(image)

        image[image <= threshold] = 0
        image[image > threshold] = 1
        return image

    # region METHOD___get_threshold [DOMAIN(7): DocumentProcessing; CONCEPT(6): Method; TECH(6): Python]
    # endregion METHOD_binarize
    def __get_threshold(self, gray_img: np.ndarray) -> int:
        c, x = np.histogram(gray_img, bins=255)
        h, w = gray_img.shape
        total = h * w

        sum_val = 0
        for t in range(255):
            sum_val = sum_val + (t * c[t] / total)

        var_max = 0
        threshold = 0

        omega_1 = 0
        mu_k = 0

        for t in range(254):
            omega_1 = omega_1 + c[t] / total
            omega_2 = 1 - omega_1
            mu_k = mu_k + t * (c[t] / total)
            mu_1 = mu_k / omega_1 if omega_1 != 0. else 0.
            mu_2 = (sum_val - mu_k) / omega_2 if omega_2 != 0. else 0.
            sum_of_neighbors = np.sum(c[max(1, t - self.n):min(255, t + self.n)])
            denom = total
            current_var = (1 - sum_of_neighbors / denom) * (omega_1 * mu_1 ** 2 + omega_2 * mu_2 ** 2)

            if current_var > var_max:
                var_max = current_var
                threshold = t

# endregion CLASS_ValleyEmphasisBinarizer
        return threshold

    # endregion METHOD___get_threshold


# region MODULE_CONTRACT [DOMAIN(8): DocumentProcessing; CONCEPT(7): Reader_valley_emphasis_binarizer; TECH(6): Python, dedoc]
## @modulecontract
## @purpose Read and parse PDF documents, extracting lines with metadata, tables, and attachments into UnstructuredDocument.
## @scope Machine learning classification for document layout analysis.
## @input [File path (str), parameters (Optional[dict]) — document on disk.]
## @output [UnstructuredDocument with lines, tables, attachments, and warnings.]
## @links [USES_API(9): dedoc.data_structures.*; USES_API(8): dedoc.readers.BaseReader]
## @invariants
## - read() ALWAYS returns an UnstructuredDocument.
## @rationale
## Q: Why is this reader separated from others?
## A: Each reader handles one format family — isolation prevents format coupling and simplifies extension.
## @changes
## LAST_CHANGE: [v1.0.0 – Added SEMANTIC TEMPLATE markup and LDD logging.]
## @modulemap
## CLASS [6][ValleyEmphasisBinarizer reader/processor] => ValleyEmphasisBinarizer
## @usecases
## - [read]: System (Pipeline) → ParseDocument(PDF) → UnstructuredDocument
def _module_contract():
    pass
# endregion MODULE_CONTRACT
# GREP_SUMMARY: valley_emphasis_binarizer, dedoc, reader, PDF, PdfReader, BaseReader, PDF, pdfminer, tabby, OCR, tables, image, txtlayer, columns, orientation, paragraphs, metadata, extraction, line, bbox, ValleyEmphasisBinarizer
# STRUCTURE: ▶ Init ┌PDF file┐ → [ValleyEmphasisBinarizer] ○ can_read? → ○ read → [__init__ → binarize → __get_threshold] → ⊕ UnstructuredDocument(lines, tables, attachments)
