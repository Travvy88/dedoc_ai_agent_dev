# region MODULE_CONTRACT [DOMAIN(8): LegalDocuments; CONCEPT(9): BodyStructure, LawHierarchy; TECH(7): PythonPackage]
## @modulecontract
## @purpose Provide the package entry point for the law body section hierarchy builder — assigns levels to lines in the main body portion of legal documents.
## @scope Package initialization for body_builder subpackage.
## @input None (package-level).
## @output Public symbols re-exported from body builder modules.
## @links [USES_API(8): dedoc.structure_extractors.hierarchy_level_builders.law_builders]
## @invariants
## - Body hierarchy follows legal document article/chapter/section conventions.
## @rationale
## Q: Why a separate body builder?
## A: The main body of laws has distinct structural patterns (articles, chapters, parts) different from appendices and other document types.
## @changes
## LAST_CHANGE: [v1.0.0 – Added semantic template markup]
## @modulemap
## @usecases
## - [Body hierarchy]: LawLines → BodyBuilder → BodyLevels → StructuredLaw
def _module_contract():
    pass
# endregion MODULE_CONTRACT
# GREP_SUMMARY: body_builder, init, structure_extractors, law, body, article, chapter, legal document
# STRUCTURE: ▶ body_builder/__init__ → ⊕ import body builder modules → ⎋ __all__
