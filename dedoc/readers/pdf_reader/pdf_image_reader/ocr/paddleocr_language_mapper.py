# region MODULE_CONTRACT [DOMAIN(9): OCR; CONCEPT(9): LanguageMapping, PaddleOCR; TECH(7): Python]
## @modulecontract
## @purpose To provide a stateless bidirectional language-code mapping service between Tesseract and PaddleOCR notation, validate engine-language compatibility, and group languages by PP-OCRv5 recognition model groups. This module contains zero ML dependencies — it is a pure data-mapping layer.
## @scope Tesseract→PaddleOCR code mapping, dual-notation normalization, v6 language capability check, engine-language validation, v5 language grouping.
## @input Tesseract language codes (e.g. "rus", "eng") or PaddleOCR short codes (e.g. "ru", "en").
## @output Mapped PaddleOCR codes, validation errors, grouped language dicts.
## @links [USES_API(0): Pure Python — no external deps.]
## @invariants
## - TESSERACT_TO_PADDLE and SHORT_TO_TESSERACT are ALWAYS strict inverses (bijection) for all defined entries.
## - V6_LANGUAGES contains exactly 50 entries.
## - LANGUAGE_TO_V5_GROUP maps every short paddle code to exactly one group.
## - All static methods are pure functions (no side effects).
## @rationale
## Q: Why use a static class instead of a module-level dict?
## A: A class groups all mapping concerns (data + validation + grouping) under a single namespace, improving grep-ability and import ergonomics for agent navigation.
## @changes
## LAST_CHANGE: [v1.0.0 – Initial creation: bidirectional mapper, v6 validation, v5 grouping.]
## @modulemap
## CLASS 10[Bidirectional Tesseract↔PaddleOCR language mapper with validation and grouping] => PaddleOCRLanguageMapper
## @usecases
## - [map_tesseract_to_paddle]: PaddleOCREngine → ConvertLanguageCode → PaddleOCRFormat
## - [normalize_language]: PaddleOCREngine → NormalizeAnyFormat → CanonicalShortCode
## - [validate_engine_language]: PaddleOCREngine → ValidateCompatibility → ErrorOrOk
## - [group_languages]: PaddleOCREngine → GroupByRecModel → MultiPassGroups
def _module_contract():
    pass
# endregion MODULE_CONTRACT
# GREP_SUMMARY: PaddleOCR, language, mapper, Tesseract, OCR, v5, v6, eslav, cyrillic, latin, grouping, validation, bilingual, dual-notation, language-code
# STRUCTURE: ▶ Static Data ┌TESSERACT_TO_PADDLE + SHORT_TO_TESSERACT (31 pairs)┐ + ┌V6_LANGUAGES (50)┐ + ┌V5_GROUP_TO_REC_MODEL (12)┐ + ┌LANGUAGE_TO_V5_GROUP (32)┐ → ○ map_tesseract_to_paddle(tesseract_lang) → ⊕ paddle_code → ○ normalize_language(lang_code) → ⊕ canonical_short → ○ is_v6_language(paddle_lang) → ◇ ∈ V6_LANGUAGES ? ⊕ True┃False → ○ validate_engine_language(engine, tesseract_langs) → ◇ v6 + ∉V6 → ⚡ ValueError → ○ group_languages(paddle_langs) → ⊕ dict[group → [langs]]

import logging

logger = logging.getLogger(__name__)

# region CLASS_PaddleOCRLanguageMapper [DOMAIN(9): OCR; CONCEPT(9): LanguageMapping; TECH(7): Python]
## @purpose To serve as the single source of truth for language-code translation between Tesseract and PaddleOCR ecosystems, enabling the PaddleOCREngine to accept Tesseract-format language parameters from the existing dedoc API and transparently convert them.
## @uses Pure Python data structures (dict, set).
## @complexity 7
class PaddleOCRLanguageMapper:

    # region CLASS_DATA: TESSERACT_TO_PADDLE [DOMAIN(9): OCR; CONCEPT(8): DataMapping]
    ## @purpose Bijective map: Tesseract 4-letter codes → PaddleOCR short codes (31 pairs).
    TESSERACT_TO_PADDLE: dict[str, str] = {
        "rus": "ru",
        "eng": "en",
        "deu": "de",
        "fra": "fr",
        "spa": "es",
        "ita": "it",
        "por": "pt",
        "pol": "pl",
        "nld": "nl",
        "swe": "sv",
        "dan": "da",
        "nor": "no",
        "fin": "fi",
        "ces": "cs",
        "hun": "hu",
        "ron": "ro",
        "tur": "tr",
        "vie": "vi",
        "ind": "id",
        "msa": "ms",
        "bel": "be",
        "ukr": "uk",
        "bul": "bg",
        "kaz": "kk",
        "ara": "ar",
        "hin": "hi",
        "kor": "ko",
        "tha": "th",
        "ell": "el",
        "jpn": "japan",
        "chi_sim": "ch",
        "chi_tra": "chinese_cht",
    }
    # endregion CLASS_DATA: TESSERACT_TO_PADDLE

    # region CLASS_DATA: SHORT_TO_TESSERACT [DOMAIN(9): OCR; CONCEPT(8): InverseMapping]
    ## @purpose Inverse of TESSERACT_TO_PADDLE — enables bidirectional lookup for normalization.
    SHORT_TO_TESSERACT: dict[str, str] = {v: k for k, v in TESSERACT_TO_PADDLE.items()}
    # endregion CLASS_DATA: SHORT_TO_TESSERACT

    # region CLASS_DATA: V6_LANGUAGES [DOMAIN(9): OCR; CONCEPT(8): CapabilitySet]
    ## @purpose Set of 50 languages natively supported by PP-OCRv6 (no Cyrillic, Arabic, etc.).
    V6_LANGUAGES: set[str] = {
        "ch", "chinese_cht", "en", "japan",
        "af", "az", "bs", "ca", "cs", "cy", "da", "de", "es", "et",
        "eu", "fi", "fr", "ga", "gl", "hr", "hu", "id", "is", "it",
        "ku", "la", "lb", "lt", "lv", "mi", "ms", "mt", "nl", "no",
        "oc", "pl", "pt", "qu", "rm", "ro", "rs_latin", "sk", "sl",
        "sq", "sv", "sw", "tl", "tr", "uz", "vi",
    }
    # endregion CLASS_DATA: V6_LANGUAGES

    # region CLASS_DATA: V5_GROUP_TO_REC_MODEL [DOMAIN(8): OCR; CONCEPT(8): ModelSelection]
    ## @purpose Mapping from language group name → PP-OCRv5 recognition model name.
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

    # region CLASS_DATA: LANGUAGE_TO_V5_GROUP [DOMAIN(8): OCR; CONCEPT(8): LanguageGrouping]
    ## @purpose Mapping from PaddleOCR short code → v5 language group name.
    LANGUAGE_TO_V5_GROUP: dict[str, str] = {
        "ru": "eslav",
        "be": "eslav",
        "uk": "eslav",
        "bg": "cyrillic",
        "mn": "cyrillic",
        "kk": "cyrillic",
        "en": "en",
        "de": "latin",
        "fr": "latin",
        "es": "latin",
        "it": "latin",
        "pt": "latin",
        "pl": "latin",
        "nl": "latin",
        "sv": "latin",
        "da": "latin",
        "no": "latin",
        "fi": "latin",
        "cs": "latin",
        "hu": "latin",
        "ro": "latin",
        "tr": "latin",
        "vi": "latin",
        "id": "latin",
        "ms": "latin",
        "ar": "arabic",
        "fa": "arabic",
        "hi": "devanagari",
        "ko": "korean",
        "korean": "korean",
        "th": "th",
        "el": "el",
        "te": "te",
        "ta": "ta",
        "ch": "server_rec",
        "chinese_cht": "server_rec",
        "japan": "server_rec",
    }
    # endregion CLASS_DATA: LANGUAGE_TO_V5_GROUP

    # region METHOD_map_tesseract_to_paddle [DOMAIN(9): OCR; CONCEPT(9): CodeConversion; TECH(5): dict-lookup]
    ## @purpose To convert a Tesseract 4-letter language code (e.g. "rus") into PaddleOCR short code (e.g. "ru"), raising ValueError if unknown.
    ## @io str -> str
    ## @complexity 2
    @staticmethod
    def map_tesseract_to_paddle(tesseract_lang: str) -> str:
        # LDD-log: attempt Tesseract→Paddle lookup
        result = PaddleOCRLanguageMapper.TESSERACT_TO_PADDLE.get(tesseract_lang)
        if result is None:
            logger.error(f"[IMP:9][map_tesseract_to_paddle][UNKNOWN] Tesseract code '{tesseract_lang}' not found in mapping table.")
            raise ValueError(f"Unknown Tesseract language code: '{tesseract_lang}'. Supported codes: {', '.join(sorted(PaddleOCRLanguageMapper.TESSERACT_TO_PADDLE.keys()))}")
        logger.debug(f"[IMP:4][map_tesseract_to_paddle][MAP] '{tesseract_lang}' -> '{result}'")
        return result
    # endregion METHOD_map_tesseract_to_paddle

    # region METHOD_normalize_language [DOMAIN(9): OCR; CONCEPT(8): Normalization; TECH(5): dual-lookup]
    ## @purpose To accept any language format (Tesseract "rus" or short "ru") and return the canonical PaddleOCR short code. Enables backward compatibility with existing Tesseract-format API parameters.
    ## @io str -> str
    ## @complexity 3
    @staticmethod
    def normalize_language(lang_code: str) -> str:
        # LDD-log: normalize any format to PaddleOCR short code
        # If the code is already a known short paddle code (2-9 chars in SHORT_TO_TESSERACT keys), return it directly.
        if lang_code in PaddleOCRLanguageMapper.SHORT_TO_TESSERACT:
            logger.debug(f"[IMP:4][normalize_language][SHORT] '{lang_code}' is already a short paddle code.")
            return lang_code
        # If it is a Tesseract code, map it.
        if lang_code in PaddleOCRLanguageMapper.TESSERACT_TO_PADDLE:
            result = PaddleOCRLanguageMapper.TESSERACT_TO_PADDLE[lang_code]
            logger.debug(f"[IMP:4][normalize_language][TESS] '{lang_code}' -> paddle '{result}'")
            return result
        # If neither, raise error
        logger.error(f"[IMP:9][normalize_language][UNKNOWN] Language code '{lang_code}' is neither a known Tesseract code nor a short paddle code.")
        raise ValueError(f"Unknown language code: '{lang_code}'. Provide a Tesseract code (e.g. 'rus', 'eng') or a short code (e.g. 'ru', 'en').")
    # endregion METHOD_normalize_language

    # region METHOD_is_v6_language [DOMAIN(8): OCR; CONCEPT(7): CapabilityCheck; TECH(3): set-membership]
    ## @purpose To determine whether a given PaddleOCR short language code is natively supported by PP-OCRv6 (one of the 50 v6 languages).
    ## @io str -> bool
    ## @complexity 1
    @staticmethod
    def is_v6_language(paddle_lang: str) -> bool:
        # LDD-log: check v6 membership
        result = paddle_lang in PaddleOCRLanguageMapper.V6_LANGUAGES
        logger.debug(f"[IMP:4][is_v6_language][CHECK] '{paddle_lang}' in V6_LANGUAGES = {result}")
        return result
    # endregion METHOD_is_v6_language

    # region METHOD_validate_engine_language [DOMAIN(9): OCR; CONCEPT(9): Validation; TECH(6): engine-compatibility]
    ## @purpose To validate that the given Tesseract language string (possibly joined with "+") is compatible with the chosen OCR engine version. For "paddle_v6", raises ValueError if any language is not in the 50-language V6 set.
    ## @io str, str -> None
    ## @complexity 4
    @staticmethod
    def validate_engine_language(engine: str, tesseract_langs: str) -> None:
        # LDD-log: engine-language validation
        if not engine.startswith("paddle_"):
            logger.debug(f"[IMP:4][validate_engine_language][SKIP] Engine '{engine}' is not a paddle engine, no validation needed.")
            return

        engine_version = engine.split("_")[1]  # "v5" or "v6"
        if engine_version != "v6":
            logger.debug(f"[IMP:4][validate_engine_language][SKIP] Engine '{engine}' version is not v6, no validation needed.")
            return

        # Split multi-language string on "+"
        raw_langs = [l.strip() for l in tesseract_langs.split("+")]
        unsupported = []
        for raw_lang in raw_langs:
            paddle_lang = PaddleOCRLanguageMapper.normalize_language(raw_lang)
            if not PaddleOCRLanguageMapper.is_v6_language(paddle_lang):
                unsupported.append(paddle_lang)

        if unsupported:
            msg = (
                f"Language(s) {unsupported} are not supported by PP-OCRv6. "
                f"PP-OCRv6 supports only {sorted(PaddleOCRLanguageMapper.V6_LANGUAGES)}. "
                f"Use 'paddle_v5' for Cyrillic, Arabic, Hindi, Korean, Thai, Greek, Telugu, Tamil, or CJK scripts."
            )
            logger.error(f"[IMP:10][validate_engine_language][FAIL] {msg}")
            raise ValueError(msg)

        logger.info(f"[IMP:8][validate_engine_language][OK] All languages '{tesseract_langs}' are valid for {engine}.")
    # endregion METHOD_validate_engine_language

    # region METHOD_group_languages [DOMAIN(8): OCR; CONCEPT(8): LanguageGrouping; TECH(5): dict-grouping]
    ## @purpose To group a list of PaddleOCR short language codes by their PP-OCRv5 recognition model group. Each group key maps to the list of languages in that group. Used by multi-pass OCR to run one recognition pass per group.
    ## @io list[str] -> dict[str, list[str]]
    ## @complexity 4
    @staticmethod
    def group_languages(paddle_langs: list[str]) -> dict[str, list[str]]:
        # LDD-log: group languages by v5 rec model group
        groups: dict[str, list[str]] = {}
        for lang in paddle_langs:
            group = PaddleOCRLanguageMapper.LANGUAGE_TO_V5_GROUP.get(lang)
            if group is None:
                logger.warning(f"[IMP:7][group_languages][UNKNOWN_GROUP] Language '{lang}' has no v5 group mapping, skipping.")
                continue
            if group not in groups:
                groups[group] = []
            groups[group].append(lang)
            logger.debug(f"[IMP:5][group_languages][ASSIGN] '{lang}' -> group '{group}'")

        logger.info(f"[IMP:8][group_languages][RESULT] {len(groups)} groups: { {k: v for k, v in groups.items()} }")
        return groups
    # endregion METHOD_group_languages
# endregion CLASS_PaddleOCRLanguageMapper
