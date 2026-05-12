from typing import Any, Dict

import numpy as np
from PIL import Image
from torchvision import transforms

import logging

logger = logging.getLogger(__name__)

from dedoc.readers.pdf_reader.pdf_image_reader.columns_orientation_classifier.columns_orientation_classifier import ColumnsOrientationClassifier


# region CLASS_ImageTransform [DOMAIN(8): DocumentProcessing; CONCEPT(7): Reader; TECH(6): Python]
class ImageTransform(object):
    """
    Class transformation input Image before Network
    """

    # region METHOD___init__ [DOMAIN(7): DocumentProcessing; CONCEPT(6): Method; TECH(6): Python]
    def __init__(self) -> None:
        self.transform = transforms.Compose([
            transforms.Lambda(ColumnsOrientationClassifier.my_resize),
            transforms.CenterCrop(1200),
            transforms.ToTensor(),
            transforms.Normalize(mean=[0.5, 0.5, 0.5], std=[0.5, 0.5, 0.5])
        ])

    # region METHOD___call__ [DOMAIN(7): DocumentProcessing; CONCEPT(6): Method; TECH(6): Python]
    # endregion METHOD___init__
    def __call__(self, image: np.ndarray) -> Image:
        pil_image = Image.fromarray(np.uint8(image)).convert("RGB")
        image = self.transform(pil_image)
# endregion CLASS_ImageTransform
        return image


# region CLASS_TransformWithLabels [DOMAIN(8): DocumentProcessing; CONCEPT(7): Reader; TECH(6): Python]
    # endregion METHOD___call__
class TransformWithLabels(object):
    """
    Class transformation input data [Image, label] before Network
    """

    # region METHOD___init__ [DOMAIN(7): DocumentProcessing; CONCEPT(6): Method; TECH(6): Python]
    def __init__(self) -> None:
        self.transform = transforms.Compose([
            transforms.Lambda(ColumnsOrientationClassifier.my_resize),
            transforms.CenterCrop(1200),
            transforms.ToTensor(),
            transforms.Normalize(mean=[0.5, 0.5, 0.5], std=[0.5, 0.5, 0.5])
        ])

    # region METHOD___call__ [DOMAIN(7): DocumentProcessing; CONCEPT(6): Method; TECH(6): Python]
    # endregion METHOD___init__
    def __call__(self, sample: dict) -> Dict[str, Any]:
        image, orientation, columns = sample["image"], sample["orientation"], sample["columns"]
        pil_image = Image.fromarray(np.uint8(image)).convert("RGB")
        image = self.transform(pil_image)

# endregion CLASS_TransformWithLabels
        return {"image": image, "orientation": orientation, "columns": columns, "image_name": sample["image_name"]}

    # endregion METHOD___call__


# region MODULE_CONTRACT [DOMAIN(8): DocumentProcessing; CONCEPT(7): Reader_transforms; TECH(6): Python, dedoc]
## @modulecontract
## @purpose Read and parse PDF documents, extracting lines with metadata, tables, and attachments into UnstructuredDocument.
## @scope Machine learning classification for document layout analysis.
## @input [File path (str), parameters (Optional[dict]) — document on disk.]
## @output [UnstructuredDocument with lines, tables, attachments, and warnings.]
## @links [USES_API(9): dedoc.data_structures.*; USES_API(8): dedoc.readers.BaseReader]
## @invariants
## - read() ALWAYS returns an UnstructuredDocument.
## @rationale
## Q: Why is this reader separated from others?
## A: Each reader handles one format family — isolation prevents format coupling and simplifies extension.
## @changes
## LAST_CHANGE: [v1.0.0 – Added SEMANTIC TEMPLATE markup and LDD logging.]
## @modulemap
## CLASS [4][ImageTransform reader/processor] => ImageTransform
## CLASS [4][TransformWithLabels reader/processor] => TransformWithLabels
## @usecases
## - [read]: System (Pipeline) → ParseDocument(PDF) → UnstructuredDocument
def _module_contract():
    pass
# endregion MODULE_CONTRACT
# GREP_SUMMARY: transforms, dedoc, reader, PDF, PdfReader, BaseReader, PDF, pdfminer, tabby, OCR, tables, image, txtlayer, columns, orientation, paragraphs, metadata, extraction, line, bbox, ImageTransform, TransformWithLabels
# STRUCTURE: ▶ Init ┌PDF file┐ → [ImageTransform] ○ can_read? → ○ read → [__init__ → __call__] → ⊕ UnstructuredDocument(lines, tables, attachments)
