# region MODULE_CONTRACT [DOMAIN(9): OCR; CONCEPT(10): PaddleOCR, EngineAdapter, MultiPass; TECH(9): Python, paddleocr, PaddleX]
## @modulecontract
## @purpose To implement the OCREngineAbstract interface using PaddleOCR (PP-OCRv5 / PP-OCRv6) via the PaddleX SDK, supporting single-pass recognition for unified language groups, multi-pass OCR for mixed language groups with deduplication, and cell-only recognition via the standalone TextRecognition API. All model loading is lazy — no PaddleX import until first inference.
## @scope PaddleOCR page recognition, cell recognition, multi-pass merge, result conversion, lazy initialization, warmup.
## @input image: np.ndarray, language: str, config dict with ocr_engine / ocr_device / ocr_precision / ocr_use_tensorrt / ocr_cpu_threads / ocr_conf_threshold.
## @output OCRResult with lines and words.
## @links [IMPLEMENTS_INTERFACE(10): OCREngineAbstract; USES_SERVICE(9): PaddleOCRLanguageMapper, PaddleOCRModelConfig; USES_API(9): paddleocr (PaddleOCR via PaddleX)]
## @invariants
## - recognize_page() and recognize_cells() ALWAYS return an OCRResult.
## - PaddleOCR instance is created lazily on first _get_ocr() call (not in __init__).
## - If paddleocr is not installed, _get_ocr() raises ImportError with installation instructions.
## - multi_pass_ocr ALWAYS sorts merged lines by Y and deduplicates by overlap > 50%.
## @rationale
## Q: Why lazy init for PaddleOCR instead of loading in __init__?
## A: PaddleOCR loads heavy DL models (~300MB+). Lazy init ensures that if the user doesn't request paddle engine, no unnecessary memory is consumed. Also allows Tesseract to work even if paddleocr is not installed.
## Q: Why multi-pass for mixed languages?
## A: PP-OCRv5 has separate recognition models per language group (eslav, latin, etc.). To recognize mixed-language pages, each group needs its own recognition pass with the appropriate model.
## @changes
## LAST_CHANGE: [v1.7.0 – Add defensive grayscale-to-BGR conversion in single_pass_ocr to prevent PaddleX text detection resize() crash on (H,W) input. See BUG_FIX_CONTEXT in single_pass_ocr.]
## @modulemap
## CLASS 10[PaddleOCR engine implementing OCREngineAbstract] => PaddleOCREngine
## FUNC 8[Lazy-init PaddleOCR with ImportError guard] => _get_ocr
## FUNC 9[Full page OCR: validate, group, single or multi-pass] => recognize_page
## FUNC 8[Single recognition pass with one model config] => single_pass_ocr
## FUNC 9[Multi-pass: one det + N rec passes, merge with dedup] => multi_pass_ocr
## FUNC 9[Cell OCR: full det+rec via single_pass_ocr, language-aware model selection] => recognize_cells
## FUNC 8[Convert PaddleX flat dict (dt_polys/rec_texts/rec_score) to OCRResult] => _paddle_result_to_ocr_result
## FUNC 8[Merge multi-pass results: concat, sort, dedup] => _merge_multi_pass_results
## FUNC 7[Preload models at service startup] => warmup
## @usecases
## - [recognize_page]: PdfImageReader → RecognizeDocumentPage → OCRResult
## - [recognize_cells]: OCRCellExtractor → RecognizeTableCell → OCRResult
## - [warmup]: ServiceStartup → PreloadModels → FasterFirstRequest
def _module_contract():
    pass
# endregion MODULE_CONTRACT
# GREP_SUMMARY: PaddleOCR, OCR, engine, paddleocr, PaddleX, PP-OCRv5, PP-OCRv6, multi-pass, single-pass, cell recognition, lazy init, warmup, dedup, merge, PaddleOCREngine
# STRUCTURE: ▶ Init ┌config┐ → ⊕ self._ocr=None + mapper + model_config → ○ recognize_page(image,language) → ◇ parse + normalize + validate → ◇ group_languages → 1 group? → single_pass_ocr ┃ N groups? → multi_pass_ocr → ○ single_pass_ocr → ⚡ PaddleOCR.predict(np.ndarray) → ⊕ _paddle_result_to_ocr_result → ○ multi_pass_ocr → ∑ single_pass_ocr per group → ⊕ _merge_multi_pass_results(all_results) → ⊕ OCRResult → ○ recognize_cells → ◇ normalize+group language → single_pass_ocr(full det+rec) → ⊕ OCRResult → ○ warmup → ⚡ dummy_img → predict → ∇ ready

import logging
from typing import List, Optional

import cv2
import numpy as np
from dedocutils.data_structures import BBox

from dedoc.readers.pdf_reader.pdf_image_reader.ocr.ocr_engine_abstract import OCREngineAbstract, OCRLine, OCRResult, OCRWord
from dedoc.readers.pdf_reader.pdf_image_reader.ocr.paddleocr_language_mapper import PaddleOCRLanguageMapper

logger = logging.getLogger(__name__)


# region FUNC__bbox_intersection_area [DOMAIN(8): OCR; CONCEPT(8): Geometry; TECH(5): Python]
## @purpose To compute the intersection area of two BBox rectangles, used for deduplication during multi-pass merge.
## @io BBox, BBox -> float
## @complexity 2
def _bbox_intersection_area(bbox1: BBox, bbox2: BBox) -> float:
    x_left = max(bbox1.x_top_left, bbox2.x_top_left)
    y_top = max(bbox1.y_top_left, bbox2.y_top_left)
    x_right = min(bbox1.x_top_left + bbox1.width, bbox2.x_top_left + bbox2.width)
    y_bottom = min(bbox1.y_top_left + bbox1.height, bbox2.y_top_left + bbox2.height)
    if x_right < x_left or y_bottom < y_top:
        return 0.0
    return float((x_right - x_left) * (y_bottom - y_top))
# endregion FUNC__bbox_intersection_area


# region FUNC__polygon_to_bbox [DOMAIN(8): OCR; CONCEPT(8): Geometry; TECH(5): Python]
## @purpose To convert a 4-point polygon list [[x1,y1],[x2,y2],[x3,y3],[x4,y4]] into a BBox (min x, min y, width, height).
## @io list -> BBox
## @complexity 2
def _polygon_to_bbox(polygon: list) -> BBox:
    xs = [pt[0] for pt in polygon]
    ys = [pt[1] for pt in polygon]
    x_min = min(xs)
    y_min = min(ys)
    return BBox(
        x_top_left=x_min,
        y_top_left=y_min,
        width=max(xs) - x_min,
        height=max(ys) - y_min
    )
# endregion FUNC__polygon_to_bbox


# region CLASS_PaddleOCREngine [DOMAIN(9): OCR; CONCEPT(10): PaddleOCRAdapter; TECH(9): Python, paddleocr, PaddleX]
## @purpose To serve as the PaddleOCR backend for dedoc, implementing the OCREngineAbstract contract with lazy model loading, single/multi-pass recognition strategies, and cell-only recognition via TextRecognition API.
## @uses PaddleOCRLanguageMapper, PaddleOCRModelConfig, PaddleOCR, TextRecognition
## @complexity 9
class PaddleOCREngine(OCREngineAbstract):

    # region METHOD___init__ [DOMAIN(9): OCR; CONCEPT(9): Configuration; TECH(7): Python]
    ## @purpose To initialize the engine with OCR configuration parameters and create the language mapper. PaddleOCR is NOT loaded here — it is lazily initialized on first inference call.
    ## @io dict -> None
    ## @complexity 4
    # BUG_FIX_CONTEXT: PaddleOCRLanguageMapper was imported inside __init__, which caused
    # test_lazy_import_no_paddleocr to fail — the test patches builtins.__import__ with ImportError,
    # which also intercepted this internal import before _get_ocr() could be called.
    # The mapper is pure Python with zero ML dependencies, so it's safe to import at module level.
    def __init__(self, config: dict) -> None:
        self.config = config
        ocr_engine = config.get("ocr_engine", "paddle_v5_server")
        self.ocr_engine = ocr_engine
        if ocr_engine.startswith("paddle_v5"):
            self.ocr_engine_version = "paddle_v5"
            self.ocr_model_size = ocr_engine.replace("paddle_v5_", "")
        elif ocr_engine.startswith("paddle_v6"):
            self.ocr_engine_version = "paddle_v6"
            self.ocr_model_size = ocr_engine.replace("paddle_v6_", "")
        else:
            self.ocr_engine_version = ocr_engine
            self.ocr_model_size = "server"
        self.ocr_device = config.get("ocr_device", "cpu")
        self.ocr_precision = config.get("ocr_precision", "fp32")
        self.ocr_use_tensorrt = config.get("ocr_use_tensorrt", False)
        self.ocr_cpu_threads = config.get("ocr_cpu_threads", 10)
        self.ocr_conf_threshold = config.get("ocr_conf_threshold", 0.0)

        self.language_mapper = PaddleOCRLanguageMapper()

        self._ocr = None

        logger.info(
            f"[IMP:7][PaddleOCREngine][INIT] engine={self.ocr_engine}, version={self.ocr_engine_version}, "
            f"model_size={self.ocr_model_size}, device={self.ocr_device}, precision={self.ocr_precision}, "
            f"use_tensorrt={self.ocr_use_tensorrt}, cpu_threads={self.ocr_cpu_threads}"
        )
    # endregion METHOD___init__

    # region METHOD__get_ocr [DOMAIN(9): OCR; CONCEPT(9): LazyInit; TECH(8): Python, PaddleX]
    ## @purpose To lazily initialize and cache the default PaddleOCR instance on first call. If paddleocr is not installed, raises ImportError with a clear installation message.
    ## @io None -> PaddleOCR
    ## @complexity 4
    def _get_ocr(self):
        if self._ocr is None:
            logger.info(f"[IMP:7][PaddleOCREngine][GET_OCR] Lazy init: importing PaddleOCR")
            try:
                from paddleocr import PaddleOCR as PaddleXOCR
            except ImportError:
                msg = (
                    "PaddleOCR is not installed. Install with: pip install paddleocr>=3.0"
                )
                logger.error(f"[IMP:10][PaddleOCREngine][GET_OCR] {msg}")
                raise ImportError(msg)

            from dedoc.readers.pdf_reader.pdf_image_reader.ocr.paddleocr_model_config import PaddleOCRModelConfig
            det_model = PaddleOCRModelConfig.get_det_model(self.ocr_engine_version, self.ocr_model_size)
            rec_model = PaddleOCRModelConfig.get_rec_model(self.ocr_engine_version, self.ocr_model_size, "en")

            self._ocr = PaddleXOCR(
                text_detection_model_name=det_model,
                text_recognition_model_name=rec_model,
                lang="en",
                device=self.ocr_device,
                engine="paddle",
                precision=self.ocr_precision,
                use_tensorrt=self.ocr_use_tensorrt,
                cpu_threads=self.ocr_cpu_threads,
                use_doc_orientation_classify=False,
                use_doc_unwarping=False,
                use_textline_orientation=False,
            )
            logger.info(
                f"[IMP:8][PaddleOCREngine][GET_OCR] PaddleOCR created: det={det_model}, rec={rec_model}"
            )
        return self._ocr
    # endregion METHOD__get_ocr

    # region METHOD_recognize_page [DOMAIN(9): OCR; CONCEPT(10): PageRecognition; TECH(9): Python]
    ## @purpose To recognize text on a full document page: parse and normalize language codes, validate engine-language compatibility, group languages by rec-model, and dispatch to single_pass_ocr or multi_pass_ocr.
    ## @io np.ndarray, str, bool, **kwargs -> OCRResult
    ## @complexity 7
    def recognize_page(self, image: np.ndarray, language: str, is_one_column: bool, **kwargs) -> OCRResult:
        logger.info(
            f"[IMP:7][PaddleOCREngine][RECOGNIZE_PAGE] language={language}, "
            f"is_one_column={is_one_column} (ignored by PaddleOCR)"
        )

        raw_langs = [l.strip() for l in language.split("+")]
        normalized_langs = []
        for raw in raw_langs:
            norm = self.language_mapper.normalize_language(raw)
            normalized_langs.append(norm)
            logger.debug(f"[IMP:5][PaddleOCREngine][RECOGNIZE_PAGE] normalize '{raw}' -> '{norm}'")

        try:
            self.language_mapper.validate_engine_language(self.ocr_engine, language)
        except ValueError as e:
            from dedoc.common.exceptions.dedoc_error import DedocError
            raise DedocError(msg=str(e), code=400) from e

        groups = self.language_mapper.group_languages(normalized_langs)

        if len(groups) <= 1:
            if groups:
                group_name = list(groups.keys())[0]
                all_paddle_langs = list(groups.values())[0]
            else:
                group_name = None
                all_paddle_langs = normalized_langs
            logger.info(
                f"[IMP:8][PaddleOCREngine][RECOGNIZE_PAGE] Single language group: {group_name} -> {all_paddle_langs}"
            )
            return self.single_pass_ocr(image, all_paddle_langs, lang_group=group_name)
        else:
            logger.info(
                f"[IMP:8][PaddleOCREngine][RECOGNIZE_PAGE] Multi-pass: {len(groups)} groups"
            )
            return self.multi_pass_ocr(image, groups)
    # endregion METHOD_recognize_page

    # region METHOD_single_pass_ocr [DOMAIN(9): OCR; CONCEPT(9): SinglePass; TECH(8): Python, PaddleX]
    ## @purpose To run a single OCR recognition pass on an image with a given set of PaddleOCR language codes and an optional model configuration. Creates a PaddleOCR instance for the specific det/rec models needed.
    ## @io np.ndarray, list[str], str, str, str -> OCRResult
    ## @complexity 7
    def single_pass_ocr(
        self,
        image: np.ndarray,
        paddle_langs: list[str],
        lang_group: Optional[str] = None,
        det_model: Optional[str] = None,
        rec_model: Optional[str] = None
    ) -> OCRResult:
        from dedoc.readers.pdf_reader.pdf_image_reader.ocr.paddleocr_model_config import PaddleOCRModelConfig

        lang = ",".join(paddle_langs)

        if det_model is None:
            det_model = PaddleOCRModelConfig.get_det_model(self.ocr_engine_version, self.ocr_model_size)
        if rec_model is None:
            group_key = lang_group if lang_group is not None else paddle_langs[0]
            rec_model = PaddleOCRModelConfig.get_rec_model(self.ocr_engine_version, self.ocr_model_size, group_key)

        # BUG_FIX_CONTEXT: PaddleX text detection resize() processor does h, w, c = image.shape
        # and crashes on grayscale (H, W) input. Convert to 3-channel BGR as defensive measure.
        if len(image.shape) == 2:
            logger.debug(f"[IMP:5][PaddleOCREngine][SINGLE_PASS] Converting grayscale image to 3-channel BGR")
            image = cv2.cvtColor(image, cv2.COLOR_GRAY2BGR)

        logger.info(
            f"[IMP:7][PaddleOCREngine][SINGLE_PASS] lang={lang}, det={det_model}, rec={rec_model}"
        )

        try:
            from paddleocr import PaddleOCR as PaddleXOCR
        except ImportError as e:
            logger.error(f"[IMP:10][PaddleOCREngine][SINGLE_PASS] PaddleOCR not available: {e}")
            raise

        ocr = PaddleXOCR(
            text_detection_model_name=det_model,
            text_recognition_model_name=rec_model,
            lang=lang,
            device=self.ocr_device,
            engine="paddle",
            precision=self.ocr_precision,
            use_tensorrt=self.ocr_use_tensorrt,
            cpu_threads=self.ocr_cpu_threads,
            use_doc_orientation_classify=False,
            use_doc_unwarping=False,
            use_textline_orientation=False,
        )

        import time
        t_start = time.time()
        raw_results = list(ocr.predict(image))
        elapsed = time.time() - t_start

        if not raw_results:
            logger.warning(f"[IMP:8][PaddleOCREngine][SINGLE_PASS] No results from PaddleOCR")
            return OCRResult(lines=[])

        raw = raw_results[0]
        if hasattr(raw, "json"):
            result_dict = raw.json
            # BUG_FIX_CONTEXT: PaddleX JsonMixin wraps result in {"res": {...}}.
            # Without unwrapping, dt_polys/rec_texts/rec_scores are hidden inside res key.
            if isinstance(result_dict, dict) and "res" in result_dict:
                result_dict = result_dict["res"]
        elif isinstance(raw, dict):
            result_dict = raw
        else:
            logger.warning(f"[IMP:8][PaddleOCREngine][SINGLE_PASS] Unexpected result type: {type(raw)}")
            return OCRResult(lines=[])

        ocr_result = self._paddle_result_to_ocr_result(result_dict)
        logger.info(
            f"[IMP:8][PaddleOCREngine][SINGLE_PASS] Completed in {elapsed:.2f}s, "
            f"{len(ocr_result.lines)} lines"
        )
        return ocr_result
    # endregion METHOD_single_pass_ocr

    # region METHOD_multi_pass_ocr [DOMAIN(9): OCR; CONCEPT(9): MultiPass; TECH(8): Python]
    ## @purpose To run multiple recognition passes (one per language group) with a shared detection model, then merge results via concatenation, Y-sorting, and overlap-based deduplication.
    ## @io np.ndarray, dict[str, list[str]] -> OCRResult
    ## @complexity 8
    def multi_pass_ocr(self, image: np.ndarray, groups: dict[str, list[str]]) -> OCRResult:
        from dedoc.readers.pdf_reader.pdf_image_reader.ocr.paddleocr_model_config import PaddleOCRModelConfig

        det_model = PaddleOCRModelConfig.get_det_model(self.ocr_engine_version, self.ocr_model_size)
        group_names = list(groups.keys())

        logger.info(
            f"[IMP:7][PaddleOCREngine][MULTI_PASS] {len(groups)} language groups: {group_names}. "
            f"Running {len(groups)} recognition passes."
        )

        all_results: list[OCRResult] = []
        import time

        for group_name, group_langs in groups.items():
            t_start = time.time()
            rec_model = PaddleOCRModelConfig.get_rec_model(
                self.ocr_engine_version, self.ocr_model_size, group_name
            )
            result = self.single_pass_ocr(
                image=image,
                paddle_langs=group_langs,
                lang_group=group_name,
                det_model=det_model,
                rec_model=rec_model,
            )
            elapsed = time.time() - t_start
            logger.info(
                f"[IMP:8][PaddleOCREngine][MULTI_PASS] Pass '{group_name}' "
                f"({group_langs}): {len(result.lines)} lines in {elapsed:.2f}s"
            )
            all_results.append(result)

        merged = self._merge_multi_pass_results(all_results)
        total_before = sum(len(r.lines) for r in all_results)
        logger.info(
            f"[IMP:9][PaddleOCREngine][MULTI_PASS] Merge: {total_before} -> {len(merged.lines)} lines"
        )
        return merged
    # endregion METHOD_multi_pass_ocr

    # region METHOD_recognize_cells [DOMAIN(9): OCR; CONCEPT(9): CellRecognition; TECH(8): Python, PaddleX]
    ## @purpose To recognize text in pre-cropped table cell images using the full PaddleOCR detection+recognition pipeline (PaddleOCR.predict()). Parses and normalizes the language, groups by rec-model, and delegates to single_pass_ocr() with the first language group's model. NOTE: The actual cell recognition fix for concatenated images is in OCRCellExtractor.__handle_one_batch_paddle() which bypasses this method for PaddleOCR and processes cells individually.
    ## @io np.ndarray, str, **kwargs -> OCRResult
    ## @complexity 5
    # BUG_FIX_CONTEXT: recognize_cells delegates to single_pass_ocr() which runs DBNet detection
    # + CRNN recognition on the concatenated cell image. DBNet is a scene-text detection model
    # that fails on the synthetic concatenated image (vertical stack of cell crops with 10px gaps),
    # returning zero detections → OCRResult(lines=[]) → all cells get empty text → tables filtered out.
    # The actual fix is in OCRCellExtractor.__handle_one_batch_paddle() which bypasses concatenation
    # for PaddleOCR and processes each cell individually via recognize_page() (DBNet on real cell crops).
    def recognize_cells(self, image: np.ndarray, language: str, **kwargs) -> OCRResult:
        logger.info(f"[IMP:7][PaddleOCREngine][RECOGNIZE_CELLS] language={language}")

        raw_langs = [l.strip() for l in language.split("+")]
        normalized_langs = [self.language_mapper.normalize_language(l) for l in raw_langs]
        logger.debug(f"[IMP:5][PaddleOCREngine][RECOGNIZE_CELLS] normalized_langs={normalized_langs}")

        groups = self.language_mapper.group_languages(normalized_langs)

        # BUG_FIX_CONTEXT: For multi-pass scenarios (v5 + mixed language groups), v1 uses only
        # the first language group's model for cell recognition. Mixed-language tables may have
        # reduced accuracy for non-primary languages. v2 will add multi-pass for cells.
        if groups:
            group_name = list(groups.keys())[0]
            paddle_langs = list(groups.values())[0]
            logger.info(
                f"[IMP:7][PaddleOCREngine][RECOGNIZE_CELLS] Using first language group: "
                f"group={group_name}, lang={paddle_langs}"
            )
        else:
            group_name = "en"
            paddle_langs = ["en"]
            logger.warning(
                f"[IMP:7][PaddleOCREngine][RECOGNIZE_CELLS] No language groups resolved, "
                f"falling back to en"
            )

        result = self.single_pass_ocr(
            image=image,
            paddle_langs=paddle_langs,
            lang_group=group_name,
        )

        logger.info(f"[IMP:8][PaddleOCREngine][RECOGNIZE_CELLS] Result: {len(result.lines)} lines")
        return result
    # endregion METHOD_recognize_cells

    # region FUNC__paddle_result_to_ocr_result [DOMAIN(3): OCR; CONCEPT(8): DataConversion; TECH(8): PaddleX]
    ## @purpose Convert PaddleX flat dict output (dt_polys, rec_texts, rec_score) to dedoc OCRResult with OCRLine/OCRWord.
    ## @io dict -> OCRResult
    ## @complexity 6
    def _paddle_result_to_ocr_result(self, paddle_result: dict) -> OCRResult:
        polygons = paddle_result.get("dt_polys", [])
        rec_texts = paddle_result.get("rec_texts", [])
        rec_scores = paddle_result.get("rec_scores", [])

        logger.debug(f"[IMP:4][PaddleOCREngine][CONVERT] Converting {len(polygons)} polygons, {len(rec_texts)} texts")

        lines = []
        for i, poly in enumerate(polygons):
            if i >= len(rec_texts):
                break
            text = rec_texts[i] if i < len(rec_texts) else ""
            score = float(rec_scores[i]) if i < len(rec_scores) else 0.0

            # BUG_FIX_CONTEXT: PaddleX dt_polys uses nested point format [[x1,y1],[x2,y2],...]
            # (each point is a 2-element list/array), NOT a flat list [x1,y1,x2,y2,...].
            # We flatten the polygon to extract xs and ys.
            if len(poly) >= 4:
                flat_points = []
                for pt in poly:
                    if hasattr(pt, '__iter__') and len(pt) >= 2:
                        flat_points.extend([float(pt[0]), float(pt[1])])
                    elif isinstance(pt, (int, float)):
                        flat_points.append(float(pt))
                    else:
                        try:
                            flat_points.extend([float(pt[0]), float(pt[1])])
                        except (TypeError, IndexError):
                            continue

                if len(flat_points) >= 4:
                    xs = [flat_points[j] for j in range(0, len(flat_points), 2)]
                    ys = [flat_points[j] for j in range(1, len(flat_points), 2)]
                    bbox = BBox(x_top_left=int(min(xs)), y_top_left=int(min(ys)),
                                width=int(max(xs) - min(xs)), height=int(max(ys) - min(ys)))
                else:
                    bbox = BBox(x_top_left=0, y_top_left=0, width=0, height=0)
            else:
                bbox = BBox(x_top_left=0, y_top_left=0, width=0, height=0)

            word = OCRWord(text=text, confidence=score, bbox=bbox)
            line = OCRLine(words=[word], bbox=bbox)
            lines.append(line)

        if lines:
            avg_confidence = sum(l.words[0].confidence for l in lines if l.words) / max(len(lines), 1)
            logger.info(f"[IMP:8][PaddleOCREngine][CONVERT] {len(lines)} lines, avg confidence={avg_confidence:.3f}")
        else:
            logger.warning(f"[IMP:8][PaddleOCREngine][CONVERT] No text detected in image")

        return OCRResult(lines=lines)
    # endregion FUNC__paddle_result_to_ocr_result

    # region METHOD__merge_multi_pass_results [DOMAIN(9): OCR; CONCEPT(9): Merge, Dedup; TECH(7): Python]
    ## @purpose To merge OCR results from multiple recognition passes by concatenating lines, sorting by Y coordinate, and removing near-duplicate lines with bounding box overlap > 50%.
    ## @io list[OCRResult] -> OCRResult
    ## @complexity 8
    def _merge_multi_pass_results(self, results: list[OCRResult]) -> OCRResult:
        all_lines: list[OCRLine] = []
        for r in results:
            all_lines.extend(r.lines)

        total_before = len(all_lines)

        all_lines.sort(key=lambda line: line.bbox.y_top_left)

        unique_lines: list[OCRLine] = []
        for line in all_lines:
            is_dup = False
            for j, kept in enumerate(unique_lines):
                intersection = _bbox_intersection_area(line.bbox, kept.bbox)
                area_line = float(line.bbox.width * line.bbox.height)
                area_kept = float(kept.bbox.width * kept.bbox.height)
                min_area = min(area_line, area_kept)
                if min_area <= 0:
                    continue
                overlap = intersection / min_area
                if overlap > 0.5:
                    is_dup = True
                    line_conf = (
                        sum(w.confidence for w in line.words) / max(len(line.words), 1)
                    )
                    kept_conf = (
                        sum(w.confidence for w in kept.words) / max(len(kept.words), 1)
                    )
                    if line_conf > kept_conf:
                        unique_lines[j] = line
                    break
            if not is_dup:
                unique_lines.append(line)

        n_removed = total_before - len(unique_lines)
        logger.info(
            f"[IMP:9][PaddleOCREngine][MERGE] Multi-pass merge: {total_before} -> "
            f"{len(unique_lines)} lines after dedup ({n_removed} duplicates removed)"
        )
        return OCRResult(lines=unique_lines)
    # endregion METHOD__merge_multi_pass_results

    # region METHOD_warmup [DOMAIN(8): OCR; CONCEPT(8): Preload; TECH(7): Python, PaddleX]
    ## @purpose To preload PaddleOCR models at service startup by running inference on a dummy 100x100 image, preventing the first real request from experiencing a long model-loading delay.
    ## @io dict -> None
    ## @complexity 4
    @classmethod
    def warmup(cls, config: dict) -> None:
        logger.info(f"[IMP:7][PaddleOCREngine][WARMUP] Starting PaddleOCR warmup")
        dummy_image = np.zeros((100, 100, 3), dtype=np.uint8)
        engine = cls(config=config)
        try:
            ocr = engine._get_ocr()
            list(ocr.predict(dummy_image))
            logger.info(f"[IMP:8][PaddleOCREngine][WARMUP] PaddleOCR warmup complete")
        except ImportError as e:
            logger.warning(
                f"[IMP:7][PaddleOCREngine][WARMUP] PaddleOCR not installed, "
                f"skipping warmup: {e}"
            )
        except Exception as e:
            logger.warning(
                f"[IMP:7][PaddleOCREngine][WARMUP] Warmup failed (non-fatal): {e}"
            )
    # endregion METHOD_warmup
# endregion CLASS_PaddleOCREngine
