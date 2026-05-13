import logging
from typing import Optional

from dedoc.converters.concrete_converters.abstract_converter import AbstractConverter

logger = logging.getLogger(__name__)


# region CLASS_ExcelConverter [DOMAIN(9): DocumentProcessing; CONCEPT(9): Conversion, XlsToXlsx; TECH(8): soffice, subprocess]
## @purpose To convert xlsx-like documents (.xls, .ods) into XLSX format using the LibreOffice soffice headless application.
class ExcelConverter(AbstractConverter):
    """
    Converts xlsx-like documents (.xls, .ods) into XLSX using the soffice application.
    Look to the :class:`~dedoc.converters.AbstractConverter` documentation to get the information about the methods' parameters.
    """

    # region METHOD___init__ [DOMAIN(8): Initialization; CONCEPT(7): Configuration; TECH(6): PythonConstructor]
    ## @purpose To initialize the converter with excel-like extension and MIME type registries from the global extensions configuration.
    ## @uses converted_extensions, converted_mimes
    ## @io config: Optional[dict] -> None
    ## @complexity 2
    def __init__(self, *, config: Optional[dict] = None) -> None:
        from dedoc.extensions import converted_extensions, converted_mimes
        super().__init__(config=config, converted_extensions=converted_extensions.excel_like_format, converted_mimes=converted_mimes.excel_like_format)
        logger.debug(f"[IMP:4][ExcelConverter][INIT] Registered excel-like formats")
    # endregion METHOD___init__

    # region METHOD_convert [DOMAIN(9): DocumentProcessing; CONCEPT(9): Conversion, XlsToXlsx; TECH(8): soffice, subprocess]
    ## @purpose To convert an xlsx-like document to .xlsx by invoking soffice --headless --convert-to xlsx and waiting for the output file.
    ## @uses os, splitext_, _run_subprocess
    ## @io file_path: str, parameters: Optional[dict] -> str
    ## @complexity 4
    def convert(self, file_path: str, parameters: Optional[dict] = None) -> str:
        """
        Convert the xlsx-like documents into files with .xlsx extension using the soffice application.
        """
        import os
        from dedoc.utils.utils import splitext_

        file_dir, file_name = os.path.split(file_path)
        name_wo_ext, _ = splitext_(file_name)
        command = ["soffice", "--headless", "--convert-to", "xlsx", "--outdir", file_dir, file_path]
        converted_file_path = os.path.join(file_dir, f"{name_wo_ext}.xlsx")
        logger.info(f"[IMP:7][ExcelConverter][CONVERT] Running soffice for file_path={file_path}")
        self._run_subprocess(command=command, filename=file_name, expected_path=converted_file_path)
        logger.info(f"[IMP:9][ExcelConverter][RESULT] Converted to {converted_file_path}")

        return converted_file_path
    # endregion METHOD_convert
# endregion CLASS_ExcelConverter

# region MODULE_CONTRACT [DOMAIN(9): DocumentProcessing; CONCEPT(9): Conversion, XlsToXlsx; TECH(8): soffice, LibreOffice]
## @modulecontract
## @purpose To normalize xlsx-like documents (.xls, .ods) into the XLSX format via LibreOffice headless conversion, providing a uniform input format for downstream spreadsheet readers.
## @scope Excel-like document format normalization via soffice.
## @input Files with excel-like extensions or MIME types.
## @output Converted .xlsx file path.
## @links [USES_API(9): LibreOffice soffice; READS_DATA_FROM(7): dedoc.extensions.converted_extensions]
## @invariants
## - convert() always invokes soffice with --headless --convert-to xlsx.
## - Output file path is always {dir}/{name_wo_ext}.xlsx.
## @rationale
## Q: Why soffice instead of openpyxl for conversion?
## A: soffice handles legacy binary .xls and .ods formats that openpyxl cannot read.
## @changes
## LAST_CHANGE: [v1.0.0 — Added semantic markup and LDD logging]
## @modulemap
## CLASS 9[Converts excel-like formats to XLSX via LibreOffice] => ExcelConverter
## @usecases
## - [ExcelConverter.convert]: User (Upload) → NormalizeToXlsx → XlsxFileReady
def _module_contract():
    pass
# endregion MODULE_CONTRACT
# GREP_SUMMARY: excel converter, soffice, libreoffice, xls, ods, conversion, headless, spreadsheet
# STRUCTURE: ▶ ┌file_path┐ → ◇ splitext_ → ⚡ soffice --headless --convert-to xlsx → ⊕ _run_subprocess [timeout] → ◇ check expected_path → ⎋ .xlsx path
