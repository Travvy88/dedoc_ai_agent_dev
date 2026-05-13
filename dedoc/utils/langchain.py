# region MODULE_CONTRACT [DOMAIN(8): DocumentProcessing; CONCEPT(7): PipelineOrchestration; TECH(6): FactoryPattern, LazyImport]
## @modulecontract
## @purpose To dynamically construct manager configuration dictionaries that wire together converters, readers, structure extractors, and metadata extractors based on file extension and parsing parameters. Acts as the central factory for Dedoc processing pipelines.
## @scope Manager config factory for full pipeline, PDF-only pipeline, and minimal attachment-handling pipeline.
## @input File path, split mode, parsing parameters dict.
## @output Manager configuration dict with converter, reader, structure_extractor, structure_constructor, document_metadata_extractor, attachments_handler.
## @links [USES_API(7): dedoc.converters, dedoc.readers, dedoc.structure_extractors, dedoc.metadata_extractors]
## @invariants
## - make_manager_config ALWAYS returns a config dict with all 6 required keys.
## - If with_attachments is True, make_minimal_manager_config is used instead of extension-based routing.
## - Unknown extensions raise BadFileFormatError.
## @rationale
## Q: Why use lazy imports inside functions?
## A: Avoids circular import issues and reduces startup memory by loading only the components needed for a specific file type.
## @changes
## LAST_CHANGE: [v1.0.0 – Added SEMANTIC TEMPLATE markup and LDD logging]
## @modulemap
## DATA 9[Extension format groups] => supported_extensions
## FUNC 10[Full pipeline manager config factory] => make_manager_config
## FUNC 9[PDF-only pipeline manager config factory] => make_manager_pdf_config
## FUNC 8[Minimal attachment pipeline config] => make_minimal_manager_config
## @usecases
## - [make_manager_config]: DedocManager → SelectPipeline → Appropriate reader/converter/extractors wired
def _module_contract():
    pass
# endregion MODULE_CONTRACT
# GREP_SUMMARY: manager config, factory, pipeline, converter, reader, structure extractor, lazy import, extension routing, attachment
# STRUCTURE: ▶ ┌supported_extensions (from extensions)┐ → ⚡ make_manager_config: ┌file_path,split,parsing_params┐ → 〈with_attachments? → make_minimal〉 ∨ get_mime_extension → CASE extension ∋[excel,docx,pptx,html,eml,mhtml,archive,image,pdf,csv,txt,json] → ⚡ instantiate reader+converter+extractor → ⊕ split chooses constructor → ⚡ assemble config dict → ⎋ config

import logging

from dedoc.extensions import converted_extensions, recognized_extensions

logger = logging.getLogger(__name__)

supported_extensions = {
    format_group: {*recognized_extensions._asdict()[format_group], *converted_extensions._asdict()[format_group]}
    for format_group in recognized_extensions._asdict().keys()
}


# region FUNC_make_manager_config [DOMAIN(9): DocumentProcessing; CONCEPT(8): PipelineOrchestration; TECH(7): FactoryPattern, LazyImport]
## @purpose To build a complete manager configuration dictionary by selecting the appropriate converter, reader, and metadata extractor for a given file extension, enabling dynamic pipeline assembly.
## @uses get_mime_extension, get_param_with_attachments, BadFileFormatError
## @io (str, str, dict) -> dict
## @complexity 9
def make_manager_config(file_path: str, split: str, parsing_params: dict) -> dict:
    from dedoc.utils.parameter_utils import get_param_with_attachments
    from dedoc.utils.utils import get_mime_extension
    from dedoc.common.exceptions.bad_file_error import BadFileFormatError

    if get_param_with_attachments(parsing_params):
        logger.info(f"[IMP:7][make_manager_config][ROUTE] Attachments mode, delegating to minimal config")
        return make_minimal_manager_config(split, parsing_params)

    mime, extension = get_mime_extension(file_path=file_path)
    logger.info(f"[IMP:7][make_manager_config][DETECT] File: {file_path}, mime={mime}, ext={extension}")

    if extension in supported_extensions["excel_like_format"]:
        from dedoc.converters.concrete_converters.excel_converter import ExcelConverter
        from dedoc.readers.excel_reader.excel_reader import ExcelReader
        from dedoc.metadata_extractors.concrete_metadata_extractors.base_metadata_extractor import BaseMetadataExtractor
        converter, reader, metadata_extractor = ExcelConverter(), ExcelReader(), BaseMetadataExtractor()
    elif extension in supported_extensions["docx_like_format"]:
        from dedoc.converters.concrete_converters.docx_converter import DocxConverter
        from dedoc.readers.docx_reader.docx_reader import DocxReader
        from dedoc.metadata_extractors.concrete_metadata_extractors.docx_metadata_extractor import DocxMetadataExtractor
        converter, reader, metadata_extractor = DocxConverter(), DocxReader(), DocxMetadataExtractor()
    elif extension in supported_extensions["pptx_like_format"]:
        from dedoc.converters.concrete_converters.pptx_converter import PptxConverter
        from dedoc.readers.pptx_reader.pptx_reader import PptxReader
        from dedoc.metadata_extractors.concrete_metadata_extractors.base_metadata_extractor import BaseMetadataExtractor
        converter, reader, metadata_extractor = PptxConverter(), PptxReader(), BaseMetadataExtractor()
    elif extension in supported_extensions["html_like_format"]:
        from dedoc.readers.html_reader.html_reader import HtmlReader
        from dedoc.metadata_extractors.concrete_metadata_extractors.base_metadata_extractor import BaseMetadataExtractor
        converter, reader, metadata_extractor = None, HtmlReader(), BaseMetadataExtractor()
    elif extension in supported_extensions["eml_like_format"]:
        from dedoc.readers.email_reader.email_reader import EmailReader
        from dedoc.metadata_extractors.concrete_metadata_extractors.base_metadata_extractor import BaseMetadataExtractor
        converter, reader, metadata_extractor = None, EmailReader(), BaseMetadataExtractor()
    elif extension in supported_extensions["mhtml_like_format"]:
        from dedoc.readers.mhtml_reader.mhtml_reader import MhtmlReader
        from dedoc.metadata_extractors.concrete_metadata_extractors.base_metadata_extractor import BaseMetadataExtractor
        converter, reader, metadata_extractor = None, MhtmlReader(), BaseMetadataExtractor()
    elif extension in supported_extensions["archive_like_format"]:
        from dedoc.readers.archive_reader.archive_reader import ArchiveReader
        from dedoc.metadata_extractors.concrete_metadata_extractors.base_metadata_extractor import BaseMetadataExtractor
        converter, reader, metadata_extractor = None, ArchiveReader(), BaseMetadataExtractor()
    elif extension in supported_extensions["image_like_format"]:
        from dedoc.converters.concrete_converters.png_converter import PNGConverter
        from dedoc.readers.pdf_reader.pdf_image_reader.pdf_image_reader import PdfImageReader
        from dedoc.metadata_extractors.concrete_metadata_extractors.image_metadata_extractor import ImageMetadataExtractor
        converter, reader, metadata_extractor = PNGConverter(), PdfImageReader(), ImageMetadataExtractor()
    elif extension in supported_extensions["pdf_like_format"]:
        from dedoc.utils.parameter_utils import get_param_pdf_with_txt_layer
        from dedoc.converters.concrete_converters.pdf_converter import PDFConverter
        from dedoc.metadata_extractors.concrete_metadata_extractors.pdf_metadata_extractor import PdfMetadataExtractor
        pdf_with_text_layer = get_param_pdf_with_txt_layer(parsing_params)
        if pdf_with_text_layer == "true":
            from dedoc.readers.pdf_reader.pdf_txtlayer_reader.pdf_txtlayer_reader import PdfTxtlayerReader
            converter, reader, metadata_extractor = PDFConverter(), PdfTxtlayerReader(), PdfMetadataExtractor()
        elif pdf_with_text_layer == "tabby":
            from dedoc.readers.pdf_reader.pdf_txtlayer_reader.pdf_tabby_reader import PdfTabbyReader
            converter, reader, metadata_extractor = PDFConverter(), PdfTabbyReader(), PdfMetadataExtractor()
        elif pdf_with_text_layer == "false":
            from dedoc.readers.pdf_reader.pdf_image_reader.pdf_image_reader import PdfImageReader
            converter, reader, metadata_extractor = PDFConverter(), PdfImageReader(), PdfMetadataExtractor()
        else:
            from dedoc.readers.pdf_reader.pdf_auto_reader.pdf_auto_reader import PdfAutoReader
            converter, reader, metadata_extractor = PDFConverter(), PdfAutoReader(), PdfMetadataExtractor()
    elif extension in supported_extensions["csv_like_format"]:
        from dedoc.readers.csv_reader.csv_reader import CSVReader
        from dedoc.metadata_extractors.concrete_metadata_extractors.base_metadata_extractor import BaseMetadataExtractor
        converter, reader, metadata_extractor = None, CSVReader(), BaseMetadataExtractor()
    elif extension in supported_extensions["txt_like_format"]:
        from dedoc.converters.concrete_converters.txt_converter import TxtConverter
        from dedoc.readers.txt_reader.raw_text_reader import RawTextReader
        from dedoc.metadata_extractors.concrete_metadata_extractors.base_metadata_extractor import BaseMetadataExtractor
        converter, reader, metadata_extractor = TxtConverter(), RawTextReader(), BaseMetadataExtractor()
    elif extension in supported_extensions["json_like_format"]:
        from dedoc.readers.json_reader.json_reader import JsonReader
        from dedoc.metadata_extractors.concrete_metadata_extractors.base_metadata_extractor import BaseMetadataExtractor
        converter, reader, metadata_extractor = None, JsonReader(), BaseMetadataExtractor()
    else:
        logger.critical(f"[IMP:10][make_manager_config][UNKNOWN] No reader for mime={mime}, ext={extension}")
        raise BadFileFormatError(f'Could not find the suitable reader for the file with mime = "{mime}", extension = "{extension}".')

    if split == "node":
        from dedoc.structure_constructors.concrete_structure_constructors.tree_constructor import TreeConstructor
        constructors, default_constructor = {"tree": TreeConstructor()}, TreeConstructor()
    else:
        from dedoc.structure_constructors.concrete_structure_constructors.linear_constructor import LinearConstructor
        constructors, default_constructor = {"linear": LinearConstructor()}, LinearConstructor()

    from dedoc.converters.converter_composition import ConverterComposition
    from dedoc.readers.reader_composition import ReaderComposition
    from dedoc.structure_extractors.structure_extractor_composition import StructureExtractorComposition
    from dedoc.structure_constructors.structure_constructor_composition import StructureConstructorComposition
    from dedoc.structure_extractors.concrete_structure_extractors.default_structure_extractor import DefaultStructureExtractor
    from dedoc.attachments_handler.attachments_handler import AttachmentsHandler
    from dedoc.metadata_extractors.metadata_extractor_composition import MetadataExtractorComposition

    manager_config = dict(
        converter=ConverterComposition(converters=[converter] if converter else []),
        reader=ReaderComposition(readers=[reader]),
        structure_extractor=StructureExtractorComposition(extractors={"other": DefaultStructureExtractor()}, default_key="other"),
        structure_constructor=StructureConstructorComposition(constructors=constructors, default_constructor=default_constructor),
        document_metadata_extractor=MetadataExtractorComposition(extractors=[metadata_extractor]),
        attachments_handler=AttachmentsHandler()
    )
    logger.info(f"[IMP:8][make_manager_config][ASSEMBLED] Config built for extension={extension}, split={split}")
    return manager_config
# endregion FUNC_make_manager_config


# region FUNC_make_manager_pdf_config [DOMAIN(9): DocumentProcessing; CONCEPT(8): PipelineOrchestration; TECH(7): FactoryPattern]
## @purpose To build a PDF-only manager configuration, raising BadFileFormatError for non-PDF extensions to enforce input type constraints.
## @uses get_mime_extension, get_param_with_attachments, BadFileFormatError
## @io (str, str, dict) -> dict
## @complexity 8
def make_manager_pdf_config(file_path: str, split: str, parsing_params: dict) -> dict:
    from dedoc.utils.parameter_utils import get_param_with_attachments
    from dedoc.utils.utils import get_mime_extension
    from dedoc.common.exceptions.bad_file_error import BadFileFormatError

    if get_param_with_attachments(parsing_params):
        logger.info(f"[IMP:7][make_manager_pdf_config][ROUTE] Attachments mode, delegating to minimal config")
        return make_minimal_manager_config(split, parsing_params)

    mime, extension = get_mime_extension(file_path=file_path)
    logger.info(f"[IMP:7][make_manager_pdf_config][DETECT] File: {file_path}, mime={mime}, ext={extension}")

    if extension in supported_extensions["pdf_like_format"]:
        from dedoc.utils.parameter_utils import get_param_pdf_with_txt_layer
        from dedoc.converters.concrete_converters.pdf_converter import PDFConverter
        from dedoc.metadata_extractors.concrete_metadata_extractors.pdf_metadata_extractor import PdfMetadataExtractor
        pdf_with_text_layer = get_param_pdf_with_txt_layer(parsing_params)
        if pdf_with_text_layer == "true":
            from dedoc.readers.pdf_reader.pdf_txtlayer_reader.pdf_txtlayer_reader import PdfTxtlayerReader
            converter, reader, metadata_extractor = PDFConverter(), PdfTxtlayerReader(), PdfMetadataExtractor()
        elif pdf_with_text_layer == "tabby":
            from dedoc.readers.pdf_reader.pdf_txtlayer_reader.pdf_tabby_reader import PdfTabbyReader
            converter, reader, metadata_extractor = PDFConverter(), PdfTabbyReader(), PdfMetadataExtractor()
        elif pdf_with_text_layer == "false":
            from dedoc.readers.pdf_reader.pdf_image_reader.pdf_image_reader import PdfImageReader
            converter, reader, metadata_extractor = PDFConverter(), PdfImageReader(), PdfMetadataExtractor()
        else:
            from dedoc.readers.pdf_reader.pdf_auto_reader.pdf_auto_reader import PdfAutoReader
            converter, reader, metadata_extractor = PDFConverter(), PdfAutoReader(), PdfMetadataExtractor()
    else:
        logger.critical(f"[IMP:10][make_manager_pdf_config][WRONG_TYPE] Not a PDF: mime={mime}, ext={extension}")
        raise BadFileFormatError(f'Could not find the suitable reader for the file with mime = "{mime}", extension = "{extension}".')

    if split == "node":
        from dedoc.structure_constructors.concrete_structure_constructors.tree_constructor import TreeConstructor
        constructors, default_constructor = {"tree": TreeConstructor()}, TreeConstructor()
    else:
        from dedoc.structure_constructors.concrete_structure_constructors.linear_constructor import LinearConstructor
        constructors, default_constructor = {"linear": LinearConstructor()}, LinearConstructor()

    from dedoc.converters.converter_composition import ConverterComposition
    from dedoc.readers.reader_composition import ReaderComposition
    from dedoc.structure_extractors.structure_extractor_composition import StructureExtractorComposition
    from dedoc.structure_constructors.structure_constructor_composition import StructureConstructorComposition
    from dedoc.structure_extractors.concrete_structure_extractors.default_structure_extractor import DefaultStructureExtractor
    from dedoc.attachments_handler.attachments_handler import AttachmentsHandler
    from dedoc.metadata_extractors.metadata_extractor_composition import MetadataExtractorComposition

    manager_config = dict(
        converter=ConverterComposition(converters=[converter]),
        reader=ReaderComposition(readers=[reader]),
        structure_extractor=StructureExtractorComposition(extractors={"other": DefaultStructureExtractor()}, default_key="other"),
        structure_constructor=StructureConstructorComposition(constructors=constructors, default_constructor=default_constructor),
        document_metadata_extractor=MetadataExtractorComposition(extractors=[metadata_extractor]),
        attachments_handler=AttachmentsHandler()
    )
    logger.info(f"[IMP:8][make_manager_pdf_config][ASSEMBLED] PDF config built for split={split}")
    return manager_config
# endregion FUNC_make_manager_pdf_config


# region FUNC_make_minimal_manager_config [DOMAIN(8): DocumentProcessing; CONCEPT(7): PipelineOrchestration; TECH(6): FactoryPattern]
## @purpose To construct a minimal manager configuration with all available converters and readers for attachment-heavy or multi-format scenarios.
## @io (str, dict) -> dict
## @complexity 7
def make_minimal_manager_config(split: str, parsing_params: dict) -> dict:
    from dedoc.attachments_handler.attachments_handler import AttachmentsHandler
    from dedoc.converters.concrete_converters.binary_converter import BinaryConverter
    from dedoc.converters.concrete_converters.docx_converter import DocxConverter
    from dedoc.converters.concrete_converters.excel_converter import ExcelConverter
    from dedoc.converters.concrete_converters.pdf_converter import PDFConverter
    from dedoc.converters.concrete_converters.png_converter import PNGConverter
    from dedoc.converters.concrete_converters.pptx_converter import PptxConverter
    from dedoc.converters.concrete_converters.txt_converter import TxtConverter
    from dedoc.converters.converter_composition import ConverterComposition
    from dedoc.metadata_extractors.concrete_metadata_extractors.base_metadata_extractor import BaseMetadataExtractor
    from dedoc.metadata_extractors.concrete_metadata_extractors.docx_metadata_extractor import DocxMetadataExtractor
    from dedoc.metadata_extractors.concrete_metadata_extractors.image_metadata_extractor import ImageMetadataExtractor
    from dedoc.metadata_extractors.concrete_metadata_extractors.note_metadata_extarctor import NoteMetadataExtractor
    from dedoc.metadata_extractors.concrete_metadata_extractors.pdf_metadata_extractor import PdfMetadataExtractor
    from dedoc.metadata_extractors.metadata_extractor_composition import MetadataExtractorComposition
    from dedoc.readers.archive_reader.archive_reader import ArchiveReader
    from dedoc.readers.csv_reader.csv_reader import CSVReader
    from dedoc.readers.docx_reader.docx_reader import DocxReader
    from dedoc.readers.email_reader.email_reader import EmailReader
    from dedoc.readers.excel_reader.excel_reader import ExcelReader
    from dedoc.readers.html_reader.html_reader import HtmlReader
    from dedoc.readers.json_reader.json_reader import JsonReader
    from dedoc.readers.mhtml_reader.mhtml_reader import MhtmlReader
    from dedoc.readers.note_reader.note_reader import NoteReader
    from dedoc.readers.pdf_reader.pdf_image_reader.pdf_image_reader import PdfImageReader
    from dedoc.readers.pptx_reader.pptx_reader import PptxReader
    from dedoc.readers.reader_composition import ReaderComposition
    from dedoc.readers.txt_reader.raw_text_reader import RawTextReader
    from dedoc.structure_constructors.structure_constructor_composition import StructureConstructorComposition
    from dedoc.structure_extractors.concrete_structure_extractors.default_structure_extractor import DefaultStructureExtractor
    from dedoc.structure_extractors.structure_extractor_composition import StructureExtractorComposition
    from dedoc.utils.parameter_utils import get_param_pdf_with_txt_layer

    logger.info(f"[IMP:7][make_minimal_manager_config][INIT] Building minimal config for split={split}")

    converters = [DocxConverter(), ExcelConverter(), PptxConverter(), TxtConverter(), PDFConverter(), PNGConverter(), BinaryConverter()]
    readers = []
    pdf_with_text_layer = get_param_pdf_with_txt_layer(parsing_params)
    if pdf_with_text_layer == "true":
        from dedoc.readers.pdf_reader.pdf_txtlayer_reader.pdf_txtlayer_reader import PdfTxtlayerReader
        readers.append(PdfTxtlayerReader())
    elif pdf_with_text_layer == "tabby":
        from dedoc.readers.pdf_reader.pdf_txtlayer_reader.pdf_tabby_reader import PdfTabbyReader
        readers.append(PdfTabbyReader())
    elif pdf_with_text_layer != "false":
        from dedoc.readers.pdf_reader.pdf_auto_reader.pdf_auto_reader import PdfAutoReader
        readers.append(PdfAutoReader())

    readers.extend([
        DocxReader(), ExcelReader(), PptxReader(), RawTextReader(), CSVReader(), HtmlReader(), NoteReader(), JsonReader(), ArchiveReader(), PdfImageReader(),
        EmailReader(), MhtmlReader()
    ])

    metadata_extractors = [DocxMetadataExtractor(), PdfMetadataExtractor(), ImageMetadataExtractor(), NoteMetadataExtractor(), BaseMetadataExtractor()]

    if split == "node":
        from dedoc.structure_constructors.concrete_structure_constructors.tree_constructor import TreeConstructor
        constructors, default_constructor = {"tree": TreeConstructor()}, TreeConstructor()
    else:
        from dedoc.structure_constructors.concrete_structure_constructors.linear_constructor import LinearConstructor
        constructors, default_constructor = {"linear": LinearConstructor()}, LinearConstructor()

    logger.info(f"[IMP:8][make_minimal_manager_config][ASSEMBLED] Minimal config: {len(converters)} converters, {len(readers)} readers, {len(metadata_extractors)} extractors")
    return dict(
        converter=ConverterComposition(converters=converters),
        reader=ReaderComposition(readers=readers),
        structure_extractor=StructureExtractorComposition(extractors={"other": DefaultStructureExtractor()}, default_key="other"),
        structure_constructor=StructureConstructorComposition(constructors=constructors, default_constructor=default_constructor),
        document_metadata_extractor=MetadataExtractorComposition(extractors=metadata_extractors),
        attachments_handler=AttachmentsHandler()
    )
# endregion FUNC_make_minimal_manager_config
