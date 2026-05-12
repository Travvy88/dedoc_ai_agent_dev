import logging
from typing import Tuple

from dedocutils.data_structures import BBox

from dedoc.data_structures.annotation import Annotation

logger = logging.getLogger(__name__)


# region CLASS_BBoxAnnotation [DOMAIN(4): DocumentProcessing; CONCEPT(5): TextAnnotation, BoundingBox; TECH(3): DataStructure, JSON]
## @purpose Store coordinates of the line's bounding box in relative coordinates for PDF documents.
class BBoxAnnotation(Annotation):
    """
    Coordinates of the line's bounding box (in relative coordinates) - for pdf documents.
    """
    name = "bounding box"

    # region METHOD___init__ [DOMAIN(4): DocumentProcessing; CONCEPT(5): TextAnnotation; TECH(3): DataStructure, JSON]
    ## @purpose Initialize bounding box annotation with BBox object serialized as JSON.
    ## @uses Annotation.__init__, json, BBox.to_relative_dict
    ## @io (int, int, BBox, int, int) -> None
    ## @complexity 4
    def __init__(self, start: int, end: int, value: BBox, page_width: int, page_height: int) -> None:
        """
        :param start: start of the annotated text (usually zero)
        :param end: end of the annotated text (usually end of the line)
        :param value: bounding box where line is located
        :param page_width: width of original image with this bbox
        :param page_height: height of original image with this bbox
        """
        import json

        logger.debug(f"[IMP:4][BBoxAnnotation][INIT] start={start}, end={end}, page_width={page_width}, page_height={page_height}")

        if not isinstance(value, BBox):
            raise ValueError("the value of bounding box annotation should be instance of BBox")

        super().__init__(start=start, end=end, name=BBoxAnnotation.name, value=json.dumps(value.to_relative_dict(page_width, page_height)), is_mergeable=False)
        logger.debug(f"[IMP:4][BBoxAnnotation][INIT] BBoxAnnotation created successfully")
    # endregion METHOD___init__

    # region METHOD_get_bbox_from_value [DOMAIN(4): DocumentProcessing; CONCEPT(5): TextAnnotation; TECH(3): DataStructure, JSON]
    ## @purpose Deserialize JSON bounding box value back to BBox object with absolute coordinates.
    ## @uses json, BBox
    ## @io str -> Tuple[BBox, int, int]
    ## @complexity 4
    @staticmethod
    def get_bbox_from_value(value: str) -> Tuple[BBox, int, int]:
        """
        Returns: BBox object, page_width, page_height
        """
        import json

        logger.debug(f"[IMP:4][BBoxAnnotation][GET_BBOX] Deserializing BBox from value")

        bbox_dict = json.loads(value)
        bbox = BBox(x_top_left=int(bbox_dict["x_top_left"] * bbox_dict["page_width"]),
                    y_top_left=int(bbox_dict["y_top_left"] * bbox_dict["page_height"]),
                    width=int(bbox_dict["width"] * bbox_dict["page_width"]),
                    height=int(bbox_dict["height"] * bbox_dict["page_height"]))
        logger.debug(f"[IMP:4][BBoxAnnotation][GET_BBOX] Deserialized BBox: x={bbox.x_top_left}, y={bbox.y_top_left}, w={bbox.width}, h={bbox.height}")
        return bbox, bbox_dict["page_width"], bbox_dict["page_height"]
    # endregion METHOD_get_bbox_from_value
# endregion CLASS_BBoxAnnotation

# region MODULE_CONTRACT [DOMAIN(4): DocumentProcessing; CONCEPT(5): TextAnnotation, BoundingBox; TECH(3): DataStructure, Python, BBox]
## @modulecontract
## @purpose Provide bounding box annotation — stores line coordinates as relative JSON for PDF documents.
## @scope Text annotation for spatial coordinates of lines.
## @input BBox object, page dimensions.
## @output BBoxAnnotation instance with JSON-serialized relative coordinates.
## @links [INHERITS(9): Annotation, USES_API(9): dedocutils.data_structures.BBox]
## @invariants
## - value is JSON with keys: x_top_left, y_top_left, width, height, page_width, page_height
## - is_mergeable is always False
## @rationale
## Q: Why store relative coordinates rather than absolute?
## A: Relative coordinates are resolution-independent and survive image resizing.
## @changes
## LAST_CHANGE: [v1.0.0 – Added semantic markup and LDD logging]
## @modulemap
## CLASS 10[Bounding box annotation] => BBoxAnnotation
## @usecases
## - [BBoxAnnotation]: PDF_Reader → ExtractLineBBox → BBoxAnnotationStored
def _module_contract():
    pass
# endregion MODULE_CONTRACT
# GREP_SUMMARY: bounding, box, BBox, annotation, text, document, PDF, coordinates, relative, JSON
# STRUCTURE: ▶ Init [start, end, BBox, page_w, page_h] → ◇ isinstance(value, BBox) → ⊕ BBox.to_relative_dict→json.dumps → super().__init__(name="bounding box") → ⎋ BBoxAnnotation
