import logging

from .alignment_annotation import AlignmentAnnotation
from .attach_annotation import AttachAnnotation
from .bbox_annotation import BBoxAnnotation
from .bold_annotation import BoldAnnotation
from .color_annotation import ColorAnnotation
from .confidence_annotation import ConfidenceAnnotation
from .indentation_annotation import IndentationAnnotation
from .italic_annotation import ItalicAnnotation
from .linked_text_annotation import LinkedTextAnnotation
from .size_annotation import SizeAnnotation
from .spacing_annotation import SpacingAnnotation
from .strike_annotation import StrikeAnnotation
from .style_annotation import StyleAnnotation
from .subscript_annotation import SubscriptAnnotation
from .superscript_annotation import SuperscriptAnnotation
from .table_annotation import TableAnnotation
from .underlined_annotation import UnderlinedAnnotation
from .reference_annotation import ReferenceAnnotation

logger = logging.getLogger(__name__)

__all__ = ['AlignmentAnnotation', 'AttachAnnotation', 'BBoxAnnotation', 'BoldAnnotation', 'ColorAnnotation', 'ConfidenceAnnotation',
           'IndentationAnnotation', 'ItalicAnnotation', 'LinkedTextAnnotation', 'SizeAnnotation', 'SpacingAnnotation', 'StrikeAnnotation',
           'StyleAnnotation', 'SubscriptAnnotation', 'SuperscriptAnnotation', 'TableAnnotation', 'UnderlinedAnnotation', 'ReferenceAnnotation']

logger.debug(f"[IMP:4][concrete_annotations__init__][INIT] Exported {len(__all__)} annotation types")

# region MODULE_CONTRACT [DOMAIN(9): DocumentProcessing, Annotations; CONCEPT(8): ModuleAggregation, ConcreteAnnotations; TECH(5): Python, PackageInit]
## @modulecontract
## @purpose Aggregate all concrete annotation types into a single namespace for use by readers and converters.
## @scope Re-export of all concrete annotation classes (bold, italic, size, color, etc.).
## @input None (package-level imports).
## @output Unified __all__ list containing all annotation symbols.
## @links [EXPORTS(10): AlignmentAnnotation, AttachAnnotation, BBoxAnnotation, BoldAnnotation, ColorAnnotation, ConfidenceAnnotation, IndentationAnnotation, ItalicAnnotation, LinkedTextAnnotation, SizeAnnotation, SpacingAnnotation, StrikeAnnotation, StyleAnnotation, SubscriptAnnotation, SuperscriptAnnotation, TableAnnotation, UnderlinedAnnotation, ReferenceAnnotation]
## @invariants
## - __all__ includes all 18 concrete annotation types
## @rationale
## Q: Why separate concrete_annotations from the base Annotation?
## A: Clean separation of base class from its implementations, enabling independent evolution.
## @changes
## LAST_CHANGE: [v1.0.0 – Added semantic markup and LDD logging]
## @modulemap
## MODULE 10[Concrete annotation exports] => __init__
## @usecases
## - [__init__]: Reader/Converter → ImportAnnotations → AllAnnotationTypesAvailable
def _module_contract():
    pass
# endregion MODULE_CONTRACT
# GREP_SUMMARY: annotations, concrete, exports, init, package, Alignment, Attach, BBox, Bold, Color, Confidence, Indentation, Italic, LinkedText, Size, Spacing, Strike, Style, Subscript, Superscript, Table, Underlined, Reference
# STRUCTURE: ▶ Import ┌18 annotation classes┐ → ⊕ __all__ = [all symbols] → ⎋ public namespace
