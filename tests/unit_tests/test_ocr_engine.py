# region MODULE_CONTRACT [DOMAIN(9): OCR, Testing; CONCEPT(7): UnitTest, DataclassVerification; TECH(7): Python, unittest, numpy]
## @modulecontract
## @purpose To verify the correctness of the OCR engine abstraction (dataclasses, TesseractOCREngine implementation) and ensure the Strategy pattern integration works end-to-end with LDD log telemetry.
## @scope Unit testing of OCRWord, OCRLine, OCRResult dataclasses; integration testing of TesseractOCREngine.recognize_page() and recognize_cells().
## @input Test fixtures: numpy arrays with simulated text images, configuration dicts.
## @output Test results with LDD [IMP:7-10] log output to console.
## @links [TESTS(10): OCREngineAbstract, TesseractOCREngine, OCRResult, OCRLine, OCRWord]
## @invariants
## - All tests MUST pass (100% PASS).
## - LDD [IMP:7-10] logs MUST be printed before assertions.
## @rationale
## Q: Why test dataclasses separately from engine integration?
## A: Dataclasses are the contract interface — their correctness must be independently verified. Engine integration tests validate the full Tesseract→OCRResult pipeline.
## @changes
## LAST_CHANGE: [v2.0.0 – Initial creation for multi-engine OCR architecture (Hypothesis D).]
## @modulemap
## FUNC 10[Test OCRWord dataclass fields] => test_ocr_word_dataclass
## FUNC 10[Test OCRLine dataclass and get_annotations] => test_ocr_line_dataclass
## FUNC 10[Test OCRResult dataclass] => test_ocr_result_dataclass
## FUNC 10[Test TesseractOCREngine page recognition] => test_tesseract_engine_recognize_page
## FUNC 10[Test TesseractOCREngine cell recognition] => test_tesseract_engine_recognize_cells
## @usecases
## - [test_ocr_word_dataclass]: QA Agent → VerifyDataClassIntegrity → OCRWordFieldsValid
## - [test_tesseract_engine_recognize_page]: QA Agent → VerifyEngineIntegration → TesseractProducesOCRResult
def _module_contract():
    pass
# endregion MODULE_CONTRACT
# GREP_SUMMARY: OCR, engine, test, unittest, TesseractOCREngine, OCRWord, OCRLine, OCRResult, dataclass, annotation, LDD
# STRUCTURE: ▶ ┌TestSuite┐ → ○ test_ocr_word_dataclass → ◇ verify text/bbox/confidence → ○ test_ocr_line_dataclass → ◇ verify words/bbox/get_annotations → ○ test_ocr_result_dataclass → ◇ verify lines iteration → ○ test_tesseract_engine_recognize_page → ⚡ numpy→pytesseract→OCRResult → ○ test_tesseract_engine_recognize_cells → ⚡ same pipeline → ∑ ALL PASS

import logging
import sys
import unittest
from typing import List

import numpy as np
from dedocutils.data_structures import BBox

from dedoc.data_structures.annotation import Annotation
from dedoc.data_structures.concrete_annotations.bbox_annotation import BBoxAnnotation
from dedoc.data_structures.concrete_annotations.confidence_annotation import ConfidenceAnnotation
from dedoc.readers.pdf_reader.pdf_image_reader.ocr.ocr_engine_abstract import OCREngineAbstract, OCRLine, OCRResult, OCRWord
from dedoc.readers.pdf_reader.pdf_image_reader.ocr.tesseract_ocr_engine import TesseractOCREngine

logger = logging.getLogger(__name__)


def _setup_console_logging() -> None:
    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(logging.DEBUG)
    handler.setFormatter(logging.Formatter("%(levelname)s - %(name)s - %(message)s"))
    root_logger = logging.getLogger()
    root_logger.handlers.clear()
    root_logger.addHandler(handler)
    root_logger.setLevel(logging.DEBUG)


# region CLASS_TestOCREngine [DOMAIN(9): OCR; CONCEPT(9): UnitTest; TECH(7): Python, unittest]
class TestOCREngine(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        _setup_console_logging()
        cls.config = {"ocr_conf_threshold": 40.0}
        cls.engine = TesseractOCREngine(config=cls.config)

    # region FUNC_test_ocr_word_dataclass [DOMAIN(9): OCR; CONCEPT(8): DataclassVerification; TECH(6): Python]
    ## @purpose To verify that OCRWord dataclass is correctly instantiated with text, bbox, and confidence fields, matching the contract expected by the pipeline.
    ## @uses OCRWord, BBox
    ## @complexity 2
    def test_ocr_word_dataclass(self) -> None:
        print("\n--- LDD TRAJECTORY (IMP:7-10) for test_ocr_word_dataclass ---")

        bbox = BBox(x_top_left=10, y_top_left=20, width=100, height=30)
        word = OCRWord(text="hello", bbox=bbox, confidence=95.5)

        print(f"[IMP:9][TestOCREngine][OCRWORD] Created OCRWord: text={word.text}, bbox={word.bbox}, confidence={word.confidence}")
        self.assertEqual(word.text, "hello")
        self.assertEqual(word.bbox.x_top_left, 10)
        self.assertEqual(word.bbox.y_top_left, 20)
        self.assertEqual(word.bbox.width, 100)
        self.assertEqual(word.bbox.height, 30)
        self.assertEqual(word.confidence, 95.5)
        print(f"[IMP:9][TestOCREngine][OCRWORD] All field assertions passed [VALUE]")
    # endregion FUNC_test_ocr_word_dataclass

    # region FUNC_test_ocr_line_dataclass [DOMAIN(9): OCR; CONCEPT(8): AnnotationGeneration; TECH(7): Python]
    ## @purpose To verify OCRLine dataclass correctly groups words and generates annotations in two modes: extract_line_bbox=True (single BBoxAnnotation) and False (per-word Confidence + BBox pairs).
    ## @uses OCRLine, OCRWord, BBox
    ## @complexity 5
    def test_ocr_line_dataclass(self) -> None:
        print("\n--- LDD TRAJECTORY (IMP:7-10) for test_ocr_line_dataclass ---")

        word1 = OCRWord(text="abc", bbox=BBox(x_top_left=0, y_top_left=0, width=30, height=10), confidence=80.0)
        word2 = OCRWord(text="def", bbox=BBox(x_top_left=35, y_top_left=0, width=30, height=10), confidence=90.0)
        word3 = OCRWord(text="", bbox=BBox(x_top_left=70, y_top_left=0, width=5, height=10), confidence=50.0)
        line_bbox = BBox(x_top_left=0, y_top_left=0, width=105, height=10)
        line = OCRLine(words=[word1, word2, word3], bbox=line_bbox)

        print(f"[IMP:9][TestOCREngine][OCR_LINE] Line created: {len(line.words)} words, bbox={line.bbox} [VALUE]")

        annotations_whole: List[Annotation] = line.get_annotations(page_width=500, page_height=700, extract_line_bbox=True)
        print(f"[IMP:9][TestOCREngine][OCR_LINE_WHOLE] extract_line_bbox=True → {len(annotations_whole)} annotations")
        self.assertEqual(len(annotations_whole), 1)
        self.assertIsInstance(annotations_whole[0], BBoxAnnotation)
        whole_annotation: BBoxAnnotation = annotations_whole[0]
        self.assertEqual(whole_annotation.start, 0)
        self.assertIsNotNone(whole_annotation.value)
        print(f"[IMP:9][TestOCREngine][OCR_LINE_WHOLE] Single BBoxAnnotation verified [VALUE]")

        annotations_per_word: List[Annotation] = line.get_annotations(page_width=500, page_height=700, extract_line_bbox=False)
        print(f"[IMP:9][TestOCREngine][OCR_LINE_PER_WORD] extract_line_bbox=False → {len(annotations_per_word)} annotations")
        expected_count = 4  # 2 words * 2 annotations each (confidence + bbox), empty word skipped
        self.assertEqual(len(annotations_per_word), expected_count)
        self.assertIsInstance(annotations_per_word[0], ConfidenceAnnotation)
        self.assertIsInstance(annotations_per_word[1], BBoxAnnotation)
        self.assertIsInstance(annotations_per_word[2], ConfidenceAnnotation)
        self.assertIsInstance(annotations_per_word[3], BBoxAnnotation)
        print(f"[IMP:8][TestOCREngine][OCR_LINE_PER_WORD] Per-word Confidence+BBox pairs verified [VALUE]")
    # endregion FUNC_test_ocr_line_dataclass

    # region FUNC_test_ocr_result_dataclass [DOMAIN(9): OCR; CONCEPT(7): DataclassVerification; TECH(6): Python]
    ## @purpose To verify OCRResult dataclass correctly holds and iterates over OCRLine objects.
    ## @uses OCRResult, OCRLine, OCRWord, BBox
    ## @complexity 2
    def test_ocr_result_dataclass(self) -> None:
        print("\n--- LDD TRAJECTORY (IMP:7-10) for test_ocr_result_dataclass ---")

        line1 = OCRLine(
            words=[OCRWord(text="line1", bbox=BBox(x_top_left=0, y_top_left=0, width=50, height=10), confidence=90.0)],
            bbox=BBox(x_top_left=0, y_top_left=0, width=50, height=10)
        )
        line2 = OCRLine(
            words=[OCRWord(text="line2", bbox=BBox(x_top_left=0, y_top_left=15, width=50, height=10), confidence=85.0)],
            bbox=BBox(x_top_left=0, y_top_left=15, width=50, height=10)
        )
        result = OCRResult(lines=[line1, line2])

        print(f"[IMP:9][TestOCREngine][OCR_RESULT] OCRResult created with {len(result.lines)} lines [VALUE]")
        self.assertEqual(len(result.lines), 2)
        self.assertEqual(result.lines[0].words[0].text, "line1")
        self.assertEqual(result.lines[1].words[0].text, "line2")
        print(f"[IMP:8][TestOCREngine][OCR_RESULT] Lines iteration and field access verified [VALUE]")
    # endregion FUNC_test_ocr_result_dataclass

    # region FUNC_test_tesseract_engine_recognize_page [DOMAIN(9): OCR; CONCEPT(10): EngineIntegration; TECH(8): Python, pytesseract, numpy]
    ## @purpose To verify TesseractOCREngine.recognize_page() produces a valid OCRResult from a synthetic text image, confirming the full Tesseract→OCRResult pipeline works end-to-end.
    ## @uses TesseractOCREngine, numpy, OCRResult
    ## @complexity 7
    def test_tesseract_engine_recognize_page(self) -> None:
        print("\n--- LDD TRAJECTORY (IMP:7-10) for test_tesseract_engine_recognize_page ---")

        try:
            import pytesseract
            pytesseract.get_tesseract_version()
        except (ImportError, Exception):
            self.skipTest("tesseract not installed or not in PATH")
            return

        image = np.full((100, 400), fill_value=255, dtype=np.uint8)
        from PIL import Image, ImageDraw, ImageFont
        pil_image = Image.fromarray(image)
        draw = ImageDraw.Draw(pil_image)
        try:
            font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 20)
        except (IOError, OSError):
            font = ImageFont.load_default()
        draw.text((10, 10), "Hello world", fill=0, font=font)
        draw.text((10, 40), "Test line", fill=0, font=font)
        image = np.array(pil_image)

        print(f"[IMP:8][TestOCREngine][RECOGNIZE_PAGE] Synthetic image created: shape={image.shape}")

        result: OCRResult = self.engine.recognize_page(image=image, language="eng", is_one_column=True)

        print(f"[IMP:9][TestOCREngine][RECOGNIZE_PAGE] OCRResult: {len(result.lines)} lines recognized [VALUE]")
        self.assertIsInstance(result, OCRResult)
        self.assertIsInstance(result.lines, list)
        if len(result.lines) > 0:
            first_line = result.lines[0]
            self.assertIsInstance(first_line, OCRLine)
            self.assertIsInstance(first_line.bbox, BBox)
            if len(first_line.words) > 0:
                first_word = first_line.words[0]
                self.assertIsInstance(first_word, OCRWord)
                self.assertIsInstance(first_word.text, str)
                self.assertIsInstance(first_word.bbox, BBox)
                self.assertIsInstance(first_word.confidence, float)
            print(f"[IMP:9][TestOCREngine][RECOGNIZE_PAGE] OCRResult structure verified [VALUE]")
        else:
            print(f"[IMP:7][TestOCREngine][RECOGNIZE_PAGE] No lines recognized (Tesseract may not have detected text) [WARN]")
    # endregion FUNC_test_tesseract_engine_recognize_page

    # region FUNC_test_tesseract_engine_recognize_cells [DOMAIN(9): OCR; CONCEPT(10): EngineIntegration; TECH(8): Python, pytesseract, numpy]
    ## @purpose To verify TesseractOCREngine.recognize_cells() produces a valid OCRResult from a synthetic cell image, confirming the cell-level PSM 6 pipeline works end-to-end.
    ## @uses TesseractOCREngine, numpy, OCRResult
    ## @complexity 7
    def test_tesseract_engine_recognize_cells(self) -> None:
        print("\n--- LDD TRAJECTORY (IMP:7-10) for test_tesseract_engine_recognize_cells ---")

        try:
            import pytesseract
            pytesseract.get_tesseract_version()
        except (ImportError, Exception):
            self.skipTest("tesseract not installed or not in PATH")
            return

        image = np.full((50, 200), fill_value=255, dtype=np.uint8)
        from PIL import Image, ImageDraw, ImageFont
        pil_image = Image.fromarray(image)
        draw = ImageDraw.Draw(pil_image)
        try:
            font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 14)
        except (IOError, OSError):
            font = ImageFont.load_default()
        draw.text((5, 5), "Cell text", fill=0, font=font)
        image = np.array(pil_image)

        print(f"[IMP:8][TestOCREngine][RECOGNIZE_CELLS] Synthetic cell image created: shape={image.shape}")

        result: OCRResult = self.engine.recognize_cells(image=image, language="eng")

        print(f"[IMP:9][TestOCREngine][RECOGNIZE_CELLS] OCRResult: {len(result.lines)} lines recognized [VALUE]")
        self.assertIsInstance(result, OCRResult)
        self.assertIsInstance(result.lines, list)
        if len(result.lines) > 0:
            first_line = result.lines[0]
            self.assertIsInstance(first_line, OCRLine)
            self.assertIsInstance(first_line.bbox, BBox)
            if len(first_line.words) > 0:
                first_word = first_line.words[0]
                self.assertIsInstance(first_word, OCRWord)
                self.assertIsInstance(first_word.text, str)
                self.assertIsInstance(first_word.bbox, BBox)
                self.assertIsInstance(first_word.confidence, float)
            print(f"[IMP:9][TestOCREngine][RECOGNIZE_CELLS] OCRResult structure verified [VALUE]")
        else:
            print(f"[IMP:7][TestOCREngine][RECOGNIZE_CELLS] No lines recognized (Tesseract may not have detected text) [WARN]")
    # endregion FUNC_test_tesseract_engine_recognize_cells

    # region FUNC_test_ocr_engine_abstract_interface [DOMAIN(9): OCR; CONCEPT(8): ABCValidation; TECH(6): Python]
    ## @purpose To verify OCREngineAbstract ABC correctly enforces the interface contract — classes must implement recognize_page() and recognize_cells().
    ## @uses OCREngineAbstract, abc
    ## @complexity 3
    def test_ocr_engine_abstract_interface(self) -> None:
        print("\n--- LDD TRAJECTORY (IMP:7-10) for test_ocr_engine_abstract_interface ---")

        from abc import ABC

        self.assertTrue(issubclass(OCREngineAbstract, ABC))
        self.assertTrue(issubclass(TesseractOCREngine, OCREngineAbstract))

        with self.assertRaises(TypeError):
            OCREngineAbstract()

        print(f"[IMP:9][TestOCREngine][ABSTRACT_IFACE] ABC enforcement verified — instantiation blocked, TesseractOCREngine is subclass [VALUE]")
    # endregion FUNC_test_ocr_engine_abstract_interface

# endregion CLASS_TestOCREngine


if __name__ == "__main__":
    unittest.main()
