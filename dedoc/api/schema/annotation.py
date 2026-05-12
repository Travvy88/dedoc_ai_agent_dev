# region MODULE_CONTRACT [DOMAIN(9): DocumentProcessing, AnnotationModel; CONCEPT(8): TextAnnotation, InlineMetadata; TECH(7): Pydantic, BaseModel]
## @modulecontract
## @purpose Define the Annotation schema — a Pydantic model describing a piece of inline text metadata (font style, links, etc.) with character-level range.
## @scope Text annotation data model for document lines.
## @input None (standalone model).
## @output Pydantic BaseModel `Annotation` with start, end, name, value fields.
## @links [USES_API(7): pydantic.BaseModel]
## @invariants
## - Annotation.start <= Annotation.end for all valid annotations.
## - Annotation.name is always a non-empty string identifying the annotation type.
## @rationale
## Q: Why use Pydantic BaseModel instead of dataclass?
## A: Pydantic provides built-in JSON serialization, Field descriptions for OpenAPI schema generation, and FastAPI integration.
## @changes
## LAST_CHANGE: [v1.0.0 – Initial creation with semantic markup]
## @modulemap
## CLASS 10[Inline text annotation with character range] => Annotation
## @usecases
## - [Annotation]: APIConsumer => DeserializeAnnotationJSON => RenderStyledText
def _module_contract():
    pass
# endregion MODULE_CONTRACT
# GREP_SUMMARY: annotation, text, inline, metadata, bold, italic, font, character range, Pydantic, schema
# STRUCTURE: ▶ Pydantic BaseModel → Annotation ┌start:int, end:int, name:str, value:str┐ → ⎋ JSON-serializable

import logging

from pydantic import BaseModel, Field

logger = logging.getLogger(__name__)

# region CLASS_Annotation [DOMAIN(9): DocumentProcessing; CONCEPT(8): TextAnnotation; TECH(7): PydanticBaseModel]
## @purpose Represent a single inline annotation (e.g., bold, italic, link) spanning a character range within document text.
## @io (int, int, str, str) -> JSON serializable model
class Annotation(BaseModel):
    """
    The piece of information about the text line: it's appearance or links to another document object.
    For example Annotation(1, 13, "italic", "True") says that text between 1st and 13th symbol was written in italic.

    :ivar start: start of the annotated text
    :ivar end: end of the annotated text (end isn't included)
    :ivar name: annotation's name, specific for each type of annotation
    :ivar value: information about annotated text, depends on the type of annotation, e.g. "True"/"False", "10.0", etc.

    :vartype start: int
    :vartype end: int
    :vartype name: str
    :vartype value: str
    """
    start: int = Field(description="Start of the annotated text", example=0)
    end: int = Field(description="End of the annotated text (end isn't included)", example=5)
    name: str = Field(description="Annotation name", example="italic")
    value: str = Field(description="Annotation value. For example, it may be font size value for size type", example="True")
# endregion CLASS_Annotation
