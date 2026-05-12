import logging

from .concrete_converters.abstract_converter import AbstractConverter
from .concrete_converters.binary_converter import BinaryConverter
from .concrete_converters.docx_converter import DocxConverter
from .concrete_converters.excel_converter import ExcelConverter
from .concrete_converters.pdf_converter import PDFConverter
from .concrete_converters.png_converter import PNGConverter
from .concrete_converters.pptx_converter import PptxConverter
from .concrete_converters.txt_converter import TxtConverter
from .converter_composition import ConverterComposition

logger = logging.getLogger(__name__)

__all__ = ["AbstractConverter", "BinaryConverter", "DocxConverter", "ExcelConverter", "ConverterComposition", "PDFConverter", "PNGConverter",
           "PptxConverter", "TxtConverter"]

# region MODULE_CONTRACT [DOMAIN(9): DocumentProcessing; CONCEPT(7): Conversion; TECH(7): PythonImport]
## @modulecontract
## @purpose To expose all converter classes and ConverterComposition from a single public entry point, enabling the rest of the system to import converters without knowledge of internal file layout.
## @scope Public API surface for the converters subsystem.
## @input None (re-exports internal modules).
## @output Re-exported symbols: AbstractConverter, BinaryConverter, DocxConverter, ExcelConverter, ConverterComposition, PDFConverter, PNGConverter, PptxConverter, TxtConverter.
## @links [USES_API(7): dedoc.converters.concrete_converters.*]
## @invariants
## - __all__ always lists every public converter symbol.
## @rationale
## Q: Why gather all imports here?
## A: Single import point simplifies dependency management for agents and consumers.
## @changes
## LAST_CHANGE: [v1.0.0 — Added semantic markup and LDD logging]
## @modulemap
## FUNC 5[init re-exports] => __init__
## @usecases
## - [__init__]: System (Startup) → ImportConverters → AllConvertersAvailable
def _module_contract():
    pass
# endregion MODULE_CONTRACT
# GREP_SUMMARY: converters, import, public API, AbstractConverter, BinaryConverter, DocxConverter, ExcelConverter, ConverterComposition, PDFConverter, PNGConverter, PptxConverter, TxtConverter
# STRUCTURE: ▶ ┌internal modules┐ → ⊕ re-export symbols → ⎋ __all__ public surface
