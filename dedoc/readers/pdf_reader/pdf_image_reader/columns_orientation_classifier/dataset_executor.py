import os
from typing import Callable, Dict

import logging

logger = logging.getLogger(__name__)

import pandas as pd
import torch
from skimage import io
from torch.utils.data import DataLoader, Dataset
from torchvision import transforms

from dedoc.readers.pdf_reader.pdf_image_reader.columns_orientation_classifier.transforms import TransformWithLabels


# region CLASS_DatasetImageOrient [DOMAIN(8): DocumentProcessing; CONCEPT(7): Reader; TECH(6): Python]
class DatasetImageOrient(object):
    """
    Class to loading dataset from csv_file and root_dir
    """

    # region METHOD___init__ [DOMAIN(7): DocumentProcessing; CONCEPT(6): Method; TECH(6): Python]
    def __init__(self, csv_file: str, root_dir: str, transform: Callable = None) -> None:
        """
        Args:
            csv_file (string): Path to the csv file with annotations.
            root_dir (string): Directory with all the images.
            transform (callable, optional): Optional transform to be applied on a sample.
        """
        self.label_loader = pd.read_csv(csv_file)
        self.root_dir = root_dir
        self.transform = transform

    # region METHOD___len__ [DOMAIN(7): DocumentProcessing; CONCEPT(6): Method; TECH(6): Python]
    # endregion METHOD___init__
    def __len__(self) -> int:
        return len(self.label_loader)

    # region METHOD___getitem__ [DOMAIN(7): DocumentProcessing; CONCEPT(6): Method; TECH(6): Python]
    # endregion METHOD___len__
    def __getitem__(self, idx: torch.Tensor) -> Dict[str, str]:
        if torch.is_tensor(idx):
            idx = idx.tolist()

        img_name = os.path.join(self.root_dir, self.label_loader.iloc[idx, 0])
        image = io.imread(img_name)
        label = self.label_loader.iloc[idx, 1:]
        orientation = label["orientation"]
        orientation = orientation.astype("int")
        columns = label["columns"]
        columns = columns.astype("int")
        sample = {"image": image, "orientation": orientation, "columns": columns, "image_name": img_name}

        if self.transform:
            sample = self.transform(sample)

# endregion CLASS_DatasetImageOrient
        return sample


# region CLASS_DataLoaderImageOrient [DOMAIN(8): DocumentProcessing; CONCEPT(7): Reader; TECH(6): Python]
    # endregion METHOD___getitem__
class DataLoaderImageOrient(Dataset):
    """
    Class create torch DataLoader
    """
    # region METHOD___init__ [DOMAIN(7): DocumentProcessing; CONCEPT(6): Method; TECH(6): Python]
    def __init__(self) -> None:
        self.transform = transforms.Compose([TransformWithLabels()])
        self.classes = ("1", "2", "0", "90", "180", "270")

    # region METHOD_load_dataset [DOMAIN(7): DocumentProcessing; CONCEPT(6): Method; TECH(6): Python]
    # endregion METHOD___init__
    def load_dataset(self, csv_path: str, image_path: str, batch_size: int = 4) -> DataLoader:
        trainset = DatasetImageOrient(csv_file=csv_path, root_dir=image_path, transform=self.transform)
        trainloader = DataLoader(trainset, batch_size=batch_size, shuffle=True, num_workers=2)
        self.amount = len(trainset)

        return trainloader

    # region METHOD___len__ [DOMAIN(7): DocumentProcessing; CONCEPT(6): Method; TECH(6): Python]
    # endregion METHOD_load_dataset
    def __len__(self) -> int:
# endregion CLASS_DataLoaderImageOrient
        return self.amount

    # endregion METHOD___len__


# region MODULE_CONTRACT [DOMAIN(8): DocumentProcessing; CONCEPT(7): Reader_dataset_executor; TECH(6): Python, dedoc]
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
## CLASS [6][DatasetImageOrient reader/processor] => DatasetImageOrient
## CLASS [6][DataLoaderImageOrient reader/processor] => DataLoaderImageOrient
## @usecases
## - [read]: System (Pipeline) → ParseDocument(PDF) → UnstructuredDocument
def _module_contract():
    pass
# endregion MODULE_CONTRACT
# GREP_SUMMARY: dataset_executor, dedoc, reader, PDF, PdfReader, BaseReader, PDF, pdfminer, tabby, OCR, tables, image, txtlayer, columns, orientation, paragraphs, metadata, extraction, line, bbox, DatasetImageOrient, DataLoaderImageOrient
# STRUCTURE: ▶ Init ┌PDF file┐ → [DatasetImageOrient] ○ can_read? → ○ read → [__init__ → __len__ → __getitem__] → ⊕ UnstructuredDocument(lines, tables, attachments)
