# region MODULE_CONTRACT [DOMAIN(7): Testing; CONCEPT(8): UnitTest, LDD_Telemetry; TECH(8): unittest, pytest]
## @modulecontract
## @purpose Unit tests for format image reader bbox module.
## @scope Unit testing of dedoc module: format, image, reader, bbox.
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
## CLASS 8[Unit tests] => TestImageReaderWithBBox
## @usecases
## - [Tests]: QA Agent (Verify) => RunTestsWithTelemetry => DiagnosticTrajectoryVisible
def _module_contract():
    pass
# endregion MODULE_CONTRACT
# GREP_SUMMARY: format, image, reader, bbox, TestImageReaderWithBBox, test_line_order, unit_test, unittest, LDD_telemetry, semantic_markup, unit_test
# STRUCTURE: ▶ Init → ◇ Execute → ⊕ Verify → ∑ assertions → ⎋ PASS/FAIL


import logging

logger = logging.getLogger(__name__)

import os
import re
import unittest

import cv2

from dedoc.readers.pdf_reader.pdf_image_reader.ocr.ocr_line_extractor import OCRLineExtractor
from tests.test_utils import get_test_config


# region CLASS_TestImageReaderWithBBox [DOMAIN(7): Testing; CONCEPT(8): UnitTest, LDD_Telemetry; TECH(8): unittest, pytest]
## @purpose Test suite for format, image, reader, bbox module.
class TestImageReaderWithBBox(unittest.TestCase):
    abs_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "data", "scanned"))
    reader = OCRLineExtractor(config=get_test_config())

    # region METHOD_test_line_order [DOMAIN(7): Testing; CONCEPT(8): LDD_Telemetry; TECH(8): unittest]
    ## @purpose Verify: line order.
    ## @complexity 5
    def test_line_order(self) -> None:
        # LDD TELEMETRY: log execution context before assertions
        print(f"\n--- LDD TRAJECTORY (IMP:7-10) for TestImageReaderWithBBox::test_line_order ---")
        print(f"  [LDD_TEST][IMP:8][TestImageReaderWithBBox][test_line_order] Test logic executed, entering assertion phase")
        image = cv2.imread(os.path.join(self.abs_path, "part.png"))
        page = self.reader.split_image2lines(image=image, page_num=1, is_one_column_document=True)
        bboxes = [bbox for bbox in page.bboxes if bbox.text.strip() != ""]
        for bbox in bboxes:
            for word in bbox.words:
                word.text = re.sub(r"\s+", "", word.text)
        self.assertEqual("Утвержден", bboxes[0].text.strip())
        self.assertEqual("приказом ФСТЭК России", bboxes[1].text.strip())
        self.assertEqual("Утвержден", bboxes[0].text.strip())
        self.assertEqual("приказом ФСТЭК России", bboxes[1].text.strip())
        self.assertEqual("Порядок согласования", bboxes[3].text.strip())
        self.assertEqual("субъектом критической информационной инфраструктуры", bboxes[4].text.strip())
        self.assertEqual("Российской Федерации с Федеральной службой по техническому и", bboxes[5].text.strip())
        self.assertEqual("экспортному контролю подключения значимого объекта критической", bboxes[6].text.strip())
        self.assertEqual("информационной инфраструктуры Российской Федерации", bboxes[7].text.strip())
        self.assertEqual("к сети связи общего пользования", bboxes[8].text.strip())
        self.assertEqual("критической информационной инфраструктуры Российской Федерации (далее", bboxes[10].text.strip())
        self.assertEqual("субъект критической информационной инфраструктуры) с ФСТЭК России", bboxes[11].text.strip())
        self.assertEqual("подключения значимого объекта критической информационной инфраструктуры", bboxes[12].text.strip())
        self.assertEqual("пользования, осуществляемого в соответствии с пунктом 3 Правил подготовки и", bboxes[14].text.strip())
        self.assertEqual("использования ресурсов единой сети электросвязи Российской Федерации для", bboxes[15].text.strip())
        self.assertEqual("обеспечения функционирования значимых объектов критической", bboxes[16].text.strip())
        self.assertEqual("информационной инфраструктуры, утвержденных постановлением", bboxes[17].text.strip())
        self.assertEqual("Правительства Российской Федерации от 8 июня 2019 г №743 (Собрание", bboxes[18].text.strip())
        self.assertEqual("законодательства Российской Федерации, 2019, № 24, ст. 3099) (далее", bboxes[19].text.strip())
        self.assertEqual("Правила).", bboxes[20].text.strip())
        self.assertEqual("2. Согласование подключения создаваемого значимого объекта", bboxes[21].text.strip())
        self.assertEqual("осуществляется до ввода его в действие на этапе, определяемом субъектом", bboxes[22].text.strip())
        self.assertEqual("критической информационной инфраструктуры. Согласование подключения", bboxes[23].text.strip())
        self.assertEqual("действующего значимого объекта осуществляется до заключения договора с", bboxes[24].text.strip())
        self.assertEqual("оператором связи, предусмотренного пунктом 6 Правил.", bboxes[25].text.strip())
        self.assertEqual("3.В случае если значимый объект на момент его включения в реестр", bboxes[26].text.strip())
        self.assertEqual("значимых критической информационной инфраструктуры", bboxes[27].text.strip())
        self.assertEqual("Российской Федерации (лалее - реестр объектов критической", bboxes[28].text.strip())
        self.assertEqual("информационной инфраструктуры) подключен к сети связи общего", bboxes[29].text.strip())
        self.assertEqual("пользования, согласование ФСТЭК России в соответствии с настоящим", bboxes[30].text.strip())
        self.assertEqual("Порядком не требуется.", bboxes[31].text.strip())
        self.assertEqual("4. Для согласования подключения значимого объекта к сети связи общего", bboxes[32].text.strip())
        self.assertEqual("пользования субъект критической информационной инфраструктуры", bboxes[33].text.strip())
        self.assertEqual("представляет посредством почтового отправления или непосредственно", bboxes[34].text.strip())
        self.assertEqual("в ФСТЭК России следующие сведения:", bboxes[35].text.strip())
        self.assertEqual("Порядок ведения реестра значимых объектов критической информационной инфраструкту-", bboxes[36].text.strip())
        self.assertEqual("№227 «Об утверждении Порядка ведения реестра значимых объектов критической информа-", bboxes[38].text.strip())
        self.assertEqual("ционной нифраструктуры Российской Федерации» (зарегистрирован Минюстом России", bboxes[39].text.strip())

    # endregion METHOD_test_line_order
# endregion CLASS_TestImageReaderWithBBox