import logging
from typing import Optional

logger = logging.getLogger(__name__)


# region FUNC__get_manager_config [DOMAIN(8): Configuration; CONCEPT(8): Composition, DependencyAssembly; TECH(7): FactoryPattern]
## @purpose To assemble the full dependency injection graph for DedocManager by instantiating all converters, readers, metadata extractors, structure extractors, structure constructors, and attachment handlers with their concrete implementations, wiring them together as compositions.
## @uses All concrete converters, readers, extractors, constructors, handlers
## @io dict -> dict
## @complexity 8
def _get_manager_config(config: dict) -> dict:
    """
    Imports are here in order not to do all of them when someone does `import dedoc`
    """
    # LDD-log: assembly start
    logger.info(f"[IMP:7][_get_manager_config][ASSEMBLY_START] Assembling manager configuration components")
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
    from dedoc.readers.article_reader.article_reader import ArticleReader
    from dedoc.readers.csv_reader.csv_reader import CSVReader
    from dedoc.readers.docx_reader.docx_reader import DocxReader
    from dedoc.readers.email_reader.email_reader import EmailReader
    from dedoc.readers.excel_reader.excel_reader import ExcelReader
    from dedoc.readers.html_reader.html_reader import HtmlReader
    from dedoc.readers.json_reader.json_reader import JsonReader
    from dedoc.readers.mhtml_reader.mhtml_reader import MhtmlReader
    from dedoc.readers.note_reader.note_reader import NoteReader
    from dedoc.readers.pdf_reader.pdf_auto_reader.pdf_auto_reader import PdfAutoReader
    from dedoc.readers.pdf_reader.pdf_image_reader.pdf_image_reader import PdfImageReader
    from dedoc.readers.pdf_reader.pdf_txtlayer_reader.pdf_tabby_reader import PdfTabbyReader
    from dedoc.readers.pdf_reader.pdf_txtlayer_reader.pdf_txtlayer_reader import PdfTxtlayerReader
    from dedoc.readers.pdf_reader.pdf_txtlayer_reader.pdf_broken_encoding_reader import PdfBrokenEncodingReader
    from dedoc.readers.pptx_reader.pptx_reader import PptxReader
    from dedoc.readers.reader_composition import ReaderComposition
    from dedoc.readers.txt_reader.raw_text_reader import RawTextReader
    from dedoc.structure_constructors.concrete_structure_constructors.linear_constructor import LinearConstructor
    from dedoc.structure_constructors.concrete_structure_constructors.tree_constructor import TreeConstructor
    from dedoc.structure_constructors.structure_constructor_composition import StructureConstructorComposition
    from dedoc.structure_extractors.concrete_structure_extractors.article_structure_extractor import ArticleStructureExtractor
    from dedoc.structure_extractors.concrete_structure_extractors.classifying_law_structure_extractor import ClassifyingLawStructureExtractor
    from dedoc.structure_extractors.concrete_structure_extractors.default_structure_extractor import DefaultStructureExtractor
    from dedoc.structure_extractors.concrete_structure_extractors.diploma_structure_extractor import DiplomaStructureExtractor
    from dedoc.structure_extractors.concrete_structure_extractors.fintoc_structure_extractor import FintocStructureExtractor
    from dedoc.structure_extractors.concrete_structure_extractors.foiv_law_structure_extractor import FoivLawStructureExtractor
    from dedoc.structure_extractors.concrete_structure_extractors.law_structure_excractor import LawStructureExtractor
    from dedoc.structure_extractors.concrete_structure_extractors.tz_structure_extractor import TzStructureExtractor
    from dedoc.structure_extractors.structure_extractor_composition import StructureExtractorComposition

    converters = [
        DocxConverter(config=config),
        ExcelConverter(config=config),
        PptxConverter(config=config),
        TxtConverter(config=config),
        PDFConverter(config=config),
        PNGConverter(config=config),
        BinaryConverter(config=config)
    ]
    readers = [
        ArticleReader(config=config),
        DocxReader(config=config),
        ExcelReader(config=config),
        PptxReader(config=config),
        RawTextReader(config=config),
        CSVReader(config=config),
        HtmlReader(config=config),
        NoteReader(config=config),
        JsonReader(config=config),
        ArchiveReader(config=config),
        PdfAutoReader(config=config),
        PdfTabbyReader(config=config),
        PdfTxtlayerReader(config=config),
        PdfBrokenEncodingReader(config=config),
        PdfImageReader(config=config),
        EmailReader(config=config),
        MhtmlReader(config=config)
    ]

    metadata_extractors = [
        DocxMetadataExtractor(config=config),
        PdfMetadataExtractor(config=config),
        ImageMetadataExtractor(config=config),
        NoteMetadataExtractor(config=config),
        BaseMetadataExtractor(config=config)
    ]

    law_extractors = {
        FoivLawStructureExtractor.document_type: FoivLawStructureExtractor(config=config),
        LawStructureExtractor.document_type: LawStructureExtractor(config=config)
    }
    structure_extractors = {
        DefaultStructureExtractor.document_type: DefaultStructureExtractor(config=config),
        DiplomaStructureExtractor.document_type: DiplomaStructureExtractor(config=config),
        TzStructureExtractor.document_type: TzStructureExtractor(config=config),
        ClassifyingLawStructureExtractor.document_type: ClassifyingLawStructureExtractor(extractors=law_extractors, config=config),
        ArticleStructureExtractor.document_type: ArticleStructureExtractor(config=config),
        FintocStructureExtractor.document_type: FintocStructureExtractor(config=config)
    }

    return dict(
        converter=ConverterComposition(converters=converters),
        reader=ReaderComposition(readers=readers),
        structure_extractor=StructureExtractorComposition(extractors=structure_extractors, default_key="other", config=config),
        structure_constructor=StructureConstructorComposition(
            constructors={"linear": LinearConstructor(), "tree": TreeConstructor()},
            default_constructor=TreeConstructor()
        ),
        document_metadata_extractor=MetadataExtractorComposition(extractors=metadata_extractors),
        attachments_handler=AttachmentsHandler(config=config)
    )
    # LDD-log: assembly complete
    logger.info(f"[IMP:8][_get_manager_config][ASSEMBLY_COMPLETE] Manager config assembled: "
                f"{len(converters)} converters, {len(readers)} readers, "
                f"{len(structure_extractors)} structure extractors, {len(metadata_extractors)} metadata extractors")
# endregion FUNC__get_manager_config


# region CLASS_ConfigurationManager [DOMAIN(8): Configuration; CONCEPT(7): Singleton, Caching; TECH(6): LazyInitialization]
## @purpose To provide a singleton caching layer for the manager configuration, ensuring the expensive assembly of all pipeline components happens at most once per process.
class ConfigurationManager(object):
    """
    Pattern Singleton for configuration service
    INFO: Configuration class and config are created once at the first call
    For initialization ConfigurationManager call ConfigurationManager.getInstance().initConfig(new_config: dict)
    If you need default config, call ConfigurationManager.getInstance()
    """
    __instance = None
    __config = None

    # region METHOD_get_instance [DOMAIN(7): Singleton; CONCEPT(8): LazyInstantiation; TECH(6): classmethod]
    ## @purpose To return the singleton ConfigurationManager instance, creating it on first access.
    ## @uses cls.__instance
    ## @io None -> ConfigurationManager
    ## @complexity 3
    @classmethod
    def get_instance(cls: "ConfigurationManager") -> "ConfigurationManager":
        """
        Actual object creation will happen when we use ConfigurationManager.getInstance()
        """
        logger.debug(f"[IMP:4][ConfigurationManager][GET_INSTANCE] Accessing singleton")
        if not cls.__instance:
            cls.__instance = ConfigurationManager()
            logger.info(f"[IMP:8][ConfigurationManager][GET_INSTANCE] Created new ConfigurationManager singleton")

        return cls.__instance
    # endregion METHOD_get_instance

    # region METHOD_init_config [DOMAIN(7): Configuration; CONCEPT(6): Caching; TECH(5): Setter]
    ## @purpose To initialize or override the cached manager configuration, accepting either a pre-built config or delegating to _get_manager_config for assembly.
    ## @uses _get_manager_config
    ## @io (dict, Optional[dict]) -> None
    ## @complexity 3
    def init_config(self, config: dict, new_config: Optional[dict] = None) -> None:
        if new_config is None:
            logger.info(f"[IMP:7][ConfigurationManager][INIT_CONFIG] Building manager config from _get_manager_config")
            self.__config = _get_manager_config(config)
        else:
            logger.info(f"[IMP:7][ConfigurationManager][INIT_CONFIG] Using provided manager config")
            self.__config = new_config
    # endregion METHOD_init_config

    # region METHOD_get_config [DOMAIN(7): Configuration; CONCEPT(6): LazyInit; TECH(5): Delegation]
    ## @purpose To return the cached manager configuration, triggering lazy assembly via init_config if not yet initialized.
    ## @uses init_config
    ## @io dict -> dict
    ## @complexity 3
    def get_config(self, config: dict) -> dict:
        if self.__config is None:
            logger.debug(f"[IMP:4][ConfigurationManager][GET_CONFIG] Cache miss, initializing")
            self.init_config(config)
        return self.__config
    # endregion METHOD_get_config
# endregion CLASS_ConfigurationManager


# region FUNC_get_manager_config [DOMAIN(7): Configuration; CONCEPT(6): Facade; TECH(5): Delegation]
## @purpose Convenience function that delegates to the ConfigurationManager singleton to retrieve the assembled manager configuration, providing a clean import-time interface.
## @uses ConfigurationManager.get_instance().get_config
## @io dict -> dict
## @complexity 2
def get_manager_config(config: dict) -> dict:
    logger.debug(f"[IMP:4][get_manager_config][FACADE] Delegating to ConfigurationManager")
    return ConfigurationManager().get_instance().get_config(config)
# endregion FUNC_get_manager_config

# region MODULE_CONTRACT [DOMAIN(8): Configuration; CONCEPT(8): DependencyAssembly, Factory; TECH(7): Composition, Singleton]
## @modulecontract
## @purpose To assemble and cache the complete dependency injection graph for DedocManager — instantiating all 7 converters, 17 readers, 5 metadata extractors, 6 structure extractors, 2 structure constructors, and 1 attachments handler — wiring them together as composable pipeline stages.
## @scope Dependency assembly for document processing pipeline, singleton caching, component instantiation.
## @input Application configuration dictionary.
## @output Manager configuration dictionary with all pipeline components ready for injection into DedocManager.
## @links [USES_API(9): All concrete converters, readers, extractors, constructors, handlers]
## @invariants
## - Manager config is assembled at most once per process lifetime (singleton + caching).
## - All mandatory components (reader, structure_extractor, structure_constructor, metadata_extractor, attachments_handler) are never None.
## @rationale
## Q: Why lazy imports inside _get_manager_config and not at module level?
## A: Dedoc supports 17+ document formats; importing all readers/converters eagerly on `import dedoc` would be prohibitively slow. Lazy imports defer cost to first use.
## @changes
## LAST_CHANGE: [v1.0.0 – Added SEMANTIC TEMPLATE markup and LDD logging]
## @modulemap
## FUNC 10[Assembles complete component graph] => _get_manager_config
## CLASS 9[Singleton cache for manager config] => ConfigurationManager
## FUNC 8[Facade to get manager config] => get_manager_config
## @usecases
## - [_get_manager_config]: Orchestrator => AssemblePipelineComponents => CompleteManagerConfig
## - [ConfigurationManager]: Startup => CacheExpensiveInit => ReuseAcrossCalls
def _module_contract():
    pass
# endregion MODULE_CONTRACT
# GREP_SUMMARY: manager config, dependency assembly, factory, singleton, converters, readers, structure extractors, metadata extractors, pipeline components, ConfigurationManager, get_manager_config
# STRUCTURE: ▶ get_manager_config → ◇ ConfigurationManager singleton → init_config? → ⚡ _get_manager_config → ⊕ converters[] + readers[] + metadata_extractors[] + structure_extractors[] + constructors[] + attachments_handler → ∑ dict → ⎷ cached
