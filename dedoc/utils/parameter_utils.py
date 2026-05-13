# region MODULE_CONTRACT [DOMAIN(7): DocumentProcessing; CONCEPT(8): Configuration; TECH(6): ParameterParsing]
## @modulecontract
## @purpose To provide a centralized set of parameter extraction and validation functions for the Dedoc API, normalizing user-supplied query parameters into typed values with sensible defaults.
## @scope Boolean parameter parsing, language normalization, document type resolution, page slicing, GPU availability checking, path resolution.
## @input Optional dict of user parameters, logger instance.
## @output Typed primitive values (bool, str, int, Optional[int]).
## @links [USES_API(6): dedoc.config.get_config]
## @invariants
## - All boolean extractors return False when parameters is None.
## - get_param_page_slice raises ValueError on malformed page range strings.
## - get_path_param always creates the target directory if it does not exist.
## @rationale
## Q: Why have individual getters instead of a generic config object?
## A: Explicit per-parameter functions provide type safety, documented defaults, and IDE autocomplete — critical for a large API surface.
## @changes
## LAST_CHANGE: [v1.0.0 – Added SEMANTIC TEMPLATE markup and LDD logging]
## @modulemap
## FUNC 5[Bool value coercion] => get_bool_value
## FUNC 6[Dict bool param extractor] => get_bool_parameter
## FUNC 5[Language normalization] => get_param_language
## FUNC 4[Document type extractor] => get_param_document_type
## FUNC 5[With attachments flag] => get_param_with_attachments
## FUNC 5[Content analysis flag] => get_param_need_content_analysis
## FUNC 5[Header/footer analysis flag] => get_param_need_header_footers_analysis
## FUNC 5[PDF table analysis flag] => get_param_need_pdf_table_analysis
## FUNC 5[GOST frame analysis flag] => get_param_need_gost_frame_analysis
## FUNC 5[Binarization flag] => get_param_need_binarization
## FUNC 5[One column document flag] => get_param_is_one_column_document
## FUNC 4[Document orientation] => get_param_document_orientation
## FUNC 5[PDF text layer mode] => get_param_pdf_with_txt_layer
## FUNC 4[Table type] => get_param_table_type
## FUNC 7[Page slice parsing] => get_param_page_slice
## FUNC 6[GPU availability check] => get_param_gpu_available
## FUNC 6[Path parameter resolver] => get_path_param
## FUNC 6[Attachments dir resolver] => get_param_attachments_dir
## @usecases
## - [get_param_page_slice]: API → ParsePageRange → (first_page, last_page) tuple
## - [get_param_gpu_available]: DedocManager → CheckGPU → Configuration updated
def _module_contract():
    pass
# endregion MODULE_CONTRACT
# GREP_SUMMARY: parameters, configuration, boolean, language, document type, page slice, GPU, path resolution, attachments
# STRUCTURE: ▶ ┌imports┐ → ⚡ get_bool_value: ┌param, default┐ → 〈isinstance bool ? T : str.lower=="true"〉 → ⎋ bool; ⚡ ParamMap: ⋯ → ⎋ typed values

import logging
import os
import subprocess
from logging import Logger
from typing import Any, Dict, Optional, Tuple

from dedoc.config import get_config

logger = logging.getLogger(__name__)


# region FUNC_get_bool_value [DOMAIN(5): Configuration; CONCEPT(4): TypeCoercion; TECH(3): PythonTyping]
## @purpose To coerce an optional parameter into a boolean value, normalizing string "true"/"false" to Python bool.
## @io (Optional[bool or str], bool) -> bool
## @complexity 2
def get_bool_value(parameter: Optional[bool or str], default_value: bool = False) -> bool:
    if parameter is None:
        return default_value

    return parameter if isinstance(parameter, bool) else str(parameter).lower() == "true"
# endregion FUNC_get_bool_value


# region FUNC_get_bool_parameter [DOMAIN(6): Configuration; CONCEPT(5): DictParameter; TECH(4): ParameterExtraction]
## @purpose To extract a named boolean parameter from a dictionary with a default fallback.
## @uses get_bool_value
## @io (Optional[dict], str, bool) -> bool
## @complexity 3
def get_bool_parameter(parameters: Optional[dict], parameter_name: str, default_value: bool = False) -> bool:
    parameters = {} if parameters is None else parameters
    return get_bool_value(parameters.get(parameter_name), default_value)
# endregion FUNC_get_bool_parameter


# region FUNC_get_param_language [DOMAIN(7): DocumentProcessing; CONCEPT(6): Language; TECH(4): Normalization]
## @purpose To normalize a user-supplied language parameter into canonical short forms (rus, eng, rus+eng) for downstream OCR and NLP components.
## @io Optional[dict] -> str
## @complexity 3
def get_param_language(parameters: Optional[dict]) -> str:
    if parameters is None:
        return "rus+eng"
    language = parameters.get("language", "rus+eng")
    if language == "ru" or language == "rus":
        language = "rus"
    elif language == "en" or language == "eng":
        language = "eng"
    elif language == "ru+en" or language == "rus+eng":
        language = "rus+eng"
    logger.debug(f"[IMP:4][get_param_language][NORMALIZE] Language: {language}")
    return language
# endregion FUNC_get_param_language


# region FUNC_get_param_document_type [DOMAIN(7): DocumentProcessing; CONCEPT(6): DocumentType; TECH(4): Normalization]
## @purpose To extract and normalize the document type parameter, defaulting to "other" for unrecognized types.
## @io Optional[dict] -> str
## @complexity 2
def get_param_document_type(parameters: Optional[dict]) -> str:
    if parameters is None:
        return "other"
    document_type = str(parameters.get("document_type", "other")).lower()
    return document_type
# endregion FUNC_get_param_document_type


# region FUNC_get_param_with_attachments [DOMAIN(7): DocumentProcessing; CONCEPT(6): Attachments; TECH(4): BooleanExtract]
## @purpose To determine whether the document processing should include attachment extraction.
## @io Optional[dict] -> bool
## @complexity 2
def get_param_with_attachments(parameters: Optional[dict]) -> bool:
    if parameters is None:
        return False
    return str(parameters.get("with_attachments", "false")).lower() == "true"
# endregion FUNC_get_param_with_attachments


# region FUNC_get_param_need_content_analysis [DOMAIN(7): DocumentProcessing; CONCEPT(6): ContentAnalysis; TECH(4): BooleanExtract]
## @purpose To extract the content analysis flag controlling whether deep document content analysis is performed.
## @io Optional[dict] -> bool
## @complexity 2
def get_param_need_content_analysis(parameters: Optional[dict]) -> bool:
    if parameters is None:
        return False
    return str(parameters.get("need_content_analysis", "false")).lower() == "true"
# endregion FUNC_get_param_need_content_analysis


# region FUNC_get_param_need_header_footers_analysis [DOMAIN(7): DocumentProcessing; CONCEPT(6): HeaderFooter; TECH(4): BooleanExtract]
## @purpose To extract the header/footer analysis flag for PDF document processing.
## @io Optional[dict] -> bool
## @complexity 2
def get_param_need_header_footers_analysis(parameters: Optional[dict]) -> bool:
    if parameters is None:
        return False
    need_header_footers_analysis = str(parameters.get("need_header_footer_analysis", "False")).lower() == "true"
    return need_header_footers_analysis
# endregion FUNC_get_param_need_header_footers_analysis


# region FUNC_get_param_need_pdf_table_analysis [DOMAIN(7): DocumentProcessing; CONCEPT(6): TableDetection; TECH(4): BooleanExtract]
## @purpose To extract the PDF table analysis flag, defaulting to True for table detection in PDF documents.
## @io Optional[dict] -> bool
## @complexity 2
def get_param_need_pdf_table_analysis(parameters: Optional[dict]) -> bool:
    if parameters is None:
        return False
    need_pdf_table_analysis = str(parameters.get("need_pdf_table_analysis", "True")).lower() == "true"
    return need_pdf_table_analysis
# endregion FUNC_get_param_need_pdf_table_analysis


# region FUNC_get_param_need_gost_frame_analysis [DOMAIN(7): DocumentProcessing; CONCEPT(6): GOST; TECH(4): BooleanExtract]
## @purpose To extract the GOST frame analysis flag for documents following Russian GOST standards.
## @io Optional[dict] -> bool
## @complexity 2
def get_param_need_gost_frame_analysis(parameters: Optional[dict]) -> bool:
    if parameters is None:
        return False
    need_gost_frame_analysis = str(parameters.get("need_gost_frame_analysis", "False")).lower() == "true"
    return need_gost_frame_analysis
# endregion FUNC_get_param_need_gost_frame_analysis


# region FUNC_get_param_need_binarization [DOMAIN(7): DocumentProcessing; CONCEPT(6): Binarization; TECH(4): BooleanExtract]
## @purpose To extract the binarization flag for image preprocessing.
## @io Optional[dict] -> bool
## @complexity 2
def get_param_need_binarization(parameters: Optional[dict]) -> bool:
    if parameters is None:
        return False
    need_binarization = str(parameters.get("need_binarization", "False")).lower() == "true"
    return need_binarization
# endregion FUNC_get_param_need_binarization


# region FUNC_get_param_is_one_column_document [DOMAIN(7): DocumentProcessing; CONCEPT(6): Layout; TECH(4): BooleanExtract]
## @purpose To extract the one-column document layout flag, returning None for auto-detection mode.
## @io Optional[dict] -> Optional[bool]
## @complexity 3
def get_param_is_one_column_document(parameters: Optional[dict]) -> Optional[bool]:
    if parameters is None:
        return None

    is_one_column_document = str(parameters.get("is_one_column_document", "auto"))
    if is_one_column_document.lower() == "auto":
        return None
    else:
        return is_one_column_document.lower() == "true"
# endregion FUNC_get_param_is_one_column_document


# region FUNC_get_param_document_orientation [DOMAIN(7): DocumentProcessing; CONCEPT(6): Layout; TECH(4): ParameterExtract]
## @purpose To extract the document orientation parameter, returning None for auto-detection.
## @io Optional[dict] -> Optional[bool]
## @complexity 2
def get_param_document_orientation(parameters: Optional[dict]) -> Optional[bool]:
    if parameters is None:
        return None
    document_orientation = str(parameters.get("document_orientation", "auto"))
    if document_orientation.lower() == "no_change":
        return False
    else:
        return None
# endregion FUNC_get_param_document_orientation


# region FUNC_get_param_pdf_with_txt_layer [DOMAIN(8): DocumentProcessing; CONCEPT(7): PDF; TECH(5): TextLayerDetection]
## @purpose To determine the PDF text layer processing mode (true, false, tabby, auto_tabby) which selects the appropriate reader strategy.
## @io Optional[dict] -> str
## @complexity 3
def get_param_pdf_with_txt_layer(parameters: Optional[dict]) -> str:
    if parameters is None:
        return "auto_tabby"
    pdf_with_txt_layer = str(parameters.get("pdf_with_text_layer", "auto_tabby")).lower()
    return pdf_with_txt_layer
# endregion FUNC_get_param_pdf_with_txt_layer


# region FUNC_get_param_table_type [DOMAIN(7): DocumentProcessing; CONCEPT(6): TableDetection; TECH(4): ParameterExtract]
## @purpose To extract the table type parameter for specialized table handling.
## @io Optional[dict] -> str
## @complexity 2
def get_param_table_type(parameters: Optional[dict]) -> str:
    if parameters is None:
        return ""

    return str(parameters.get("table_type", ""))
# endregion FUNC_get_param_table_type


# region FUNC_get_param_page_slice [DOMAIN(8): DocumentProcessing; CONCEPT(7): Pagination; TECH(6): StringParsing]
## @purpose To parse a "pages" parameter string (e.g., "1:5") into zero-indexed first and last page numbers, supporting open-ended ranges.
## @io Dict[str, Any] -> Tuple[Optional[int], Optional[int]]
## @complexity 5
def get_param_page_slice(parameters: Dict[str, Any]) -> Tuple[Optional[int], Optional[int]]:
    pages = parameters.get("pages", "")
    if pages is None or pages.strip() == "":
        return None, None
    try:
        first_page, last_page = pages.split(":")
        first_page = None if first_page == "" else int(first_page) - 1
        last_page = None if last_page == "" else int(last_page)

        first_page = 0 if first_page is None or first_page < 0 else first_page
        last_page = 0 if last_page and last_page < 0 else last_page

        logger.debug(f"[IMP:5][get_param_page_slice][PARSE] Pages range: ({first_page}, {last_page})")
        return first_page, last_page
    except Exception:
        logger.error(f"[IMP:9][get_param_page_slice][ERROR] Bad page limit: {pages}")
        raise ValueError(f"Error input parameter 'pages'. Bad page limit {pages}")
# endregion FUNC_get_param_page_slice


# region FUNC_get_param_gpu_available [DOMAIN(8): DocumentProcessing; CONCEPT(7): GPU; TECH(7): subprocess, nvidia-smi]
## @purpose To check GPU availability via nvidia-smi and update the parameter dict accordingly, preventing runtime errors from missing GPU.
## @uses subprocess
## @io (Optional[dict], Logger) -> bool
## @complexity 5
def get_param_gpu_available(parameters: Optional[dict], logger: Logger) -> bool:
    parameters = {} if parameters is None else parameters

    if not parameters.get("on_gpu", False):
        return False

    try:
        subprocess.run(["nvidia-smi"], check=True, stdout=subprocess.DEVNULL)
        logger.info(f"[IMP:7][get_param_gpu_available][CHECK] GPU is available")
    except (subprocess.CalledProcessError, FileNotFoundError):
        logger.warning(f"[IMP:8][get_param_gpu_available][UNAVAILABLE] No GPU device available! Changing configuration on_gpu to False!")
        parameters["on_gpu"] = False
        return False

    return True
# endregion FUNC_get_param_gpu_available


# region FUNC_get_path_param [DOMAIN(7): DocumentProcessing; CONCEPT(6): Configuration; TECH(5): FileSystem]
## @purpose To resolve a path parameter from user input or config defaults, creating the directory if it does not exist.
## @uses get_config
## @io (Optional[dict], str) -> str
## @complexity 4
def get_path_param(parameters: Optional[dict], path_key: str) -> str:
    parameters = {} if parameters is None else parameters
    path_value = parameters.get(path_key)

    if path_value is None:
        default_config = get_config()
        path_value = default_config.get(path_key, default_config["resources_path"])

    os.makedirs(path_value, exist_ok=True)
    logger.debug(f"[IMP:5][get_path_param][RESOLVE] Path for {path_key}: {path_value}")
    return path_value
# endregion FUNC_get_path_param


# region FUNC_get_param_attachments_dir [DOMAIN(7): DocumentProcessing; CONCEPT(6): Attachments; TECH(5): FileSystem]
## @purpose To resolve the attachments directory from user parameters or derive it from the input file path.
## @io (Optional[dict], str) -> str
## @complexity 4
def get_param_attachments_dir(parameters: Optional[dict], file_path: str) -> str:
    default_dir = os.path.dirname(file_path) if os.path.isfile(file_path) else file_path
    parameters = {} if parameters is None else parameters

    attachments_dir = parameters.get("attachments_dir", None)
    attachments_dir = attachments_dir if attachments_dir else default_dir
    os.makedirs(attachments_dir, exist_ok=True)
    logger.debug(f"[IMP:5][get_param_attachments_dir][RESOLVE] Attachments dir: {attachments_dir}")
    return attachments_dir
# endregion FUNC_get_param_attachments_dir
