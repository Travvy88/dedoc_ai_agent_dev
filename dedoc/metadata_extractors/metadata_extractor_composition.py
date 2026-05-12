# region MODULE_CONTRACT [DOMAIN(8): DocumentProcessing, MetadataExtraction; CONCEPT(8): CompositePattern, StrategyChain; TECH(6): PythonComposition]
## @modulecontract
## @purpose To implement a composite/chain-of-responsibility facade that delegates metadata extraction to the first suitable extractor in an ordered list.
## @scope Extractor composition, delegation, first-match dispatching.
## @input List[AbstractMetadataExtractor] via constructor.
## @output dict with metadata from the first capable extractor.
## @links [USES_API(8): AbstractMetadataExtractor.can_extract, AbstractMetadataExtractor.extract]
## @invariants
## - extract() either returns a dict or raises Exception — never returns None.
## - The order of extractors determines priority (first match wins).
## @rationale
## Q: Why use composition instead of inheritance?
## A: Metadata extraction needs to support multiple formats dynamically. Composite pattern allows the system to try extractors in priority order without knowing which format is being processed upfront.
## @changes
## LAST_CHANGE: [v1.0.0 — Semantic template markup and LDD logging added.]
## @modulemap
## CLASS 9[Composite dispatcher for metadata extractors] => MetadataExtractorComposition
## @usecases
## - [MetadataExtractorComposition]: DedocManager → ExtractMetadata → TryExtractorsInOrder → ReturnMetadata
def _module_contract():
    pass
# endregion MODULE_CONTRACT
# GREP_SUMMARY: composition, composite, metadata, extractor, chain, dispatcher, delegation, first-match
# STRUCTURE: ▶ CLASS MetadataExtractorComposition: ■ __init__ ┌list of extractors┐ → ◇ extract: ○ Loop ∋extractor▪▪can_extract? → ⊕ extract → ∑ result → ⚡ Exception if no match

import logging
from typing import List, Optional

from dedoc.metadata_extractors.abstract_metadata_extractor import AbstractMetadataExtractor

logger = logging.getLogger(__name__)


# region CLASS_MetadataExtractorComposition [DOMAIN(8): DocumentProcessing, MetadataExtraction; CONCEPT(8): CompositePattern, StrategyChain; TECH(6): PythonComposition]
## @purpose To serve as the primary entry point for metadata extraction — iterates an ordered list of extractors and returns the result of the first capable one.
class MetadataExtractorComposition:
    # region METHOD_init [DOMAIN(6): Configuration; CONCEPT(5): Constructor; TECH(4): PythonDefaults]
    ## @purpose To inject the ordered list of metadata extractors that form the extraction chain.
    ## @uses None
    ## @io List[AbstractMetadataExtractor] -> None
    ## @complexity 2
    def __init__(self, extractors: List[AbstractMetadataExtractor]) -> None:
        self.extractors = extractors
        logger.debug(f"[IMP:4][MetadataExtractorComposition][INIT] Extractors count={len(self.extractors)}")
    # endregion METHOD_init

    # region METHOD_extract [DOMAIN(8): MetadataExtraction; CONCEPT(8): ChainOfResponsibility; TECH(6): PythonIteration]
    ## @purpose To attempt extraction with each registered extractor in order, returning the result of the first one that reports capability via can_extract().
    ## @uses os.path, AbstractMetadataExtractor.can_extract, AbstractMetadataExtractor.extract
    ## @io str × Optional[str] × Optional[str] × Optional[dict] × Optional[str] × Optional[str] -> dict
    ## @complexity 6
    def extract(self,
                file_path: str,
                converted_filename: Optional[str] = None,
                original_filename: Optional[str] = None,
                parameters: Optional[dict] = None,
                extension: Optional[str] = None,
                mime: Optional[str] = None) -> dict:
        """
        Extract metadata using one of the extractors if suitable extractor was found.

        :param file_path: path to the file to extract metadata. \
        If dedoc manager is used, the file gets a new name during processing - this name should be passed here (for example 23141.doc)
        :param converted_filename: name of the file after renaming and conversion (if dedoc manager is used, for example 23141.docx), \
        by default it's a name from the file_path. Converted file should be located in the same directory as the file before converting.
        :param original_filename: name of the file before renaming (if dedoc manager is used), by default it's a name from the file_path
        :param parameters: additional parameters for document parsing, see :ref:`parameters_description` for more details
        :param extension: file extension, for example .doc or .pdf
        :param mime: MIME type of file
        :return: dict with metadata information about the document
        """
        import os.path

        for extractor in self.extractors:
            logger.debug(f"[IMP:5][MetadataExtractorComposition][TRY_EXTRACTOR] Trying {extractor.__class__.__name__} for file={os.path.basename(file_path)}")
            if extractor.can_extract(
                file_path=file_path,
                converted_filename=converted_filename,
                original_filename=original_filename,
                parameters=parameters,
                extension=extension,
                mime=mime
            ):
                logger.info(f"[IMP:9][MetadataExtractorComposition][MATCH] Extractor {extractor.__class__.__name__} matched for file={os.path.basename(file_path)}")
                return extractor.extract(file_path=file_path, converted_filename=converted_filename, original_filename=original_filename, parameters=parameters)
        logger.warning(f"[IMP:8][MetadataExtractorComposition][NO_MATCH] No extractor found for file={os.path.basename(file_path)}")
        raise Exception(f"Can't extract metadata from from file {os.path.basename(file_path)}")
    # endregion METHOD_extract
# endregion CLASS_MetadataExtractorComposition
