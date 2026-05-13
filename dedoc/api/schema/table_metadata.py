# region MODULE_CONTRACT [DOMAIN(9): DocumentProcessing, TableMetadata; CONCEPT(7): TableProperties, PageLocation; TECH(7): Pydantic, BaseModel]
## @modulecontract
## @purpose Define the TableMetadata schema — a Pydantic model for table-level metadata: unique identifier, page number, rotation angle, and title.
## @scope Table metadata model.
## @input None (standalone model).
## @output Pydantic BaseModel `TableMetadata` with page_id, uid, rotated_angle, title.
## @links [USES_API(7): pydantic.BaseModel]
## @invariants
## - uid is always a non-empty unique string.
## - rotated_angle is in degrees, may be 0.0 for non-rotated tables.
## @rationale
## Q: Why include rotated_angle?
## A: OCR-based table recognition on scanned documents may detect tables at non-zero angles; this metadata preserves that information for correct rendering.
## @changes
## LAST_CHANGE: [v1.0.0 – Initial creation with semantic markup]
## @modulemap
## CLASS 8[Table-level metadata — UID, page, rotation, title] => TableMetadata
## @usecases
## - [TableMetadata]: TableDetector => AnnotateTableLocation => LinkTableToPage
def _module_contract():
    pass
# endregion MODULE_CONTRACT
# GREP_SUMMARY: table, metadata, uid, page, rotation, angle, title, Pydantic, schema
# STRUCTURE: ▶ Pydantic BaseModel → TableMetadata ┌page_id:Optional[int], uid:str, rotated_angle:float, title:str┐ → ⎋ JSON

import logging
from typing import Optional

from pydantic import BaseModel, Field

logger = logging.getLogger(__name__)

# region CLASS_TableMetadata [DOMAIN(9): DocumentProcessing; CONCEPT(7): TableMetadata; TECH(7): PydanticBaseModel]
## @purpose Hold table-level metadata: unique identifier (for cross-referencing), page number, rotation angle, and optional title.
## @io (page_id, uid, rotated_angle, title) -> JSON serializable model
class TableMetadata(BaseModel):
    """
    Holds the information about table unique identifier, rotation angle (if table has been rotated - for images) and so on.

    :ivar page_id: number of the page where table starts
    :ivar uid: unique identifier of the table (used for linking table to text)
    :ivar rotated_angle: value of the rotation angle by which the table was rotated during recognition
    :ivar title: table's title

    :vartype page_id: Optional[int]
    :vartype uid: str
    :vartype rotated_angle: float
    :vartype title: str
    """
    page_id: Optional[int] = Field(description="Number of the page where the table starts", example=0)
    uid: str = Field(description="Unique identifier of the table", example="e8ba5523-8546-4804-898c-2f4835a1804f")
    rotated_angle: float = Field(description="Value of the rotation angle (in degrees) by which the table was rotated during recognition", example=1.0)
    title: str = Field(description="Table's title")
# endregion CLASS_TableMetadata
