# region MODULE_CONTRACT [DOMAIN(9): OCR; CONCEPT(9): TesseractAdapter, EngineImplementation; TECH(8): Python, pytesseract]
## @modulecontract
## @purpose To implement the OCREngineAbstract interface using Tesseract OCR via pytesseract, converting Tesseract's raw dict output into a flat OCRResult (list of OCRLine → list of OCRWord), preserving the confidence filtering and PSM configuration logic from the legacy ocr_utils.py and ocr_page/ subsystem.
## @scope Tesseract OCR invocation, raw dict parsing, word grouping by line, confidence-based filtering, PSM configuration.
## @input image: np.ndarray, language: str, is_one_column: bool, config dict for ocr_conf_threshold.
## @output OCRResult with lines and words.
## @links [USES_API(9): pytesseract.image_to_data; IMPLEMENTS_INTERFACE(10): OCREngineAbstract]
## @invariants
## - recognize_page() and recognize_cells() ALWAYS return an OCRResult.
## - Words with confidence below ocr_conf_threshold are ALWAYS filtered out per line.
## - Line bbox comes from the level==4 Tesseract entry.
## @rationale
## Q: Why inline the dict parsing instead of using the old OcrPage.from_dict() chain?
## A: The old Page→Block→Paragraph→Line→Word hierarchy was Tesseract-specific and had no business value beyond grouping. Flattening directly to OCRLine→OCRWord eliminates 3 intermediate data classes and their sorting overhead. The confidence filtering and word ordering logic is preserved intact.
## @changes
## LAST_CHANGE: [v2.0.1 – Bug fix: compound key (block_num, par_num, line_num) for word grouping prevents cross-paragraph/cross-block line collision in Tesseract output.]
## - [v2.0.0 – Initial creation: Tesseract adapter implementation (Hypothesis D).]
## @modulemap
## CLASS 10[Tesseract OCR engine implementing OCREngineAbstract] => TesseractOCREngine
## FUNC 9[Converts Tesseract raw dict to OCRResult, grouping words by (block_num, par_num, line_num) compound key] => _raw_dict_to_ocr_result
## @usecases
## - [recognize_page]: OCRLineExtractor → RecognizeDocumentPage → OCRResult
## - [recognize_cells]: OCRCellExtractor → RecognizeTableCell → OCRResult
def _module_contract():
    pass
# endregion MODULE_CONTRACT
# GREP_SUMMARY: Tesseract, OCR, engine, pytesseract, image_to_data, PSM, confidence, threshold, recognize_page, recognize_cells, TesseractOCREngine
# STRUCTURE: ▶ Init ┌config(ocr_conf_threshold)┐ → ○ recognize_page(image,lang,is_one_column) → ⚡ psm=4|3 → pytesseract.image_to_data(DICT) → ◇ group by (block_num,par_num,line_num) compound key (level4→bbox,level5→words) → sort by (block_num,par_num,line_num) → filter conf≥threshold → ⊕ OCRResult(lines) → ○ recognize_cells(image,lang) → ⚡ psm=6 → same pipeline → ⎋ OCRResult

import logging
from collections import defaultdict
from typing import Dict, List, Tuple

import numpy as np
import pytesseract
from dedocutils.data_structures import BBox

from dedoc.readers.pdf_reader.pdf_image_reader.ocr.ocr_engine_abstract import OCREngineAbstract, OCRLine, OCRResult, OCRWord

logger = logging.getLogger(__name__)


# region CLASS_TesseractOCREngine [DOMAIN(9): OCR; CONCEPT(9): TesseractAdapter; TECH(8): Python, pytesseract]
## @purpose To serve as the default OCR engine in the dedoc pipeline, wrapping Tesseract via pytesseract and producing engine-agnostic OCRResult objects. Supports configurable confidence threshold and PSM modes for page vs. cell recognition.
## @uses pytesseract, OCREngineAbstract, OCRResult, OCRLine, OCRWord
## @complexity 6
class TesseractOCREngine(OCREngineAbstract):
    """Default OCR engine in the dedoc pipeline wrapping Tesseract via pytesseract.

    Produces engine-agnostic     :class:`~dedoc.readers.pdf_reader.pdf_image_reader.ocr.ocr_engine_abstract.OCRResult` objects with configurable
    confidence threshold and PSM modes for page vs. cell recognition.
    """

    # region METHOD___init__ [DOMAIN(8): OCR; CONCEPT(7): Configuration; TECH(6): Python]
    ## @purpose To initialize the Tesseract engine with configuration (confidence threshold) from the dedoc config dict.
    ## @io dict -> None
    ## @complexity 2
    def __init__(self, config: dict) -> None:
        """Initialize the Tesseract engine with configuration.

        Args:
            config: Dedoc configuration dictionary. Expected to contain
                an optional ``ocr_conf_threshold`` key (default: 40.0).
        """
        self.ocr_conf_threshold = config.get("ocr_conf_threshold", 40.0)
        logger.info(f"[IMP:7][TesseractOCREngine][INIT] ocr_conf_threshold={self.ocr_conf_threshold}")

    # region METHOD_recognize_page [DOMAIN(9): OCR; CONCEPT(9): PageRecognition; TECH(8): pytesseract]
    # endregion METHOD___init__
    ## @purpose To recognize text on a full document page image using Tesseract with appropriate PSM mode (4 for single-column, 3 for multi-column), and return the result as a flat OCRResult.
    ## @io np.ndarray, str, bool, **kwargs -> OCRResult
    ## @complexity 5
    def recognize_page(self, image: np.ndarray, language: str, is_one_column: bool, **kwargs) -> OCRResult:
        """Recognize text on a full document page image.

        Uses Tesseract PSM 4 for single-column documents and PSM 3 for
        multi-column layouts.

        Args:
            image: Page image as a numpy array.
            language: OCR language string (e.g. ``"rus+eng"``).
            is_one_column: ``True`` for single-column layout (PSM 4),
                ``False`` for multi-column (PSM 3).
            **kwargs: May include ``ocr_conf_threshold`` to override
                the instance-level threshold for this call.

        Returns:
            OCRResult with recognized lines and words.
        """
        # LDD-log: page recognition entry
        ocr_conf_threshold = kwargs.get("ocr_conf_threshold", self.ocr_conf_threshold)
        psm = 4 if is_one_column else 3
        logger.info(f"[IMP:7][TesseractOCREngine][RECOGNIZE_PAGE] is_one_column={is_one_column}, psm={psm}, language={language}")

        config = f"--psm {psm}"
        raw_dict = pytesseract.image_to_data(image, lang=language, output_type=pytesseract.Output.DICT, config=config)
        logger.debug(f"[IMP:4][TesseractOCREngine][RECOGNIZE_PAGE] Raw dict keys: {list(raw_dict.keys())}, entries: {len(raw_dict.get('level', []))}")

        ocr_result = self._raw_dict_to_ocr_result(raw_dict, ocr_conf_threshold=ocr_conf_threshold)
        logger.info(f"[IMP:8][TesseractOCREngine][RECOGNIZE_PAGE] Result: {len(ocr_result.lines)} lines recognized")
        return ocr_result

    # region METHOD_recognize_cells [DOMAIN(9): OCR; CONCEPT(9): CellRecognition; TECH(8): pytesseract]
    # endregion METHOD_recognize_page
    ## @purpose To recognize text in table cell images using Tesseract with PSM 6 (uniform block of text), returning results as a flat OCRResult.
    ## @io np.ndarray, str, **kwargs -> OCRResult
    ## @complexity 3
    def recognize_cells(self, image: np.ndarray, language: str, **kwargs) -> OCRResult:
        """Recognize text in table cell images.

        Uses Tesseract PSM 6 (uniform block of text).

        Args:
            image: Cell image as a numpy array.
            language: OCR language string.
            **kwargs: May include ``ocr_conf_threshold`` to override
                the default threshold (0.0) for this call.

        Returns:
            OCRResult with recognized text lines within the cell.
        """
        # LDD-log: cell recognition entry
        ocr_conf_threshold = kwargs.get("ocr_conf_threshold", 0.0)
        logger.info(f"[IMP:7][TesseractOCREngine][RECOGNIZE_CELLS] language={language}")

        config = "--psm 6"
        raw_dict = pytesseract.image_to_data(image, lang=language, output_type=pytesseract.Output.DICT, config=config)
        logger.debug(f"[IMP:4][TesseractOCREngine][RECOGNIZE_CELLS] Raw dict entries: {len(raw_dict.get('level', []))}")

        ocr_result = self._raw_dict_to_ocr_result(raw_dict, ocr_conf_threshold=ocr_conf_threshold)
        logger.info(f"[IMP:8][TesseractOCREngine][RECOGNIZE_CELLS] Result: {len(ocr_result.lines)} lines recognized")
        return ocr_result

    # region METHOD__raw_dict_to_ocr_result [DOMAIN(9): OCR; CONCEPT(9): Parsing, DataConversion; TECH(7): Python, pytesseract]
    # endregion METHOD_recognize_cells
    ## @purpose To convert Tesseract's raw image_to_data dict output into a flat OCRResult by grouping level==5 words by compound key (block_num, line_num) to prevent cross-block line collisions, applying confidence filtering, and extracting line bounding boxes from level==4 entries.
    ## @io Dict -> OCRResult
    ## @complexity 6
    def _raw_dict_to_ocr_result(self, raw_dict: Dict[str, list], ocr_conf_threshold: float = None) -> OCRResult:
        """Convert Tesseract's raw image_to_data dict into an OCRResult.

        Groups level-5 (word) entries by compound key
        ``(block_num, line_num)``, extracts line bounding boxes from level-4
        entries, filters words by confidence threshold, and assembles
        :class:`~dedoc.readers.pdf_reader.pdf_image_reader.ocr.ocr_engine_abstract.OCRLine` objects in reading order.

        Args:
            raw_dict: The dictionary returned by
                ``pytesseract.image_to_data(output_type=DICT)``.
            ocr_conf_threshold: Minimum confidence value for a word to be
                included. Falls back to ``self.ocr_conf_threshold`` if
                ``None``.

        Returns:
            OCRResult containing the parsed lines.
        """
        if ocr_conf_threshold is None:
            ocr_conf_threshold = self.ocr_conf_threshold
        n_entries = len(raw_dict.get("level", []))
        logger.debug(f"[IMP:4][TesseractOCREngine][RAW_TO_RESULT] Processing {n_entries} entries")

        # BUG_FIX_CONTEXT: Compound (block_num, par_num, line_num) key replaces single line_num key.
        # The old approach used only line_num as key, which merged lines from different
        # blocks/paragraphs sharing the same line_num into a single garbled OCRLine. Tesseract resets
        # line_num per parent paragraph (level 3), so block 1 para 2 line 1 and block 1 para 1 line 1
        # were conflated. psm=4 (single column of variable sizes) may produce multiple paragraphs
        # within a single block, making (block_num, line_num) insufficient for uniqueness.
        # Sorting by (block_num, par_num, line_num) ensures correct reading order across all segments.
        block_para_line_to_head: Dict[tuple, dict] = {}
        block_para_line_to_words: Dict[tuple, List[dict]] = defaultdict(list)

        # BUG_FIX_CONTEXT: Iterating raw dict by index to handle Tesseract output where entries share a single list per key.
        # Previously the old code used OcrElement.from_ocr_dict() for the same purpose.
        for i in range(n_entries):
            entry = {key: raw_dict[key][i] for key in raw_dict.keys()}
            level = int(entry["level"])

            compound_key = (int(entry["block_num"]), int(entry["par_num"]), int(entry["line_num"]))

            if level == 4:
                block_para_line_to_head[compound_key] = entry
            elif level == 5:
                block_para_line_to_words[compound_key].append(entry)

        logger.debug(f"[IMP:5][TesseractOCREngine][RAW_TO_RESULT] Found {len(block_para_line_to_head)} line heads, {sum(len(v) for v in block_para_line_to_words.values())} total words")

        ocr_lines: List[OCRLine] = []

        # BUG_FIX_CONTEXT: Sorted by (block_num, par_num, line_num) ensures correct reading-order traversal
        # across multiple paragraphs and blocks. Single-paragraph documents sort by line_num naturally.
        for (block_num, par_num, line_num) in sorted(block_para_line_to_words.keys()):
            word_entries = block_para_line_to_words[(block_num, par_num, line_num)]
            head = block_para_line_to_head.get((block_num, par_num, line_num))

            if head is None:
                logger.warning(f"[IMP:7][TesseractOCREngine][RAW_TO_RESULT] No level==4 head for block={block_num} par={par_num} line={line_num}, skipping")
                continue

            line_bbox = BBox(
                x_top_left=head["left"],
                y_top_left=head["top"],
                width=head["width"],
                height=head["height"]
            )

            # BUG_FIX_CONTEXT: Confidence filtering mirrors OcrLine.from_list() line 67-69.
            # Words are sorted by word_num, filtered by ocr_conf_threshold, then converted to OCRWord.
            word_entries_sorted = sorted(word_entries, key=lambda w: int(w["word_num"]))
            filtered_words = [
                w for w in word_entries_sorted
                if float(w["conf"]) >= ocr_conf_threshold
            ]

            if not filtered_words:
                logger.debug(f"[IMP:5][TesseractOCREngine][RAW_TO_RESULT] All words filtered for block={block_num} par={par_num} line={line_num}")
                continue

            ocr_words = [
                OCRWord(
                    text=str(entry["text"]).replace("\u2014", " "),
                    bbox=BBox(
                        x_top_left=entry["left"],
                        y_top_left=entry["top"],
                        width=entry["width"],
                        height=entry["height"]
                    ),
                    confidence=float(entry["conf"])
                )
                for entry in filtered_words
            ]

            ocr_lines.append(OCRLine(words=ocr_words, bbox=line_bbox))

        logger.info(f"[IMP:9][TesseractOCREngine][RAW_TO_RESULT] Converted to {len(ocr_lines)} OCRLine objects")
        return OCRResult(lines=ocr_lines)
    # endregion METHOD__raw_dict_to_ocr_result
# endregion CLASS_TesseractOCREngine
