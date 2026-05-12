import logging
from typing import Dict, Optional, Tuple

from dedoc.api.api_args import QueryParameters
from dedoc.common.exceptions.bad_file_error import BadFileFormatError
from dedoc.common.exceptions.conversion_error import ConversionError
from dedoc.common.exceptions.dedoc_error import DedocError
from dedoc.data_structures.parsed_document import ParsedDocument
from dedoc.data_structures.unstructured_document import UnstructuredDocument

logger = logging.getLogger(__name__)


# region CLASS_DedocManager [DOMAIN(9): DocumentProcessing; CONCEPT(9): Orchestrator, Pipeline; TECH(8): Composition, Delegation]
## @purpose To orchestrate the entire document processing pipeline (convert → read → metadata → structure → construct → attachments), serving as the central coordinator that composes all specialized processors into a single `parse` operation.
class DedocManager:
    """
    This class allows to run the whole pipeline of the document processing:

        1. Converting
        2. Reading
        3. Metadata extraction
        4. Structure extraction
        5. Output structure construction
        6. Attachments handling
    """

    # region METHOD___init__ [DOMAIN(8): Composition; CONCEPT(7): DependencyInjection; TECH(7): LazyImport]
    ## @purpose To initialize the DedocManager with all pipeline components (converter, reader, structure_extractor, structure_constructor, metadata_extractor, attachments_handler), wiring them together for document processing.
    ## @uses dedoc.config.get_config, dedoc.manager_config.get_manager_config
    ## @io (Optional[dict], Optional[dict]) -> None
    ## @complexity 6
    def __init__(self, config: Optional[dict] = None, manager_config: Optional[dict] = None) -> None:
        """
        :param config: config for document processing
        :param manager_config: dictionary with different stage document processors.

        The following keys should be in the `manager_config` dictionary:
            - converter (optional) (:class:`~dedoc.converters.ConverterComposition`)
            - reader (:class:`~dedoc.readers.ReaderComposition`)
            - structure_extractor (:class:`~dedoc.structure_extractors.StructureExtractorComposition`)
            - structure_constructor (:class:`~dedoc.structure_constructors.StructureConstructorComposition`)
            - document_metadata_extractor (:class:`~dedoc.metadata_extractors.MetadataExtractorComposition`)
            - attachments_handler (:class:`~dedoc.attachments_handler.AttachmentsHandler`)
        """
        import logging

        from dedoc.config import get_config
        from dedoc.manager_config import get_manager_config

        # LDD-log: init start
        logger.debug(f"[IMP:4][DedocManager][INIT] Initializing DedocManager with pipeline components")

        self.config = get_config() if config is None else config
        self.logger = self.config.get("logger", logging.getLogger())
        manager_config = get_manager_config(self.config) if manager_config is None else manager_config

        self.converter = manager_config.get("converter", None)
        self.reader = manager_config.get("reader", None)
        assert self.reader is not None, "Reader shouldn't be None"
        self.structure_extractor = manager_config.get("structure_extractor", None)
        assert self.structure_extractor is not None, "Structure extractor shouldn't be None"
        self.structure_constructor = manager_config.get("structure_constructor", None)
        assert self.structure_constructor is not None, "Structure constructor shouldn't be None"
        self.document_metadata_extractor = manager_config.get("document_metadata_extractor", None)
        assert self.document_metadata_extractor is not None, "Document metadata extractor shouldn't be None"
        self.attachments_handler = manager_config.get("attachments_handler", None)
        assert self.attachments_handler is not None, "Attachments handler shouldn't be None"

        self.default_parameters = QueryParameters().to_dict()

        # LDD-log: init complete
        logger.info(f"[IMP:8][DedocManager][INIT] Pipeline initialized: reader={type(self.reader).__name__}, "
                    f"structure_extractor={type(self.structure_extractor).__name__}, "
                    f"structure_constructor={type(self.structure_constructor).__name__}")
    # endregion METHOD___init__

    # region METHOD_parse [DOMAIN(9): Orchestration; CONCEPT(8): ErrorHandling, Pipeline; TECH(7): Delegation]
    ## @purpose To execute the full document processing pipeline on a given file, with error handling that enriches exceptions with file metadata before re-raising.
    ## @uses __parse_no_error_handling, __init_parameters, BaseMetadataExtractor
    ## @io (str, Optional[Dict[str, str]]) -> ParsedDocument
    ## @complexity 7
    def parse(self, file_path: str, parameters: Optional[Dict[str, str]] = None) -> ParsedDocument:
        """
        Run the whole pipeline of the document processing.
        If some error occurred, file metadata are stored in the exception's metadata field.

        :param file_path: full path where the file is located
        :param parameters: any parameters, specify how to parse file, see :ref:`parameters_description` for more details
        :return: parsed document
        """
        import os.path

        parameters = self.__init_parameters(file_path, parameters)
        # LDD-log: parse start — boundary event
        self.logger.info(f"[IMP:7][DedocManager][PARSE_START] Get file {os.path.basename(file_path)} with parameters {parameters}")

        try:
            result = self.__parse_no_error_handling(file_path=file_path, parameters=parameters)
            # LDD-log: parse success — business value
            self.logger.info(f"[IMP:9][DedocManager][PARSE_SUCCESS] Document parsed: {os.path.basename(file_path)}")
            return result
        except DedocError as e:
            from dedoc.metadata_extractors.concrete_metadata_extractors.base_metadata_extractor import BaseMetadataExtractor

            file_dir, file_name = os.path.split(file_path)
            e.filename = file_name
            e.metadata = BaseMetadataExtractor._get_base_meta_information(directory=file_dir, filename=file_name, name_actual=file_name)
            # LDD-log: error with metadata enrichment
            self.logger.error(f"[IMP:9][DedocManager][PARSE_ERROR] Failed to parse {file_name}: {e}")
            raise e
    # endregion METHOD_parse

    # region METHOD___parse_no_error_handling [DOMAIN(9): Pipeline; CONCEPT(8): SequentialProcessing; TECH(7): tempfile, shutil]
    ## @purpose To execute the 6-step document processing pipeline (file copy → convert+read+metadata → structure extraction → output construction → attachments) without error handling, serving as the core processing workflow.
    ## @uses converter, reader, structure_extractor, structure_constructor, attachments_handler, __read_with_mime_auto_detection, __save
    ## @io (str, Dict[str, str]) -> ParsedDocument
    ## @complexity 8
    def __parse_no_error_handling(self, file_path: str, parameters: Dict[str, str]) -> ParsedDocument:
        """
        Function of complete document parsing without errors handling.

        :param file_path: full path where the file is located
        :param parameters: any parameters, specify how to parse file
        :return: parsed document
        """
        import os.path
        import shutil
        import tempfile
        from dedoc.utils.utils import get_unique_name

        if not os.path.isfile(path=file_path):
            raise FileNotFoundError(file_path)
        # LDD-log: pipeline start
        self.logger.info(f"[IMP:7][DedocManager][PIPELINE_START] Start handle {file_path}")
        file_dir, file_name = os.path.split(file_path)
        unique_filename = get_unique_name(file_name)

        with tempfile.TemporaryDirectory() as tmp_dir:
            tmp_file_path = os.path.join(tmp_dir, unique_filename)
            shutil.copy(file_path, tmp_file_path)

            # Steps 1-3 - Converting, Reading content and Adding meta-information
            # LDD-log: content extraction phase
            self.logger.info(f"[IMP:7][DedocManager][CONTENT_EXTRACT] Extract content from file {file_name}")
            converted_file_path, unstructured_document = self.__read_with_mime_auto_detection(
                file_name=file_name, parameters=parameters, file_path=tmp_file_path
            )

            # Step 4 - Extract structure
            # LDD-log: structure extraction phase
            self.logger.info(f"[IMP:7][DedocManager][STRUCTURE_EXTRACT] Extract structure from file {file_name}")
            unstructured_document = self.structure_extractor.extract(unstructured_document, parameters)

            if self.config.get("labeling_mode", False):
                self.__save(converted_file_path, unstructured_document)

            # Step 5 - Form the output structure
            # LDD-log: output construction phase
            self.logger.info(f"[IMP:7][DedocManager][OUTPUT_CONSTRUCT] Get structured document {file_name}")
            parsed_document = self.structure_constructor.construct(document=unstructured_document, parameters=parameters)

            # Step 6 - Get attachments
            # LDD-log: attachments phase
            self.logger.info(f"[IMP:7][DedocManager][ATTACHMENTS] Get attachments {file_name}")
            attachments = self.attachments_handler.handle_attachments(document_parser=self, document=unstructured_document, parameters=parameters)
            parsed_document.add_attachments(attachments)

            # LDD-log: pipeline complete — business value
            self.logger.info(f"[IMP:9][DedocManager][PIPELINE_COMPLETE] Finish handle {file_name}")
        return parsed_document
    # endregion METHOD___parse_no_error_handling

    # region METHOD___init_parameters [DOMAIN(6): Parameters; CONCEPT(5): DefaultsMerging; TECH(4): DictOperations]
    ## @purpose To merge user-provided parameters with defaults and set the attachments directory based on file path, ensuring every pipeline step has a complete parameter set.
    ## @uses QueryParameters.to_dict
    ## @io (str, Optional[dict]) -> dict
    ## @complexity 3
    def __init_parameters(self, file_path: str, parameters: Optional[dict]) -> dict:
        import os.path

        parameters = {} if parameters is None else parameters
        result_parameters = {}

        for parameter_name, parameter_value in self.default_parameters.items():
            result_parameters[parameter_name] = parameters.get(parameter_name, parameter_value)

        attachments_dir = parameters.get("attachments_dir", None)
        result_parameters["attachments_dir"] = os.path.dirname(file_path) if attachments_dir is None else attachments_dir

        # LDD-log: parameters merged
        logger.debug(f"[IMP:4][DedocManager][INIT_PARAMS] Parameters initialized: attachments_dir={result_parameters['attachments_dir']}")
        return result_parameters
    # endregion METHOD___init_parameters

    # region METHOD___read_with_mime_auto_detection [DOMAIN(8): ContentReading; CONCEPT(8): MimeDetection, FallbackStrategy; TECH(7): FileTypeAutoDetection]
    ## @purpose To read a file first using its original extension, and if conversion fails, fall back to content-based MIME detection for a second attempt, ensuring robust file format handling.
    ## @uses __parse_file, get_file_mime_by_content, mime2extension, get_mime_extension
    ## @io (str, str, Optional[dict]) -> Tuple[str, UnstructuredDocument]
    ## @complexity 7
    def __read_with_mime_auto_detection(self, file_path: str, file_name: str, parameters: Optional[dict]) -> Tuple[str, UnstructuredDocument]:
        import os.path
        from dedoc.extensions import mime2extension
        from dedoc.utils.utils import get_file_mime_by_content, get_mime_extension

        # firstly, try to read file using its original extension
        mime, extension = get_mime_extension(file_path=file_path)
        # LDD-log: primary read attempt
        self.logger.info(f"[IMP:7][DedocManager][MIME_DETECT] Reading {file_name} with mime={mime}, extension={extension}")
        try:
            converted_file_path, document = self.__parse_file(file_path=file_path, file_name=file_name, parameters=parameters, mime=mime, extension=extension)
        except (ConversionError, BadFileFormatError) as e:
            # secondly, try to read file using mime obtained by file's content
            detected_mime = get_file_mime_by_content(file_path)
            detected_extension = mime2extension.get(detected_mime, "")
            # LDD-log: fallback read attempt
            self.logger.warning(f"[IMP:8][DedocManager][MIME_FALLBACK] Could not read file {file_name} with mime = \"{mime}\", extension = \"{extension}\" ({e}). "
                                f'Detected file mime = "{detected_mime}", extension = "{detected_extension}"')
            fixed_file_path = f"{file_path}{detected_extension}"
            os.rename(file_path, fixed_file_path)
            converted_file_path, document = self.__parse_file(
                file_path=fixed_file_path, file_name=file_name, parameters=parameters, mime=detected_mime, extension=detected_extension
            )
            document.warnings.append(f'Incorrect extension "{extension}". Detected mime = "{detected_mime}", extension = "{detected_extension}"')

        return converted_file_path, document
    # endregion METHOD___read_with_mime_auto_detection

    # region METHOD___parse_file [DOMAIN(8): DocumentParsing; CONCEPT(7): Composition; TECH(6): Delegation]
    ## @purpose To execute the convert-read-metadata sub-pipeline for a single file: convert the raw file, read its content into an UnstructuredDocument, and attach extracted metadata.
    ## @uses converter.convert, reader.read, document_metadata_extractor.extract
    ## @io (str, str, Optional[dict], str, str) -> Tuple[str, UnstructuredDocument]
    ## @complexity 5
    def __parse_file(self, file_path: str, file_name: str, parameters: Optional[dict], extension: str, mime: str) -> Tuple[str, UnstructuredDocument]:
        import os.path
        from dedoc.utils.utils import get_mime_extension

        # LDD-log: conversion step
        self.logger.debug(f"[IMP:5][DedocManager][CONVERT] Converting {file_name} (mime={mime}, ext={extension})")
        converted_file_path = self.converter.convert(file_path, parameters=parameters, mime=mime, extension=extension)
        if converted_file_path != file_path:
            mime, extension = get_mime_extension(file_path=converted_file_path)
            self.logger.debug(f"[IMP:5][DedocManager][CONVERT] Converted to {converted_file_path} (mime={mime})")

        # LDD-log: reading step
        self.logger.debug(f"[IMP:5][DedocManager][READ] Reading {os.path.basename(converted_file_path)}")
        unstructured_document = self.reader.read(file_path=converted_file_path, parameters=parameters, mime=mime, extension=extension)

        # LDD-log: metadata extraction step
        self.logger.debug(f"[IMP:5][DedocManager][METADATA] Extracting metadata for {file_name}")
        metadata = self.document_metadata_extractor.extract(file_path=file_path, converted_filename=os.path.basename(converted_file_path),
                                                             original_filename=file_name, parameters=parameters, mime=mime, extension=extension)

        unstructured_document.metadata = {**unstructured_document.metadata, **metadata}
        return converted_file_path, unstructured_document
    # endregion METHOD___parse_file

    # region METHOD___save [DOMAIN(5): Persistence; CONCEPT(6): LabelingMode; TECH(5): FileSystemOperations]
    ## @purpose To persist classified document lines and the original document to disk during labeling mode, enabling training dataset collection.
    ## @uses save_line_with_meta, get_path_original_documents
    ## @io (str, UnstructuredDocument) -> None
    ## @complexity 4
    def __save(self, file_path: str, classified_document: UnstructuredDocument) -> None:
        import os.path
        import shutil
        from dedoc.utils.train_dataset_utils import get_path_original_documents, save_line_with_meta

        # LDD-log: save for labeling
        self.logger.info(f"[IMP:8][DedocManager][SAVE_LABELING] Save document lines to {self.config['intermediate_data_path']}")
        save_line_with_meta(lines=classified_document.lines, config=self.config, original_document=os.path.basename(file_path))
        shutil.copy(file_path, os.path.join(get_path_original_documents(self.config), os.path.basename(file_path)))
    # endregion METHOD___save
# endregion CLASS_DedocManager

# region MODULE_CONTRACT [DOMAIN(9): DocumentProcessing; CONCEPT(9): Orchestrator, Pipeline; TECH(8): Composition, Delegation]
## @modulecontract
## @purpose To serve as the central orchestrator of the Dedoc document processing system, composing all specialized processors (converters, readers, extractors, constructors, attachment handlers) into a single, resilient `parse` pipeline with automatic MIME detection, error enrichment, and labeling mode support.
## @scope Document parsing orchestration, pipeline composition, error handling with metadata enrichment, MIME-based format auto-detection, labeling mode persistence.
## @input File paths, optional processing parameters, configuration dictionaries.
## @output ParsedDocument with content, structure, metadata, and attachments.
## @links [USES_API(9): dedoc.config, dedoc.manager_config; READS_DATA_FROM(8): filesystem; CALLS_COMPOSITION(9): ConverterComposition, ReaderComposition, StructureExtractorComposition, StructureConstructorComposition, MetadataExtractorComposition, AttachmentsHandler]
## @invariants
## - Every `parse()` call returns a ParsedDocument or raises a DedocError with enriched metadata.
## - Pipeline steps execute in fixed order: convert → read → metadata → structure extract → output construct → attachments.
## - MIME fallback is attempted exactly once on ConversionError/BadFileFormatError.
## @rationale
## Q: Why compose via dependency injection in __init__ rather than hardcoding all components?
## A: Dedoc supports 17+ document formats each with specific readers and converters. DI allows testing with mock components and selective replacement of pipeline stages without touching orchestration logic.
## @changes
## LAST_CHANGE: [v1.0.0 – Added SEMANTIC TEMPLATE markup and comprehensive LDD logging across all pipeline stages]
## @modulemap
## CLASS 10[Central document processing orchestrator] => DedocManager
## @usecases
## - [DedocManager.parse]: APIHandler => ParseDocument => ParsedDocumentWithMetadata
## - [DedocManager.__parse_no_error_handling]: Orchestrator => ExecutePipeline => StructuredOutput
## - [DedocManager.__read_with_mime_auto_detection]: ContentReader => DetectMimeAndRead => UnstructuredDocument
def _module_contract():
    pass
# endregion MODULE_CONTRACT
# GREP_SUMMARY: orchestrator, pipeline, document processing, parse, DedocManager, converter, reader, structure extractor, structure constructor, metadata extractor, attachments handler, MIME detection, error handling, labeling mode
# STRUCTURE: ▶ parse(file) → ⚡ __init_parameters → ⟦try⟧ __parse_no_error_handling → ┌copy to tmp┐ → ◇ __read_with_mime_auto_detection {try mime → fail? → detect content mime} → ⊕ structure_extractor.extract → ⊕ structure_constructor.construct → ⊕ attachments_handler → ⎋ ParsedDocument ⬗ DedocError ⟦catch⟧ enrich metadata → re-raise
