import json
import logging
from collections import OrderedDict

from dedoc.data_structures.annotation import Annotation

logger = logging.getLogger(__name__)


# region CLASS_ColorAnnotation [DOMAIN(4): DocumentProcessing; CONCEPT(5): TextAnnotation, Color; TECH(3): DataStructure]
## @purpose Mark color of some text inside the line in RGB format.
class ColorAnnotation(Annotation):
    """
    Color of some text inside the line in the RGB format.
    """
    name = "color_annotation"

    # region METHOD___init__ [DOMAIN(4): DocumentProcessing; CONCEPT(5): TextAnnotation; TECH(3): DataStructure, JSON]
    ## @purpose Initialize color annotation with validated RGB values.
    ## @uses Annotation.__init__, json
    ## @io (int, int, float, float, float) -> None
    ## @complexity 4
    def __init__(self, start: int, end: int, red: float, green: float, blue: float) -> None:
        """
        :param start: start of the colored text
        :param end: end of the colored text (not included)
        :param red: mean value of the red color component in the pixels that are not white in the given bounding box
        :param green: mean value of the green color component in the pixels that are not white in the given bounding box
        :param blue: mean value of the blue color component in the pixels that are not white in the given bounding box
        """
        logger.debug(f"[IMP:4][ColorAnnotation][INIT] start={start}, end={end}, red={red}, green={green}, blue={blue}")

        assert red >= 0
        assert green >= 0
        assert blue >= 0

        self.red = red
        self.blue = blue
        self.green = green

        value = OrderedDict()
        value["red"] = red
        value["blue"] = blue
        value["green"] = green
        super().__init__(start=start, end=end, name=ColorAnnotation.name, value=json.dumps(value))
        logger.debug(f"[IMP:4][ColorAnnotation][INIT] ColorAnnotation created successfully")
    # endregion METHOD___init__

    # region METHOD___str__ [DOMAIN(4): DocumentProcessing; CONCEPT(5): TextAnnotation; TECH(3): DataStructure]
    ## @purpose Return string representation of the color annotation.
    ## @io None -> str
    ## @complexity 1
    def __str__(self) -> str:
        return f"ColorAnnotation(red={self.red}, green={self.green}, blue={self.blue})"
    # endregion METHOD___str__
# endregion CLASS_ColorAnnotation

# region MODULE_CONTRACT [DOMAIN(4): DocumentProcessing; CONCEPT(5): TextAnnotation, Color; TECH(3): DataStructure, Python]
## @modulecontract
## @purpose Provide RGB color annotation — stores the mean color of text pixels in a bounding box as JSON-encoded RGB.
## @scope Text annotation for color formatting.
## @input RGB float values (red, green, blue).
## @output ColorAnnotation instance with JSON-serialized color value.
## @links [INHERITS(9): Annotation]
## @invariants
## - red >= 0, green >= 0, blue >= 0
## - value is JSON-encoded OrderedDict with "red", "green", "blue" keys
## @rationale
## Q: Why store color as JSON string rather than tuple?
## A: Annotation.value is str-typed; JSON provides a structured yet serializable format.
## @changes
## LAST_CHANGE: [v1.0.0 – Added semantic markup and LDD logging]
## @modulemap
## CLASS 10[Color text annotation] => ColorAnnotation
## @usecases
## - [ColorAnnotation]: Reader → ExtractTextColor → ColorAnnotationStored
def _module_contract():
    pass
# endregion MODULE_CONTRACT
# GREP_SUMMARY: color, RGB, annotation, text, formatting, document, JSON, red, green, blue
# STRUCTURE: ▶ Init [start, end, red, green, blue] → ◇ assert RGB >= 0 → ⊕ OrderedDict→json.dumps → super().__init__(name="color_annotation") → ⎋ ColorAnnotation
