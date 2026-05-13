import logging
from typing import Optional

from dedoc.converters.concrete_converters.abstract_converter import AbstractConverter

logger = logging.getLogger(__name__)


# region CLASS_BinaryConverter [DOMAIN(9): DocumentProcessing; CONCEPT(8): Conversion, ImageToPng; TECH(7): PythonDelegation]
## @purpose To convert binary blob files (mime=application/octet-stream) that carry image-like extensions (.bmp, .jpg, .tiff, etc.) into PNG by delegating to PNGConverter.
class BinaryConverter(AbstractConverter):
    """
    Converts image-like documents with `mime=application/octet-stream` into PNG.
    Look to the :class:`~dedoc.converters.AbstractConverter` documentation to get the information about the methods' parameters.
    """

    # region METHOD___init__ [DOMAIN(8): Initialization; CONCEPT(7): DependencyInjection; TECH(6): PythonConstructor]
    ## @purpose To initialize the converter and its internal PNGConverter delegate.
    ## @uses PNGConverter
    ## @io config: Optional[dict] -> None
    ## @complexity 2
    def __init__(self, *, config: Optional[dict] = None) -> None:
        from dedoc.converters.concrete_converters.png_converter import PNGConverter
        super().__init__(config=config)
        self.png_converter = PNGConverter(config=self.config)
        logger.debug(f"[IMP:4][BinaryConverter][INIT] Initialized with PNGConverter delegate")
    # endregion METHOD___init__

    # region METHOD_can_convert [DOMAIN(9): DocumentProcessing; CONCEPT(8): FormatDetection; TECH(7): MimeExtension]
    ## @purpose To detect image-like binary files by checking for mime=application/octet-stream combined with a known image extension.
    ## @uses get_mime_extension, supported_image_types
    ## @io file_path: Optional[str], extension: Optional[str], mime: Optional[str], parameters: Optional[dict] -> bool
    ## @complexity 3
    def can_convert(self,
                    file_path: Optional[str] = None,
                    extension: Optional[str] = None,
                    mime: Optional[str] = None,
                    parameters: Optional[dict] = None) -> bool:
        """
        Checks if the document is image-like (e.g. it has .bmp, .jpg, .tiff, etc. extension) and has `mime=application/octet-stream`.
        """
        from dedoc.utils import supported_image_types
        from dedoc.utils.utils import get_mime_extension

        mime, extension = get_mime_extension(file_path=file_path, mime=mime, extension=extension)
        result = mime == "application/octet-stream" and extension in supported_image_types
        logger.debug(f"[IMP:6][BinaryConverter][CAN_CONVERT] mime={mime}, extension={extension} => {result}")
        return result
    # endregion METHOD_can_convert

    # region METHOD_convert [DOMAIN(9): DocumentProcessing; CONCEPT(9): Conversion, ImageToPng; TECH(7): Delegation]
    ## @purpose To convert an image-like binary file to PNG by delegating to the internal PNGConverter.
    ## @uses PNGConverter.convert
    ## @io file_path: str, parameters: Optional[dict] -> str
    ## @complexity 2
    def convert(self, file_path: str, parameters: Optional[dict] = None) -> str:
        """
        Convert the image-like and application/octet-stream documents into files with .png extension.
        """
        logger.info(f"[IMP:7][BinaryConverter][CONVERT] Delegating to PNGConverter for file_path={file_path}")
        result = self.png_converter.convert(file_path, parameters=parameters)
        logger.info(f"[IMP:9][BinaryConverter][RESULT] Converted to {result}")
        return result
    # endregion METHOD_convert
# endregion CLASS_BinaryConverter

# region MODULE_CONTRACT [DOMAIN(9): DocumentProcessing; CONCEPT(8): Conversion, ImageToPng; TECH(7): PythonDelegation]
## @modulecontract
## @purpose To handle binary blob files (octet-stream) that are actually images by detecting their extension and delegating conversion to PNGConverter.
## @scope Binary image detection (mime + extension heuristic), PNG conversion delegation.
## @input File with mime=application/octet-stream and image extension.
## @output Converted PNG file path.
## @links [USES_API(9): dedoc.converters.concrete_converters.png_converter.PNGConverter; READS_DATA_FROM(7): dedoc.utils.supported_image_types]
## @invariants
## - can_convert() returns True ONLY when mime is octet-stream AND extension is a known image type.
## - convert() always delegates to PNGConverter.
## @rationale
## Q: Why a separate BinaryConverter instead of extending PNGConverter?
## A: Some systems report images as octet-stream. The heuristic keeps PNGConverter focused on true image MIMEs and isolates the edge case.
## @changes
## LAST_CHANGE: [v1.0.0 — Added semantic markup and LDD logging]
## @modulemap
## CLASS 8[Converts binary-blob images to PNG via delegation] => BinaryConverter
## @usecases
## - [BinaryConverter.convert]: User (Upload) → DetectBinaryImage → ConvertToPng
def _module_contract():
    pass
# endregion MODULE_CONTRACT
# GREP_SUMMARY: binary converter, octet-stream, image conversion, PNG, delegation, mime detection
# STRUCTURE: ▶ ┌file┐ → ◇ can_convert:〈mime=octet-stream ∧ ext∈images ? T/F〉 → ⚡ convert → ⟦PNGConverter⟧ → ⊕ png_path → ⎋ result
