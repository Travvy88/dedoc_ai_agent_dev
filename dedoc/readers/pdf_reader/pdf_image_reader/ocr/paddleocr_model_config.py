# region MODULE_CONTRACT [DOMAIN(8): OCR; CONCEPT(8): ModelConfiguration, PaddleOCR; TECH(5): Python]
## @modulecontract
## @purpose To provide deterministic model-name resolution for PaddleOCR detection and recognition models based on engine version (paddle_v5 / paddle_v6) and model size preset (medium / small / tiny / server / mobile). This module contains zero ML dependencies — it is a pure string-configuration layer.
## @scope Detection model selection, recognition model selection, v5 group-based rec model lookup.
## @input engine_version (str), model_size (str), lang_group (str for v5 rec).
## @output Model name strings for PaddleOCR/PaddleX API.
## @links [USES_API(0): Pure Python — no external deps.]
## @invariants
## - get_det_model ALWAYS returns a non-empty string.
## - get_rec_model ALWAYS returns a non-empty string.
## - Unknown engine_version raises ValueError.
## - Unknown model_size raises ValueError.
## @rationale
## Q: Why use a static class instead of a module-level function?
## A: Consistent namespace with PaddleOCRLanguageMapper; both are stateless configuration services used by PaddleOCREngine.
## @changes
## LAST_CHANGE: [v1.2.0 – Merged ocr_model into ocr_engine; renamed parameter to model_size; removed auto fallback.]
## @modulemap
## CLASS 10[Model name resolver for PaddleOCR detection and recognition] => PaddleOCRModelConfig
## @usecases
## - [get_det_model]: PaddleOCREngine → ResolveDetModelName → PaddleX API
## - [get_rec_model]: PaddleOCREngine → ResolveRecModelName → PaddleX API
def _module_contract():
    pass
# endregion MODULE_CONTRACT
# GREP_SUMMARY: PaddleOCR, model, config, detection, recognition, PP-OCRv5, PP-OCRv6, det, rec, model-name, engine-config
# STRUCTURE: ▶ get_det_model(engine_version, model_size) → ◇ v6: medium / small / tiny → ⊕ PP-OCRv6_*_det ┃ ◇ v5: server / mobile → ⊕ PP-OCRv5_*_det → ○ get_rec_model(engine_version, model_size, lang_group) → ◇ v6: medium / small / tiny → ⊕ PP-OCRv6_*_rec ┃ ◇ v5: lookup V5_GROUP_TO_REC_MODEL[lang_group] → ⊕ rec_model_name

import logging

logger = logging.getLogger(__name__)

# region CLASS_PaddleOCRModelConfig [DOMAIN(8): OCR; CONCEPT(8): ModelConfiguration; TECH(5): Python]
## @purpose To serve as the single point of model-name resolution for PaddleOCR engines, enabling PaddleOCREngine to select the correct detection and recognition models without hardcoding model names in the engine implementation.
## @uses PaddleOCRLanguageMapper (for V5_GROUP_TO_REC_MODEL reference via class attribute re-use concept).
## @complexity 4
class PaddleOCRModelConfig:

    # region CLASS_DATA: V5_GROUP_TO_REC_MODEL [DOMAIN(8): OCR; CONCEPT(7): ModelLookup]
    ## @purpose Mapping from language group name → PP-OCRv5 recognition model name. Kept as local copy so this module has zero dependencies (even on PaddleOCRLanguageMapper).
    V5_GROUP_TO_REC_MODEL: dict[str, str] = {
        "eslav": "eslav_PP-OCRv5_mobile_rec",
        "cyrillic": "cyrillic_PP-OCRv5_mobile_rec",
        "en": "en_PP-OCRv5_mobile_rec",
        "latin": "latin_PP-OCRv5_mobile_rec",
        "arabic": "arabic_PP-OCRv5_mobile_rec",
        "devanagari": "devanagari_PP-OCRv5_mobile_rec",
        "korean": "korean_PP-OCRv5_mobile_rec",
        "th": "th_PP-OCRv5_mobile_rec",
        "el": "el_PP-OCRv5_mobile_rec",
        "te": "te_PP-OCRv5_mobile_rec",
        "ta": "ta_PP-OCRv5_mobile_rec",
        "server_rec": "PP-OCRv5_server_rec",
    }
    # endregion CLASS_DATA: V5_GROUP_TO_REC_MODEL

    # region METHOD_get_det_model [DOMAIN(8): OCR; CONCEPT(8): DetectionModelSelection; TECH(4): branching]
    ## @purpose To resolve the detection model name based on engine version and model size preset.
    ## @io str, str -> str
    ## @complexity 3
    @staticmethod
    def get_det_model(engine_version: str, model_size: str) -> str:
        # LDD-log: resolve detection model name
        if engine_version == "paddle_v6":
            if model_size == "medium":
                model = "PP-OCRv6_medium_det"
            elif model_size == "small":
                model = "PP-OCRv6_small_det"
            elif model_size == "tiny":
                model = "PP-OCRv6_tiny_det"
            else:
                logger.error(f"[IMP:9][get_det_model][UNKNOWN] Unknown model_size '{model_size}' for engine_version '{engine_version}'.")
                raise ValueError(f"Unknown model_size '{model_size}' for engine_version '{engine_version}'. Supported: medium, small, tiny.")
            logger.info(f"[IMP:7][get_det_model][RESOLVE] {engine_version} + {model_size} -> '{model}'")
            return model
        elif engine_version == "paddle_v5":
            if model_size == "server":
                model = "PP-OCRv5_server_det"
            elif model_size == "mobile":
                model = "PP-OCRv5_mobile_det"
            else:
                logger.error(f"[IMP:9][get_det_model][UNKNOWN] Unknown model_size '{model_size}' for engine_version '{engine_version}'.")
                raise ValueError(f"Unknown model_size '{model_size}' for engine_version '{engine_version}'. Supported: server, mobile.")
            logger.info(f"[IMP:7][get_det_model][RESOLVE] {engine_version} + {model_size} -> '{model}'")
            return model
        else:
            logger.error(f"[IMP:9][get_det_model][UNKNOWN_ENGINE] Unknown engine_version '{engine_version}'.")
            raise ValueError(f"Unknown engine_version '{engine_version}'. Supported: paddle_v5, paddle_v6.")
    # endregion METHOD_get_det_model

    # region METHOD_get_rec_model [DOMAIN(8): OCR; CONCEPT(8): RecognitionModelSelection; TECH(4): branching + lookup]
    ## @purpose To resolve the recognition model name based on engine version, model size preset, and language group (for v5).
    ## @io str, str, str -> str
    ## @complexity 3
    @staticmethod
    def get_rec_model(engine_version: str, model_size: str, lang_group: str) -> str:
        # LDD-log: resolve recognition model name
        if engine_version == "paddle_v6":
            if model_size == "medium":
                model = "PP-OCRv6_medium_rec"
            elif model_size == "small":
                model = "PP-OCRv6_small_rec"
            elif model_size == "tiny":
                model = "PP-OCRv6_tiny_rec"
            else:
                logger.error(f"[IMP:9][get_rec_model][UNKNOWN] Unknown model_size '{model_size}' for engine_version '{engine_version}'.")
                raise ValueError(f"Unknown model_size '{model_size}' for engine_version '{engine_version}'. Supported: medium, small, tiny.")
            logger.info(f"[IMP:7][get_rec_model][RESOLVE] {engine_version} + {model_size} -> '{model}'")
            return model
        elif engine_version == "paddle_v5":
            model = PaddleOCRModelConfig.V5_GROUP_TO_REC_MODEL.get(lang_group)
            if model is None:
                logger.error(f"[IMP:9][get_rec_model][UNKNOWN_GROUP] Unknown lang_group '{lang_group}' for v5 rec model lookup.")
                raise ValueError(f"Unknown lang_group '{lang_group}'. Supported: {', '.join(sorted(PaddleOCRModelConfig.V5_GROUP_TO_REC_MODEL.keys()))}.")
            logger.info(f"[IMP:7][get_rec_model][RESOLVE] {engine_version} + lang_group='{lang_group}' -> '{model}'")
            return model
        else:
            logger.error(f"[IMP:9][get_rec_model][UNKNOWN_ENGINE] Unknown engine_version '{engine_version}'.")
            raise ValueError(f"Unknown engine_version '{engine_version}'. Supported: paddle_v5, paddle_v6.")
    # endregion METHOD_get_rec_model
# endregion CLASS_PaddleOCRModelConfig
