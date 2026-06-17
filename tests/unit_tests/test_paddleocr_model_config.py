# region MODULE_CONTRACT [DOMAIN(9): Testing; CONCEPT(8): ModelConfig, PaddleOCR; TECH(8): unittest]
## @modulecontract
## @purpose To verify PaddleOCRModelConfig correctness: detection and recognition model name resolution for both PP-OCRv5 and PP-OCRv6 across all supported OCR model presets. All tests are pure logic (no ML dependencies).
## @scope Unit tests for PaddleOCRModelConfig static methods.
## @input None.
## @output Test pass/fail with LDD telemetry output.
## @links [USES_API(0): unittest, PaddleOCRModelConfig]
## @invariants
## - All tests pass without network access or ML model loading.
## - Every assertion is preceded by an [IMP:9] log line for agent traceability.
## @changes
## LAST_CHANGE: [v1.0.0 – Initial creation: model config test suite with LDD telemetry.]
## @modulemap
## CLASS 10[Comprehensive test suite for PaddleOCRModelConfig] => TestPaddleOCRModelConfig
## @usecases
## - [test_v6_auto_det]: Verify v6+auto→medium_det
## - [test_v5_rec_eslav]: Verify v5+eslav→eslav_PP-OCRv5_mobile_rec
def _module_contract():
    pass
# endregion MODULE_CONTRACT
# GREP_SUMMARY: test, PaddleOCR, model config, unittest, detection, recognition, PP-OCRv5, PP-OCRv6, det, rec, LDD
# STRUCTURE: ▶ setUp → ○ 9 test methods ∋ ◇ get_det_model / get_rec_model → ⚡ LDD [IMP:9] log → ✔ assertEqual → ∑ all pass

import io
import logging
import unittest

from dedoc.readers.pdf_reader.pdf_image_reader.ocr.paddleocr_model_config import PaddleOCRModelConfig

logger = logging.getLogger(__name__)

# region CLASS_TestPaddleOCRModelConfig [DOMAIN(9): Testing; CONCEPT(8): ModelConfig; TECH(8): unittest]
## @purpose To validate every aspect of PaddleOCRModelConfig: detection and recognition model resolution for both v5 and v6 engines across all presets.
## @uses unittest.TestCase, PaddleOCRModelConfig
## @complexity 5
class TestPaddleOCRModelConfig(unittest.TestCase):

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

    # region METHOD_test_v6_medium_det_legacy [DOMAIN(8): Testing; CONCEPT(7): DetectionModel; TECH(4): unittest]
    ## @purpose Verify that v6+medium resolves to PP-OCRv6_medium_det (was auto, now explicit).
    ## @complexity 1
    def test_v6_medium_det_legacy(self):
        result = PaddleOCRModelConfig.get_det_model("paddle_v6", "medium")
        print(f"[IMP:9][test_v6_medium_det_legacy] get_det_model(v6, medium) = '{result}' (expected 'PP-OCRv6_medium_det')")
        self.assertEqual(result, "PP-OCRv6_medium_det")
    # endregion METHOD_test_v6_medium_det_legacy

    # region METHOD_test_v6_small_det [DOMAIN(8): Testing; CONCEPT(7): DetectionModel; TECH(4): unittest]
    ## @purpose Verify that v6+small resolves to PP-OCRv6_small_det.
    ## @complexity 1
    def test_v6_small_det(self):
        result = PaddleOCRModelConfig.get_det_model("paddle_v6", "small")
        print(f"[IMP:9][test_v6_small_det] get_det_model(v6, small) = '{result}' (expected 'PP-OCRv6_small_det')")
        self.assertEqual(result, "PP-OCRv6_small_det")
    # endregion METHOD_test_v6_small_det

    # region METHOD_test_v6_tiny_det [DOMAIN(8): Testing; CONCEPT(7): DetectionModel; TECH(4): unittest]
    ## @purpose Verify that v6+tiny resolves to PP-OCRv6_tiny_det.
    ## @complexity 1
    def test_v6_tiny_det(self):
        result = PaddleOCRModelConfig.get_det_model("paddle_v6", "tiny")
        print(f"[IMP:9][test_v6_tiny_det] get_det_model(v6, tiny) = '{result}' (expected 'PP-OCRv6_tiny_det')")
        self.assertEqual(result, "PP-OCRv6_tiny_det")
    # endregion METHOD_test_v6_tiny_det

    # region METHOD_test_v6_medium_det [DOMAIN(8): Testing; CONCEPT(7): DetectionModel; TECH(4): unittest]
    ## @purpose Verify that v6+medium resolves to PP-OCRv6_medium_det explicitly.
    ## @complexity 1
    def test_v6_medium_det(self):
        result = PaddleOCRModelConfig.get_det_model("paddle_v6", "medium")
        print(f"[IMP:9][test_v6_medium_det] get_det_model(v6, medium) = '{result}' (expected 'PP-OCRv6_medium_det')")
        self.assertEqual(result, "PP-OCRv6_medium_det")
    # endregion METHOD_test_v6_medium_det

    # region METHOD_test_v5_server_det_legacy [DOMAIN(8): Testing; CONCEPT(7): DetectionModel; TECH(4): unittest]
    ## @purpose Verify that v5+server resolves to PP-OCRv5_server_det (was auto, now explicit).
    ## @complexity 1
    def test_v5_server_det_legacy(self):
        result = PaddleOCRModelConfig.get_det_model("paddle_v5", "server")
        print(f"[IMP:9][test_v5_server_det_legacy] get_det_model(v5, server) = '{result}' (expected 'PP-OCRv5_server_det')")
        self.assertEqual(result, "PP-OCRv5_server_det")
    # endregion METHOD_test_v5_server_det_legacy

    # region METHOD_test_v5_server_det [DOMAIN(8): Testing; CONCEPT(7): DetectionModel; TECH(4): unittest]
    ## @purpose Verify that v5+server resolves to PP-OCRv5_server_det.
    ## @complexity 1
    def test_v5_server_det(self):
        result = PaddleOCRModelConfig.get_det_model("paddle_v5", "server")
        print(f"[IMP:9][test_v5_server_det] get_det_model(v5, server) = '{result}' (expected 'PP-OCRv5_server_det')")
        self.assertEqual(result, "PP-OCRv5_server_det")
    # endregion METHOD_test_v5_server_det

    # region METHOD_test_v5_mobile_det [DOMAIN(8): Testing; CONCEPT(7): DetectionModel; TECH(4): unittest]
    ## @purpose Verify that v5+mobile resolves to PP-OCRv5_mobile_det.
    ## @complexity 1
    def test_v5_mobile_det(self):
        result = PaddleOCRModelConfig.get_det_model("paddle_v5", "mobile")
        print(f"[IMP:9][test_v5_mobile_det] get_det_model(v5, mobile) = '{result}' (expected 'PP-OCRv5_mobile_det')")
        self.assertEqual(result, "PP-OCRv5_mobile_det")
    # endregion METHOD_test_v5_mobile_det

    # region METHOD_test_v6_rec [DOMAIN(8): Testing; CONCEPT(7): RecognitionModel; TECH(4): unittest]
    ## @purpose Verify v6 recognition model resolution: medium/small/tiny.
    ## @complexity 2
    def test_v6_rec(self):
        cases = [
            ("medium", "PP-OCRv6_medium_rec"),
            ("small", "PP-OCRv6_small_rec"),
            ("tiny", "PP-OCRv6_tiny_rec"),
        ]
        for ocr_model, expected in cases:
            result = PaddleOCRModelConfig.get_rec_model("paddle_v6", ocr_model, "en")
            print(f"[IMP:9][test_v6_rec] get_rec_model(v6, {ocr_model}, _) = '{result}' (expected '{expected}')")
            self.assertEqual(result, expected)
    # endregion METHOD_test_v6_rec

    # region METHOD_test_v5_rec_eslav [DOMAIN(8): Testing; CONCEPT(7): RecognitionModel; TECH(4): unittest]
    ## @purpose Verify v5 recognition model resolution for eslav group.
    ## @complexity 1
    def test_v5_rec_eslav(self):
        result = PaddleOCRModelConfig.get_rec_model("paddle_v5", "server", "eslav")
        expected = "eslav_PP-OCRv5_mobile_rec"
        print(f"[IMP:9][test_v5_rec_eslav] get_rec_model(v5, auto, eslav) = '{result}' (expected '{expected}')")
        self.assertEqual(result, expected)
    # endregion METHOD_test_v5_rec_eslav

    # region METHOD_test_v5_rec_latin [DOMAIN(8): Testing; CONCEPT(7): RecognitionModel; TECH(4): unittest]
    ## @purpose Verify v5 recognition model resolution for latin group.
    ## @complexity 1
    def test_v5_rec_latin(self):
        result = PaddleOCRModelConfig.get_rec_model("paddle_v5", "server", "latin")
        expected = "latin_PP-OCRv5_mobile_rec"
        print(f"[IMP:9][test_v5_rec_latin] get_rec_model(v5, auto, latin) = '{result}' (expected '{expected}')")
        self.assertEqual(result, expected)
    # endregion METHOD_test_v5_rec_latin

    # region METHOD_test_v5_rec_server_rec [DOMAIN(8): Testing; CONCEPT(7): RecognitionModel; TECH(4): unittest]
    ## @purpose Verify v5 recognition model resolution for server_rec group (CJK).
    ## @complexity 1
    def test_v5_rec_server_rec(self):
        result = PaddleOCRModelConfig.get_rec_model("paddle_v5", "server", "server_rec")
        expected = "PP-OCRv5_server_rec"
        print(f"[IMP:9][test_v5_rec_server_rec] get_rec_model(v5, auto, server_rec) = '{result}' (expected '{expected}')")
        self.assertEqual(result, expected)
    # endregion METHOD_test_v5_rec_server_rec
# endregion CLASS_TestPaddleOCRModelConfig
