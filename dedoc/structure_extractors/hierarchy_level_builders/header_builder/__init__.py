# region MODULE_CONTRACT [DOMAIN(8): DocumentStructure; CONCEPT(9): HeaderDetection, HierarchyBuilding; TECH(7): PythonPackage]
## @modulecontract
## @purpose Provide the package entry point for header-based hierarchy level builder — assigns hierarchy levels to lines identified as section headers.
## @scope Package initialization for header_builder subpackage.
## @input None (package-level).
## @output Public symbols re-exported from header builder modules.
## @links [USES_API(8): dedoc.structure_extractors.hierarchy_level_builders]
## @invariants
## - Header levels are assigned based on typographic and positional features (font size, bold, indentation).
## @rationale
## Q: Why a separate header builder?
## A: Header detection relies on visual/metadata features distinct from content-based hierarchy (law, diploma, TOC).
## @changes
## LAST_CHANGE: [v1.0.0 – Added semantic template markup]
## @modulemap
## @usecases
## - [Header hierarchy]: DocumentLines → HeaderBuilder → HeaderLevels → StructuredDocument
def _module_contract():
    pass
# endregion MODULE_CONTRACT
# GREP_SUMMARY: header_builder, init, structure_extractors, header detection, font size, bold, typographic hierarchy
# STRUCTURE: ▶ header_builder/__init__ → ⊕ import header builder modules → ⎋ __all__
