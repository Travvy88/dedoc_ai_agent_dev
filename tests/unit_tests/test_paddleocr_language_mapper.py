# region MODULE_CONTRACT [DOMAIN(9): Testing; CONCEPT(8): LanguageMapper, PaddleOCR; TECH(8): unittest]
## @modulecontract
## @purpose To verify PaddleOCRLanguageMapper correctness: Tesseract↔Paddle mapping, dual-format normalization, v6 capability check, engine-language validation, and v5 language grouping. All tests are pure logic (no ML dependencies).
## @scope Unit tests for PaddleOCRLanguageMapper static methods.
## @input None.
## @output Test pass/fail with LDD telemetry output.
## @links [USES_API(0): unittest, PaddleOCRLanguageMapper]
## @invariants
## - All tests pass without network access or ML model loading.
## - Every assertion is preceded by an [IMP:9] log line for agent traceability.
## @changes
## LAST_CHANGE: [v1.0.0 – Initial creation: full mapper test suite with LDD telemetry.]
## @modulemap
## CLASS 10[Comprehensive test suite for PaddleOCRLanguageMapper] => TestPaddleOCRLanguageMapper
## @usecases
## - [test_map_all_tesseract_codes]: Verify 31 Tesseract→Paddle mappings
## - [test_validate_engine_language_v6_fail]: Verify v6+rus raises ValueError
def _module_contract():
    pass
# endregion MODULE_CONTRACT
# GREP_SUMMARY: test, PaddleOCR, language mapper, unittest, Tesseract, v5, v6, normalization, validation, grouping, LDD
# STRUCTURE: ▶ setUp → ○ 12 test methods ∋ ◇ map/normalize/validate/group → ⚡ LDD [IMP:9] log → ✔ assertX → ∑ all pass

import io
import logging
import unittest

from dedoc.readers.pdf_reader.pdf_image_reader.ocr.paddleocr_language_mapper import PaddleOCRLanguageMapper

logger = logging.getLogger(__name__)

# region CLASS_TestPaddleOCRLanguageMapper [DOMAIN(9): Testing; CONCEPT(8): LanguageMapper; TECH(8): unittest]
## @purpose To validate every aspect of PaddleOCRLanguageMapper: mapping, dual-format normalization, v6 membership, engine-language validation, and v5 grouping.
## @uses unittest.TestCase, PaddleOCRLanguageMapper
## @complexity 6
class TestPaddleOCRLanguageMapper(unittest.TestCase):

    # region METHOD_setUp [DOMAIN(6): Testing; CONCEPT(5): FixtureSetup; TECH(4): Python]
    ## @purpose Configure logging stream handler for LDD telemetry capture.
    ## @complexity 2
    def setUp(self):
        self.log_stream = io.StringIO()
        self.handler = logging.StreamHandler(self.log_stream)
        self.handler.setLevel(logging.DEBUG)
        logging.getLogger().addHandler(self.handler)
        logging.getLogger().setLevel(logging.DEBUG)
    # endregion METHOD_setUp

    # region METHOD_tearDown [DOMAIN(6): Testing; CONCEPT(5): FixtureTearDown; TECH(4): Python]
    ## @purpose Remove logging handler to prevent duplicate output across tests.
    ## @complexity 1
    def tearDown(self):
        logging.getLogger().removeHandler(self.handler)
        self.handler.close()
    # endregion METHOD_tearDown

    # region METHOD_test_map_all_tesseract_codes [DOMAIN(9): Testing; CONCEPT(9): MappingVerification; TECH(6): unittest]
    ## @purpose Verify that all 31 Tesseract→PaddleOCR code pairs map correctly.
    ## @complexity 3
    def test_map_all_tesseract_codes(self):
        tesseract_to_expected = {
            "rus": "ru", "eng": "en", "deu": "de", "fra": "fr",
            "spa": "es", "ita": "it", "por": "pt", "pol": "pl",
            "nld": "nl", "swe": "sv", "dan": "da", "nor": "no",
            "fin": "fi", "ces": "cs", "hun": "hu", "ron": "ro",
            "tur": "tr", "vie": "vi", "ind": "id", "msa": "ms",
            "bel": "be", "ukr": "uk", "bul": "bg", "kaz": "kk",
            "ara": "ar", "hin": "hi", "kor": "ko", "tha": "th",
            "ell": "el", "jpn": "japan", "chi_sim": "ch",
            "chi_tra": "chinese_cht",
        }
        for tesseract_code, expected_paddle in tesseract_to_expected.items():
            result = PaddleOCRLanguageMapper.map_tesseract_to_paddle(tesseract_code)
            print(f"[IMP:9][test_map_all_tesseract_codes] '{tesseract_code}' -> '{result}' (expected '{expected_paddle}')")
            self.assertEqual(result, expected_paddle)

        self.assertEqual(len(tesseract_to_expected), 32)

        self.handler.flush()
        log_output = self.log_stream.getvalue()
        imp9_count = sum(1 for line in log_output.splitlines() if "[IMP:9]" in line)
        print(f"[IMP:9][test_map_all_tesseract_codes] Total [IMP:9] log lines: {imp9_count}")
    # endregion METHOD_test_map_all_tesseract_codes

    # region METHOD_test_normalize_tesseract_format [DOMAIN(8): Testing; CONCEPT(7): Normalization; TECH(5): unittest]
    ## @purpose Verify that Tesseract-format codes are normalized to PaddleOCR short format.
    ## @complexity 2
    def test_normalize_tesseract_format(self):
        pairs = [("rus", "ru"), ("eng", "en"), ("deu", "de")]
        for tesseract_code, expected in pairs:
            result = PaddleOCRLanguageMapper.normalize_language(tesseract_code)
            print(f"[IMP:9][test_normalize_tesseract_format] normalize('{tesseract_code}') = '{result}' (expected '{expected}')")
            self.assertEqual(result, expected)
    # endregion METHOD_test_normalize_tesseract_format

    # region METHOD_test_normalize_short_format [DOMAIN(8): Testing; CONCEPT(7): Normalization; TECH(5): unittest]
    ## @purpose Verify that already-short PaddleOCR codes pass through unchanged.
    ## @complexity 1
    def test_normalize_short_format(self):
        codes = ["ru", "en", "de"]
        for code in codes:
            result = PaddleOCRLanguageMapper.normalize_language(code)
            print(f"[IMP:9][test_normalize_short_format] normalize('{code}') = '{result}' (expected unchanged)")
            self.assertEqual(result, code)
    # endregion METHOD_test_normalize_short_format

    # region METHOD_test_is_v6_language_true [DOMAIN(8): Testing; CONCEPT(7): V6Capability; TECH(4): unittest]
    ## @purpose Verify that known v6 languages return True.
    ## @complexity 2
    def test_is_v6_language_true(self):
        v6_codes = ["en", "de", "fr", "ch", "japan", "chinese_cht",
                     "es", "it", "pt", "pl", "nl", "sv", "da", "no",
                     "fi", "cs", "hu", "ro", "tr", "vi", "id", "ms"]
        for code in v6_codes:
            result = PaddleOCRLanguageMapper.is_v6_language(code)
            print(f"[IMP:9][test_is_v6_language_true] is_v6('{code}') = {result} (expected True)")
            self.assertTrue(result)
    # endregion METHOD_test_is_v6_language_true

    # region METHOD_test_is_v6_language_false [DOMAIN(8): Testing; CONCEPT(7): V6Capability; TECH(4): unittest]
    ## @purpose Verify that non-v6 languages return False.
    ## @complexity 1
    def test_is_v6_language_false(self):
        non_v6_codes = ["ru", "ar", "hi", "ko", "th", "el", "be", "uk", "bg", "kk"]
        for code in non_v6_codes:
            result = PaddleOCRLanguageMapper.is_v6_language(code)
            print(f"[IMP:9][test_is_v6_language_false] is_v6('{code}') = {result} (expected False)")
            self.assertFalse(result)
    # endregion METHOD_test_is_v6_language_false

    # region METHOD_test_validate_engine_language_v6_ok [DOMAIN(9): Testing; CONCEPT(8): Validation; TECH(5): unittest]
    ## @purpose Verify that v6 + supported language passes without exception.
    ## @complexity 2
    def test_validate_engine_language_v6_ok(self):
        try:
            PaddleOCRLanguageMapper.validate_engine_language("paddle_v6", "eng")
            print("[IMP:9][test_validate_engine_language_v6_ok] paddle_v6 + eng = OK (no exception)")
        except ValueError as e:
            self.fail(f"validate_engine_language raised ValueError unexpectedly: {e}")
    # endregion METHOD_test_validate_engine_language_v6_ok

    # region METHOD_test_validate_engine_language_v6_fail [DOMAIN(9): Testing; CONCEPT(8): Validation; TECH(5): unittest]
    ## @purpose Verify that v6 + unsupported language (Cyrillic) raises ValueError with informative message.
    ## @complexity 2
    def test_validate_engine_language_v6_fail(self):
        with self.assertRaises(ValueError) as ctx:
            PaddleOCRLanguageMapper.validate_engine_language("paddle_v6", "rus")
        print(f"[IMP:9][test_validate_engine_language_v6_fail] paddle_v6 + rus -> ValueError: '{str(ctx.exception)}'")
        self.assertIn("not supported by PP-OCRv6", str(ctx.exception))
        self.assertIn("paddle_v5", str(ctx.exception))
    # endregion METHOD_test_validate_engine_language_v6_fail

    # region METHOD_test_validate_engine_language_v5_all [DOMAIN(8): Testing; CONCEPT(7): Validation; TECH(4): unittest]
    ## @purpose Verify that v5 accepts all languages (including Cyrillic, Arabic, Hindi).
    ## @complexity 2
    def test_validate_engine_language_v5_all(self):
        for lang in ["rus", "ara", "hin"]:
            try:
                PaddleOCRLanguageMapper.validate_engine_language("paddle_v5", lang)
                print(f"[IMP:9][test_validate_engine_language_v5_all] paddle_v5 + {lang} = OK")
            except ValueError as e:
                self.fail(f"paddle_v5 + {lang} raised ValueError: {e}")
    # endregion METHOD_test_validate_engine_language_v5_all

    # region METHOD_test_group_languages_single_group [DOMAIN(8): Testing; CONCEPT(7): Grouping; TECH(4): unittest]
    ## @purpose Verify that a single language returns exactly one group.
    ## @complexity 1
    def test_group_languages_single_group(self):
        result = PaddleOCRLanguageMapper.group_languages(["en"])
        expected = {"en": ["en"]}
        print(f"[IMP:9][test_group_languages_single_group] group(['en']) = {result} (expected {expected})")
        self.assertEqual(result, expected)
    # endregion METHOD_test_group_languages_single_group

    # region METHOD_test_group_languages_multi_group [DOMAIN(8): Testing; CONCEPT(8): Grouping; TECH(5): unittest]
    ## @purpose Verify that two languages from different groups produce two separate groups.
    ## @complexity 2
    def test_group_languages_multi_group(self):
        result = PaddleOCRLanguageMapper.group_languages(["ru", "en"])
        expected = {"eslav": ["ru"], "en": ["en"]}
        print(f"[IMP:9][test_group_languages_multi_group] group(['ru', 'en']) = {result} (expected {expected})")
        self.assertEqual(result, expected)
        self.assertIn("ru", result["eslav"])
        self.assertIn("en", result["en"])
    # endregion METHOD_test_group_languages_multi_group

    # region METHOD_test_group_languages_same_group [DOMAIN(8): Testing; CONCEPT(7): Grouping; TECH(4): unittest]
    ## @purpose Verify that two languages from the same group are merged into one group.
    ## @complexity 1
    def test_group_languages_same_group(self):
        result = PaddleOCRLanguageMapper.group_languages(["de", "fr"])
        expected = {"latin": ["de", "fr"]}
        print(f"[IMP:9][test_group_languages_same_group] group(['de', 'fr']) = {result} (expected {expected})")
        self.assertEqual(result, expected)
    # endregion METHOD_test_group_languages_same_group

    # region METHOD_test_group_languages_three_groups [DOMAIN(8): Testing; CONCEPT(8): Grouping; TECH(5): unittest]
    ## @purpose Verify that three languages from three different groups produce three groups.
    ## @complexity 2
    def test_group_languages_three_groups(self):
        result = PaddleOCRLanguageMapper.group_languages(["ru", "en", "japan"])
        expected = {"eslav": ["ru"], "en": ["en"], "server_rec": ["japan"]}
        print(f"[IMP:9][test_group_languages_three_groups] group(['ru', 'en', 'japan']) = {result} (expected {expected})")
        self.assertEqual(result, expected)
        self.assertIn("ru", result["eslav"])
        self.assertIn("en", result["en"])
        self.assertIn("japan", result["server_rec"])
    # endregion METHOD_test_group_languages_three_groups
# endregion CLASS_TestPaddleOCRLanguageMapper
