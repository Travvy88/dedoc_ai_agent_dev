import logging
from typing import Optional

from dedoc.api.schema.table_metadata import TableMetadata as ApiTableMetadata
from dedoc.data_structures.serializable import Serializable

logger = logging.getLogger(__name__)


# region CLASS_TableMetadata [DOMAIN(9): DocumentProcessing, DataStructures; CONCEPT(9): Table, Metadata; TECH(6): Python, API]
## @purpose Hold table-level metadata: page ID, unique identifier, rotation angle, and title.
class TableMetadata(Serializable):
    """
    This class holds the information about table unique identifier, rotation angle (if table has been rotated - for images) and so on.

    :ivar page_id: number of the page where table starts
    :ivar uid: unique identifier of the table (used for linking table to text)
    :ivar rotated_angle: value of the rotation angle by which the table was rotated during recognition
    :ivar title: table's title

    :vartype page_id: Optional[int]
    :vartype uid: str
    :vartype rotated_angle: float
    :vartype title: str
    """

    # region METHOD___init__ [DOMAIN(9): DocumentProcessing; CONCEPT(9): Table; TECH(6): Python]
    ## @purpose Initialize table metadata with page ID, auto-generated UID, rotation angle, and title.
    ## @uses uuid
    ## @io (Optional[int], Optional[str], float, str) -> None
    ## @complexity 2
    def __init__(self, page_id: Optional[int], uid: Optional[str] = None, rotated_angle: float = 0.0, title: str = "") -> None:
        """
        :param page_id: number of the page where table starts
        :param uid: unique identifier of the table
        :param rotated_angle: rotation angle by which the table was rotated during recognition
        :param title: table's title
        """
        import uuid

        logger.debug(f"[IMP:4][TableMetadata][INIT] page_id={page_id}, uid={uid}, rotated_angle={rotated_angle}, title={title}")
        self.page_id: Optional[int] = page_id
        self.uid: str = str(uuid.uuid4()) if not uid else uid
        self.rotated_angle: float = rotated_angle
        self.title: str = title
        logger.debug(f"[IMP:4][TableMetadata][INIT] TableMetadata created: uid={self.uid}")
    # endregion METHOD___init__

    # region METHOD_to_api_schema [DOMAIN(9): DocumentProcessing; CONCEPT(8): Serialization; TECH(6): API]
    ## @purpose Convert table metadata to API schema.
    ## @uses ApiTableMetadata
    ## @io None -> ApiTableMetadata
    ## @complexity 2
    def to_api_schema(self) -> ApiTableMetadata:
        logger.debug(f"[IMP:4][TableMetadata][TO_API] Converting to API schema")
        return ApiTableMetadata(uid=self.uid, page_id=self.page_id, rotated_angle=self.rotated_angle, title=self.title)
    # endregion METHOD_to_api_schema
# endregion CLASS_TableMetadata

# region MODULE_CONTRACT [DOMAIN(9): DocumentProcessing, DataStructures; CONCEPT(9): Table, Metadata; TECH(6): Python, API]
## @modulecontract
## @purpose Define the TableMetadata data structure — holds table identification, location, rotation, and title.
## @scope Table metadata: page location, UID generation, rotation angle, title.
## @input Page ID, optional UID, rotation angle, title.
## @output TableMetadata instance with auto-generated UID.
## @links [INHERITS(5): Serializable, USES_API(8): ApiTableMetadata]
## @invariants
## - uid is always a non-empty string (auto-generated with uuid4 if not provided)
## @rationale
## Q: Why auto-generate UID with uuid4?
## A: Tables need globally unique identifiers for cross-referencing from text annotations. UUID4 provides collision-resistant IDs without coordination.
## @changes
## LAST_CHANGE: [v1.0.0 – Added semantic markup and LDD logging]
## @modulemap
## CLASS 10[Table metadata container] => TableMetadata
## METHOD 6[Constructor] => __init__
## METHOD 8[API schema conversion] => to_api_schema
## @usecases
## - [TableMetadata]: Reader → ExtractTableMetadata → TableMetadataStored
def _module_contract():
    pass
# endregion MODULE_CONTRACT
# GREP_SUMMARY: TableMetadata, table, metadata, page_id, uid, rotated_angle, title, API, serializable
# STRUCTURE: ▶ TableMetadata ┌page_id?, uid?, rotated_angle, title┐ → ◇ uid auto-gen (uuid4) → ⊕ to_api_schema → ⎋ ApiTableMetadata
