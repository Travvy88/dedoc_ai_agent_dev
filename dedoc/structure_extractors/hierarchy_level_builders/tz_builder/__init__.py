# region MODULE_CONTRACT [DOMAIN(8): TechnicalDocuments; CONCEPT(9): TZStructure, HierarchyBuilding; TECH(7): PythonPackage]
## @modulecontract
## @purpose Provide the package entry point for technical specification (ТЗ) hierarchy builder — assigns levels to lines in technical specification documents.
## @scope Package initialization for tz_builder subpackage.
## @input None (package-level).
## @output Public symbols re-exported from TZ builder modules.
## @links [USES_API(8): dedoc.structure_extractors.hierarchy_level_builders]
## @invariants
## - TZ hierarchy follows ГОСТ technical specification document conventions.
## @rationale
## Q: Why a dedicated TZ builder?
## A: Technical specifications have a distinctive structure (sections like «Общие положения», «Требования», etc.) warranting a specialized builder.
## @changes
## LAST_CHANGE: [v1.0.0 – Added semantic template markup]
## @modulemap
## @usecases
## - [TZ hierarchy]: TZLines → TzBuilder → TzLevels → StructuredTZ
def _module_contract():
    pass
# endregion MODULE_CONTRACT
# GREP_SUMMARY: tz_builder, init, structure_extractors, technical specification, ТЗ, ГОСТ, hierarchy
# STRUCTURE: ▶ tz_builder/__init__ → ⊕ import TZ builder modules → ⎋ __all__
