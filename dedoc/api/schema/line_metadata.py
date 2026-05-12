# region MODULE_CONTRACT [DOMAIN(9): DocumentProcessing, LineMetadata; CONCEPT(7): ParagraphMetadata, LineAttributes; TECH(7): Pydantic, BaseModel, Extra]
## @modulecontract
## @purpose Define the LineMetadata schema — a Pydantic model for paragraph/line-level metadata (paragraph type, page number, line number) with extra attributes support.
## @scope Document line/paragraph metadata model.
## @input None (standalone model with Extra.allow).
## @output Pydantic BaseModel `LineMetadata` with paragraph_type, page_id, line_id + extra fields.
## @links [USES_API(7): pydantic.BaseModel, pydantic.Extra]
## @invariants
## - page_id >= 0.
## - paragraph_type is always a non-empty string (e.g., "raw_text", "header", "list_item").
## - Extra fields preserved for format-specific metadata.
## @rationale
## Q: Why Extra.allow for line metadata?
## A: Different parsers attach different metadata (heading levels, indentation, list numbering). Extra.allow prevents loss.
## @changes
## LAST_CHANGE: [v1.0.0 – Initial creation with semantic markup]
## @modulemap
## CLASS 9[Line/paragraph metadata with extra attributes] => LineMetadata
## @usecases
## - [LineMetadata]: StructureExtractor => AnnotateParagraph => PassToTreeNode
def _module_contract():
    pass
# endregion MODULE_CONTRACT
# GREP_SUMMARY: line, metadata, paragraph, type, page, line_id, extra, Pydantic, schema
# STRUCTURE: ▶ Pydantic BaseModel (Extra.allow) → LineMetadata ┌paragraph_type:str, page_id:int, line_id:Optional[int], +extra┐ → ⎋ JSON

import logging
from typing import Optional

from pydantic import BaseModel, Extra, Field

logger = logging.getLogger(__name__)

# region CLASS_LineMetadata [DOMAIN(9): DocumentProcessing; CONCEPT(7): LineMetadata; TECH(7): PydanticBaseModel]
## @purpose Hold paragraph/line-level metadata (type, page, line number) with extensible extra attributes for format-specific annotations.
## @io (paragraph_type, page_id, line_id, **extra) -> JSON serializable model
class LineMetadata(BaseModel):
    """
    Holds information about document node/line metadata, such as page number or line type.

    :ivar paragraph_type: type of the document line/paragraph (header, list_item, list, etc.)
    :ivar page_id: page number where paragraph starts, the numeration starts from page 0
    :ivar line_id: line number inside the entire document, the numeration starts from line 0

    :vartype paragraph_type: str
    :vartype page_id: int
    :vartype line_id: Optional[int]

    Additional variables may be added with other line metadata.
    """
    class Config:
        extra = Extra.allow

    paragraph_type: str = Field(description="Type of the document line/paragraph (header, list_item, list, etc.)", example="raw_text")
    page_id: int = Field(description="Page number of the line/paragraph beginning", example=0)
    line_id: Optional[int] = Field(description="Line number", example=1)
# endregion CLASS_LineMetadata
