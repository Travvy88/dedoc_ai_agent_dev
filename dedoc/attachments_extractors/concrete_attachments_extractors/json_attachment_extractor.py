# region MODULE_CONTRACT [DOMAIN(8): DocumentProcessing; CONCEPT(8): AttachmentExtraction; TECH(7): json, HTML]
## @modulecontract
## @purpose Extract HTML content from JSON files as attachment files: navigates JSON paths specified in parameters, extracts string leaves, and writes them as .html attachments.
## @scope JSON file attachment extraction: parameter-driven HTML field extraction via JSON key path navigation.
## @input File path to .json document; parameters dict with optional "html_fields" (JSON array of key paths).
## @output List of AttachedFile objects containing HTML content extracted from the JSON.
## @links [USES_API(9): AbstractAttachmentsExtractor._content2attach_file]
## @links [USES_API(7): dedoc.utils.parameter_utils.get_param_need_content_analysis]
## @links [USES_API(8): recognized_extensions.json_like_format, recognized_mimes.json_like_format]
## @invariants
## - extract ALWAYS returns a List[AttachedFile] (may be empty).
## - Only string leaves on the specified paths produce attachments; non-string values are skipped.
## - __get_value_by_keys does NOT handle KeyError — caller must guarantee valid paths.
## @rationale
## Q: Why extract HTML from JSON instead of just returning the JSON itself?
## A: JSON documents often contain HTML blobs at specific key paths (e.g., rich text fields). Converting them to .html attachments enables downstream HTML parsing by Dedoc's document readers.
## @changes
## LAST_CHANGE: [v1.0.0 – Semantic markup + LDD logging added]
## @modulemap
## CLASS 8[Extracts HTML attachments from JSON files] => JsonAttachmentsExtractor
## METHOD 5[Constructor: registers recognized json extensions/mimes] => __init__
## METHOD 8[Main extraction: reads html_fields paths, extracts HTML, serializes] => extract
## METHOD 7[Navigates JSON by key path to leaf value] => __get_value_by_keys
## @usecases
## - [extract]: DedocManager => ExtractHtmlFromJson => List[AttachedFile]
def _module_contract():
    pass
# endregion MODULE_CONTRACT
# GREP_SUMMARY: json, attachments, extractor, html_fields, key_path, navigation, html, serialization
# STRUCTURE: ▶ Init ┌recognized json extensions/mimes┐ → ⚡ extract(file_path, params) → ○ read JSON → ◇ parse html_fields paths → ○ ∀path: __get_value_by_keys(data, keys) → 〈str? → write .html→ read binary → ⊕ attachment〉 → ∑ List[AttachedFile] → ⎋

from typing import List, Optional

from dedoc.attachments_extractors.abstract_attachment_extractor import AbstractAttachmentsExtractor
from dedoc.data_structures.attached_file import AttachedFile

import logging

logger = logging.getLogger(__name__)


# region CLASS_JsonAttachmentsExtractor [DOMAIN(8): DocumentProcessing; CONCEPT(8): AttachmentExtraction; TECH(7): json, HTML]
## @purpose Extract HTML string values from JSON files as file attachments, navigated by parameter-specified key paths.
class JsonAttachmentsExtractor(AbstractAttachmentsExtractor):
    # region METHOD___init__ [DOMAIN(8): DocumentProcessing; CONCEPT(5): Initialization; TECH(4): PythonConfig]
    ## @purpose Initialize the JSON extractor with recognized json-like file extensions and MIME types.
    ## @uses dedoc.extensions.recognized_extensions, dedoc.extensions.recognized_mimes
    ## @io Optional[dict] -> None
    ## @complexity 2
    def __init__(self, *, config: Optional[dict] = None) -> None:
        from dedoc.extensions import recognized_extensions, recognized_mimes
        super().__init__(config=config, recognized_extensions=recognized_extensions.json_like_format, recognized_mimes=recognized_mimes.json_like_format)
        logger.debug(f"[IMP:4][JsonAttachmentsExtractor][INIT] Initialized with json-like format recognition")
    # endregion METHOD___init__

    # region METHOD_extract [DOMAIN(8): DocumentProcessing; CONCEPT(8): AttachmentExtraction; TECH(7): json, FileIO]
    ## @purpose Extract HTML content from a JSON file at paths specified in parameters["html_fields"] and convert them to .html AttachedFile objects.
    ## @uses json.load, AbstractAttachmentsExtractor._content2attach_file
    ## @io str, Optional[dict] -> List[AttachedFile]
    ## @complexity 6
    def extract(self, file_path: str, parameters: Optional[dict] = None) -> List[AttachedFile]:
        import json
        import os
        from dedoc.utils.parameter_utils import get_param_need_content_analysis

        parameters = {} if parameters is None else parameters
        tmpdir, filename = os.path.split(file_path)
        attachments = []

        logger.debug(f"[IMP:6][JsonAttachmentsExtractor][EXTRACT] Extracting HTML fields from json: {filename}")

        with open(os.path.join(tmpdir, filename)) as f:
            data = json.load(f)

        field_keys = json.loads(parameters.get("html_fields")) if parameters.get("html_fields") else []
        logger.info(f"[IMP:7][JsonAttachmentsExtractor][EXTRACT] Found {len(field_keys)} html_field paths in parameters")

        for keys in field_keys:
            path = json.dumps(keys, ensure_ascii=False)
            attached_filename = f"{path}.html"
            attachment_file_path = os.path.join(tmpdir, attached_filename)
            field_content = self.__get_value_by_keys(data, keys)

            if not isinstance(field_content, str):
                logger.debug(f"[IMP:3][JsonAttachmentsExtractor][EXTRACT] Skipping non-string value at path {path}")
                continue

            with open(attachment_file_path, "w") as f:
                f.write(field_content)

            with open(attachment_file_path, mode="rb") as f:
                binary_data = f.read()

            attachments.append((attached_filename, binary_data))
            logger.debug(f"[IMP:5][JsonAttachmentsExtractor][EXTRACT] Extracted HTML at path {path} -> {attached_filename}")

        need_content_analysis = get_param_need_content_analysis(parameters)
        logger.info(f"[IMP:9][JsonAttachmentsExtractor][EXTRACT] Total HTML attachments extracted: {len(attachments)} from {filename}")
        return self._content2attach_file(content=attachments, tmpdir=tmpdir, need_content_analysis=need_content_analysis, parameters=parameters)
    # endregion METHOD_extract

    # region METHOD___get_value_by_keys [DOMAIN(7): DataNavigation; CONCEPT(7): JSONTraversal; TECH(5): dict]
    ## @purpose Navigate a nested dictionary by a sequential list of keys to retrieve the leaf value.
    ## @uses (none — pure dict traversal)
    ## @io dict, List[str] -> Any
    ## @complexity 3
    def __get_value_by_keys(self, data: dict, keys: List[str]) -> dict:
        value = data

        for key in keys:
            value = value[key]
            logger.debug(f"[IMP:3][JsonAttachmentsExtractor][GET_VALUE] Key={key}, type={type(value).__name__}")

        return value
    # endregion METHOD___get_value_by_keys
# endregion CLASS_JsonAttachmentsExtractor
