import logging
from typing import Optional

from dedoc.converters.concrete_converters.abstract_converter import AbstractConverter

logger = logging.getLogger(__name__)


# region CLASS_PDFConverter [DOMAIN(9): DocumentProcessing; CONCEPT(9): Conversion, PdfToPdf; TECH(8): ddjvu, subprocess]
## @purpose To convert pdf-like documents (.djvu) into PDF format using the ddjvu command-line application.
class PDFConverter(AbstractConverter):
    """
    Converts pdf-like documents (.djvu) into PDF using the ddjvu application.
    Look to the :class:`~dedoc.converters.AbstractConverter` documentation to get the information about the methods' parameters.
    """

    # region METHOD___init__ [DOMAIN(8): Initialization; CONCEPT(7): Configuration; TECH(6): PythonConstructor]
    ## @purpose To initialize the converter with pdf-like extension and MIME type registries from the global extensions configuration.
    ## @uses converted_extensions, converted_mimes
    ## @io config: Optional[dict] -> None
    ## @complexity 2
    def __init__(self, *, config: Optional[dict] = None) -> None:
        from dedoc.extensions import converted_extensions, converted_mimes
        super().__init__(config=config, converted_extensions=converted_extensions.pdf_like_format, converted_mimes=converted_mimes.pdf_like_format)
        logger.debug(f"[IMP:4][PDFConverter][INIT] Registered pdf-like formats")
    # endregion METHOD___init__

    # region METHOD_convert [DOMAIN(9): DocumentProcessing; CONCEPT(9): Conversion, PdfToPdf; TECH(8): ddjvu, subprocess]
    ## @purpose To convert a pdf-like document to .pdf by invoking ddjvu --format=pdf and waiting for the output file.
    ## @uses os, splitext_, _run_subprocess
    ## @io file_path: str, parameters: Optional[dict] -> str
    ## @complexity 4
    def convert(self, file_path: str, parameters: Optional[dict] = None) -> str:
        """
        Convert the pdf-like documents into files with .pdf extension using the ddjvu application.
        """
        import os
        from dedoc.utils.utils import splitext_

        file_dir, file_name = os.path.split(file_path)
        name_wo_ext, _ = splitext_(file_name)
        converted_file_path = os.path.join(file_dir, f"{name_wo_ext}.pdf")
        command = ["ddjvu", "--format=pdf", file_path, converted_file_path]
        logger.info(f"[IMP:7][PDFConverter][CONVERT] Running ddjvu for file_path={file_path}")
        self._run_subprocess(command=command, filename=file_name, expected_path=converted_file_path)
        logger.info(f"[IMP:9][PDFConverter][RESULT] Converted to {converted_file_path}")

        return converted_file_path
    # endregion METHOD_convert
# endregion CLASS_PDFConverter

# region MODULE_CONTRACT [DOMAIN(9): DocumentProcessing; CONCEPT(9): Conversion, PdfToPdf; TECH(8): ddjvu, DjVuLibre]
## @modulecontract
## @purpose To normalize pdf-like documents (.djvu) into the PDF format via the ddjvu utility, providing a uniform input format for downstream PDF readers.
## @scope PDF-like document format normalization via ddjvu.
## @input Files with pdf-like extensions or MIME types (e.g. .djvu).
## @output Converted .pdf file path.
## @links [USES_API(9): ddjvu (DjVuLibre); READS_DATA_FROM(7): dedoc.extensions.converted_extensions]
## @invariants
## - convert() always invokes ddjvu with --format=pdf.
## - Output file path is always {dir}/{name_wo_ext}.pdf.
## @rationale
## Q: Why ddjvu instead of a Python library?
## A: ddjvu is the reference DjVu-to-PDF converter from the DjVuLibre project. No pure-Python equivalent exists.
## @changes
## LAST_CHANGE: [v1.0.0 — Added semantic markup and LDD logging]
## @modulemap
## CLASS 9[Converts pdf-like formats to PDF via ddjvu] => PDFConverter
## @usecases
## - [PDFConverter.convert]: User (Upload) → NormalizeToPdf → PdfFileReady
def _module_contract():
    pass
# endregion MODULE_CONTRACT
# GREP_SUMMARY: pdf converter, ddjvu, djvu, conversion, subprocess, DjVuLibre
# STRUCTURE: ▶ ┌file_path┐ → ◇ splitext_ → ⚡ ddjvu --format=pdf file_path converted_path → ⊕ _run_subprocess [timeout] → ◇ check expected_path → ⎋ .pdf path
