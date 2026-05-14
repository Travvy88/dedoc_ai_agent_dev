import logging
import os
import sys

logger = logging.getLogger(__name__)

# region CLASS_Configuration [DOMAIN(8): Configuration; CONCEPT(7): Singleton; TECH(6): LazyInitialization]
## @purpose To provide a lazily-initialized, singleton configuration service that assembles all application settings from environment variables and defaults into a single dictionary, ensuring consistent access across the entire document processing pipeline.
class Configuration(object):
    """
    Pattern Singleton for configuration service
    INFO: Configuration class and config are created once at the first call
    """
    __instance = None
    __config = None

    # region METHOD_get_instance [DOMAIN(7): Singleton; CONCEPT(8): LazyInstantiation; TECH(6): classmethod]
    ## @purpose To return the singleton Configuration instance, creating it on first access.
    ## @uses cls.__instance
    ## @io None -> Configuration
    ## @complexity 3
    @classmethod
    def get_instance(cls: "Configuration") -> "Configuration":
        """
        Actual object creation will happen when we use Configuration.getInstance()
        """
        # LDD-log: singleton access
        logger.debug(f"[IMP:4][Configuration][GET_INSTANCE] Accessing singleton")
        if not cls.__instance:
            cls.__instance = Configuration()
            logger.info(f"[IMP:8][Configuration][GET_INSTANCE] Created new Configuration singleton")

        return cls.__instance
    # endregion METHOD_get_instance

    # region METHOD_get_config [DOMAIN(8): Configuration; CONCEPT(7): DictAssembly; TECH(6): EnvironmentVariables]
    ## @purpose To assemble and cache the full application configuration dictionary from environment variables, OS paths, and hardcoded defaults, enabling downstream components to access settings without repeated parsing.
    ## @uses os, sys, logging
    ## @io None -> dict
    ## @complexity 7
    def get_config(self) -> dict:
        if self.__config is None:
            # LDD-log: lazy config initialization start
            logger.info(f"[IMP:7][Configuration][GET_CONFIG] Building configuration dictionary from environment")

            logging.basicConfig(stream=sys.stdout, level=logging.INFO, format="%(asctime)s - %(pathname)s - %(levelname)s - %(message)s")

            resources_path = os.environ.get("RESOURCES_PATH", os.path.join(os.path.expanduser("~"), ".cache", "dedoc", "resources"))
            self.__config = dict(
                # -----------------------------------------RESOURCES PATH SETTINGS----------------------------------------------------
                resources_path=resources_path,
                intermediate_data_path=os.path.join(resources_path, "datasets"),
                table_path="/tmp/tables",

                # -----------------------------------------COMMON DEBUG SETTINGS----------------------------------------------------
                debug_mode=False,
                path_debug=os.path.join(os.path.abspath(os.sep), "tmp", "dedoc"),

                # --------------------------------------------JOBLIB SETTINGS-------------------------------------------------------
                # number of parallel jobs in some tasks as OCR
                n_jobs=1,

                # --------------------------------------------GPU SETTINGS----------------------------------------------------------
                # set gpu in XGBoost and torch models
                on_gpu=False,

                # ---------------------------------------------API SETTINGS---------------------------------------------------------
                # max file size in bytes
                max_content_length=512 * 1024 * 1024,
                # application port
                api_port=int(os.environ.get("DOCREADER_PORT", "1231")),
                static_files_dirs={},
                # log settings
                logger=logging.getLogger(),
                import_path_init_api_args="dedoc.api.api_args",

                # ----------------------------------------TABLE RECOGNIZER DEBUG SETTINGS-------------------------------------------
                # path to save debug images for tables recognizer
                path_detect=os.path.join(os.path.abspath(os.sep), "tmp", "dedoc", "debug_tables", "imgs", "detect_lines"),

                # -------------------------------------------RECOGNIZE SETTINGS-----------------------------------------------------
                # TESSERACT OCR confidence threshold ( values: [-1 - undefined;  0.0 : 100.0 % - confidence value)
                ocr_conf_threshold=40.0,
                # OCR engine name: "tesseract" (default), future: "easyocr", "paddleocr", etc.
                ocr_engine="tesseract",
                # max depth of document structure tree
                recursion_deep_subparagraphs=30,

                # -------------------------------------------EXTERNAL SERVICES SETTINGS---------------------------------------------
                grobid_max_connection_attempts=3
            )
            # LDD-log: config built
            logger.info(f"[IMP:8][Configuration][GET_CONFIG] Configuration built: resources_path={resources_path}")
        return self.__config
    # endregion METHOD_get_config
# endregion CLASS_Configuration

# region FUNC_get_config [DOMAIN(8): Configuration; CONCEPT(6): Facade; TECH(5): Delegation]
## @purpose Convenience function that delegates to the Configuration singleton to retrieve the application configuration dictionary, providing a terse import-time interface for downstream modules.
## @uses Configuration.get_instance().get_config
## @io None -> dict
## @complexity 2
def get_config() -> dict:
    # LDD-log: facade call
    logger.debug(f"[IMP:4][get_config][FACADE] Delegating to Configuration.get_instance().get_config()")
    return Configuration.get_instance().get_config()
# endregion FUNC_get_config

# region MODULE_CONTRACT [DOMAIN(8): Configuration; CONCEPT(7): Singleton, ApplicationSettings; TECH(6): EnvironmentVariables, LazyInit]
## @modulecontract
## @purpose To provide a centralized, lazily-initialized, singleton-based configuration service that assembles all application-level settings (paths, API ports, OCR thresholds, GPU flags, debug modes) for the Dedoc document processing system.
## @scope Application configuration assembly, environment variable reading, default value provision, logging setup.
## @input Environment variables (RESOURCES_PATH, DOCREADER_PORT) and OS filesystem paths.
## @output A singleton Configuration instance providing a unified configuration dictionary.
## @links [USES_API(8): os.environ, logging; READS_DATA_FROM(7): filesystem paths]
## @invariants
## - `get_config()` always returns the same dictionary reference (single-init via __config caching).
## - Configuration singleton is created exactly once per process lifetime.
## @rationale
## Q: Why Singleton + lazy initialization for configuration?
## A: Dedoc has many components (readers, converters, extractors) that all need config. Singleton ensures consistency; lazy init avoids expensive config assembly on import.
## @changes
## LAST_CHANGE: [v1.0.0 – Added SEMANTIC TEMPLATE markup and LDD logging]
## @modulemap
## CLASS 10[Singleton configuration holder] => Configuration
## FUNC 8[Shortcut to get config dict] => get_config
## @usecases
## - [Configuration.get_config]: DocumentProcessor => GetApplicationSettings => AllSettingsAvailable
## - [get_config]: ExternalModule => QuickConfigRetrieval => ConfigDictReturned
def _module_contract():
    pass
# endregion MODULE_CONTRACT
# GREP_SUMMARY: configuration, singleton, get_config, resources_path, API settings, OCR threshold, GPU, environment variables, lazy initialization, application settings, config dict
# STRUCTURE: ▶ ┌get_config()┐ → ◇ __config is None? → ⚡ os.environ + defaults → ⊕ __config dict → ⎋ cached → ∑ singleton return
