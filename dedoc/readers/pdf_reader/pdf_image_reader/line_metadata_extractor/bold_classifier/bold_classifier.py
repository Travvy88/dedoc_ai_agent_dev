from typing import List

import numpy as np
from dedocutils.data_structures import BBox

import logging

logger = logging.getLogger(__name__)

from dedoc.readers.pdf_reader.pdf_image_reader.line_metadata_extractor.bold_classifier.agglomerative_clusterizer import BoldAgglomerativeClusterizer
from dedoc.readers.pdf_reader.pdf_image_reader.line_metadata_extractor.bold_classifier.valley_emphasis_binarizer import ValleyEmphasisBinarizer


# region CLASS_BoldClassifier [DOMAIN(8): DocumentProcessing; CONCEPT(7): Reader; TECH(6): Python]
class BoldClassifier:
    """
    This class classifies words (or lines) in bboxes as bold or non-bold.
    Given a list of bboxes and an image, it returns a list of boldness probabilities (actually only 0 and 1 for now)
    """
    # region METHOD___init__ [DOMAIN(7): DocumentProcessing; CONCEPT(6): Method; TECH(6): Python]
    def __init__(self) -> None:
        self.permissible_h_bbox = 5
        self.binarizer = ValleyEmphasisBinarizer()
        self.clusterizer = BoldAgglomerativeClusterizer()

    # region METHOD_classify [DOMAIN(7): DocumentProcessing; CONCEPT(6): Method; TECH(6): Python]
    # endregion METHOD___init__
    def classify(self, image: np.ndarray, bboxes: List[BBox]) -> List[float]:
        if len(bboxes) == 0:
            return []

        if len(bboxes) == 1:
            return [0.0]

        bboxes_evaluation = self.__get_bboxes_evaluation(image, bboxes)
        bold_probabilities = self.__clusterize(bboxes_evaluation)
        return bold_probabilities

    # region METHOD___get_bboxes_evaluation [DOMAIN(7): DocumentProcessing; CONCEPT(6): Method; TECH(6): Python]
    # endregion METHOD_classify
    def __get_bboxes_evaluation(self, image: np.ndarray, bboxes: List[BBox]) -> List[float]:
        processed_image = self.__preprocessing(image)
        bboxes_evaluation = self.__get_evaluation_bboxes(processed_image, bboxes)
        return bboxes_evaluation

    # region METHOD___preprocessing [DOMAIN(7): DocumentProcessing; CONCEPT(6): Method; TECH(6): Python]
    # endregion METHOD___get_bboxes_evaluation
    def __preprocessing(self, image: np.ndarray) -> np.ndarray:
        return self.binarizer.binarize(image)

    # region METHOD___get_evaluation_bboxes [DOMAIN(7): DocumentProcessing; CONCEPT(6): Method; TECH(6): Python]
    # endregion METHOD___preprocessing
    def __get_evaluation_bboxes(self, image: np.ndarray, bboxes: List[BBox]) -> List[float]:
        bboxes_evaluation = [self.__evaluation_one_bbox(image, bbox) for bbox in bboxes]
        return bboxes_evaluation

    # region METHOD___evaluation_one_bbox [DOMAIN(7): DocumentProcessing; CONCEPT(6): Method; TECH(6): Python]
    # endregion METHOD___get_evaluation_bboxes
    def __evaluation_one_bbox(self, image: np.ndarray, bbox: BBox) -> float:
        bbox_image = image[bbox.y_top_left:bbox.y_bottom_right, bbox.x_top_left:bbox.x_bottom_right]
        return self.__evaluation_one_bbox_image(bbox_image) if self.__is_correct_bbox_image(bbox_image) else 1.

    # region METHOD___evaluation_one_bbox_image [DOMAIN(7): DocumentProcessing; CONCEPT(6): Method; TECH(6): Python]
    # endregion METHOD___evaluation_one_bbox
    def __evaluation_one_bbox_image(self, image: np.ndarray) -> float:
        base_line_image = self.__get_base_line_image(image)
        base_line_image_without_spaces = self.__get_rid_spaces(base_line_image)

        p_img = base_line_image[:, :-1] - base_line_image[:, 1:]
        p_img[abs(p_img) > 0] = 1.
        p_img[p_img < 0] = 0.
        p = p_img.mean()

        s = 1 - base_line_image_without_spaces.mean()

        if p > s or s == 0:
            evaluation = 1.
        else:
            evaluation = p / s
        return evaluation

    # region METHOD___clusterize [DOMAIN(7): DocumentProcessing; CONCEPT(6): Method; TECH(6): Python]
    # endregion METHOD___evaluation_one_bbox_image
    def __clusterize(self, bboxes_evaluation: List[float]) -> List[float]:
        vector_bbox_evaluation = np.array(bboxes_evaluation)
        vector_bbox_indicators = self.clusterizer.clusterize(vector_bbox_evaluation)
        bboxes_indicators = list(vector_bbox_indicators)
        return bboxes_indicators

    # region METHOD___get_rid_spaces [DOMAIN(7): DocumentProcessing; CONCEPT(6): Method; TECH(6): Python]
    # endregion METHOD___clusterize
    def __get_rid_spaces(self, image: np.ndarray) -> np.ndarray:
        x = image.mean(0)
        not_space = x < 0.95
        if len(not_space) > 3:
            return image
        return image[:, not_space]

    # region METHOD___get_base_line_image [DOMAIN(7): DocumentProcessing; CONCEPT(6): Method; TECH(6): Python]
    # endregion METHOD___get_rid_spaces
    def __get_base_line_image(self, image: np.ndarray) -> np.ndarray:
        h = image.shape[0]
        if h < self.permissible_h_bbox:
            return image
        mean_ = image.mean(1)
        delta_mean = abs(mean_[:-1] - mean_[1:])

        max1 = 0
        max2 = 0
        argmax1 = 0
        argmax2 = 0
        for i, delta_mean_i in enumerate(delta_mean):
            if delta_mean_i <= max2:
                continue
            if delta_mean_i > max1:
                max2 = max1
                argmax2 = argmax1
                max1 = delta_mean_i
                argmax1 = i
            else:
                max2 = delta_mean_i
                argmax2 = i
        h_min = min(argmax1, argmax2)
        h_max = min(max(argmax1, argmax2) + 1, h)
        if h_max - h_min < self.permissible_h_bbox:
            return image
        return image[h_min:h_max, :]

    # region METHOD___is_correct_bbox_image [DOMAIN(7): DocumentProcessing; CONCEPT(6): Method; TECH(6): Python]
    # endregion METHOD___get_base_line_image
    def __is_correct_bbox_image(self, image: np.ndarray) -> bool:
        h, w = image.shape[0:2]
# endregion CLASS_BoldClassifier
        return h > 3 and w > 3

    # endregion METHOD___is_correct_bbox_image


# region MODULE_CONTRACT [DOMAIN(8): DocumentProcessing; CONCEPT(7): Reader_bold_classifier; TECH(6): Python, dedoc]
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
## CLASS [22][BoldClassifier reader/processor] => BoldClassifier
## @usecases
## - [read]: System (Pipeline) → ParseDocument(PDF) → UnstructuredDocument
def _module_contract():
    pass
# endregion MODULE_CONTRACT
# GREP_SUMMARY: bold_classifier, dedoc, reader, PDF, PdfReader, BaseReader, PDF, pdfminer, tabby, OCR, tables, image, txtlayer, columns, orientation, paragraphs, metadata, extraction, line, bbox, BoldClassifier
# STRUCTURE: ▶ Init ┌PDF file┐ → [BoldClassifier] ○ can_read? → ○ read → [__init__ → classify → __get_bboxes_evaluation] → ⊕ UnstructuredDocument(lines, tables, attachments)
