# region MODULE_CONTRACT [DOMAIN(8): DocumentProcessing; CONCEPT(7): ImageProcessing; TECH(7): PIL, opencv, numpy]
## @modulecontract
## @purpose To provide image manipulation utilities for the document processing pipeline: cropping, rotation, pixel frequency analysis, bounding box extraction, and text area detection.
## @scope Image cropping, rotation, edge detection, bounding box operations, image concatenation, text area isolation.
## @input numpy arrays, PIL Images, BBox objects.
## @output numpy arrays, PIL Images, BBox objects.
## @links [USES_API(8): PIL, numpy, opencv, scipy]
## @invariants
## - rotate_image always returns a non-cropped image with expanded dimensions.
## - crop_image_text always returns a valid BBox even on empty edges.
## - get_concat_v returns a single image if input list has length 1.
## @rationale
## Q: Why expand image bounds during rotation?
## A: Avoids information loss from corner clipping, which is critical for OCR quality.
## @changes
## LAST_CHANGE: [v1.0.0 – Added SEMANTIC TEMPLATE markup and LDD logging]
## @modulemap
## FUNC 6[Highest pixel frequency color] => get_highest_pixel_frequency
## FUNC 7[BBox crop + resize] => get_bbox_from_image
## FUNC 8[Image rotation with bound expansion] => rotate_image
## FUNC 7[Text area crop via Canny edges] => crop_image_text
## FUNC 5[Rectangle overlay on image] => draw_rectangle
## FUNC 5[Vertical image concatenation] => get_concat_v
## @usecases
## - [crop_image_text]: StructureExtractor → IsolateTextArea → Text BBox extracted
## - [rotate_image]: Preprocessor → DeskewImage → Rotated image ready for OCR
def _module_contract():
    pass
# endregion MODULE_CONTRACT
# GREP_SUMMARY: image, crop, rotate, bounding box, PIL, numpy, opencv, Canny, edge detection, text area, concatenation
# STRUCTURE: ▶ ┌imports: PIL, numpy, cv2, scipy┐ → ⚡ PixelFreq: ┌image┐ → unique counts → argmax → ⎋ color; ⚡ BBoxCrop: ┌image,bbox┐ → image.crop → resize → ⎋ Image; ⚡ Rotate: ┌image,angle┐ → getRotationMatrix2D → warpAffine → ⎋ rotated; ⚡ CropText: ┌image┐ → Canny → maximum_filter → edge_projection → ⎋ BBox

import logging
from copy import deepcopy
from typing import List, Tuple

import numpy as np
from PIL import Image, ImageDraw
from dedocutils.data_structures import BBox

logger = logging.getLogger(__name__)


# region FUNC_get_highest_pixel_frequency [DOMAIN(6): ImageProcessing; CONCEPT(5): ColorAnalysis; TECH(5): numpy]
## @purpose To find the most frequent pixel intensity in a grayscale image, avoiding black (0) and defaulting to white (255) for background detection.
## @uses numpy
## @io np.ndarray -> int
## @complexity 3
def get_highest_pixel_frequency(image: np.ndarray) -> int:
    unique, counts = np.unique(image.reshape(-1, 1), axis=0, return_counts=True)
    color = unique[np.argmax(counts)][0]
    if color == 0:
        color = np.uint8(255)

    logger.debug(f"[IMP:4][get_highest_pixel_frequency][RESULT] Highest freq color (non-black): {color}")
    return color
# endregion FUNC_get_highest_pixel_frequency


# region FUNC_get_bbox_from_image [DOMAIN(7): ImageProcessing; CONCEPT(6): Cropping; TECH(6): PIL]
## @purpose To extract a sub-region from an image by bounding box, with optional resizing for uniform downstream processing.
## @uses PIL.Image
## @io (Image.Image, BBox, Tuple[int,int]) -> Image.Image
## @complexity 4
def get_bbox_from_image(image: Image.Image, bbox: BBox, resize: Tuple[int, int] = (300, 15)) -> Image.Image:
    rectangle = (bbox.x_top_left, bbox.y_top_left, bbox.x_bottom_right, bbox.y_bottom_right)
    if isinstance(image, np.ndarray):
        image = Image.fromarray(image)
    cropped = image.crop(rectangle)
    if resize is not None:
        cropped = cropped.resize((300, 15)).convert("RGB")
    return cropped
# endregion FUNC_get_bbox_from_image


# region FUNC_rotate_image [DOMAIN(8): ImageProcessing; CONCEPT(7): Deskewing; TECH(7): opencv]
## @purpose To rotate an image by a given angle with automatic bound expansion, preventing corner cropping and preserving all content for OCR.
## @uses opencv
## @io (np.ndarray, float, Tuple[int,int,int]) -> np.ndarray
## @complexity 6
def rotate_image(image: np.ndarray, angle: float, color_bound: Tuple[int, int, int] = (255, 255, 255)) -> np.ndarray:
    import cv2

    height, width = image.shape[:2]
    image_center = (width / 2, height / 2)
    rotation_mat = cv2.getRotationMatrix2D(image_center, angle, 1.)

    abs_cos = abs(rotation_mat[0, 0])
    abs_sin = abs(rotation_mat[0, 1])

    bound_w = int(height * abs_sin + width * abs_cos)
    bound_h = int(height * abs_cos + width * abs_sin)

    rotation_mat[0, 2] += bound_w / 2 - image_center[0]
    rotation_mat[1, 2] += bound_h / 2 - image_center[1]

    rotated_mat = cv2.warpAffine(image, rotation_mat, (bound_w, bound_h), borderMode=cv2.BORDER_CONSTANT, borderValue=color_bound)
    logger.debug(f"[IMP:5][rotate_image][ROTATE] Angle={angle}, input_shape={(height,width)}, output_shape={(bound_h,bound_w)}")
    return rotated_mat
# endregion FUNC_rotate_image


# region FUNC_crop_image_text [DOMAIN(8): ImageProcessing; CONCEPT(7): TextAreaDetection; TECH(7): opencv, scipy]
## @purpose To detect the bounding box of text content in an image using Canny edge detection and maximum filtering, cropping out empty margins.
## @uses opencv, scipy.ndimage.maximum_filter
## @io np.ndarray -> BBox
## @complexity 7
def crop_image_text(image: np.ndarray) -> BBox:
    import cv2
    from scipy.ndimage import maximum_filter

    im_height, im_width = image.shape[0], image.shape[1]
    edges = cv2.Canny(image, 100, 200)
    edges = maximum_filter(edges, (10, 10))
    y_sum = np.arange(edges.shape[0])[edges.max(axis=1) > 0]
    x_sum = np.arange(edges.shape[1])[edges.max(axis=0) > 0]
    if y_sum.shape[0] > 0 and x_sum.shape[0] > 0:
        y_top = max(0, y_sum.min() - 10)
        y_bottom = min(im_height, y_sum.max() + 10)
        x_top = max(0, x_sum.min() - 10)
        x_bottom = min(im_width, x_sum.max() + 10)
        bbox = BBox(x_top, y_top, x_bottom - x_top, y_bottom - y_top)
        logger.debug(f"[IMP:5][crop_image_text][DETECT] Text BBox: ({x_top},{y_top}) {x_bottom-x_top}x{y_bottom-y_top}")
        return bbox
    else:
        logger.debug(f"[IMP:5][crop_image_text][FALLBACK] No edges found, returning full image BBox")
        return BBox(x_top_left=0, y_top_left=0, width=im_width, height=im_height)
# endregion FUNC_crop_image_text


# region FUNC_draw_rectangle [DOMAIN(5): ImageProcessing; CONCEPT(4): Annotation; TECH(5): PIL]
## @purpose To draw a colored rectangle outline on an image, used for visualizing detected bounding boxes in debug/demo outputs.
## @uses PIL.ImageDraw, deepcopy
## @io (Image.Image, int, int, int, int, Tuple[int,int,int]) -> np.ndarray
## @complexity 3
def draw_rectangle(image: Image.Image, x_top_left: int, y_top_left: int, width: int, height: int, color: Tuple[int, int, int] = (0, 0, 0)) -> np.ndarray:
    if color == "black":
        color = (0, 0, 0)
    source_img = deepcopy(image).convert("RGBA")

    draw = ImageDraw.Draw(source_img)
    x_bottom_right = x_top_left + width + 5
    y_bottom_right = y_top_left + height + 5
    start_point = (x_top_left - 5, y_top_left - 5)
    end_point = (x_bottom_right, y_bottom_right)
    draw.rectangle((start_point, end_point), outline=color, width=5)

    return np.array(source_img)
# endregion FUNC_draw_rectangle


# region FUNC_get_concat_v [DOMAIN(5): ImageProcessing; CONCEPT(4): Composition; TECH(5): PIL]
## @purpose To vertically concatenate a list of PIL images into a single combined image, preserving the maximum width.
## @uses PIL.Image
## @io List[Image.Image] -> Image.Image
## @complexity 3
def get_concat_v(images: List[Image.Image]) -> Image.Image:
    if len(images) == 1:
        return images[0]
    width = max((image.width for image in images))
    height = sum((image.height for image in images))
    dst = Image.new("RGB", (width, height))
    height = 0
    for image in images:
        dst.paste(image, (0, height))
        height += image.height
    return dst
# endregion FUNC_get_concat_v
