# region MODULE_CONTRACT [DOMAIN(8): DocumentProcessing; CONCEPT(7): MLTraining; TECH(6): DatasetPreparation, PIL, numpy]
## @modulecontract
## @purpose To provide utilities for preparing training datasets from document processing results: saving LineWithMeta objects as JSON lines, merging lines with same BBox, and managing image/document paths for ML model training workflows.
## @scope Training dataset creation, line postprocessing (BBox deduplication), image path management, document path resolution.
## @input LineWithMeta objects, config dict, original document path.
## @output JSON lines files, image directories, document paths.
## @links [USES_API(6): PIL, numpy, json]
## @invariants
## - __postprocess_lines merges consecutive lines with identical bounding boxes.
## - save_line_with_meta always creates intermediate directories if they do not exist.
## @rationale
## Q: Why merge lines with identical BBox?
## A: Some readers produce multiple LineWithMeta fragments for the same visual region. Pre-merging simplifies annotation and reduces dataset noise.
## @changes
## LAST_CHANGE: [v1.0.0 – Added SEMANTIC TEMPLATE markup and LDD logging]
## @modulemap
## FUNC 3[numpy to PIL] => __to_pil
## FUNC 4[Create images path] => __create_images_path
## FUNC 5[Original documents path] => get_path_original_documents
## FUNC 4[Per-document images path] => _get_images_path
## FUNC 7[Save lines as JSON] => save_line_with_meta
## FUNC 6[Merge lines with same BBox] => __postprocess_lines
## FUNC 4[Get original document file path] => get_original_document_path
## @usecases
## - [save_line_with_meta]: DataPipeline → ExportTrainingData → Lines written to JSON lines file
def _module_contract():
    pass
# endregion MODULE_CONTRACT
# GREP_SUMMARY: training, dataset, JSON lines, LineWithMeta, bounding box, bbox deduplication, images path, document path
# STRUCTURE: ▶ ┌imports┐ → ⚡ save_line_with_meta: ┌lines, document, config┐ → create_images_path → postprocess_lines (merge same bbox) → ◇ write each line as JSON → ⎋ None; ⚡ __postprocess_lines: ┌lines┐ → ◇ loop: skip no-bbox, merge same as prev → ⎋ merged

import json
import logging
import os
from typing import List

import numpy as np
from PIL import Image

from dedoc.data_structures.line_with_meta import LineWithMeta

logger = logging.getLogger(__name__)


# region FUNC___to_pil [DOMAIN(4): ImageProcessing; CONCEPT(3): Conversion; TECH(3): PIL]
## @purpose To convert a numpy array to a PIL Image.
## @uses PIL.Image
## @io np.ndarray -> Image
## @complexity 2
def __to_pil(image: np.ndarray) -> Image:
    return Image.fromarray(image)
# endregion FUNC___to_pil


# region FUNC___create_images_path [DOMAIN(5): FileSystem; CONCEPT(4): PathManagement; TECH(3): os]
## @purpose To assert labeling mode is configured and create the intermediate data directory if missing.
## @io dict -> None
## @complexity 3
def __create_images_path(config: dict) -> None:
    assert config.get("labeling_mode")
    assert config.get("intermediate_data_path") is not None
    if not os.path.isdir(config.get("intermediate_data_path")):
        os.makedirs(config.get("intermediate_data_path"))
        logger.debug(f"[IMP:5][__create_images_path][CREATE] Created {config['intermediate_data_path']}")
# endregion FUNC___create_images_path


# region FUNC_get_path_original_documents [DOMAIN(5): FileSystem; CONCEPT(4): PathManagement; TECH(3): os]
## @purpose To resolve and create the directory path for original training documents.
## @io dict -> str
## @complexity 3
def get_path_original_documents(config: dict) -> str:
    path = os.path.join(config["intermediate_data_path"], "original_documents")
    os.makedirs(path, exist_ok=True)
    return path
# endregion FUNC_get_path_original_documents


# region FUNC__get_images_path [DOMAIN(5): FileSystem; CONCEPT(4): PathManagement; TECH(3): os]
## @purpose To resolve and create the per-document images directory for storing rendered page images.
## @uses get_path_original_documents
## @io (dict, str) -> str
## @complexity 3
def _get_images_path(config: dict, document_name: str) -> str:
    images_path = os.path.join(get_path_original_documents(config), document_name.split(".")[0])
    os.makedirs(images_path, exist_ok=True)
    return images_path
# endregion FUNC__get_images_path


# region FUNC_save_line_with_meta [DOMAIN(8): DocumentProcessing; CONCEPT(7): DatasetPreparation; TECH(6): JSON_serialization]
## @purpose To save a list of LineWithMeta objects as JSON lines in the training dataset, merging lines with identical bounding boxes before writing.
## @uses __create_images_path, __postprocess_lines
## @io (List[LineWithMeta], str, *, config: dict) -> None
## @complexity 5
def save_line_with_meta(lines: List[LineWithMeta], original_document: str, *, config: dict) -> None:
    __create_images_path(config)

    lines = __postprocess_lines(lines)

    logger.info(f"[IMP:7][save_line_with_meta][SAVE] Writing {len(lines)} lines for {original_document}")
    with open(os.path.join(config["intermediate_data_path"], "lines.jsonlines"), "a") as out:
        for line in lines:
            line_dict = json.loads(json.dumps(line, default=lambda o: o.__dict__, ensure_ascii=False))
            line_dict["original_document"] = os.path.basename(original_document)
            out.write(json.dumps(line_dict, ensure_ascii=False))
            out.write("\n")
# endregion FUNC_save_line_with_meta


# region FUNC___postprocess_lines [DOMAIN(7): DocumentProcessing; CONCEPT(6): BBoxDeduplication; TECH(5): AnnotationFiltering]
## @purpose To merge consecutive lines that share the same bounding box, reducing dataset fragmentation for ML training.
## @io List[LineWithMeta] -> List[LineWithMeta]
## @complexity 5
def __postprocess_lines(lines: List[LineWithMeta]) -> List[LineWithMeta]:
    postprocessed_lines = []
    prev_bbox = None
    for line in lines:
        bbox_annotations = [annotation for annotation in line.annotations if annotation.name == "bounding box"]
        if not bbox_annotations:
            postprocessed_lines.append(line)
            continue

        bbox = bbox_annotations[0].value
        if not prev_bbox or prev_bbox != bbox:
            postprocessed_lines.append(line)
            prev_bbox = bbox
            continue
        postprocessed_lines[-1] += line

    logger.debug(f"[IMP:5][__postprocess_lines][MERGE] Original: {len(lines)}, after merge: {len(postprocessed_lines)}")
    return postprocessed_lines
# endregion FUNC___postprocess_lines


# region FUNC_get_original_document_path [DOMAIN(5): FileSystem; CONCEPT(4): PathResolution; TECH(3): os]
## @purpose To resolve the full filesystem path to an original document from a page metadata entry.
## @io (str, List[dict]) -> str
## @complexity 2
def get_original_document_path(path2documents: str, page: List[dict]) -> str:
    return os.path.join(path2documents, page[0]["original_document"])
# endregion FUNC_get_original_document_path
