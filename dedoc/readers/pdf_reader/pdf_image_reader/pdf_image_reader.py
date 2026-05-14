import os
from typing import List, Optional, Tuple

from numpy import ndarray

from dedoc.data_structures.unstructured_document import UnstructuredDocument
from dedoc.readers.pdf_reader.data_classes.line_with_location import LineWithLocation
from dedoc.readers.pdf_reader.data_classes.pdf_image_attachment import PdfImageAttachment
from dedoc.readers.pdf_reader.data_classes.tables.scantable import ScanTable
from dedoc.readers.pdf_reader.pdf_base_reader import ParametersForParseDoc, PdfBaseReader


# region CLASS_PdfImageReader [DOMAIN(8): DocumentProcessing; CONCEPT(7): Reader; TECH(6): Python]
class PdfImageReader(PdfBaseReader):
    """
    This class allows to extract content from the .pdf documents without a textual layer (not copyable documents),
    as well as from images (scanned documents).

    The following features are implemented to enhance the recognition results:

    * optical character recognition using Tesseract OCR;

    * table detection and recognition;

    * document binarization (configure via `need_binarization` parameter);

    * document orientation correction (automatically rotate on 90, 180, 270 degrees if it's needed);

    * one and two column documents classification;

    * detection of bold text.

    It isn't recommended to use this reader for extracting content from PDF documents with a correct textual layer, use other PDF readers instead.
    """

    # region METHOD___init__ [DOMAIN(7): DocumentProcessing; CONCEPT(6): Method; TECH(6): Python]
    def __init__(self, *, config: Optional[dict] = None) -> None:
        from dedocutils.preprocessing import AdaptiveBinarizer, SkewCorrector
        from dedoc.readers.pdf_reader.pdf_image_reader.columns_orientation_classifier.columns_orientation_classifier import ColumnsOrientationClassifier
        from dedoc.readers.pdf_reader.pdf_image_reader.ocr.ocr_line_extractor import OCRLineExtractor
        from dedoc.config import get_config
        from dedoc.extensions import recognized_extensions, recognized_mimes
        from dedoc.utils import supported_image_types

        supported_image_extensions = {ext for ext in supported_image_types if ext.startswith(".")}
        super().__init__(
            config=config,
            recognized_extensions=recognized_extensions.pdf_like_format.union(recognized_extensions.image_like_format).union(supported_image_extensions),
            recognized_mimes=recognized_mimes.pdf_like_format.union(recognized_mimes.image_like_format)
        )
        self.skew_corrector = SkewCorrector()
        self.column_orientation_classifier = ColumnsOrientationClassifier(on_gpu=self.config.get("on_gpu", False),
                                                                          checkpoint_path=os.path.join(get_config()["resources_path"],
                                                                                                       "scan_orientation_efficient_net_b0.pth"),
                                                                          config=self.config)
        self.binarizer = AdaptiveBinarizer()
        ocr_engine_name = self.config.get("ocr_engine", "tesseract")
        if ocr_engine_name == "tesseract":
            from dedoc.readers.pdf_reader.pdf_image_reader.ocr.tesseract_ocr_engine import TesseractOCREngine
            ocr_engine = TesseractOCREngine(config=self.config)
        else:
            raise ValueError(f"Unknown OCR engine: {ocr_engine_name}")
        self._current_engine_name = ocr_engine_name
        self.ocr_engine = ocr_engine
        self.ocr = OCRLineExtractor(config=self.config, engine=ocr_engine)
        self.table_recognizer.ocr_engine = ocr_engine
        self.page_number = None

    # region METHOD_read [DOMAIN(7): DocumentProcessing; CONCEPT(6): Method; TECH(6): Python]
    # endregion METHOD___init__
    def read(self, file_path: str, parameters: Optional[dict] = None) -> UnstructuredDocument:
        # BUG_FIX_CONTEXT: ocr_engine was only available via global config at startup. AC5 requires per-request engine selection via
        # API parameter. This override checks parameters["ocr_engine"] before processing and swaps the engine if it differs
        # from the currently active one, updating self.ocr_engine, self.ocr, and self.table_recognizer.ocr_engine.
        self._set_ocr_engine_from_parameters(parameters)
        return super().read(file_path, parameters)

    # region METHOD__set_ocr_engine_from_parameters [DOMAIN(8): OCR; CONCEPT(7): EngineSelection; TECH(6): Python]
    # endregion METHOD_read
    def _set_ocr_engine_from_parameters(self, parameters: Optional[dict] = None) -> None:
        """
        Check parameters dict for ocr_engine override and swap engine if it differs from the current one.
        Updates self.ocr_engine, self.ocr, and self.table_recognizer.ocr_engine in sync.
        """
        ocr_engine_name = (parameters or {}).get("ocr_engine") or self.config.get("ocr_engine", "tesseract")
        if ocr_engine_name == getattr(self, "_current_engine_name", None):
            return
        if ocr_engine_name == "tesseract":
            from dedoc.readers.pdf_reader.pdf_image_reader.ocr.tesseract_ocr_engine import TesseractOCREngine
            from dedoc.readers.pdf_reader.pdf_image_reader.ocr.ocr_line_extractor import OCRLineExtractor
            ocr_engine = TesseractOCREngine(config=self.config)
            self._current_engine_name = "tesseract"
            self.ocr_engine = ocr_engine
            self.ocr = OCRLineExtractor(config=self.config, engine=ocr_engine)
            self.table_recognizer.ocr_engine = ocr_engine
            self.logger.debug(f"[IMP:7][PdfImageReader][SET_ENGINE] Switched OCR engine to '{ocr_engine_name}'")
        else:
            raise ValueError(f"Unknown OCR engine: {ocr_engine_name}")
    # endregion METHOD__set_ocr_engine_from_parameters

    # region METHOD__process_one_page [DOMAIN(7): DocumentProcessing; CONCEPT(6): Method; TECH(6): Python]
    # endregion METHOD__set_ocr_engine_from_parameters
    def _process_one_page(self,
                          image: ndarray,
                          parameters: ParametersForParseDoc,
                          page_number: int,
                          path: str) -> Tuple[List[LineWithLocation], List[ScanTable], List[PdfImageAttachment], List[float]]:
        import os
        from datetime import datetime
        import cv2
        from dedoc.utils.parameter_utils import get_path_param

        #  --- Step 1: correct orientation and detect column count ---
        self.page_number = page_number
        rotated_image, is_one_column_document, angle = self._detect_column_count_and_orientation(image, parameters)
        if self.config.get("debug_mode", False):
            self.logger.info(f"Angle page rotation = {angle}")

        #  --- Step 2: do binarization ---
        if parameters.need_binarization:
            rotated_image, _ = self.binarizer.preprocess(rotated_image)
            if self.config.get("debug_mode", False):
                debug_dir = get_path_param(self.config, "path_debug")
                cv2.imwrite(os.path.join(debug_dir, f"{datetime.now().strftime('%H-%M-%S')}_result_binarization.jpg"), rotated_image)

        #  --- Step 3: table detection and recognition ---
        if parameters.need_pdf_table_analysis:
            clean_image, tables = self.table_recognizer.recognize_tables_from_image(
                image=rotated_image,
                page_number=page_number,
                language=parameters.language,
                table_type=parameters.table_type
            )
        else:
            clean_image, tables = rotated_image, []

        # --- Step 4: plain text recognition and text style detection ---
        page = self.ocr.split_image2lines(image=clean_image, language=parameters.language, is_one_column_document=is_one_column_document, page_num=page_number)

        lines = self.metadata_extractor.extract_metadata_and_set_annotations(page_with_lines=page)
        return lines, tables, page.attachments, [angle]

    # region METHOD__detect_column_count_and_orientation [DOMAIN(7): DocumentProcessing; CONCEPT(6): Method; TECH(6): Python]
    # endregion METHOD__process_one_page
    def _detect_column_count_and_orientation(self, image: ndarray, parameters: ParametersForParseDoc) -> Tuple[ndarray, bool, float]:
        """
        Function :
            - detects the number of page columns
            - detects page orientation angle
            - rotates the page on detected angle
        Return: rotated_image and indicator if the page is one-column
        """
        import os
        import cv2
        from dedoc.utils.parameter_utils import get_path_param

        columns, angle = None, None

        if parameters.is_one_column_document is None or parameters.document_orientation is None:
            columns, angle = self.column_orientation_classifier.predict(image)
            self.logger.info(f"Predicted orientation angle = {angle}, columns = {columns}")

        is_one_column_document = columns == 1 if parameters.is_one_column_document is None else parameters.is_one_column_document
        angle = angle if parameters.document_orientation is None else 0
        self.logger.info(f"Final orientation angle = {angle}, is_one_column_document = {is_one_column_document}")

        rotated_image, result_angle = self.skew_corrector.preprocess(image, {"orientation_angle": angle})
        result_angle = result_angle["rotated_angle"]

        if self.config.get("debug_mode", False):
            debug_dir = get_path_param(self.config, "path_debug")
            img_path = os.path.join(debug_dir, f"page-{self.page_number}_result_orientation.jpg")
            self.logger.info(f"Save image to {img_path}")
            cv2.imwrite(img_path, rotated_image)

# endregion CLASS_PdfImageReader
        return rotated_image, is_one_column_document, result_angle

    # endregion METHOD__detect_column_count_and_orientation


# region MODULE_CONTRACT [DOMAIN(8): DocumentProcessing; CONCEPT(7): Reader_pdf_image_reader; TECH(6): Python, dedoc]
## @modulecontract
## @purpose Read and parse PDF documents, extracting lines with metadata, tables, and attachments into UnstructuredDocument.
## @scope Document parsing pipeline: PDF format reading.
## @input [File path (str), parameters (Optional[dict]) — document on disk.]
## @output [UnstructuredDocument with lines, tables, attachments, and warnings.]
## @links [USES_API(9): dedoc.data_structures.*; USES_API(8): dedoc.readers.BaseReader]
## @invariants
## - read() ALWAYS returns an UnstructuredDocument.
## @rationale
## Q: Why is this reader separated from others?
## A: Each reader handles one format family — isolation prevents format coupling and simplifies extension.
## @changes
## LAST_CHANGE: [v1.1.0 – Added _set_ocr_engine_from_parameters for per-request OCR engine selection (AC5).]
## @modulemap
## CLASS [8][PdfImageReader reader/processor] => PdfImageReader
## @usecases
## - [read]: System (Pipeline) → ParseDocument(PDF) → UnstructuredDocument
def _module_contract():
    pass
# endregion MODULE_CONTRACT
# GREP_SUMMARY: pdf_image_reader, dedoc, reader, PDF, PdfReader, BaseReader, PDF, pdfminer, tabby, OCR, tables, image, txtlayer, columns, orientation, paragraphs, metadata, extraction, line, bbox, PdfImageReader
# STRUCTURE: ▶ Init ┌PDF file┐ → [PdfImageReader] ○ can_read? → ○ read → [__init__ → read → _process_one_page] → ⊕ UnstructuredDocument(lines, tables, attachments)
