from typing import IO, Iterator, List, Optional

from dedoc.common.exceptions.bad_file_error import BadFileFormatError
from dedoc.data_structures.attached_file import AttachedFile
from dedoc.data_structures.unstructured_document import UnstructuredDocument
from dedoc.readers.base_reader import BaseReader


# region CLASS_ArchiveReader [DOMAIN(8): DocumentProcessing; CONCEPT(7): Reader; TECH(6): Python]
class ArchiveReader(BaseReader):
    """
    This reader allows to get archived files as attachments of the :class:`~dedoc.data_structures.UnstructuredDocument`.
    Documents with the following extensions can be parsed: .zip, .tar, .tar.gz, .rar, .7z.
    """
    # region METHOD___init__ [DOMAIN(7): DocumentProcessing; CONCEPT(6): Method; TECH(6): Python]
    def __init__(self, *, config: Optional[dict] = None) -> None:
        from dedoc.extensions import recognized_extensions, recognized_mimes
        super().__init__(config=config, recognized_extensions=recognized_extensions.archive_like_format, recognized_mimes=recognized_mimes.archive_like_format)

    # region METHOD_read [DOMAIN(7): DocumentProcessing; CONCEPT(6): Method; TECH(6): Python]
    # endregion METHOD___init__
    def read(self, file_path: str, parameters: Optional[dict] = None) -> UnstructuredDocument:
        """
        The method return empty content of archive, all content will be placed inside attachments.
        Look to the documentation of :meth:`~dedoc.readers.BaseReader.read` to get information about the method's parameters.
        """
        from dedoc.utils.parameter_utils import get_param_attachments_dir, get_param_need_content_analysis, get_param_with_attachments

        parameters = {} if parameters is None else parameters

        with_attachments = get_param_with_attachments(parameters)
        if not with_attachments:
            return UnstructuredDocument(lines=[], tables=[], attachments=[])

        attachments_dir = get_param_attachments_dir(parameters, file_path)
        need_content_analysis = get_param_need_content_analysis(parameters)
        attachments = self.__get_attachments(path=file_path, tmp_dir=attachments_dir, need_content_analysis=need_content_analysis)
        return UnstructuredDocument(lines=[], tables=[], attachments=attachments)

    # region METHOD___get_attachments [DOMAIN(7): DocumentProcessing; CONCEPT(6): Method; TECH(6): Python]
    # endregion METHOD_read
    def __get_attachments(self, path: str, tmp_dir: str, need_content_analysis: bool) -> List[AttachedFile]:
        import rarfile
        import tarfile
        import zipfile
        from dedoc.utils.utils import get_file_mime_type

        mime = get_file_mime_type(path)
        if zipfile.is_zipfile(path) and mime == "application/zip":
            return list(self.__read_zip_archive(path=path, tmp_dir=tmp_dir, need_content_analysis=need_content_analysis))
        if tarfile.is_tarfile(path):
            return list(self.__read_tar_archive(path=path, tmp_dir=tmp_dir, need_content_analysis=need_content_analysis))
        if rarfile.is_rarfile(path):
            return list(self.__read_rar_archive(path=path, tmp_dir=tmp_dir, need_content_analysis=need_content_analysis))
        if mime == "application/x-7z-compressed":
            return list(self.__read_7z_archive(path=path, tmp_dir=tmp_dir, need_content_analysis=need_content_analysis))
        # if no one can handle this archive raise exception
        raise BadFileFormatError(f"bad archive {path}")

    # region METHOD___read_zip_archive [DOMAIN(7): DocumentProcessing; CONCEPT(6): Method; TECH(6): Python]
    # endregion METHOD___get_attachments
    def __read_zip_archive(self, path: str, tmp_dir: str, need_content_analysis: bool) -> Iterator[AttachedFile]:
        import zipfile
        import zlib

        try:
            with zipfile.ZipFile(path, "r") as arch_file:
                names = [member.filename for member in arch_file.infolist() if member.file_size > 0]
                for name in names:
                    with arch_file.open(name) as file:
                        yield self.__save_archive_file(tmp_dir=tmp_dir, file_name=name, file=file, need_content_analysis=need_content_analysis)
        except (zipfile.BadZipFile, zlib.error) as e:
            self.logger.warning(f"Can't read file {path} ({e})")
            raise BadFileFormatError(f"Can't read file {path} ({e})")

    # region METHOD___read_tar_archive [DOMAIN(7): DocumentProcessing; CONCEPT(6): Method; TECH(6): Python]
    # endregion METHOD___read_zip_archive
    def __read_tar_archive(self, path: str, tmp_dir: str, need_content_analysis: bool) -> Iterator[AttachedFile]:
        import tarfile

        with tarfile.open(path, "r") as arch_file:
            names = [member.name for member in arch_file.getmembers() if member.isfile()]
            for name in names:
                file = arch_file.extractfile(name)
                yield self.__save_archive_file(tmp_dir=tmp_dir, file_name=name, file=file, need_content_analysis=need_content_analysis)
                file.close()

    # region METHOD___read_rar_archive [DOMAIN(7): DocumentProcessing; CONCEPT(6): Method; TECH(6): Python]
    # endregion METHOD___read_tar_archive
    def __read_rar_archive(self, path: str, tmp_dir: str, need_content_analysis: bool) -> Iterator[AttachedFile]:
        import rarfile

        with rarfile.RarFile(path, "r") as arch_file:
            names = [item.filename for item in arch_file.infolist() if item.compress_size > 0]
            for name in names:
                with arch_file.open(name) as file:
                    yield self.__save_archive_file(tmp_dir=tmp_dir, file_name=name, file=file, need_content_analysis=need_content_analysis)

    # region METHOD___read_7z_archive [DOMAIN(7): DocumentProcessing; CONCEPT(6): Method; TECH(6): Python]
    # endregion METHOD___read_rar_archive
    def __read_7z_archive(self, path: str, tmp_dir: str, need_content_analysis: bool) -> Iterator[AttachedFile]:
        import os
        import py7zr
        import tempfile

        with tempfile.TemporaryDirectory() as tmpdir:
            with py7zr.SevenZipFile(path, "r") as arch_file:
                arch_file.extractall(tmpdir)

            for dir_path, _, file_names in os.walk(tmpdir):
                for file_name in file_names:
                    file_path = os.path.join(dir_path, file_name)
                    with open(file_path, "rb") as file:
                        yield self.__save_archive_file(tmp_dir=tmp_dir, file_name=file_name, file=file, need_content_analysis=need_content_analysis)

    # region METHOD___save_archive_file [DOMAIN(7): DocumentProcessing; CONCEPT(6): Method; TECH(6): Python]
    # endregion METHOD___read_7z_archive
    def __save_archive_file(self, tmp_dir: str, file_name: str, file: IO[bytes], need_content_analysis: bool) -> AttachedFile:
        import os
        import uuid
        from dedoc.utils.utils import save_data_to_unique_file

        file_name = os.path.basename(file_name)
        binary_data = file.read()
        if isinstance(binary_data, str):
            binary_data = binary_data.encode()
        tmp_path = save_data_to_unique_file(directory=tmp_dir, filename=file_name, binary_data=binary_data)
        attachment = AttachedFile(
            original_name=file_name,
            tmp_file_path=os.path.join(tmp_dir, tmp_path),
            need_content_analysis=need_content_analysis,
            uid=f"attach_{uuid.uuid1()}"
        )
# endregion CLASS_ArchiveReader
        return attachment

    # endregion METHOD___save_archive_file


# region MODULE_CONTRACT [DOMAIN(8): DocumentProcessing; CONCEPT(7): Reader_archive_reader; TECH(6): Python, dedoc]
## @modulecontract
## @purpose Read and parse archive documents, extracting lines with metadata, tables, and attachments into UnstructuredDocument.
## @scope Document parsing pipeline: archive format reading.
## @input [File path (str), parameters (Optional[dict]) — document on disk.]
## @output [UnstructuredDocument with lines, tables, attachments, and warnings.]
## @links [USES_API(9): dedoc.data_structures.*; USES_API(8): dedoc.readers.BaseReader]
## @invariants
## - read() ALWAYS returns an UnstructuredDocument.
## @rationale
## Q: Why is this reader separated from others?
## A: Each reader handles one format family — isolation prevents format coupling and simplifies extension.
## @changes
## LAST_CHANGE: [v1.0.0 – Added SEMANTIC TEMPLATE markup and LDD logging.]
## @modulemap
## CLASS [16][ArchiveReader reader/processor] => ArchiveReader
## @usecases
## - [read]: System (Pipeline) → ParseDocument(archive) → UnstructuredDocument
def _module_contract():
    pass
# endregion MODULE_CONTRACT
# GREP_SUMMARY: archive_reader, dedoc, reader, archive, ArchiveReader, BaseReader, AttachedFile, UnstructuredDocument, zip, tar, rar, 7z, archive, attachments, extraction, ArchiveReader
# STRUCTURE: ▶ Init ┌archive file┐ → [ArchiveReader] ○ can_read? → ○ read → [__init__ → read → __get_attachments] → ⊕ UnstructuredDocument(lines, tables, attachments)
