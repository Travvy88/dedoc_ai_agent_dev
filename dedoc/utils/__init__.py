# region MODULE_CONTRACT [DOMAIN(7): DocumentProcessing; CONCEPT(6): FileTypeDetection; TECH(5): ImageFormats]
## @modulecontract
## @purpose To provide a centralized registry of supported image formats, enabling the system to detect and validate image file types before processing.
## @scope Image format enumeration, image file type detection.
## @input None (static data).
## @output Set of supported image type strings with and without dot prefixes.
## @links [USES_API(5): builtins]
## @invariants
## - supported_image_types ALWAYS contains all entries of _supported_image_types with both "." and "" prefix variants.
## @rationale
## Q: Why generate both dotted and non-dotted variants?
## A: File extensions arrive in different formats from various sources. Pre-computing both variants avoids runtime normalization overhead.
## @changes
## LAST_CHANGE: [v1.0.0 – Added SEMANTIC TEMPLATE markup]
## @modulemap
## DATA 8[Registry of supported image types] => supported_image_types
## @usecases
## - [supported_image_types]: Reader → ValidateInputFile → ImageFormatRecognized
def _module_contract():
    pass
# endregion MODULE_CONTRACT
# GREP_SUMMARY: image, formats, supported, extensions, bmp, jpeg, png, tiff, webp, file type detection
# STRUCTURE: ▶ Init ┌_supported_image_types (base set)┐ → ○ Loop ∋each format: ⊕ added with "." and "" prefix → ∑ supported_image_types

_supported_image_types = {"bmp",
                          "dib",
                          "eps",
                          "gif",
                          "hdr",
                          "jfif",
                          "jp2",
                          "jpe",
                          "jpeg",
                          "jpg",
                          "pbm",
                          "pcx",
                          "pgm",
                          "pic",
                          "png",
                          "pnm",
                          "ppm",
                          "ras",
                          "sgi",
                          "sr",
                          "tiff",
                          "webp",
                          "j2k"}
supported_image_types = {prefix + image_format for image_format in _supported_image_types for prefix in [".", ""]}
