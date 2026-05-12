# region MODULE_CONTRACT [DOMAIN(8): DocumentProcessing; CONCEPT(9): AttachmentExtraction; TECH(7): ABC, PythonAbstract]
## @modulecontract
## @purpose Define the abstract contract for all attachment extractors: file recognition (can_extract), extraction (extract), parameter inspection (with_attachments), and content-to-AttachedFile serialization.
## @scope Abstract base for attachment extraction: extension/MIME matching, attachment serialization to AttachedFile list, parameter inspection.
## @input file_path, extension, mime, parameters dict, binary content tuples.
## @output Boolean (can_extract), List[AttachedFile] (extract, _content2attach_file).
## @links [USES_API(8): dedoc.data_structures.attached_file.AttachedFile]
## @links [USES_API(7): dedoc.utils.utils.get_mime_extension, dedoc.utils.utils.save_data_to_unique_file]
## @links [USES_API(7): dedoc.utils.parameter_utils.get_param_attachments_dir]
## @invariants
## - can_extract ALWAYS returns bool and NEVER raises.
## - extract is abstract; subclasses MUST implement it.
## - _content2attach_file ALWAYS returns List[AttachedFile].
## @rationale
## Q: Why use ABC with abstractmethod instead of a protocol?
## A: extract is the core polymorphic behavior; enforcing it at instantiation time via ABC prevents runtime errors from incomplete implementations.
## Q: Why lazy imports inside methods?
## A: Avoids circular imports from dedoc.utils and reduces cold-start import overhead.
## @changes
## LAST_CHANGE: [v1.0.0 – Semantic markup + LDD logging added]
## @modulemap
## CLASS 10[Abstract base contract for all attachment extractors] => AbstractAttachmentsExtractor
## METHOD 7[Constructor: stores config, recognized extensions/mimes] => __init__
## METHOD 8[Checks if this extractor can handle the given file] => can_extract
## METHOD 10[Abstract: extracts attachments from file] => extract
## METHOD 5[Static: checks with_attachments parameter] => with_attachments
## METHOD 8[Converts (name, bytes) tuples to AttachedFile list] => _content2attach_file
## @usecases
## - [can_extract]: DedocManager => SelectExtractor => bool
## - [extract]: DedocManager => ExtractAttachments => List[AttachedFile]
## - [_content2attach_file]: ConcreteExtractor => SerializeBinaryContent => List[AttachedFile]
def _module_contract():
    pass
# endregion MODULE_CONTRACT
# GREP_SUMMARY: attachments, extractor, abstract, ABC, can_extract, extract, with_attachments, AttachedFile, MIME, extension
# STRUCTURE: ▶ Init ┌config, recognized_extensions, recognized_mimes┐ → ⚡ can_extract(file_path, ext, mime) → ◇ get_mime_extension → 〈ext∋recognized ? T/F〉 → ⎋ bool; ⚡ extract(file_path, params) → [abstract]; ⚡ _content2attach_file(content_list, tmpdir) → ○ ∀(name,bytes): ⊕ AttachedFile → ∑ List[AttachedFile] → ⎋

from abc import ABC, abstractmethod
from typing import List, Optional, Set, Tuple

from dedoc.data_structures.attached_file import AttachedFile

import logging

logger = logging.getLogger(__name__)


# region CLASS_AbstractAttachmentsExtractor [DOMAIN(8): DocumentProcessing; CONCEPT(9): AttachmentExtraction; TECH(7): ABC]
## @purpose Define the abstract contract that all attachment extractors must fulfill: file recognition, extraction, and content serialization.
class AbstractAttachmentsExtractor(ABC):
    # region METHOD___init__ [DOMAIN(8): DocumentProcessing; CONCEPT(5): Initialization; TECH(4): PythonConfig]
    ## @purpose Initialize the extractor with configuration, recognized file extensions, and recognized MIME types.
    ## @io Optional[dict], Optional[Set[str]], Optional[Set[str]] -> None
    ## @complexity 4
    def __init__(self, *, config: Optional[dict] = None, recognized_extensions: Optional[Set[str]] = None, recognized_mimes: Optional[Set[str]] = None) -> None:
        self.config = {} if config is None else config
        self.logger = self.config.get("logger", logging.getLogger())
        self._recognized_extensions = {} if recognized_extensions is None else recognized_extensions
        self._recognized_mimes = {} if recognized_mimes is None else recognized_mimes
        logger.debug(f"[IMP:4][AbstractAttachmentsExtractor][INIT] Recognized extensions: {self._recognized_extensions}, mimes: {self._recognized_mimes}")
    # endregion METHOD___init__

    # region METHOD_can_extract [DOMAIN(8): DocumentProcessing; CONCEPT(8): FileRecognition; TECH(6): MIME, Extension]
    ## @purpose Determine whether this extractor can handle the given file based on its extension or MIME type.
    ## @uses dedoc.utils.utils.get_mime_extension
    ## @io Optional[str], Optional[str], Optional[str], Optional[dict] -> bool
    ## @complexity 4
    def can_extract(self,
                    file_path: Optional[str] = None,
                    extension: Optional[str] = None,
                    mime: Optional[str] = None,
                    parameters: Optional[dict] = None) -> bool:
        from dedoc.utils.utils import get_mime_extension
        mime, extension = get_mime_extension(file_path=file_path, mime=mime, extension=extension)
        result = extension.lower() in self._recognized_extensions or mime in self._recognized_mimes
        logger.debug(f"[IMP:6][AbstractAttachmentsExtractor][CAN_EXTRACT] file_path={file_path}, ext={extension}, mime={mime}, result={result}")
        return result
    # endregion METHOD_can_extract

    # region METHOD_extract [DOMAIN(9): DocumentProcessing; CONCEPT(9): AttachmentExtraction; TECH(7): ABC]
    ## @purpose Abstract method: extract attachments from the given file. Must be implemented by concrete subclasses.
    ## @io str, Optional[dict] -> List[AttachedFile]
    ## @complexity 1
    @abstractmethod
    def extract(self, file_path: str, parameters: Optional[dict] = None) -> List[AttachedFile]:
        pass
    # endregion METHOD_extract

    # region METHOD_with_attachments [DOMAIN(7): DocumentProcessing; CONCEPT(6): ParameterInspection; TECH(3): PythonDict]
    ## @purpose Static helper: check if the 'with_attachments' parameter is truthy.
    ## @io dict -> bool
    ## @complexity 2
    @staticmethod
    def with_attachments(parameters: dict) -> bool:
        result = str(parameters.get("with_attachments", "false")).lower() == "true"
        logger.debug(f"[IMP:4][AbstractAttachmentsExtractor][WITH_ATTACHMENTS] result={result}")
        return result
    # endregion METHOD_with_attachments

    # region METHOD__content2attach_file [DOMAIN(8): DocumentProcessing; CONCEPT(8): ContentSerialization; TECH(6): FileIO, UUID]
    ## @purpose Convert a list of (filename, binary_data) tuples into a list of AttachedFile objects, saving binary data to unique files on disk.
    ## @uses dedoc.utils.utils.save_data_to_unique_file, dedoc.utils.parameter_utils.get_param_attachments_dir
    ## @io List[Tuple[str, bytes]], str, bool, dict -> List[AttachedFile]
    ## @complexity 5
    def _content2attach_file(self, content: List[Tuple[str, bytes]], tmpdir: str, need_content_analysis: bool, parameters: dict) -> List[AttachedFile]:
        import os
        import uuid
        from dedoc.utils.parameter_utils import get_param_attachments_dir
        from dedoc.utils.utils import save_data_to_unique_file

        attachments = []

        attachments_dir = get_param_attachments_dir(parameters, tmpdir)
        logger.debug(f"[IMP:6][AbstractAttachmentsExtractor][CONTENT2ATTACH] Saving {len(content)} attachments to {attachments_dir}")

        for original_name, contents in content:
            tmp_file_name = save_data_to_unique_file(directory=attachments_dir, filename=original_name, binary_data=contents)
            tmp_file_path = os.path.join(attachments_dir, tmp_file_name)
            file = AttachedFile(original_name=original_name,
                                tmp_file_path=tmp_file_path,
                                uid=f"attach_{uuid.uuid4()}",
                                need_content_analysis=need_content_analysis)
            attachments.append(file)
            logger.debug(f"[IMP:3][AbstractAttachmentsExtractor][CONTENT2ATTACH] Saved attachment: {original_name} -> {tmp_file_path}")

        logger.info(f"[IMP:9][AbstractAttachmentsExtractor][CONTENT2ATTACH] Total attachments serialized: {len(attachments)}")
        return attachments
    # endregion METHOD__content2attach_file
# endregion CLASS_AbstractAttachmentsExtractor
