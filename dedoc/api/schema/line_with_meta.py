# region MODULE_CONTRACT [DOMAIN(9): DocumentProcessing, TextLine; CONCEPT(8): AnnotatedText, InlineFormatting; TECH(7): Pydantic, BaseModel]
## @modulecontract
## @purpose Define the LineWithMeta schema — a Pydantic model for a single text line with its inline annotations (font styles, links, etc.).
## @scope Text line data model with annotations.
## @input None (standalone model, references Annotation).
## @output Pydantic BaseModel `LineWithMeta` with text and annotations fields.
## @links [USES_API(7): pydantic.BaseModel; READS_DATA_FROM(8): Annotation]
## @invariants
## - text is the raw line content, may be empty.
## - annotations list may be empty but never None.
## @rationale
## Q: Why store annotations as a flat list rather than nested?
## A: Flat list is simpler for JSON serialization and allows overlapping annotations (e.g., bold+italic on same range).
## @changes
## LAST_CHANGE: [v1.0.0 – Initial creation with semantic markup]
## @modulemap
## CLASS 10[Text line with inline annotations] => LineWithMeta
## @usecases
## - [LineWithMeta]: LineExtractor => AnnotateTextRange => PassToCellOrNode
def _module_contract():
    pass
# endregion MODULE_CONTRACT
# GREP_SUMMARY: line, text, annotations, inline, bold, italic, font, Pydantic, schema, formatting
# STRUCTURE: ▶ Pydantic BaseModel → LineWithMeta ┌text:str, annotations:List[Annotation]┐ → ⎋ JSON

import logging
from typing import List

from pydantic import BaseModel, Field

from dedoc.api.schema.annotation import Annotation

logger = logging.getLogger(__name__)

# region CLASS_LineWithMeta [DOMAIN(9): DocumentProcessing; CONCEPT(8): AnnotatedText; TECH(7): PydanticBaseModel]
## @purpose Represent a single text line with its associated character-level annotations (font styles, links, references) for rich text rendering.
## @io (text, annotations) -> JSON serializable model
class LineWithMeta(BaseModel):
    """
    Textual line with text annotations.

    :ivar text: text of the line
    :ivar annotations: text annotations (font, size, bold, italic, etc.)

    :vartype text: str
    :vartype annotations: List[Annotation]
    """
    text: str = Field(description="Text of the line", example="Some text")
    annotations: List[Annotation] = Field(description="Text annotations (font, size, bold, italic, etc.)")
# endregion CLASS_LineWithMeta
