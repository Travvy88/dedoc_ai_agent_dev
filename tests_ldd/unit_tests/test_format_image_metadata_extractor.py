# region MODULE_CONTRACT [DOMAIN(7): Testing; CONCEPT(8): UnitTest, LDD_Telemetry; TECH(8): unittest, pytest]
## @modulecontract
## @purpose Unit tests for format image metadata extractor module.
## @scope Unit testing of dedoc module: format, image, metadata, extractor.
## @input Test data files from tests/data/.
## @output Test results (pass/fail) with LDD telemetry.
## @links [USES_API(7): unittest.TestCase]
## @invariants
## - All original test logic and assertions remain unchanged.
## - LDD telemetry is printed BEFORE assertions.
## @rationale
## Q: Why add LDD telemetry to tests?
## A: On failure, critical log trajectory is visible before assert traceback.
## @changes
## LAST_CHANGE: [v1.0.0 – Added LDD telemetry and semantic markup.]
## @modulemap
## CLASS 8[Unit tests] => TestImageMetadataExtractor
## @usecases
## - [Tests]: QA Agent (Verify) => RunTestsWithTelemetry => DiagnosticTrajectoryVisible
def _module_contract():
    pass
# endregion MODULE_CONTRACT
# GREP_SUMMARY: format, image, metadata, extractor, TestImageMetadataExtractor, test_broken_image_metadata_extraction, unit_test, unittest, LDD_telemetry, semantic_markup, unit_test
# STRUCTURE: ▶ Init → ◇ Execute → ⊕ Verify → ∑ assertions → ⎋ PASS/FAIL


import logging

logger = logging.getLogger(__name__)

import os
import unittest

from dedoc.metadata_extractors.concrete_metadata_extractors.image_metadata_extractor import ImageMetadataExtractor
from tests.test_utils import get_test_config


# region CLASS_TestImageMetadataExtractor [DOMAIN(7): Testing; CONCEPT(8): UnitTest, LDD_Telemetry; TECH(8): unittest, pytest]
## @purpose Test suite for format, image, metadata, extractor module.
class TestImageMetadataExtractor(unittest.TestCase):
    extractor = ImageMetadataExtractor(config=get_test_config())
    data_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "data"))
    assert os.path.isdir(data_path)

    # region METHOD_test_broken_image_metadata_extraction [DOMAIN(7): Testing; CONCEPT(8): LDD_Telemetry; TECH(8): unittest]
    ## @purpose Verify: broken image metadata extraction.
    ## @complexity 5
    def test_broken_image_metadata_extraction(self) -> None:
        # LDD TELEMETRY: log execution context before assertions
        print(f"\n--- LDD TRAJECTORY (IMP:7-10) for TestImageMetadataExtractor::test_broken_image_metadata_extraction ---")
        print(f"  [LDD_TEST][IMP:8][TestImageMetadataExtractor][test_broken_image_metadata_extraction] Test logic executed, entering assertion phase")
        file = os.path.join(self.data_path, "exif_nan.jpg")
        exif = self.extractor._get_exif(file)
        self.assertIsNone(exif.get("digital_zoom_ratio"))

    # endregion METHOD_test_broken_image_metadata_extraction
# endregion CLASS_TestImageMetadataExtractor