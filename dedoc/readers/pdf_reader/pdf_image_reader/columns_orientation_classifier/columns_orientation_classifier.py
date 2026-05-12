import logging
import os
import warnings
from os import path
from typing import Optional, Tuple

import cv2
import numpy as np
import torch
from PIL import Image
from torchvision import transforms
from torchvision.transforms.functional import resize

from dedoc.download_models import download_from_hub
from dedoc.readers.pdf_reader.pdf_image_reader.columns_orientation_classifier.model import ClassificationModelTorch


# region CLASS_ColumnsOrientationClassifier [DOMAIN(8): DocumentProcessing; CONCEPT(7): Reader; TECH(6): Python]
class ColumnsOrientationClassifier(object):
    """
    Class Classifier for work with Orientation Network. This class set device,
    preprocessing (transform) input data, weights of model
    """
    # region METHOD___init__ [DOMAIN(7): DocumentProcessing; CONCEPT(6): Method; TECH(6): Python]
    def __init__(self, on_gpu: bool, checkpoint_path: Optional[str], *, config: dict) -> None:
        self.logger = config.get("logger", logging.getLogger())
        self._set_device(on_gpu)
        self._set_transform_image()
        self.checkpoint_path = path.abspath(checkpoint_path)
        self.classes = [1, 2, 0, 90, 180, 270]
        self._net = None

    # endregion METHOD___init__
    @property
    # region METHOD_net [DOMAIN(7): DocumentProcessing; CONCEPT(6): Method; TECH(6): Python]
    def net(self) -> ClassificationModelTorch:
        if self._net is None:
            net = ClassificationModelTorch(self.checkpoint_path)
            if self.checkpoint_path is not None:
                self._load_weights(net)
            self._net = net
        self._net.to(self.device)
        return self._net

    # endregion METHOD_net
    @staticmethod
    # region METHOD_my_resize [DOMAIN(7): DocumentProcessing; CONCEPT(6): Method; TECH(6): Python]
    def my_resize(image: Image) -> Image:
        max_dim = max(image.size)
        image1 = resize(image, size=[round(image.size[1] / max_dim * 1200), round(image.size[0] / max_dim * 1200)])
        white_image = Image.new(size=(1200, 1200), color=(255, 255, 255), mode="RGB")
        white_image.paste(image1)
        return white_image

    # region METHOD__set_device [DOMAIN(7): DocumentProcessing; CONCEPT(6): Method; TECH(6): Python]
    # endregion METHOD_my_resize
    def _set_device(self, on_gpu: bool) -> None:
        """
        Set device configuration
        """
        if on_gpu and torch.cuda.is_available():
            self.device = torch.device("cuda:0")
            self.location = lambda storage, loc: storage.cuda()
        else:
            self.device = torch.device("cpu")
            self.location = "cpu"

        self.logger.warning(f"Classifier is set to device {self.device}")

    # region METHOD__load_weights [DOMAIN(7): DocumentProcessing; CONCEPT(6): Method; TECH(6): Python]
    # endregion METHOD__set_device
    def _load_weights(self, net: ClassificationModelTorch) -> None:
        if not path.isfile(self.checkpoint_path):
            from dedoc.config import get_config
            self.checkpoint_path = os.path.join(get_config()["resources_path"], "scan_orientation_efficient_net_b0.pth")
            download_from_hub(out_dir=os.path.dirname(os.path.abspath(self.checkpoint_path)),
                              out_name="scan_orientation_efficient_net_b0.pth",
                              repo_name="scan_orientation_efficient_net_b0",
                              hub_name="model.pth")

        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            net.load_state_dict(torch.load(self.checkpoint_path, map_location=self.location))
            self.logger.info(f"Weights were loaded from {self.checkpoint_path}")

    # region METHOD_save_weights [DOMAIN(7): DocumentProcessing; CONCEPT(6): Method; TECH(6): Python]
    # endregion METHOD__load_weights
    def save_weights(self, path_checkpoint: str) -> None:
        torch.save(self.net.state_dict(), path_checkpoint)
        self.logger.info(f"Weights were saved into {path_checkpoint}")

    # region METHOD__set_transform_image [DOMAIN(7): DocumentProcessing; CONCEPT(6): Method; TECH(6): Python]
    # endregion METHOD_save_weights
    def _set_transform_image(self) -> None:
        """
        Set configuration preprocessing for input image
        """
        self.transform = transforms.Compose([
            transforms.Lambda(self.my_resize),
            transforms.ToTensor(),
            transforms.Normalize(
                mean=[0.5, 0.5, 0.5], std=[0.5, 0.5, 0.5])
        ])

    # region METHOD_get_features [DOMAIN(7): DocumentProcessing; CONCEPT(6): Method; TECH(6): Python]
    # endregion METHOD__set_transform_image
    def get_features(self, image: np.array) -> torch.Tensor:
        """
        Get features for the image
        """
        image = cv2.cvtColor(np.array(image), cv2.COLOR_BGR2RGB)
        pil_image = Image.fromarray(np.uint8(image)).convert("RGB")
        tensor_image = self.transform(pil_image).unsqueeze(0).float().to(self.device)
        return tensor_image

    # region METHOD_predict [DOMAIN(7): DocumentProcessing; CONCEPT(6): Method; TECH(6): Python]
    # endregion METHOD_get_features
    def predict(self, image: np.ndarray) -> Tuple[int, int]:
        """
        Predict class orientation of input image
        """
        self.net.eval()
        with torch.no_grad():
            tensor_image = self.get_features(image)
            outputs = self.net(tensor_image)
            # first 2 classes mean columns number
            # last 4 classes mean orientation
            columns_out, orientation_out = outputs[:, :2], outputs[:, 2:]

            _, columns_predicted = torch.max(columns_out, 1)
            _, orientation_predicted = torch.max(orientation_out, 1)

        columns, orientation = int(columns_predicted[0]), int(orientation_predicted[0])
        columns_predict = self.classes[columns]
        angle_predict = self.classes[2 + orientation]
# endregion CLASS_ColumnsOrientationClassifier
        return columns_predict, angle_predict

    # endregion METHOD_predict


# region MODULE_CONTRACT [DOMAIN(8): DocumentProcessing; CONCEPT(7): Reader_columns_orientation_classifier; TECH(6): Python, dedoc]
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
## CLASS [18][ColumnsOrientationClassifier reader/processor] => ColumnsOrientationClassifier
## @usecases
## - [read]: System (Pipeline) → ParseDocument(PDF) → UnstructuredDocument
def _module_contract():
    pass
# endregion MODULE_CONTRACT
# GREP_SUMMARY: columns_orientation_classifier, dedoc, reader, PDF, PdfReader, BaseReader, PDF, pdfminer, tabby, OCR, tables, image, txtlayer, columns, orientation, paragraphs, metadata, extraction, line, bbox, ColumnsOrientationClassifier
# STRUCTURE: ▶ Init ┌PDF file┐ → [ColumnsOrientationClassifier] ○ can_read? → ○ read → [__init__ → net → my_resize] → ⊕ UnstructuredDocument(lines, tables, attachments)
