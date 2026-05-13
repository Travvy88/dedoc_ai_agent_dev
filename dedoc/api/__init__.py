# region MODULE_CONTRACT [DOMAIN(7): DocumentProcessing, APILayer; CONCEPT(6): PackageInit, PublicAPI; TECH(5): PythonPackage]
## @modulecontract
## @purpose Declare `dedoc.api` as a Python package, serving as the API layer namespace for FastAPI endpoints, request handling, and schema models.
## @scope API layer package root — contains endpoint definitions, process handlers, and schema sub-package.
## @input None (empty init).
## @output Package namespace `dedoc.api`.
## @links
## @invariants
## - Package is importable as `dedoc.api`.
## @rationale
## Q: Why an empty __init__?
## A: Minimal package marker — public API is re-exported from `dedoc.api.schema`, endpoints are imported explicitly by the application launcher.
## @changes
## LAST_CHANGE: [v1.0.0 – Initial creation with semantic markup]
## @modulemap
## PKG [API layer namespace] => dedoc.api
## @usecases
## - [dedoc.api]: ApplicationLauncher => ImportAPIModules => MountFastAPIApp
def _module_contract():
    pass
# endregion MODULE_CONTRACT
# GREP_SUMMARY: API, package, init, FastAPI, namespace, endpoints, schema
# STRUCTURE: ▶ Empty init — package marker only → ⎋ namespace dedoc.api
