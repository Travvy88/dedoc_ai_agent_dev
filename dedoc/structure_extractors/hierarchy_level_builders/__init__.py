# region MODULE_CONTRACT [DOMAIN(8): DocumentStructure; CONCEPT(9): HierarchyConstruction, LevelAssignment; TECH(7): PythonPackage]
## @modulecontract
## @purpose Provide the package entry point for hierarchy level builders — modules that assign hierarchical nesting levels to document lines based on document type.
## @scope Package initialization for hierarchy_level_builders subpackage.
## @input None (package-level).
## @output Public symbols re-exported from hierarchy builder modules.
## @links [USES_API(8): dedoc.structure_extractors]
## @invariants
## - All builders produce a consistent level assignment per line.
## - Builders are document-type-specific (law, diploma, TOC, TZ, headers).
## @rationale
## Q: Why a hierarchy builders subpackage?
## A: Hierarchy construction is the core structural inference step — isolating builders by document type keeps each strategy focused and testable.
## @changes
## LAST_CHANGE: [v1.0.0 – Added semantic template markup]
## @modulemap
## @usecases
## - [Hierarchy building]: ClassifiedLines → HierarchyBuilder → LeveledLines → StructureConstructor
def _module_contract():
    pass
# endregion MODULE_CONTRACT
# GREP_SUMMARY: hierarchy_level_builders, init, structure_extractors, hierarchy, level assignment, nesting
# STRUCTURE: ▶ hierarchy_level_builders/__init__ → ⊕ import builder modules → ⎋ __all__
