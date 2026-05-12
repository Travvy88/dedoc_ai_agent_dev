import logging
from typing import List, Optional

from dedoc.converters.concrete_converters.abstract_converter import AbstractConverter

logger = logging.getLogger(__name__)


# region CLASS_ConverterComposition [DOMAIN(9): DocumentProcessing; CONCEPT(8): ConversionPipeline; TECH(7): PythonComposition]
## @purpose To orchestrate a chain of format-specific converters, applying the first suitable one to a given file, so the caller does not need to know which converter handles which format.
class ConverterComposition:
    """
    This class allows to convert any document into the predefined list of formats according to the available list of converters.
    The list of converters is set via the class constructor.
    The first suitable converter is used (the one whose method :meth:`~dedoc.converters.AbstractConverter.can_convert` returns True), \
    so the order of converters is important.
    """

    # region METHOD___init__ [DOMAIN(8): Initialization; CONCEPT(7): DependencyInjection; TECH(6): PythonConstructor]
    ## @purpose To initialize the converter chain with an ordered list of converters.
    ## @uses List, AbstractConverter
    ## @io converters: List[AbstractConverter] -> None
    ## @complexity 1
    def __init__(self, converters: List[AbstractConverter]) -> None:
        """
        :param converters: the list of converters that have methods can_convert() and convert(), they are used for files converting into specified formats
        """
        logger.debug(f"[IMP:4][ConverterComposition][INIT] Initialized with {len(converters)} converters")
        self.converters = converters
    # endregion METHOD___init__

    # region METHOD_convert [DOMAIN(9): DocumentProcessing; CONCEPT(9): ConversionPipeline; TECH(8): MimeDetection, FileIO]
    ## @purpose To convert a file using the first suitable converter from the chain, falling back to the original file if no converter matches.
    ## @uses os, stat, get_mime_extension, AbstractConverter.can_convert, AbstractConverter.convert
    ## @io file_path: str, parameters: Optional[dict], extension: Optional[str], mime: Optional[str] -> str
    ## @complexity 5
    def convert(self, file_path: str, parameters: Optional[dict] = None, extension: Optional[str] = None, mime: Optional[str] = None) -> str:
        """
        Convert file if there is the converter that can do it.
        If there isn't any converter that is able to convert the file, it isn't changed.

        :param file_path: path of the file to convert
        :param parameters: parameters of converting, see :ref:`parameters_description` for more details
        :param extension: file extension, for example .doc or .pdf
        :param mime: MIME type of file
        :return: path of converted file if conversion was executed else path of the original file
        """
        import os
        from stat import S_IREAD, S_IRGRP, S_IROTH
        from dedoc.utils.utils import get_mime_extension

        mime, extension = get_mime_extension(file_path=file_path, extension=extension, mime=mime)
        logger.debug(f"[IMP:4][ConverterComposition][MIME_DETECT] file_path={file_path}, mime={mime}, extension={extension}")
        converted_file_path = file_path

        for converter in self.converters:
            if converter.can_convert(file_path=file_path, extension=extension, mime=mime, parameters=parameters):
                logger.info(f"[IMP:7][ConverterComposition][CONVERT] Using converter={type(converter).__name__} for file_path={file_path}")
                converted_file_path = converter.convert(file_path, parameters=parameters)
                break
        os.chmod(converted_file_path, S_IREAD | S_IRGRP | S_IROTH)
        logger.info(f"[IMP:9][ConverterComposition][RESULT] Converted path={converted_file_path}")
        return converted_file_path
    # endregion METHOD_convert
# endregion CLASS_ConverterComposition

# region MODULE_CONTRACT [DOMAIN(9): DocumentProcessing; CONCEPT(8): ConversionPipeline; TECH(7): PythonComposition]
## @modulecontract
## @purpose To provide a composite converter that iterates through a configured chain of format-specific converters, using the first match to transform any document into a processable format.
## @scope Converter chain orchestration, MIME detection delegation, file permission hardening.
## @input converters: List[AbstractConverter] passed at construction.
## @output Converted file path (str).
## @links [USES_API(8): dedoc.utils.utils.get_mime_extension, dedoc.converters.AbstractConverter]
## @invariants
## - convert() always returns a valid file path (original or converted).
## - Output file is always made world-readable via chmod.
## @rationale
## Q: Why a chain pattern instead of a registry?
## A: Converter ordering matters (e.g., DOCX before generic binary). A list preserves user-specified priority.
## @changes
## LAST_CHANGE: [v1.0.0 — Added semantic markup and LDD logging]
## @modulemap
## CLASS 9[Orchestrates ordered converter chain] => ConverterComposition
## @usecases
## - [ConverterComposition.convert]: User (Upload) → FindSuitableConverter → ConvertedFileReturned
def _module_contract():
    pass
# endregion MODULE_CONTRACT
# GREP_SUMMARY: converter composition, chain, orchestration, MIME detection, file conversion, chmod
# STRUCTURE: ▶ ┌file_path, mime, extension┐ → ◇ get_mime_extension → ○ Loop ∋converter: 〈can_convert ? convert : skip〉 → ⊕ chmod result → ⎋ converted_file_path
