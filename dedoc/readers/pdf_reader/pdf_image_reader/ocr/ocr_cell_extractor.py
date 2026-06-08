import logging
import os
from typing import Iterator, List, Optional, Tuple

import cv2
import numpy as np
from dedocutils.data_structures import BBox

from dedoc.data_structures.concrete_annotations.bbox_annotation import BBoxAnnotation
from dedoc.data_structures.concrete_annotations.confidence_annotation import ConfidenceAnnotation
from dedoc.data_structures.line_metadata import LineMetadata
from dedoc.data_structures.line_with_meta import LineWithMeta
from dedoc.readers.pdf_reader.pdf_image_reader.ocr.ocr_engine_abstract import OCREngineAbstract, OCRResult
from dedoc.readers.pdf_reader.pdf_image_reader.ocr.ocr_line_extractor import OCRLineExtractor
from dedoc.utils.image_utils import get_highest_pixel_frequency
from dedoc.utils.parameter_utils import get_path_param


# region CLASS_OCRCellExtractor [DOMAIN(8): DocumentProcessing; CONCEPT(7): Reader; TECH(6): Python]
class OCRCellExtractor:
    """Extract text from table cell images using an OCR engine.

    Handles batching of cell images, concatenation for efficient OCR
    processing, and reconstruction of cell-level :class:`~dedoc.data_structures.line_with_meta.LineWithMeta`
    objects with bounding box and confidence annotations.
    """

    # region METHOD___init__ [DOMAIN(7): DocumentProcessing; CONCEPT(6): Method; TECH(6): Python]
    def __init__(self, *, config: dict, engine: "OCREngineAbstract" = None) -> None:
        """Initialize the cell extractor.

        Args:
            config: Dedoc configuration dictionary.
            engine: An OCR engine instance. Falls back to
                :class:`~dedoc.readers.pdf_reader.pdf_image_reader.ocr.tesseract_ocr_engine.TesseractOCREngine` when ``None``.
        """
        self.config = config
        if engine is None:
            from dedoc.readers.pdf_reader.pdf_image_reader.ocr.tesseract_ocr_engine import TesseractOCREngine
            engine = TesseractOCREngine(config=config)
        self.engine = engine
        self.line_extractor = OCRLineExtractor(config=config, engine=engine)
        self.logger = config.get("logger", logging.getLogger())

    # region METHOD_get_cells_text [DOMAIN(7): DocumentProcessing; CONCEPT(6): Method; TECH(6): Python]
    # endregion METHOD___init__
    def get_cells_text(self, page_image: np.ndarray, tree_nodes: List["TableTree"], language: str) -> List[List[LineWithMeta]]:  # noqa
        """Extract text from all table cells in a page image.

        Sorts table nodes by crop box width (descending), batches them
        for efficient OCR, then maps recognized lines back to individual
        cells and produces :class:`~dedoc.data_structures.line_with_meta.LineWithMeta` objects.

        Args:
            page_image: Full page image as a numpy array.
            tree_nodes: List of table tree nodes to process.
            language: OCR language string.

        Returns:
            List of lists, where each inner list contains LineWithMeta
            objects for one table cell.
        """
        for node in tree_nodes:
            node.set_crop_text_box(page_image)

        tree_nodes.sort(key=lambda t: -t.crop_text_box.width)
        originalbox_to_fastocrbox = {}
        batches = list(self.__nodes2batch(tree_nodes))
        for num_batch, nodes_batch in enumerate(batches):

            if self.config.get("debug_mode", False):
                tmp_dir = os.path.join(get_path_param(self.config, "path_debug"), "debug_tables/batches/")
                os.makedirs(tmp_dir, exist_ok=True)
                for i, table_tree_node in enumerate(nodes_batch):
                    cv2.imwrite(os.path.join(tmp_dir, f"image_{num_batch}_{i}.png"), BBox.crop_image_by_box(page_image, table_tree_node.cell_box))

            ocr_result, chunk_boxes = self.__handle_one_batch(src_image=page_image, tree_table_nodes=nodes_batch, num_batch=num_batch, language=language)

            for chunk_index, _ in enumerate(chunk_boxes):
                originalbox_to_fastocrbox[nodes_batch[chunk_index].cell_box] = []

            # we find mapping
            for line in list(ocr_result.lines):
                chunk_index = 0
                line_center_y = line.bbox.y_top_left + int(line.bbox.height / 2)
                while chunk_index < len(chunk_boxes) and line_center_y > chunk_boxes[chunk_index].y_top_left:
                    chunk_index += 1
                chunk_index -= 1

                # save bbox mapping:
                for word in line.words:
                    # do relative coordinates (inside cell_image)
                    word.bbox.y_top_left -= chunk_boxes[chunk_index].y_top_left
                    word.bbox.x_top_left -= chunk_boxes[chunk_index].x_top_left
                    # do absolute coordinate on src_image (inside src_image)
                    word.bbox.y_top_left += nodes_batch[chunk_index].crop_text_box.y_top_left
                    word.bbox.x_top_left += nodes_batch[chunk_index].crop_text_box.x_top_left

                originalbox_to_fastocrbox[nodes_batch[chunk_index].cell_box].append(line.words)

        return self.__create_lines_with_meta(tree_nodes, originalbox_to_fastocrbox, page_image)

    # region METHOD___handle_one_batch [DOMAIN(7): DocumentProcessing; CONCEPT(6): Method; TECH(6): Python]
    # endregion METHOD_get_cells_text
    def __handle_one_batch(self, src_image: np.ndarray, tree_table_nodes: List["TableTree"], num_batch: int, language: str = "rus") \
            -> Tuple[OCRResult, List[BBox]]:  # noqa
        """Run OCR on a batch of concatenated cell images.

        Args:
            src_image: Source page image.
            tree_table_nodes: Nodes belonging to this batch.
            num_batch: Batch index (used for debug output).
            language: OCR language string.

        Returns:
            Tuple of (OCRResult, list of BBox chunk boundaries).
        """
        concatenated, chunk_boxes = self.__concat_images(src_image=src_image, tree_table_nodes=tree_table_nodes)
        if self.config.get("debug_mode", False):
            debug_dir = os.path.join(get_path_param(self.config, "path_debug"), "debug_tables", "batches")
            os.makedirs(debug_dir, exist_ok=True)
            image_path = os.path.join(debug_dir, f"stacked_batch_image_{num_batch}.png")
            cv2.imwrite(image_path, concatenated)
        ocr_result = self.engine.recognize_cells(image=concatenated, language=language)

        return ocr_result, chunk_boxes

    # region METHOD___concat_images [DOMAIN(7): DocumentProcessing; CONCEPT(6): Method; TECH(6): Python]
    # endregion METHOD___handle_one_batch
    def __concat_images(self, src_image: np.ndarray, tree_table_nodes: List["TableTree"]) -> Tuple[np.ndarray, List[BBox]]:  # noqa
        """Concatenate multiple cell images into a single stacked image.

        Cells are stacked vertically with a small spacing. The resulting
        image is passed to the OCR engine for batched recognition.

        Args:
            src_image: Source page image from which to crop cells.
            tree_table_nodes: Table nodes whose crop boxes define the
                cell regions.

        Returns:
            Tuple of (stacked image array, list of BBox chunk boundaries).
        """
        space = 10
        width = max((tree_node.crop_text_box.width + space for tree_node in tree_table_nodes))
        height = sum((tree_node.crop_text_box.height + space for tree_node in tree_table_nodes))
        # new_im = Image.fromarray(np.zeros((height, width), dtype=np.uint8) + 255)
        stacked_image = np.full((height, width), fill_value=255, dtype=np.uint8)

        y_prev = 0
        chunk_boxes = []
        for tree_node in tree_table_nodes:
            x_coord = space
            cell_image = BBox.crop_image_by_box(src_image, tree_node.crop_text_box)
            if self.config.get("debug_mode", False):
                debug_dir = os.path.join(get_path_param(self.config, "path_debug"), "debug_tables", "batches")
                os.makedirs(debug_dir, exist_ok=True)
                image_path = os.path.join(debug_dir, "cell_croped.png")
                cv2.imwrite(image_path, cell_image)
            cell_height, cell_width = cell_image.shape[0], cell_image.shape[1]

            stacked_image[y_prev:y_prev + cell_height, x_coord:x_coord + cell_width] = cell_image
            # new_im.paste(image, (x_coord, y_coord))
            # y_coord += cell_image.shape[1] + space
            inserted_image_height = cell_height + space
            chunk_boxes.append(BBox(x_top_left=x_coord, y_top_left=y_prev, width=width - x_coord, height=inserted_image_height))
            # borders.append((y_prev, y_coord))
            y_prev += inserted_image_height

        assert len(chunk_boxes) == len(tree_table_nodes)
        return stacked_image, chunk_boxes

    # region METHOD___nodes2batch [DOMAIN(7): DocumentProcessing; CONCEPT(6): Method; TECH(6): Python]
    # endregion METHOD___concat_images
    def __nodes2batch(self, tree_nodes: List["TableTree"]) -> Iterator[List["TableTree"]]:  # noqa
        """Group table nodes into batches for efficient OCR processing.

        A new batch is started when the cumulative area
        (width * height) exceeds 10⁷ or when the widest node is more
        than 1.5 times wider than the current node.

        Args:
            tree_nodes: All table tree nodes to batch.

        Yields:
            Lists of TableTree nodes comprising one batch.
        """
        batch = []
        width = 0
        height = 0
        for node in tree_nodes:
            image_height, image_width = node.crop_text_box.height, node.crop_text_box.width
            width = max(width, image_width)
            height += image_height
            if (width * height > 10 ** 7 or width > 1.5 * image_width) and len(batch) > 0:
                yield batch
                batch = []
                width = 0
                height = 0
            batch.append(node)
        if len(batch) > 0:
            yield batch

    # region METHOD___create_lines_with_meta [DOMAIN(7): DocumentProcessing; CONCEPT(6): Method; TECH(6): Python]
    # endregion METHOD___nodes2batch
    def __create_lines_with_meta(self, tree_nodes: List["TableTree"], original_box_to_fast_ocr_box: dict, original_image: np.ndarray) \
            -> List[List[LineWithMeta]]:  # noqa
        """Build LineWithMeta objects from OCR output for each cell.

        Aggregates per-cell word lists into :class:`~dedoc.data_structures.line_with_meta.LineWithMeta` objects
        with bounding box and confidence annotations, one list per cell.

        Args:
            tree_nodes: All processed table tree nodes.
            original_box_to_fast_ocr_box: Mapping from cell box to list
                of word lists (one per OCR line in that cell).
            original_image: The source page image (for bbox annotation
                dimensions).

        Returns:
            List of lists of LineWithMeta, one inner list per cell.
        """
        nodes_lines = []

        for node in tree_nodes:
            # create new line
            cell_lines = []

            for line in original_box_to_fast_ocr_box[node.cell_box]:  # step inside results of fast-ocr
                text_line = OCRCellExtractor.get_line_with_meta("")
                for word in line:
                    # add space between words
                    if len(text_line) != 0:
                        text_line += OCRCellExtractor.get_line_with_meta(" ", bbox=word.bbox, image=original_image)
                    # add confidence value
                    text_line += OCRCellExtractor.get_line_with_meta(text=word.text, bbox=word.bbox, image=original_image,
                                                                     confidences=[
                                                                         ConfidenceAnnotation(start=0, end=len(word.text), value=word.confidence / 100.)
                                                                     ])
                if len(text_line) > 0:  # add new line
                    cell_lines.append(text_line)

            nodes_lines.append(cell_lines)

        return nodes_lines

    # endregion METHOD___create_lines_with_meta
    @staticmethod
    # region METHOD_get_line_with_meta [DOMAIN(7): DocumentProcessing; CONCEPT(6): Method; TECH(6): Python]
    def get_line_with_meta(text: str,
                           bbox: Optional[BBox] = None,
                           image: Optional[np.ndarray] = None,
                           confidences: Optional[List[ConfidenceAnnotation]] = None) -> LineWithMeta:
        """Build a LineWithMeta from raw text and optional annotations.

        Args:
            text: The line text.
            bbox: Optional bounding box of the line.
            image: The source image (required when *bbox* is given).
            confidences: Optional list of confidence annotations.

        Returns:
            A fully constructed LineWithMeta.
        """
        annotations = []

        if bbox:
            assert image is not None, "BBox and image arguments should be both specified"
            height, width = image.shape[:2]
            annotations.append(BBoxAnnotation(0, len(text), bbox, page_height=height, page_width=width))

        confidences = [] if confidences is None else confidences
        for confidence in confidences:
            annotations.append(ConfidenceAnnotation(confidence.start, confidence.end, str(confidence.value)))

        return LineWithMeta(line=text, metadata=LineMetadata(page_id=0, line_id=None), annotations=annotations)

    # endregion METHOD_get_line_with_meta
    @staticmethod
    # region METHOD_upscale [DOMAIN(7): DocumentProcessing; CONCEPT(6): Method; TECH(6): Python]
    def upscale(image: Optional[np.ndarray], padding_px: int = 40) -> Tuple[Optional[np.ndarray], int]:
        """Add padding around a cell image to improve OCR accuracy.

        Fills the padding region with the most frequent pixel colour
        in the original image.

        Args:
            image: Input cell image.
            padding_px: Total padding in pixels (default 40).

        Returns:
            Tuple of (padded image, half-padding offset).
        """
        if image is None or sum(image.shape) < 5:
            return image, 0

        color_backgr = get_highest_pixel_frequency(image)

        if len(image.shape) == 2:
            bigger_cell = np.full((image.shape[0] + padding_px, image.shape[1] + padding_px), color_backgr)
            bigger_cell[padding_px // 2:-padding_px // 2, padding_px // 2:-padding_px // 2] = image
        else:
            bigger_cell = np.full((image.shape[0] + padding_px, image.shape[1] + padding_px, 3), color_backgr)
            bigger_cell[padding_px // 2:-padding_px // 2, padding_px // 2:-padding_px // 2, :] = image

        return bigger_cell, padding_px // 2
    # endregion METHOD_upscale
# endregion CLASS_OCRCellExtractor


# region MODULE_CONTRACT [DOMAIN(8): DocumentProcessing; CONCEPT(7): Reader_ocr_cell_extractor; TECH(6): Python, dedoc]
## @modulecontract
## @purpose Read and parse PDF documents, extracting lines with metadata, tables, and attachments into UnstructuredDocument.
## @scope OCR processing pipeline for document images.
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
## CLASS [16][OCRCellExtractor reader/processor] => OCRCellExtractor
## @usecases
## - [read]: System (Pipeline) → ParseDocument(PDF) → UnstructuredDocument
def _module_contract():
    pass
# endregion MODULE_CONTRACT
# GREP_SUMMARY: ocr_cell_extractor, dedoc, reader, OCR, tables, image, OCRCellExtractor, OCREngineAbstract, DI, Strategy, cell extraction
# STRUCTURE: ▶ Init ┌config + engine┐ → [OCRCellExtractor] ○ get_cells_text → __handle_one_batch → engine.recognize_cells() → ⊕ OCRResult → __create_lines_with_meta → ∑ List[List[LineWithMeta]]
