.. _add_ocr_engine:

Adding support for a new OCR engine to Dedoc
============================================

Overview
--------

Dedoc uses optical character recognition (OCR) to extract text from image-based PDF documents and scanned images.
The OCR subsystem is built on the **Strategy pattern**: the abstract interface :class:`~dedoc.readers.pdf_reader.pdf_image_reader.ocr.ocr_engine_abstract.OCREngineAbstract`
defines the contract, and concrete engine implementations (e.g., Tesseract) provide the actual text recognition logic.

The OCR abstraction consists of three flat dataclasses and one abstract base class:

* :class:`~dedoc.readers.pdf_reader.pdf_image_reader.ocr.ocr_engine_abstract.OCRWord` — a single recognized word token with its ``text``, ``bbox`` (bounding box), and ``confidence`` score.
* :class:`~dedoc.readers.pdf_reader.pdf_image_reader.ocr.ocr_engine_abstract.OCRLine` — a single line of recognized text, containing a list of :class:`~dedoc.readers.pdf_reader.pdf_image_reader.ocr.ocr_engine_abstract.OCRWord` objects, a line-level ``bbox``, and a ``get_annotations()`` method that generates dedoc :class:`~dedoc.data_structures.concrete_annotations.bbox_annotation.BBoxAnnotation` and :class:`~dedoc.data_structures.concrete_annotations.confidence_annotation.ConfidenceAnnotation` instances.
* :class:`~dedoc.readers.pdf_reader.pdf_image_reader.ocr.ocr_engine_abstract.OCRResult` — the top-level OCR output: a flat list of :class:`~dedoc.readers.pdf_reader.pdf_image_reader.ocr.ocr_engine_abstract.OCRLine` objects.
* :class:`~dedoc.readers.pdf_reader.pdf_image_reader.ocr.ocr_engine_abstract.OCREngineAbstract` — the abstract base class with two methods that every engine must implement: ``recognize_page()`` and ``recognize_cells()``.

This tutorial guides you through the process of implementing a custom OCR engine and integrating it into the dedoc pipeline.

Step 1: Implement the OCR engine class
--------------------------------------

Create a new Python class that inherits from :class:`~dedoc.readers.pdf_reader.pdf_image_reader.ocr.ocr_engine_abstract.OCREngineAbstract`.
You must implement two abstract methods:

* :meth:`~dedoc.readers.pdf_reader.pdf_image_reader.ocr.ocr_engine_abstract.OCREngineAbstract.recognize_page` — performs OCR on a full document page image and returns an :class:`~dedoc.readers.pdf_reader.pdf_image_reader.ocr.ocr_engine_abstract.OCRResult`.
* :meth:`~dedoc.readers.pdf_reader.pdf_image_reader.ocr.ocr_engine_abstract.OCREngineAbstract.recognize_cells` — performs OCR on individual table cell images and returns an :class:`~dedoc.readers.pdf_reader.pdf_image_reader.ocr.ocr_engine_abstract.OCRResult`.

Below is a minimal example implementation:

.. code-block:: python

    import numpy as np
    from dedoc.readers.pdf_reader.pdf_image_reader.ocr.ocr_engine_abstract import OCREngineAbstract, OCRResult, OCRLine, OCRWord

    class MyOCREngine(OCREngineAbstract):
        def __init__(self, config: dict) -> None:
            self.config = config

        def recognize_page(self,
                           image: np.ndarray,
                           language: str,
                           is_one_column: bool,
                           **kwargs) -> OCRResult:
            # Process the full-page image with your OCR engine.
            # Extract words, their bounding boxes, and confidence scores.
            words = [OCRWord(text="hello", bbox=..., confidence=95.0)]
            line = OCRLine(words=words, bbox=...)
            return OCRResult(lines=[line])

        def recognize_cells(self,
                            image: np.ndarray,
                            language: str,
                            **kwargs) -> OCRResult:
            # Process a table cell image with your OCR engine.
            # The output format is identical to recognize_page().
            words = [OCRWord(text="cell", bbox=..., confidence=90.0)]
            line = OCRLine(words=words, bbox=...)
            return OCRResult(lines=[line])

Step 2: Register the engine in PdfImageReader
---------------------------------------------

After implementing your OCR engine, you need to register it in :class:`~dedoc.readers.pdf_reader.pdf_image_reader.pdf_image_reader.PdfImageReader`.
Open the file ``dedoc/readers/pdf_reader/pdf_image_reader/pdf_image_reader.py`` and modify the ``__init__`` method to handle your engine name.

Locate the factory pattern where the OCR engine is created (around line 57). Add an ``elif`` branch for your engine:

.. code-block:: python

    ocr_engine_name = self.config.get("ocr_engine", "tesseract")
    if ocr_engine_name == "tesseract":
        from dedoc.readers.pdf_reader.pdf_image_reader.ocr.tesseract_ocr_engine import TesseractOCREngine
        ocr_engine = TesseractOCREngine(config=self.config)
    elif ocr_engine_name == "my_engine":
        from my_package import MyOCREngine
        ocr_engine = MyOCREngine(config=self.config)
    else:
        raise ValueError(f"Unknown OCR engine: {ocr_engine_name}")

You must also modify the :meth:`~dedoc.readers.pdf_reader.pdf_image_reader.pdf_image_reader.PdfImageReader._set_ocr_engine_from_parameters` method
(located later in the same file) to support per-request engine switching. Add the same ``elif`` branch inside that method so that
the engine can be changed dynamically via the API ``ocr_engine`` parameter without restarting the application:

.. code-block:: python

    def _set_ocr_engine_from_parameters(self, parameters: Optional[dict] = None) -> None:
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
        elif ocr_engine_name == "my_engine":
            from my_package import MyOCREngine
            from dedoc.readers.pdf_reader.pdf_image_reader.ocr.ocr_line_extractor import OCRLineExtractor
            ocr_engine = MyOCREngine(config=self.config)
            self._current_engine_name = "my_engine"
            self.ocr_engine = ocr_engine
            self.ocr = OCRLineExtractor(config=self.config, engine=ocr_engine)
            self.table_recognizer.ocr_engine = ocr_engine
            self.logger.debug(f"[IMP:7][PdfImageReader][SET_ENGINE] Switched OCR engine to '{ocr_engine_name}'")
        else:
            raise ValueError(f"Unknown OCR engine: {ocr_engine_name}")

Step 3: Use the new engine via API or config
--------------------------------------------

Once the engine is registered, you can select it in two ways:

1. **Via API parameter**: include ``ocr_engine=my_engine`` in the form data when sending a POST request to the dedoc API:

   .. code-block:: python

       import requests

       data = {
           "ocr_engine": "my_engine",
           "language": "eng",
           "pdf_with_text_layer": "false",
       }
       with open("document.pdf", "rb") as file:
           files = {"file": ("document.pdf", file)}
           r = requests.post("http://localhost:1231/upload", files=files, data=data)

2. **Via library config**: pass ``ocr_engine`` in the ``config`` dictionary when creating a :class:`~dedoc.DedocManager` or :class:`~dedoc.readers.pdf_reader.pdf_image_reader.pdf_image_reader.PdfImageReader` instance:

   .. code-block:: python

       from dedoc import DedocManager

       config = {"ocr_engine": "my_engine"}
       manager = DedocManager.from_config(config=config)
       result = manager.parse(file_path="document.pdf")

Data contract: OCRResult, OCRLine, and OCRWord
----------------------------------------------

When implementing :meth:`~dedoc.readers.pdf_reader.pdf_image_reader.ocr.ocr_engine_abstract.OCREngineAbstract.recognize_page` and
:meth:`~dedoc.readers.pdf_reader.pdf_image_reader.ocr.ocr_engine_abstract.OCREngineAbstract.recognize_cells`,
your engine must return properly structured :class:`~dedoc.readers.pdf_reader.pdf_image_reader.ocr.ocr_engine_abstract.OCRResult` objects.
The data contract is as follows:

:class:`OCRWord` fields:
    * ``text: str`` — the recognized text of a single word token.
    * ``bbox: BBox`` — the bounding box of the word on the page, as a :class:`~dedocutils.data_structures.BBox` instance describing its position and dimensions.
    * ``confidence: float`` — the confidence score of the recognition (typically in the range 0–100).

:class:`OCRLine` fields:
    * ``words: List[OCRWord]`` — the list of :class:`OCRWord` tokens that form this line, in left-to-right reading order.
    * ``bbox: BBox`` — the bounding box of the entire line on the page.
    * ``get_annotations(page_width: int, page_height: int, extract_line_bbox: bool) -> List[Annotation]`` — a method that generates dedoc annotation objects. When ``extract_line_bbox`` is ``True``, it returns a single :class:`~dedoc.data_structures.concrete_annotations.bbox_annotation.BBoxAnnotation` for the entire line. When ``False``, it returns per-word :class:`~dedoc.data_structures.concrete_annotations.bbox_annotation.BBoxAnnotation` and :class:`~dedoc.data_structures.concrete_annotations.confidence_annotation.ConfidenceAnnotation` instances. This method is already implemented in the base :class:`OCRLine` dataclass and does not need to be overridden.

:class:`OCRResult` fields:
    * ``lines: List[OCRLine]`` — the complete list of recognized text lines for the image, in top-to-bottom reading order.
