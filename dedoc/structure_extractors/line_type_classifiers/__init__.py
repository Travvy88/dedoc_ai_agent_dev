# region MODULE_CONTRACT [DOMAIN(8): DocumentStructure; CONCEPT(9): LineClassification, DocumentParsing; TECH(7): PythonPackage]
## @modulecontract
## @purpose Provide the package entry point for line type classifiers — modules that classify each document line as a header, list item, table of contents entry, raw text, or other structural type.
## @scope Package initialization for line_type_classifiers subpackage.
## @input None (package-level).
## @output Public symbols re-exported from classifier modules.
## @links [USES_API(8): dedoc.structure_extractors.feature_extractors]
## @invariants
## - Every document line receives exactly one line type label.
## @rationale
## Q: Why a separate line type classifiers package?
## A: Line type classification is the first stage of the structure extraction pipeline; isolating it enables swapping classification strategies (rule-based vs ML).
## @changes
## LAST_CHANGE: [v1.0.0 – Added semantic template markup]
## @modulemap
## @usecases
## - [Line classification]: DocumentLine → LineTypeClassifier → LineTypeLabel → HierarchyBuilder
def _module_contract():
    pass
# endregion MODULE_CONTRACT
# GREP_SUMMARY: line_type_classifiers, init, structure_extractors, line classification, header, list item, TOC, raw text
# STRUCTURE: ▶ line_type_classifiers/__init__ → ⊕ import classifier modules → ⎋ __all__
