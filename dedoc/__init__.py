# region MODULE_CONTRACT [DOMAIN(8): DocumentProcessing; CONCEPT(9): PackageEntry, PublicAPI; TECH(7): PythonPackage]
## @modulecontract
## @purpose Provide the public API entry point for the Dedoc document structure extraction library. Re-exports the core DedocManager class and package version.
## @scope Package initialization, public symbol re-export.
## @input None (package-level).
## @output Public symbols: DedocManager, __version__.
## @links [USES_API(8): dedoc_manager.DedocManager]
## @invariants
## - DedocManager and __version__ are always importable from dedoc package.
## @rationale
## Q: Why re-export DedocManager at package level?
## A: Provides a clean, single-import interface for users: `from dedoc import DedocManager`.
## @changes
## LAST_CHANGE: [v1.0.0 – Added SEMANTIC TEMPLATE markup]
## @modulemap
## CLASS 10[Document processing orchestrator] => DedocManager
## VAR 5[Package version string] => __version__
## @usecases
## - [DedocManager]: User -> import DedocManager -> parse documents
def _module_contract():
    pass
# endregion MODULE_CONTRACT
# GREP_SUMMARY: Dedoc, package entry, public API, DedocManager, __version__, import, re-export
# STRUCTURE: ▶ Import DedocManager + __version__ → ⊕ Re-export as package-level symbols → ⎋ ready for `from dedoc import DedocManager`

from .dedoc_manager import DedocManager
from .version import __version__
