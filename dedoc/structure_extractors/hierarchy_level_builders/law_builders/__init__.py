# region MODULE_CONTRACT [DOMAIN(8): LegalDocuments; CONCEPT(9): LawStructure, HierarchyBuilding; TECH(7): PythonPackage]
## @modulecontract
## @purpose Provide the package entry point for law-specific hierarchy builders — modules that construct hierarchical structure for legal documents (body, application, structure units).
## @scope Package initialization for law_builders subpackage.
## @input None (package-level).
## @output Public symbols re-exported from law builder modules.
## @links [USES_API(8): dedoc.structure_extractors.hierarchy_level_builders]
## @invariants
## - Law builders handle legal document structural conventions (articles, chapters, parts, appendices).
## @rationale
## Q: Why a dedicated law_builders package?
## A: Legal documents have the most complex and varied hierarchical structures among supported document types.
## @changes
## LAST_CHANGE: [v1.0.0 – Added semantic template markup]
## @modulemap
## @usecases
## - [Law hierarchy]: LawLines → LawBuilders → HierarchyLevels → StructuredLawDocument
def _module_contract():
    pass
# endregion MODULE_CONTRACT
# GREP_SUMMARY: law_builders, init, structure_extractors, law, legal document, hierarchy, article, chapter, appendix
# STRUCTURE: ▶ law_builders/__init__ → ⊕ import law builder modules → ⎋ __all__
