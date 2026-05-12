import logging
from typing import Optional

from dedoc.converters.concrete_converters.abstract_converter import AbstractConverter

logger = logging.getLogger(__name__)


# region CLASS_TxtConverter [DOMAIN(9): DocumentProcessing; CONCEPT(7): Conversion, FileRename; TECH(6): shutil]
## @purpose To convert txt-like documents (.xml) into TXT format by renaming/copying the file to a .txt extension, normalizing XML-based text for downstream processing.
class TxtConverter(AbstractConverter):
    """
    Converts txt-like documents (.xml) into TXT by simple renaming.
    Look to the :class:`~dedoc.converters.AbstractConverter` documentation to get the information about the methods' parameters.
    """

    # region METHOD___init__ [DOMAIN(8): Initialization; CONCEPT(7): Configuration; TECH(6): PythonConstructor]
    ## @purpose To initialize the converter with txt-like extension and MIME type registries from the global extensions configuration.
    ## @uses converted_extensions, converted_mimes
    ## @io config: Optional[dict] -> None
    ## @complexity 2
    def __init__(self, *, config: Optional[dict] = None) -> None:
        from dedoc.extensions import converted_extensions, converted_mimes
        super().__init__(config=config, converted_extensions=converted_extensions.txt_like_format, converted_mimes=converted_mimes.txt_like_format)
        logger.debug(f"[IMP:4][TxtConverter][INIT] Registered txt-like formats")
    # endregion METHOD___init__

    # region METHOD_convert [DOMAIN(9): DocumentProcessing; CONCEPT(7): Conversion, FileRename; TECH(6): shutil, FileIO]
    ## @purpose To convert a txt-like document to .txt by copying the file to a new path with the .txt extension.
    ## @uses os, shutil, splitext_
    ## @io file_path: str, parameters: Optional[dict] -> str
    ## @complexity 3
    def convert(self, file_path: str, parameters: Optional[dict] = None) -> str:
        """
        Convert the txt-like documents into files with .txt extension by renaming it.
        """
        import os
        import shutil
        from dedoc.utils.utils import splitext_

        file_dir, file_name = os.path.split(file_path)
        name_wo_ext, _ = splitext_(file_name)
        converted_file_path = os.path.join(file_dir, f"{name_wo_ext}.txt")
        logger.info(f"[IMP:7][TxtConverter][CONVERT] Copying file_path={file_path} to {converted_file_path}")
        shutil.copy(file_path, converted_file_path)
        logger.info(f"[IMP:9][TxtConverter][RESULT] Converted to {converted_file_path}")

        return converted_file_path
    # endregion METHOD_convert
# endregion CLASS_TxtConverter

# region MODULE_CONTRACT [DOMAIN(9): DocumentProcessing; CONCEPT(7): Conversion, FileRename; TECH(6): shutil]
## @modulecontract
## @purpose To normalize txt-like documents (.xml) into .txt format by simple file copy (preserving original), enabling downstream text readers to consume them with a uniform extension.
## @scope Txt-like document format normalization via file copy.
## @input Files with txt-like extensions (e.g. .xml).
## @output Converted .txt file path.
## @links [USES_API(6): shutil.copy; READS_DATA_FROM(7): dedoc.extensions.converted_extensions]
## @invariants
## - convert() always copies the file (original preserved).
## - Output file path is always {dir}/{name_wo_ext}.txt.
## @rationale
## Q: Why copy instead of rename?
## A: Preserving the original file avoids breaking upstream references and supports idempotent operation.
## @changes
## LAST_CHANGE: [v1.0.0 — Added semantic markup and LDD logging]
## @modulemap
## CLASS 7[Converts txt-like formats to TXT via file copy] => TxtConverter
## @usecases
## - [TxtConverter.convert]: User (Upload) → NormalizeToTxt → TxtFileReady
def _module_contract():
    pass
# endregion MODULE_CONTRACT
# GREP_SUMMARY: txt converter, file copy, shutil, xml, txt, renaming
# STRUCTURE: ▶ ┌file_path┐ → ◇ splitext_ → ⟦shutil.copy → {dir}/{name_wo_ext}.txt⟧ → ⎋ .txt path
