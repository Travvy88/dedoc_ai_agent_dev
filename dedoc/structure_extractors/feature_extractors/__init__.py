# region MODULE_CONTRACT [DOMAIN(8): DocumentStructure; CONCEPT(9): FeatureExtraction, LineClassification; TECH(7): PythonPackage]
## @modulecontract
## @purpose Provide the package entry point for line feature extractors — modules that compute discriminative features from document lines for downstream classification.
## @scope Package initialization for feature_extractors subpackage.
## @input None (package-level).
## @output Public symbols re-exported from feature extractor modules.
## @links [USES_API(8): dedoc.data_structures]
## @invariants
## - All feature extractors produce a consistent feature vector per line.
## @rationale
## Q: Why separate features into their own package?
## A: Feature computation is a distinct concern from classification; modular features enable composition and reuse across classifiers.
## @changes
## LAST_CHANGE: [v1.0.0 – Added semantic template markup]
## @modulemap
## @usecases
## - [Feature extraction]: DocumentLine → FeatureExtractor → FeatureVector → Classifier
def _module_contract():
    pass
# endregion MODULE_CONTRACT
# GREP_SUMMARY: feature_extractors, init, structure_extractors, line features, feature vector, classification
# STRUCTURE: ▶ feature_extractors/__init__ → ⊕ import feature modules → ⎋ __all__
