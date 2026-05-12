import logging
from typing import Optional

from dedoc.common.exceptions.conversion_error import ConversionError
from dedoc.converters.concrete_converters.abstract_converter import AbstractConverter

logger = logging.getLogger(__name__)


# region CLASS_PNGConverter [DOMAIN(9): DocumentProcessing; CONCEPT(9): Conversion, ImageToPng; TECH(8): PIL, OpenCV]
## @purpose To convert image documents (.bmp, .jpg, .tiff, .hdr, etc.) into the PNG format using PIL (Pillow) for standard images and OpenCV for exotic formats.
class PNGConverter(AbstractConverter):
    """
    Converts image-like (.bmp, .jpg, .tiff, etc.) documents into PNG.
    Look to the :class:`~dedoc.converters.AbstractConverter` documentation to get the information about the methods' parameters.
    """

    # region METHOD___init__ [DOMAIN(8): Initialization; CONCEPT(7): Configuration; TECH(6): PythonConstructor]
    ## @purpose To initialize the converter with image-like extension and MIME type registries from the global extensions configuration.
    ## @uses converted_extensions, converted_mimes
    ## @io config: Optional[dict] -> None
    ## @complexity 2
    def __init__(self, *, config: Optional[dict] = None) -> None:
        from dedoc.extensions import converted_extensions, converted_mimes
        super().__init__(config=config, converted_extensions=converted_extensions.image_like_format, converted_mimes=converted_mimes.image_like_format)
        logger.debug(f"[IMP:4][PNGConverter][INIT] Registered image-like formats")
    # endregion METHOD___init__

    # region METHOD_convert [DOMAIN(9): DocumentProcessing; CONCEPT(9): Conversion, ImageToPng; TECH(8): PIL, OpenCV, ImageIO]
    ## @purpose To convert an image file to PNG: uses OpenCV (cv2) for exotic formats (.hdr, .pic, .sr, .ras, .j2k) and PIL/Pillow for all other image types.
    ## @uses cv2, PIL.Image, UnidentifiedImageError, os, splitext_, ConversionError
    ## @io file_path: str, parameters: Optional[dict] -> str
    ## @complexity 5
    def convert(self, file_path: str, parameters: Optional[dict] = None) -> str:
        """
        Convert the image-like documents into files with .png extension.
        """
        import os
        import cv2
        from PIL import Image, UnidentifiedImageError
        from dedoc.utils.utils import splitext_

        file_dir, file_name = os.path.split(file_path)
        name_wo_ext, extension = splitext_(file_name)
        converted_file_path = os.path.join(file_dir, f"{name_wo_ext}.png")
        logger.debug(f"[IMP:4][PNGConverter][CONVERT] file_path={file_path}, extension={extension}, target={converted_file_path}")

        if extension.lower() in [".hdr", ".pic", ".sr", ".ras", ".j2k"]:
            logger.info(f"[IMP:7][PNGConverter][CONVERT_CV2] Using OpenCV for exotic format extension={extension}")
            img = cv2.imread(file_path)
            cv2.imwrite(converted_file_path, img)
        else:
            try:
                logger.debug(f"[IMP:5][PNGConverter][CONVERT_PIL] Using PIL for extension={extension}")
                img = Image.open(file_path)
            except UnidentifiedImageError as e:
                logger.critical(f"[IMP:10][PNGConverter][CONVERT_FAIL] Could not identify image file={file_name}, error={e}")
                raise ConversionError(msg=f"Could not convert file {file_name} ({e})")
            img.save(converted_file_path)

        logger.info(f"[IMP:9][PNGConverter][RESULT] Converted to {converted_file_path}")
        return converted_file_path
    # endregion METHOD_convert
# endregion CLASS_PNGConverter

# region MODULE_CONTRACT [DOMAIN(9): DocumentProcessing; CONCEPT(9): Conversion, ImageToPng; TECH(8): PIL, OpenCV]
## @modulecontract
## @purpose To normalize various image formats (.bmp, .jpg, .tiff, .hdr, .pic, .sr, .ras, .j2k) into PNG, using OpenCV for exotic formats unsupported by PIL and Pillow for standard images.
## @scope Image format normalization to PNG via PIL/OpenCV.
## @input Image files with image-like extensions.
## @output Converted .png file path.
## @links [USES_API(8): PIL (Pillow), OpenCV (cv2); READS_DATA_FROM(7): dedoc.extensions.converted_extensions]
## @invariants
## - Exotic formats (.hdr, .pic, .sr, .ras, .j2k) always use OpenCV path.
## - Other formats always use PIL path with UnidentifiedImageError handling.
## - Output file path is always {dir}/{name_wo_ext}.png.
## @rationale
## Q: Why two separate image libraries (PIL + OpenCV)?
## A: PIL cannot read exotic HDR/radiance formats. OpenCV provides fallback for these edge cases without a heavyweight dependency like ImageMagick.
## @changes
## LAST_CHANGE: [v1.0.0 — Added semantic markup and LDD logging]
## @modulemap
## CLASS 9[Converts images to PNG via PIL or OpenCV] => PNGConverter
## @usecases
## - [PNGConverter.convert]: User (Upload) → NormalizeImageToPng → PngFileReady
def _module_contract():
    pass
# endregion MODULE_CONTRACT
# GREP_SUMMARY: png converter, image conversion, PIL, Pillow, OpenCV, cv2, hdr, pic, sr, ras, j2k, UnidentifiedImageError
# STRUCTURE: ▶ ┌file_path┐ → ◇ extension in [.hdr,.pic,.sr,.ras,.j2k] ? ⚡ cv2.imread → cv2.imwrite : ⟦PIL.Image.open → img.save⟧ → ⊕ UnidentifiedImageError? ConversionError → ⎋ .png path
