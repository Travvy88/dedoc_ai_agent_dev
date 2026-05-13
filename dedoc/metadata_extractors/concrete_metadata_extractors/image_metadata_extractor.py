# region MODULE_CONTRACT [DOMAIN(8): DocumentProcessing, MetadataExtraction; CONCEPT(7): EXIFFormat, ImageMetadata; TECH(7): PIL, piexif]
## @modulecontract
## @purpose To extract EXIF metadata from images (JPG, TIFF, etc.) and merge it with base file metadata — decodes fields like camera make/model, dates, resolution, and EXIF version.
## @scope Image EXIF metadata extraction: camera info, date/time, resolution, orientation, user comments.
## @input file_path via extract(), config with recognized image formats.
## @output dict merging BaseMetadataExtractor fields + EXIF-derived fields (date_time, make, model, exif_version, orientation, etc.).
## @links [USES_API(8): BaseMetadataExtractor, PIL.ExifTags, PIL.Image, piexif.load]
## @invariants
## - _get_exif NEVER raises — on any error returns {"broken_image": True}.
## - All EXIF values are encoded/parsed through type-specific helper methods (__encode_exif, __parse_int, __parse_date, __parse_float).
## @rationale
## Q: Why use piexif.load instead of PIL's built-in _getexif()?
## A: piexif provides a standardized EXIF dictionary format that is easier to map to specific keys, and handles vendor-specific EXIF quirks better.
## @changes
## LAST_CHANGE: [v1.0.0 — Semantic template markup and LDD logging added.]
## @modulemap
## CLASS 8[Image EXIF metadata extractor] => ImageMetadataExtractor
## @usecases
## - [ImageMetadataExtractor]: MetadataExtractorComposition → ExtractImage → MergeBaseAndExif → MetadataDict
def _module_contract():
    pass
# endregion MODULE_CONTRACT
# GREP_SUMMARY: image, EXIF, metadata, PIL, piexif, make, model, date_time, orientation, resolution, camera
# STRUCTURE: ▶ CLASS ImageMetadataExtractor(ABC): ■ __init__ ┌EXIF keys map + base_extractor┐ → ⚡ extract ┌base ⊕ exif_fields┐ → _get_exif ┌PIL.Image → piexif.load → encoded dict┐ → ○ helpers: __encode_exif | __parse_int | __parse_date | __parse_float

from typing import Optional, Union

from dedoc.metadata_extractors.abstract_metadata_extractor import AbstractMetadataExtractor
from dedoc.metadata_extractors.concrete_metadata_extractors.base_metadata_extractor import BaseMetadataExtractor


# region CLASS_ImageMetadataExtractor [DOMAIN(8): DocumentProcessing, MetadataExtraction; CONCEPT(7): EXIFFormat, ImageMetadata; TECH(7): PIL, piexif]
## @purpose To extract EXIF metadata from image files using PIL + piexif, decode fields via type-specific helpers, and merge with base OS file metadata.
class ImageMetadataExtractor(AbstractMetadataExtractor):
    # region METHOD_init [DOMAIN(7): Configuration; CONCEPT(6): Constructor, EXIFKeyMapping; TECH(6): PythonDicts]
    ## @purpose To register image-format extensions/MIMEs, define the EXIF key mapping (EXIF tag → field name + decode function), and instantiate a BaseMetadataExtractor delegate.
    ## @uses dedoc.extensions, BaseMetadataExtractor
    ## @io Optional[dict] -> None
    ## @complexity 5
    def __init__(self, *, config: Optional[dict] = None) -> None:
        from dedoc.extensions import recognized_extensions, recognized_mimes
        super().__init__(config=config, recognized_extensions=recognized_extensions.image_like_format, recognized_mimes=recognized_mimes.image_like_format)
        self.keys = {
            "DateTime": ("date_time", self.__parse_date),
            "DateTimeDigitized": ("date_time_digitized", self.__parse_date),
            "DateTimeOriginal": ("date_time_original", self.__parse_date),
            "DigitalZoomRatio": ("digital_zoom_ratio", self.__parse_float),
            "ExifImageHeight": ("exif_image_height", self.__parse_int),
            "ExifImageWidth": ("exif_image_width", self.__parse_int),
            "ExifVersion": ("exif_version", self.__encode_exif),
            "LightSource": ("light_source", self.__parse_int),
            "Make": ("make", self.__encode_exif),
            "Model": ("model", self.__encode_exif),
            "Orientation": ("orientation", self.__parse_int),
            "ResolutionUnit": ("resolution_unit", self.__parse_int),
            "Software": ("software", self.__encode_exif),
            "SubjectDistanceRange": ("subject_distance_range", self.__parse_int),
            "UserComment": ("user_comment", self.__encode_exif)
        }
        self.base_extractor = BaseMetadataExtractor(config=config)
        self.logger.debug(f"[IMP:4][ImageMetadataExtractor][INIT] EXIF keys configured: {len(self.keys)} fields")
    # endregion METHOD_init

    # region METHOD_extract [DOMAIN(8): MetadataExtraction; CONCEPT(7): DataMerge; TECH(6): PythonDicts]
    ## @purpose To combine base OS file metadata with EXIF image metadata into a single result dictionary.
    ## @uses BaseMetadataExtractor.extract, _get_exif
    ## @io str × Optional[str] × Optional[str] × Optional[dict] -> dict
    ## @complexity 5
    def extract(self,
                file_path: str,
                converted_filename: Optional[str] = None,
                original_filename: Optional[str] = None,
                parameters: Optional[dict] = None) -> dict:
        """
        Add the predefined list of metadata for images.
        Look to the :meth:`~dedoc.metadata_extractors.AbstractMetadataExtractor.extract` documentation to get the information about parameters.
        """
        import os

        file_dir, file_name, converted_filename, original_filename = self._get_names(file_path, converted_filename, original_filename)
        base_fields = self.base_extractor.extract(
            file_path=file_path, converted_filename=converted_filename, original_filename=original_filename, parameters=parameters
        )
        self.logger.debug(f"[IMP:5][ImageMetadataExtractor][BASE_DONE] Base fields: {sorted(base_fields.keys())}")

        exif_fields = self._get_exif(os.path.join(file_dir, converted_filename))
        self.logger.info(f"[IMP:8][ImageMetadataExtractor][EXIF_DONE] EXIF fields extracted: {len(exif_fields)} keys")

        result = {**base_fields, **exif_fields}
        self.logger.info(f"[IMP:9][ImageMetadataExtractor][RESULT] Total metadata fields: {len(result)}")
        return result
    # endregion METHOD_extract

    # region METHOD_encode_exif [DOMAIN(5): Encoding; CONCEPT(5): ByteToString; TECH(4): PythonStrings]
    ## @purpose To safely encode EXIF values from bytes to str — returns None on UnicodeDecodeError for robustness.
    ## @uses None
    ## @io Union[str, bytes] -> Optional[str]
    ## @complexity 3
    def __encode_exif(self, exif: Union[str, bytes]) -> Optional[str]:
        if isinstance(exif, bytes):
            try:
                return exif.decode()
            except UnicodeDecodeError:
                return None
        return str(exif)
    # endregion METHOD_encode_exif

    # region METHOD_parse_int [DOMAIN(5): Parsing; CONCEPT(5): TypeConversion; TECH(4): PythonInt]
    ## @purpose To parse EXIF values to int — encodes bytes first, then attempts int conversion; returns None on failure.
    ## @uses __encode_exif
    ## @io Union[str, bytes] -> Optional[int]
    ## @complexity 3
    def __parse_int(self, exif: Union[str, bytes]) -> Optional[int]:
        try:
            exif = self.__encode_exif(exif)
            return int(exif)
        except Exception:
            return None
    # endregion METHOD_parse_int

    # region METHOD_parse_date [DOMAIN(5): Parsing; CONCEPT(6): DateTimeParsing; TECH(5): dateutil]
    ## @purpose To parse EXIF date strings into Unix timestamps — handles the ':' separator quirk in EXIF date formats.
    ## @uses dateutil.parser, __encode_exif
    ## @io Union[str, bytes] -> Optional[int]
    ## @complexity 4
    def __parse_date(self, date_str: Union[str, bytes]) -> Optional[int]:
        from dateutil import parser

        try:
            date_str = self.__encode_exif(date_str)
            date = parser.parse(date_str.replace(": ", ":"))
            return int(date.timestamp())
        except Exception:
            return None
    # endregion METHOD_parse_date

    # region METHOD_parse_float [DOMAIN(5): Parsing; CONCEPT(5): TypeConversion; TECH(4): PythonFloat]
    ## @purpose To parse EXIF values to float — returns None for NaN values to avoid downstream serialization issues.
    ## @uses math, __encode_exif
    ## @io Union[str, bytes] -> Optional[float]
    ## @complexity 4
    def __parse_float(self, exif: Union[str, bytes]) -> Optional[float]:
        import math

        try:
            exif = self.__encode_exif(exif)
            result = float(exif)
            return None if math.isnan(result) else result
        except Exception:
            return None
    # endregion METHOD_parse_float

    # region METHOD_get_exif [DOMAIN(8): EXIFExtraction; CONCEPT(7): ImageMetadataParsing; TECH(7): PIL, piexif]
    ## @purpose To open an image file with PIL, extract EXIF data via piexif, and map raw tags to cleaned field name/value pairs using self.keys mapping.
    ## @uses PIL.ExifTags, PIL.Image, piexif.load
    ## @io str -> dict
    ## @complexity 7
    def _get_exif(self, path: str) -> dict:
        import os
        from PIL import ExifTags, Image
        import piexif

        try:
            self.logger.debug(f"[IMP:5][ImageMetadataExtractor][OPEN_IMAGE] Opening image: {os.path.basename(path)}")
            image = Image.open(path)
            exif_dict = piexif.load(image.info["exif"]).get("Exif", {}) if "exif" in image.info else {}
            exif = {ExifTags.TAGS[k]: v for k, v in exif_dict.items() if k in ExifTags.TAGS}
            self.logger.debug(f"[IMP:5][ImageMetadataExtractor][RAW_EXIF] Found {len(exif)} raw EXIF tags")
            encoded_dict = {key_renamed: encode_function(exif.get(key)) for key, (key_renamed, encode_function) in self.keys.items() if key in exif}
            encoded_dict = {k: v for k, v in encoded_dict.items() if k is not None if v is not None}
            image.close()
            self.logger.info(f"[IMP:8][ImageMetadataExtractor][EXIF_ENCODED] Encoded {len(encoded_dict)} EXIF fields")
            return encoded_dict
        except Exception as e:
            self.logger.debug(f"[IMP:6][ImageMetadataExtractor][EXIF_ERROR] EXIF extraction failed for {os.path.basename(path)}: {e}")
            return {"broken_image": True}
    # endregion METHOD_get_exif
# endregion CLASS_ImageMetadataExtractor
