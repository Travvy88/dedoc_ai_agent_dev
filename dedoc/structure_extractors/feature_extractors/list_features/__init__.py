# region MODULE_CONTRACT [DOMAIN(8): DocumentStructure; CONCEPT(9): ListDetection, FeatureExtraction; TECH(7): PythonPackage]
## @modulecontract
## @purpose Provide the package entry point for list-related feature extractors — modules that detect and characterize list structures within document lines.
## @scope Package initialization for list_features subpackage.
## @input None (package-level).
## @output Public symbols re-exported from list feature modules.
## @links [USES_API(8): dedoc.structure_extractors.feature_extractors]
## @invariants
## - List features are computed per-line and indicate membership in ordered/unordered lists.
## @rationale
## Q: Why isolate list features?
## A: List detection has domain-specific heuristics (prefixes, indentation, numbering) that benefit from a dedicated module cluster.
## @changes
## LAST_CHANGE: [v1.0.0 – Added semantic template markup]
## @modulemap
## @usecases
## - [List detection]: DocumentLine → ListFeatureExtractor → ListMembershipScore → HierarchyBuilder
def _module_contract():
    pass
# endregion MODULE_CONTRACT
# GREP_SUMMARY: list_features, init, structure_extractors, list detection, ordered list, unordered list, list membership
# STRUCTURE: ▶ list_features/__init__ → ⊕ import list feature modules → ⎋ __all__
