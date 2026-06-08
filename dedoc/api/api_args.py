# region MODULE_CONTRACT [DOMAIN(8): DocumentProcessing, APIRequest; CONCEPT(7): QueryParameters, FormParsing; TECH(8): FastAPI, Dataclass]
## @modulecontract
## @purpose Define QueryParameters — a dataclass-based FastAPI Form model that captures all dedoc API query parameters for document parsing configuration.
## @scope API request parameter parsing — document type, structure options, PDF handling, table analysis, attachments, etc.
## @input FastAPI Form fields from HTTP request.
## @output QueryParameters instance with typed fields and `to_dict()` serialization.
## @links [USES_API(8): fastapi.Form; USES_API(6): dataclasses.asdict]
## @invariants
## - All Form fields have defaults (no required parameters at this level).
## - to_dict() always returns a flat dict with parameter_name -> default_value.
## @rationale
## Q: Why dataclass with Form() instead of Pydantic BaseModel?
## A: FastAPI's Form() with dataclass provides direct mapping from multipart form data and enum validation without Pydantic overhead. Fields use string enums for request validation.
## @changes
## LAST_CHANGE: [v1.1.0 – Added ocr_engine field for per-request OCR engine selection (AC5)]
## @modulemap
## CLASS 8[API query parameters as Form dataclass] => QueryParameters
## METHOD 5[Serializes dataclass to flat dict] => to_dict
## @usecases
## - [QueryParameters]: ApiEndpoint => ParseFormData => ConfigureParsingPipeline
def _module_contract():
    pass
# endregion MODULE_CONTRACT
# GREP_SUMMARY: query, parameters, form, FastAPI, dataclass, document_type, structure, pdf, tables, attachments, API request
# STRUCTURE: ▶ FastAPI Form dataclass → QueryParameters ┌~30 typed fields┐ → METHOD to_dict → Σ flat dict

import logging
from dataclasses import asdict, dataclass
from typing import Optional

from fastapi import Form

logger = logging.getLogger(__name__)

# region CLASS_QueryParameters [DOMAIN(8): DocumentProcessing; CONCEPT(7): APIRequest; TECH(8): FastAPIForm]
## @purpose Capture all dedoc API query parameters from multipart form data with enum-validated defaults for document parsing configuration.
## @io FastAPI Form(...) fields -> QueryParameters instance
@dataclass
class QueryParameters:
    # type of document structure parsing
    document_type: str = Form("", enum=["", "law", "tz", "diploma", "article", "fintoc"], description="Document domain")
    patterns: str = Form("", description='Patterns for default document type (when document_type="")')
    structure_type: str = Form("tree", enum=["linear", "tree"], description="Output structure type")
    return_format: str = Form("json", enum=["json", "html", "plain_text", "tree", "collapsed_tree", "ujson", "pretty_json"],
                              description="Response representation, most types (except json) are used for debug purposes only")

    # attachments handling
    with_attachments: str = Form("false", enum=["true", "false"], description="Enable attached files extraction")
    need_content_analysis: str = Form("false", enum=["true", "false"], description="Enable parsing contents of the attached files")
    recursion_deep_attachments: str = Form("10", description="Depth on which nested attachments will be parsed if need_content_analysis=true")
    return_base64: str = Form("false", enum=["true", "false"], description="Save attached images to the document metadata in base64 format")

    # tables handling
    need_pdf_table_analysis: str = Form("true", enum=["true", "false"], description="Enable table recognition for pdf")
    table_type: str = Form("", description="Pipeline mode for table recognition")

    # pdf handling
    pdf_with_text_layer: str = Form("auto_tabby", enum=["true", "false", "auto", "auto_tabby", "tabby", "bad_encoding"],
                                    description="Extract text from a text layer of PDF or using OCR methods for image-like documents")
    textual_layer_classifier: str = Form("ml", enum=["ml", "simple", "letter"], description="Type of classifier for PDF textual layer detection")
    each_page_textual_layer_detection: str = Form("false", enum=["true", "false"], description="Detect textual layer on each page. Slower but more accurate.")
    language: str = Form("rus+eng", description="Recognition language ('rus+eng', 'rus', 'eng', 'fra', 'spa')")
    ocr_engine: str = Form("tesseract", description="OCR engine name for image-based PDF parsing ('tesseract')")
    pages: str = Form(":", description='Page numbers range for reading PDF or images, "left:right" means read pages from left to right')
    is_one_column_document: str = Form("auto", enum=["auto", "true", "false"],
                                       description='One or multiple column document, "auto" - predict number of page columns automatically')
    document_orientation: str = Form("auto", enum=["auto", "no_change"],
                                     description='Orientation of the document pages, "auto" - predict orientation (0, 90, 180, 270 degrees), '
                                                 '"no_change" - set vertical orientation of the document without using an orientation classifier')
    need_header_footer_analysis: str = Form("false", enum=["true", "false"], description="Exclude headers and footers from PDF parsing result")
    need_binarization: str = Form("false", enum=["true", "false"], description="Binarize document pages (for images or PDF without a textual layer)")
    need_gost_frame_analysis: str = Form("false", enum=["true", "false"], description="Parameter for detecting and ignoring GOST frame of the document")

    # other formats handling
    delimiter: Optional[str] = Form(None, description="Column separator for CSV files")
    encoding: Optional[str] = Form(None, description="Document encoding")
    html_fields: str = Form("", description="List of fields for JSON documents to be parsed as HTML documents")
    handle_invisible_table: str = Form("false", enum=["true", "false"], description="Handle tables without visible borders as tables in HTML")

    # region METHOD_to_dict [DOMAIN(7): Serialization; CONCEPT(6): DictConversion; TECH(5): Dataclass]
    ## @purpose Convert the QueryParameters dataclass to a flat dict with defaults resolved for downstream pipeline configuration.
    ## @uses dataclasses.asdict
    ## @io None -> dict
    ## @complexity 3
    def to_dict(self) -> dict:
        parameters = {}

        for parameter_name, parameter_value in asdict(self).items():
            parameters[parameter_name] = getattr(parameter_value, "default", parameter_value)

        logger.debug(f"[IMP:4][QueryParameters][TO_DICT] Converted {len(parameters)} parameters to dict")
        return parameters
    # endregion METHOD_to_dict
# endregion CLASS_QueryParameters
