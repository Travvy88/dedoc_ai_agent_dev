import logging

from dedoc.config import Configuration

logger = logging.getLogger(__name__)


if __name__ == "__main__":
    logger.debug(f"[IMP:4][main][INIT] Starting Dedoc API")
    from dedoc.api.dedoc_api import get_api, run_api
    Configuration.get_instance().get_config()
    logger.info(f"[IMP:7][main][API_START] Configuration loaded, running API")
    run_api(get_api())

# region MODULE_CONTRACT [DOMAIN(8): DocumentProcessing; CONCEPT(7): EntryPoint; TECH(6): FastAPI]
## @modulecontract
## @purpose Application entry point that initializes the Dedoc API server with configuration and logging, serving as the bootstrap for the entire document processing system.
## @scope API server initialization, configuration bootstrapping.
## @input None (environment variables and config files).
## @output Running FastAPI server on configured port.
## @links [USES_API(9): dedoc.api.dedoc_api.get_api, run_api; READS_DATA_FROM(8): Configuration.get_config]
## @invariants
## - Configuration is always loaded before the API starts.
## @rationale
## Q: Why is the entry point so minimal?
## A: All heavy initialization (readers, converters, extractors) is deferred to manager_config and DedocManager, keeping the bootstrap fast and testable.
## @changes
## LAST_CHANGE: [v1.0.0 – Added SEMANTIC TEMPLATE markup and LDD logging]
## @modulemap
## FUNC 10[Application entry point] => main
## @usecases
## - [main]: Operator => StartDedocServer => DocumentProcessingAvailable
def _module_contract():
    pass
# endregion MODULE_CONTRACT
# GREP_SUMMARY: entry point, main, API initialization, Configuration, FastAPI, run_api, bootstrap, server startup
# STRUCTURE: ⚡ main → ┌Configuration.get_instance┐ → ⊕ get_config → ⚡ run_api → ∑ API server active
