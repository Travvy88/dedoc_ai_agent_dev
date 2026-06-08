import os
import sys
from datetime import datetime

# -- Path setup --------------------------------------------------------------

sys.path.insert(0, os.path.abspath(os.path.join("..", "..", "labeling")))
sys.path.insert(0, os.path.abspath(os.path.join("..", "..")))


# -- Project information -----------------------------------------------------

project = "dedoc"
_copyright_str = f"-{datetime.now().year}" if datetime.now().year > 2023 else ""
copyright = f"2023{_copyright_str}, Dedoc team"  # noqa
author = "Dedoc team"
release = "1"


# -- General configuration ---------------------------------------------------

extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.napoleon",
    "sphinx.ext.viewcode",
    "sphinx_rtd_theme",
    "sphinx_copybutton",
    "sphinx_togglebutton",
    "linuxdoc.rstFlatTable"
]
exclude_patterns = []
highlight_language = "python3"

# -- Options for the nitpicky mode -------------------------------------------

nitpicky = True
nitpick_ignore = [
    ("py:class", "abc.ABC"),
    ("py:class", "pydantic.main.BaseModel"),
    ("py:class", "scipy.stats._multivariate.dirichlet_multinomial_gen.cov"),
    ("py:class", "scipy.stats._multivariate.random_table_gen.rvs"),
    ("py:class", "pandas.core.series.Series"),
    ("py:class", "numpy.ndarray"),
    ("py:class", "pandas.core.frame.DataFrame"),
    ("py:class", "dedoc.structure_extractors.feature_extractors.toc_feature_extractor.TocItem"),
    ("py:class", "logging.Logger"),
    ("py:class", "train_dataset.data_structures.line_with_label.LineWithLabel"),
    ("py:class", "xgboost.sklearn.XGBClassifier"),
    ("py:class", "collections.Counter"),
    ("py:obj", "typing.Pattern"),
    ("py:meth", "dedoc.attachments_extractors.AbstractAttachmentsExtractor.can_extract"),
    ("py:meth", "dedoc.attachments_extractors.DocxAttachmentsExtractor.extract"),
    ("py:meth", "dedoc.converters.AbstractConverter.can_convert"),
    ("py:meth", "dedoc.converters.DocxConverter.convert"),
    ("py:meth", "dedoc.readers.BaseReader.can_read"),
    ("py:meth", "dedoc.readers.DocxReader.read"),
    ("py:meth", "dedoc.metadata_extractors.AbstractMetadataExtractor.can_extract"),
    ("py:meth", "dedoc.metadata_extractors.DocxMetadataExtractor.extract"),
    ("py:meth", "dedoc.readers.pdf_reader.pdf_image_reader.ocr.tesseract_ocr_engine.TesseractOCREngine.recognize_page"),
    ("py:meth", "dedoc.readers.pdf_reader.pdf_image_reader.ocr.tesseract_ocr_engine.TesseractOCREngine.recognize_cells"),
    ("py:meth", "dedoc.readers.pdf_reader.pdf_image_reader.ocr.tesseract_ocr_engine.TesseractOCREngine._raw_dict_to_ocr_result"),
    ("py:meth", "dedoc.readers.pdf_reader.pdf_image_reader.ocr.ocr_engine_abstract.OCREngineAbstract.recognize_page"),
    ("py:meth", "dedoc.readers.pdf_reader.pdf_image_reader.ocr.ocr_engine_abstract.OCREngineAbstract.recognize_cells"),
    ("py:meth", "dedoc.readers.pdf_reader.pdf_image_reader.ocr.ocr_engine_abstract.OCRLine.get_annotations"),
    ("py:meth", "dedoc.readers.pdf_reader.pdf_image_reader.ocr.ocr_line_extractor.OCRLineExtractor.split_image2lines"),
    ("py:meth", "dedoc.readers.pdf_reader.pdf_image_reader.ocr.ocr_line_extractor.OCRLineExtractor.__split_image2bboxes"),
    ("py:meth", "dedoc.readers.pdf_reader.pdf_image_reader.ocr.ocr_line_extractor.OCRLineExtractor._filtered_bboxes"),
    ("py:meth", "dedoc.readers.pdf_reader.pdf_image_reader.ocr.ocr_cell_extractor.OCRCellExtractor.get_cells_text"),
    ("py:meth", "dedoc.readers.pdf_reader.pdf_image_reader.ocr.ocr_cell_extractor.OCRCellExtractor.get_line_with_meta"),
    ("py:meth", "dedoc.readers.pdf_reader.pdf_image_reader.ocr.ocr_cell_extractor.OCRCellExtractor.upscale"),
    ("py:class", "dedoc.readers.pdf_reader.data_classes.text_with_bbox.TextWithBBox"),
    ("py:class", "dedoc.readers.pdf_reader.data_classes.page_with_bboxes.PageWithBBox"),
    ("py:meth", "dedoc.attachments_extractors.AbstractAttachmentsExtractor.extract"),
    ("py:meth", "dedoc.structure_extractors.FintocStructureExtractor.extract"),
    ("py:meth", "dedoc.structure_extractors.StructureExtractorComposition.extract"),
    ("py:meth", "dedoc.structure_extractors.DefaultStructureExtractor.extract"),
    ("py:meth", "dedoc.structure_extractors.AbstractStructureExtractor.extract"),
    ("py:meth", "dedoc.readers.pdf_reader.pdf_image_reader.pdf_image_reader.PdfImageReader._set_ocr_engine_from_parameters"),
    ("py:class", "OCRWord"),
    ("py:class", "OCRLine"),
    ("py:class", "OCRResult"),
    ("py:meth", "dedoc.structure_extractors.feature_extractors.abstract_extractor.AbstractFeatureExtractor.transform"),
    ("py:meth", "dedoc.structure_extractors.feature_extractors.abstract_extractor.AbstractFeatureExtractor.parameters"),
    ("py:meth", "dedoc.structure_extractors.feature_extractors.abstract_extractor.AbstractFeatureExtractor._list_features"),
    ("py:meth", "dedoc.structure_extractors.feature_extractors.abstract_extractor.AbstractFeatureExtractor._normalize_features"),
    ("py:meth", "dedoc.structure_extractors.line_type_classifiers.abstract_line_type_classifier.AbstractLineTypeClassifier.predict"),
    ("py:meth", "dedoc.structure_extractors.patterns.abstract_pattern.AbstractPattern.match"),
    ("py:meth", "dedoc.structure_extractors.patterns.abstract_pattern.AbstractPattern.get_hierarchy_level")
]

# -- Options for HTML output -------------------------------------------------

html_theme = "sphinx_rtd_theme"
html_static_path = ["_static"]
html_css_files = ["style.css"]
html_favicon = "_static/favicon.ico"
html_title = "dedoc documentation"
