# region MODULE_CONTRACT [DOMAIN(8): DocumentProcessing; CONCEPT(5): PackageInit; TECH(3): PythonPackage]
## @modulecontract
## @purpose Register the concrete_attachments_extractors subpackage: docx, xlsx, pptx, pdf, json attachment extractor implementations.
## @scope Package initialization, no runtime logic.
## @input None
## @output None (namespace registration only)
## @links [USES_API(8): AbstractOfficeAttachmentsExtractor, AbstractAttachmentsExtractor]
## @invariants
## - This file is intentionally empty; all imports happen via the parent package __init__.
## @rationale
## Q: Why is this file empty?
## A: Re-exports are centralized in the parent `dedoc/attachments_extractors/__init__.py` to provide a single import surface.
## @changes
## LAST_CHANGE: [v1.0.0 – Semantic markup added]
## @modulemap
## PKG 10[Concrete attachment extractors subpackage] => concrete_attachments_extractors
## @usecases
## - [concrete_attachments_extractors]: CodeAgent (Navigation) => LocateExtractorImplementations => InstantiateCorrectExtractor
def _module_contract():
    pass
# endregion MODULE_CONTRACT
# GREP_SUMMARY: attachments, extractors, concrete, docx, xlsx, pptx, pdf, json, office, package_init
# STRUCTURE: ▶ Init ┌empty package┐ → ○ namespace registration → ⎋ (imports delegated to parent)
