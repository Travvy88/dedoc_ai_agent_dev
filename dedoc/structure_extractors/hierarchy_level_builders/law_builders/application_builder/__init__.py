# region MODULE_CONTRACT [DOMAIN(8): LegalDocuments; CONCEPT(9): ApplicationStructure, LawHierarchy; TECH(7): PythonPackage]
## @modulecontract
## @purpose Provide the package entry point for the law application section hierarchy builder — assigns levels to lines in the application/appendix portion of legal documents.
## @scope Package initialization for application_builder subpackage.
## @input None (package-level).
## @output Public symbols re-exported from application builder modules.
## @links [USES_API(8): dedoc.structure_extractors.hierarchy_level_builders.law_builders]
## @invariants
## - Application hierarchy follows legal document appendix conventions.
## @rationale
## Q: Why a separate application builder?
## A: The application section of laws has a distinct structure (appendices, attachments) requiring dedicated hierarchy logic.
## @changes
## LAST_CHANGE: [v1.0.0 – Added semantic template markup]
## @modulemap
## @usecases
## - [Application hierarchy]: LawLines → ApplicationBuilder → ApplicationLevels → StructuredLaw
def _module_contract():
    pass
# endregion MODULE_CONTRACT
# GREP_SUMMARY: application_builder, init, structure_extractors, law, appendix, application, legal document
# STRUCTURE: ▶ application_builder/__init__ → ⊕ import application builder modules → ⎋ __all__
