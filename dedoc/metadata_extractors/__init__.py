# region MODULE_CONTRACT [DOMAIN(7): DocumentProcessing, MetadataExtraction; CONCEPT(6): PackageInit, PublicAPI; TECH(5): PythonInits]
## @modulecontract
## @purpose To expose the public API of the metadata_extractors package — all extractor classes and the composition facade.
## @scope Package initialization, re-export of concrete extractors.
## @input None (package-level imports).
## @output Public symbols: AbstractMetadataExtractor, BaseMetadataExtractor, DocxMetadataExtractor, ImageMetadataExtractor, NoteMetadataExtractor, PdfMetadataExtractor, MetadataExtractorComposition.
## @links [USES_API(7): AbstractMetadataExtractor, MetadataExtractorComposition]
## @invariants
## - __all__ always lists exactly 7 extractor symbols.
## @rationale
## Q: Why use __all__ with explicit re-exports?
## A: Provides a stable public API surface — consumers import from dedoc.metadata_extractors without knowing internal module paths.
## @changes
## LAST_CHANGE: [v1.0.0 — Semantic template markup added.]
## @modulemap
## VAR 5[Public API surface] => __all__
## @usecases
## - [Package]: ExternalConsumer → ImportExtractors → GetAvailableExtractors
def _module_contract():
    pass
# endregion MODULE_CONTRACT
# GREP_SUMMARY: metadata_extractors, package, public API, extractors, re-export, __all__
# STRUCTURE: ▶ ┌imports from submodules┐ → ⊕ __all__ ⟅7 extractor classes⟆ → ⎋ expose public API

from .abstract_metadata_extractor import AbstractMetadataExtractor
from .concrete_metadata_extractors.base_metadata_extractor import BaseMetadataExtractor
from .concrete_metadata_extractors.docx_metadata_extractor import DocxMetadataExtractor
from .concrete_metadata_extractors.image_metadata_extractor import ImageMetadataExtractor
from .concrete_metadata_extractors.note_metadata_extarctor import NoteMetadataExtractor
from .concrete_metadata_extractors.pdf_metadata_extractor import PdfMetadataExtractor
from .metadata_extractor_composition import MetadataExtractorComposition

__all__ = ['AbstractMetadataExtractor', 'BaseMetadataExtractor', 'DocxMetadataExtractor', 'ImageMetadataExtractor', 'NoteMetadataExtractor',
           'PdfMetadataExtractor', 'MetadataExtractorComposition']
