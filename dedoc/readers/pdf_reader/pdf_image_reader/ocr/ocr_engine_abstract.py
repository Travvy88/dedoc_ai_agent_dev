# region MODULE_CONTRACT [DOMAIN(9): OCR; CONCEPT(9): Abstraction, StrategyPattern; TECH(8): Python, ABC, dataclasses]
## @modulecontract
## @purpose To define a clean abstraction layer (OCREngineAbstract) and lightweight flat dataclasses (OCRResult, OCRLine, OCRWord) for OCR results, decoupling the dedoc pipeline from any specific OCR engine implementation (Tesseract, EasyOCR, PaddleOCR, etc.) via the Strategy pattern.
## @scope OCR engine interface definition, result data structures, annotation generation.
## @input None (module defines interfaces and data structures).
## @output Abstract base class and three flat dataclasses consumed by OCRLineExtractor and OCRCellExtractor.
## @links [USES_API(9): abc.ABC, dataclasses.dataclass; READS_DATA_FROM(9): dedocutils.data_structures.BBox]
## @invariants
## - OCRWord ALWAYS has text: str, bbox: BBox, confidence: float.
## - OCRLine ALWAYS has words: List[OCRWord], bbox: BBox.
## - OCRLine.get_annotations() ALWAYS returns List[Annotation].
## - OCRResult ALWAYS has lines: List[OCRLine].
## - OCREngineAbstract subclasses MUST implement recognize_page() and recognize_cells().
## @rationale
## Q: Why flat dataclasses instead of the old 5-level hierarchy (Page → Block → Paragraph → Line → Word)?
## A: The intermediate levels (Block, Paragraph) were Tesseract-specific structural groupings with no business value. Flattening eliminates unnecessary complexity and makes the data portable across OCR engines. The Strategy pattern enables hot-swapping engines via config without touching pipeline code.
## @changes
## LAST_CHANGE: [v2.0.0 – Initial creation: flat dataclasses + ABC for multi-engine OCR architecture (Hypothesis D).]
## @modulemap
## DATA 10[Single OCR word with bbox and confidence] => OCRWord
## DATA 10[OCR line: list of words, line bbox, annotation generator] => OCRLine
## DATA 10[Top-level OCR result: list of OCRLine] => OCRResult
## ABC 10[Abstract interface for OCR engines] => OCREngineAbstract
## @usecases
## - [OCRWord]: OCREngine → RecognizeText → StructuredToken
## - [OCRLine]: OCRResult → GenerateAnnotations → BBoxAnnotation + ConfidenceAnnotation
## - [OCRResult]: OCRLineExtractor → IterateLines → LinesWithBBox
## - [OCREngineAbstract]: PdfImageReader → CreateEngine → DI into OCRLineExtractor
def _module_contract():
    pass
# endregion MODULE_CONTRACT
# GREP_SUMMARY: OCR, engine, abstract, ABC, Strategy, dataclass, OCRWord, OCRLine, OCRResult, OCREngineAbstract, annotation, BBox, confidence, multi-engine, interface
# STRUCTURE: ▶ ┌ABC┐ → define ◇ recognize_page(image,lang,is_one_column)→OCRResult ⊕ recognize_cells(image,lang)→OCRResult → concrete engines ∑ OCRWord(text,bbox,confidence) ⟦OCRLine(words,bbox,get_annotations)⟧ ⟦OCRResult(lines)⟧

import logging
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import List

import numpy as np
from dedocutils.data_structures import BBox

from dedoc.data_structures.annotation import Annotation
from dedoc.data_structures.concrete_annotations.bbox_annotation import BBoxAnnotation
from dedoc.data_structures.concrete_annotations.confidence_annotation import ConfidenceAnnotation

logger = logging.getLogger(__name__)


# region DATACLASS_OCRWord [DOMAIN(9): OCR; CONCEPT(8): DataModel, FlatStructure; TECH(7): Python, dataclass]
## @purpose To represent a single recognized word token with its bounding box and confidence score, serving as the atomic unit of OCR output across all engines.
## @uses dedocutils.data_structures.BBox
## @complexity 1
@dataclass
class OCRWord:
    """A single recognized word token with its bounding box and confidence score.

    Serves as the atomic unit of OCR output across all engine implementations.
    """

    text: str
    bbox: BBox
    confidence: float
# endregion DATACLASS_OCRWord


# region DATACLASS_OCRLine [DOMAIN(9): OCR; CONCEPT(8): DataModel, AnnotationGeneration; TECH(7): Python, dataclass]
## @purpose To represent a single line of recognized text as a list of OCRWord tokens, with a line-level bounding box and built-in annotation generation for the dedoc pipeline.
## @uses dedocutils.data_structures.BBox, dedoc.data_structures.concrete_annotations.*
## @complexity 5
@dataclass
class OCRLine:
    """A single line of recognized text composed of OCRWord tokens.

    Contains a line-level bounding box and provides annotation generation
    for the dedoc pipeline, converting OCR output into structured metadata.
    """

    words: List[OCRWord]
    bbox: BBox

    def get_annotations(self, page_width: int, page_height: int, extract_line_bbox: bool) -> List[Annotation]:
        """Generate dedoc annotations for this line.

        When *extract_line_bbox* is ``True``, a single
        :class:`~dedoc.data_structures.concrete_annotations.bbox_annotation.BBoxAnnotation`
        is returned for the whole line. Otherwise per-word
        :class:`~dedoc.data_structures.concrete_annotations.bbox_annotation.BBoxAnnotation` and
        :class:`~dedoc.data_structures.concrete_annotations.confidence_annotation.ConfidenceAnnotation`
        objects are generated.

        Args:
            page_width: Width of the source page in pixels.
            page_height: Height of the source page in pixels.
            extract_line_bbox: If ``True``, emit a single line-level bbox
                annotation; otherwise emit per-word annotations.

        Returns:
            List of dedoc Annotation objects.
        """
        # LDD-log: annotation generation entry
        logger.debug(f"[IMP:5][OCRLine][GET_ANNOTATIONS] extract_line_bbox={extract_line_bbox}, word_count={len(self.words)}")

        if extract_line_bbox:
            joined_text = " ".join(w.text for w in self.words)
            return [BBoxAnnotation(0, len(joined_text), self.bbox, page_width, page_height)]

        start = 0
        annotations: List[Annotation] = []

        for word in self.words:
            if word.text == "":
                continue

            end = start + len(word.text)
            annotations.append(ConfidenceAnnotation(start, end, str(word.confidence / 100)))
            annotations.append(BBoxAnnotation(start, end, word.bbox, page_width, page_height))
            start += len(word.text) + 1

        logger.debug(f"[IMP:5][OCRLine][GET_ANNOTATIONS] Generated {len(annotations)} annotations")
        return annotations
# endregion DATACLASS_OCRLine


# region DATACLASS_OCRResult [DOMAIN(9): OCR; CONCEPT(8): DataModel, FlatStructure; TECH(7): Python, dataclass]
## @purpose To encapsulate the complete OCR output for a single image as a flat list of OCRLine objects, replacing the old nested OcrPage hierarchy.
## @complexity 1
@dataclass
class OCRResult:
    """Top-level OCR output for a single image.

    Encapsulates the complete recognition result as a flat list of OCRLine
    objects, replacing the legacy nested OcrPage hierarchy.
    """

    lines: List[OCRLine]
# endregion DATACLASS_OCRResult


# region CLASS_OCREngineAbstract [DOMAIN(9): OCR; CONCEPT(10): StrategyPattern, Abstraction; TECH(8): Python, ABC]
## @purpose To define the stable contract that all OCR engine implementations (Tesseract, EasyOCR, PaddleOCR, etc.) must fulfill, enabling runtime engine selection via configuration without modifying pipeline orchestration code.
## @uses abc.ABC, abc.abstractmethod
## @complexity 1
class OCREngineAbstract(ABC):
    """Abstract interface for OCR engine implementations.

    Defines the stable contract that all OCR engine backends (Tesseract,
    EasyOCR, PaddleOCR, etc.) must fulfill, enabling runtime engine selection
    via configuration without modifying pipeline orchestration code.
    """

    @abstractmethod
    def recognize_page(self, image: np.ndarray, language: str, is_one_column: bool, **kwargs) -> OCRResult:
        """Recognize text on a full document page.

        Args:
            image: Input page image as a numpy array.
            language: OCR language string (e.g. "rus+eng").
            is_one_column: Whether the document uses a single-column layout.
            **kwargs: Additional engine-specific parameters.

        Returns:
            OCRResult containing all recognized lines and words.
        """
        ...

    @abstractmethod
    def recognize_cells(self, image: np.ndarray, language: str, **kwargs) -> OCRResult:
        """Recognize text in table cell images.

        Args:
            image: Input cell image as a numpy array.
            language: OCR language string.
            **kwargs: Additional engine-specific parameters.

        Returns:
            OCRResult containing recognized text lines within the cell.
        """
        ...
# endregion CLASS_OCREngineAbstract
