# region MODULE_CONTRACT [DOMAIN(7): DocumentProcessing; CONCEPT(8): FileOperations, StringUtils; TECH(6): mimetypes, hashlib, requests]
## @modulecontract
## @purpose To provide general-purpose utility functions for file handling, MIME type detection, encoding detection, text similarity, and datetime conversion across the Dedoc document processing pipeline.
## @scope File I/O, MIME type inference, encoding detection, string similarity, datetime parsing, file hashing, batch iteration.
## @input File paths, binary data, text strings, UploadFile objects.
## @output File paths, MIME types, encodings, hashes, similarity scores, Unix timestamps.
## @links [USES_API(7): mimetypes, hashlib, charset_normalizer, Levenshtein, requests]
## @invariants
## - get_file_mime_type ALWAYS returns a non-empty string.
## - calculate_file_hash ALWAYS returns a hex digest string.
## - splitext_ correctly handles multi-dot extensions (e.g., .tar.gz).
## @rationale
## Q: Why use charset_normalizer instead of chardet?
## A: charset_normalizer provides more accurate encoding detection and is actively maintained.
## @changes
## LAST_CHANGE: [v1.0.0 – Added SEMANTIC TEMPLATE markup and LDD logging]
## @modulemap
## FUNC 3[List access with default] => list_get
## FUNC 2[Flatten nested lists] => flatten
## FUNC 1[Identity function] => identity
## FUNC 4[Batch iterator] => get_batch
## FUNC 6[Extension splitting with multi-dot support] => splitext_
## FUNC 7[MIME and extension resolver] => get_mime_extension
## FUNC 5[Document dict to text] => document2txt
## FUNC 6[Unique filename generator] => get_unique_name
## FUNC 7[Upload file saver] => save_upload_file
## FUNC 6[Binary data to unique file] => save_data_to_unique_file
## FUNC 7[MIME type from path] => get_file_mime_type
## FUNC 8[MIME type from file content] => get_file_mime_by_content
## FUNC 4[Extensions by MIME] => get_extensions_by_mime
## FUNC 4[Extensions by multiple MIMEs] => get_extensions_by_mimes
## FUNC 3[Regex character class match] => special_match
## FUNC 7[MD5 file hash] => calculate_file_hash
## FUNC 5[Empty DocumentContent factory] => get_empty_content
## FUNC 8[File encoding detection] => get_encoding
## FUNC 6[String similarity ratio] => similarity
## FUNC 6[Levenshtein similarity ratio] => similarity_levenshtein
## FUNC 8[ISO/IEC 8824 to Unix timestamp] => convert_datetime
## FUNC 5[Filename length trimmer] => check_filename_length
## FUNC 7[HTTP file upload sender] => send_file
## @usecases
## - [get_mime_extension]: Reader → ResolveFileType → MIME and extension determined
## - [save_upload_file]: API → ReceiveFileUpload → File saved to disk
## - [get_encoding]: Reader → DetectFileEncoding → Encoding identified for text extraction
def _module_contract():
    pass
# endregion MODULE_CONTRACT
# GREP_SUMMARY: utilities, MIME, encoding, hash, similarity, datetime, file I/O, batch, extension, upload, file type detection
# STRUCTURE: ▶ ┌Library imports┐ → ⚡ Utility functions ∋each: 〈Input → Process → Output〉 → ⎋ return

import datetime
import json
import logging
import mimetypes
import os
import re
import shutil
import time
from typing import Any, Dict, Iterable, Iterator, List, Optional, Set, Tuple, TypeVar

from fastapi import UploadFile

from dedoc.data_structures.document_content import DocumentContent
from dedoc.data_structures.hierarchy_level import HierarchyLevel
from dedoc.data_structures.line_metadata import LineMetadata
from dedoc.data_structures.tree_node import TreeNode

logger = logging.getLogger(__name__)

T = TypeVar("T")
double_dot_extensions = (".txt.gz", ".tar.gz", ".mht.gz", ".mhtml.gz", ".note.pickle")


# region FUNC_list_get [DOMAIN(5): DataStructures; CONCEPT(3): Collections; TECH(3): TypedListAccess]
## @purpose To safely access list elements by index, returning a default value when the index is out of bounds.
## @uses typing
## @io (List[T], int, Optional[T]) -> Optional[T]
## @complexity 2
def list_get(ls: List[T], index: int, default: Optional[T] = None) -> Optional[T]:
    logger.debug(f"[IMP:3][list_get][CHECK] index={index}, len={len(ls)}")
    if 0 <= index < len(ls):
        return ls[index]
    return default
# endregion FUNC_list_get


# region FUNC_flatten [DOMAIN(5): DataStructures; CONCEPT(4): Iteration; TECH(3): Generators]
## @purpose To flatten a nested list-of-lists structure into a single iterable sequence, enabling sequential processing of grouped data.
## @uses typing
## @io List[List[T]] -> Iterable[T]
## @complexity 2
def flatten(data: List[List[T]]) -> Iterable[T]:
    for group in data:
        for item in group:
            yield item
# endregion FUNC_flatten


# region FUNC_identity [DOMAIN(3): Functional; CONCEPT(2): Transform; TECH(1): Generics]
## @purpose To return its input unchanged, serving as a no-op transform in functional pipelines.
## @io T -> T
## @complexity 1
def identity(x: T) -> T:
    return x
# endregion FUNC_identity


# region FUNC_get_batch [DOMAIN(5): DataStructures; CONCEPT(5): Batching; TECH(4): Iterators]
## @purpose To partition an iterator into fixed-size batches, enabling chunked processing of large data streams.
## @uses typing
## @io (int, Iterator[T]) -> Iterator[List[T]]
## @complexity 3
def get_batch(size: int, iterable: Iterator[T]) -> Iterator[List[T]]:
    logger.debug(f"[IMP:4][get_batch][INIT] Batch size={size}")
    batch = []
    for item in iterable:
        batch.append(item)
        if len(batch) >= size:
            yield batch
            batch = []
    if len(batch) > 0:
        logger.debug(f"[IMP:4][get_batch][TAIL] Yielding final batch of size {len(batch)}")
        yield batch
# endregion FUNC_get_batch


# region FUNC_splitext_ [DOMAIN(7): DocumentProcessing; CONCEPT(6): FileExtension; TECH(5): PathParsing]
## @purpose To split a filename into (name, extension) correctly handling multi-dot extensions like .tar.gz that are common in compressed document formats.
## @uses os.path
## @io str -> Tuple[str, str]
## @complexity 4
def splitext_(path: str) -> Tuple[str, str]:
    if not path.endswith(double_dot_extensions):
        return os.path.splitext(path)

    name, *ext_list = path.rsplit(".", maxsplit=2)
    return name, f".{'.'.join(ext_list)}"
# endregion FUNC_splitext_


# region FUNC_get_mime_extension [DOMAIN(8): DocumentProcessing; CONCEPT(7): FileTypeDetection; TECH(6): mimetypes]
## @purpose To resolve the MIME type and file extension from a file path or explicit parameters, providing a single entry point for file type identification throughout the pipeline.
## @uses splitext_, get_file_mime_type
## @io (Optional[str], Optional[str], Optional[str]) -> Tuple[str, str]
## @complexity 5
def get_mime_extension(file_path: Optional[str] = None, mime: Optional[str] = None, extension: Optional[str] = None) -> Tuple[str, str]:
    logger.debug(f"[IMP:6][get_mime_extension][INIT] file_path={file_path}, mime={mime}, extension={extension}")
    if mime is not None and extension is not None:
        return mime, extension

    if file_path:
        name, extension = splitext_(file_path)
        mime = get_file_mime_type(file_path)
    else:
        assert mime is not None or extension is not None, "When file_path is None, mime or extension should be provided"
        mime = "" if mime is None else mime
        extension = "" if extension is None else extension

    logger.info(f"[IMP:7][get_mime_extension][RESULT] Resolved: mime={mime}, extension={extension}")
    return mime, extension
# endregion FUNC_get_mime_extension


# region FUNC__text_from_item [DOMAIN(6): DocumentProcessing; CONCEPT(5): TextExtraction; TECH(4): RecursiveTraversal]
## @purpose To recursively extract text from a document item dict, descending into subparagraphs to build a complete text representation.
## @io dict -> str
## @complexity 4
def _text_from_item(item: dict) -> str:
    res = item.get("text", "")
    if "subparagraphs" in item:
        res += "\n".join(_text_from_item(_) for _ in item["subparagraphs"])
    return res
# endregion FUNC__text_from_item


# region FUNC_document2txt [DOMAIN(7): DocumentProcessing; CONCEPT(6): TextSerialization; TECH(5): DictTraversal]
## @purpose To convert a structured document dictionary into a flat text string, combining header and item texts for downstream NLP processing.
## @uses _text_from_item
## @io dict -> str
## @complexity 4
def document2txt(doc: dict) -> str:
    res = doc["header"]
    for item in doc["items"]:
        res += "\n"
        res += _text_from_item(item)
    return res
# endregion FUNC_document2txt


# region FUNC_get_unique_name [DOMAIN(7): DocumentProcessing; CONCEPT(6): FileNaming; TECH(5): TimestampRandom]
## @purpose To generate a collision-resistant unique filename using a timestamp and random suffix, ensuring safe concurrent file writes.
## @uses splitext_, time, random
## @io str -> str
## @complexity 4
def get_unique_name(filename: str) -> str:
    import random

    _, ext = splitext_(filename)
    ts = int(time.time())
    rnd = random.randint(0, 1000)
    unique = str(ts) + "_" + str(rnd) + ext
    logger.debug(f"[IMP:5][get_unique_name][GENERATE] Unique name: {unique}")
    return unique
# endregion FUNC_get_unique_name


# region FUNC_save_upload_file [DOMAIN(8): DocumentProcessing; CONCEPT(7): FileIO; TECH(6): FastAPI, shutil]
## @purpose To persist an uploaded file from a FastAPI endpoint to disk with filename length validation, ensuring safe storage before processing.
## @uses shutil, check_filename_length
## @io (UploadFile, str) -> str
## @complexity 5
def save_upload_file(upload_file: UploadFile, output_dir: str) -> str:
    file_name = upload_file.filename.split("/")[-1]
    file_name = check_filename_length(file_name)
    file_path = os.path.join(output_dir, file_name)
    logger.info(f"[IMP:7][save_upload_file][SAVE] Saving to {file_path}")
    try:
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(upload_file.file, buffer)
    finally:
        upload_file.file.close()

    logger.debug(f"[IMP:6][save_upload_file][DONE] File saved: {file_path}")
    return file_path
# endregion FUNC_save_upload_file


# region FUNC_save_data_to_unique_file [DOMAIN(7): DocumentProcessing; CONCEPT(6): FileIO; TECH(5): BinaryWrite]
## @purpose To write binary data to a uniquely-named file in a target directory, avoiding collisions from concurrent writes.
## @uses get_unique_name
## @io (str, str, bytes) -> str
## @complexity 4
def save_data_to_unique_file(directory: str, filename: str, binary_data: bytes) -> str:
    unique_filename = get_unique_name(filename)
    with open(os.path.join(directory, unique_filename), "wb") as file_disc:
        file_disc.write(binary_data)

    logger.debug(f"[IMP:6][save_data_to_unique_file][SAVE] Saved as {unique_filename} in {directory}")
    return unique_filename
# endregion FUNC_save_data_to_unique_file


# region FUNC_get_file_mime_type [DOMAIN(8): DocumentProcessing; CONCEPT(7): FileTypeDetection; TECH(6): mimetypes]
## @purpose To detect the MIME type of a file from its path/extension using the mimetypes standard library.
## @uses mimetypes
## @io str -> str
## @complexity 3
def get_file_mime_type(path: str) -> str:
    mime = mimetypes.guess_type(path)[0] or "application/octet-stream"
    logger.debug(f"[IMP:5][get_file_mime_type][DETECT] Path={path}, MIME={mime}")
    return mime
# endregion FUNC_get_file_mime_type


# region FUNC_get_file_mime_by_content [DOMAIN(8): DocumentProcessing; CONCEPT(8): FileTypeDetection; TECH(7): magic, puremagic]
## @purpose To determine the MIME type by inspecting file content bytes (magic number detection), falling back to puremagic when libmagic returns octet-stream.
## @uses magic, puremagic
## @io str -> str
## @complexity 6
def get_file_mime_by_content(path: str) -> str:
    import magic
    import puremagic

    mime = magic.from_file(path, mime=True)

    if mime == "application/octet-stream":  # for files with mime in {"image/x-sun-raster", "image/x-ms-bmp"}
        try:
            mime = puremagic.from_file(path, mime=True)
            logger.debug(f"[IMP:5][get_file_mime_by_content][FALLBACK] puremagic resolved: {mime}")
        except puremagic.main.PureError:
            logger.debug(f"[IMP:5][get_file_mime_by_content][FALLBACK] puremagic failed, keeping octet-stream")

    logger.info(f"[IMP:7][get_file_mime_by_content][RESULT] Final MIME: {mime}")
    return mime
# endregion FUNC_get_file_mime_by_content


# region FUNC_get_extensions_by_mime [DOMAIN(6): DocumentProcessing; CONCEPT(5): FileTypeDetection; TECH(4): mimetypes]
## @purpose To retrieve all known file extensions for a given MIME type.
## @uses mimetypes
## @io str -> List[str]
## @complexity 2
def get_extensions_by_mime(mime: str) -> List[str]:
    return mimetypes.guess_all_extensions(mime)
# endregion FUNC_get_extensions_by_mime


# region FUNC_get_extensions_by_mimes [DOMAIN(6): DocumentProcessing; CONCEPT(5): FileTypeDetection; TECH(4): mimetypes]
## @purpose To aggregate all file extensions for a set of MIME types, useful for filtering input by multiple accepted formats.
## @uses get_extensions_by_mime
## @io Set[str] -> List[str]
## @complexity 3
def get_extensions_by_mimes(mimes: Set[str]) -> List[str]:
    exts = []
    for mime in mimes:
        exts.extend(get_extensions_by_mime(mime))
    return exts
# endregion FUNC_get_extensions_by_mimes


# region FUNC_special_match [DOMAIN(4): TextProcessing; CONCEPT(4): Validation; TECH(3): regex]
## @purpose To check if a string consists only of a specific character class (default: non-punctuation), used for content validation.
## @uses re
## @io (str, str) -> bool
## @complexity 3
def special_match(strg: str, regular_pattern: str = r"[^.?!,:;'\"\n\r ]") -> bool:
    search = re.compile(regular_pattern).search
    return not bool(search(strg))
# endregion FUNC_special_match


# region FUNC_calculate_file_hash [DOMAIN(7): DocumentProcessing; CONCEPT(6): Integrity; TECH(6): hashlib]
## @purpose To compute an MD5 hash of a file for content-based deduplication and integrity verification.
## @uses hashlib
## @io str -> str
## @complexity 4
def calculate_file_hash(path: str) -> str:
    import hashlib

    with open(path, "rb") as file:
        file_hash = hashlib.md5()
        chunk = file.read(8192)
        while chunk:
            file_hash.update(chunk)
            chunk = file.read(8192)
    hash_result = str(file_hash.hexdigest())
    logger.info(f"[IMP:7][calculate_file_hash][RESULT] Hash for {path}: {hash_result}")
    return hash_result
# endregion FUNC_calculate_file_hash


# region FUNC_get_empty_content [DOMAIN(6): DocumentProcessing; CONCEPT(5): DataFactory; TECH(5): DataStructures]
## @purpose To create an empty DocumentContent instance with a minimal valid structure, serving as a safe default for error-handling and initialization.
## @uses DocumentContent, TreeNode, LineMetadata, HierarchyLevel
## @io None -> DocumentContent
## @complexity 3
def get_empty_content() -> DocumentContent:
    return DocumentContent(
        tables=[],
        structure=TreeNode(node_id="0",
                           text="",
                           annotations=[],
                           metadata=LineMetadata(page_id=0, line_id=0, hierarchy_level=HierarchyLevel.create_root()),
                           subparagraphs=[],
                           parent=None)
    )
# endregion FUNC_get_empty_content


# region FUNC_get_encoding [DOMAIN(8): DocumentProcessing; CONCEPT(8): TextDecoding; TECH(7): charset_normalizer]
## @purpose To detect the character encoding of a file (including gzip-compressed), enabling correct text extraction from diverse document sources.
## @uses gzip, charset_normalizer
## @io (str, Optional[str]) -> Optional[str]
## @complexity 6
def get_encoding(path: str, default: str = None) -> Optional[str]:
    import gzip
    from charset_normalizer import from_bytes

    try:
        if path.endswith(".gz"):
            with gzip.open(path, "r") as file:
                blob = file.read()
        else:
            with open(path, "rb") as file:
                blob = file.read()
        dammit = from_bytes(blob)
        encoding = dammit.best().encoding
        logger.info(f"[IMP:7][get_encoding][DETECT] Encoding for {path}: {encoding}")
        return encoding
    except Exception:
        logger.warning(f"[IMP:8][get_encoding][FALLBACK] Encoding detection failed for {path}, using default={default}")
        return default
# endregion FUNC_get_encoding


# region FUNC_similarity [DOMAIN(6): TextProcessing; CONCEPT(6): StringComparison; TECH(5): difflib]
## @purpose To compute a case-insensitive string similarity ratio using difflib.SequenceMatcher, enabling fuzzy text matching.
## @uses difflib
## @io (str, str) -> float
## @complexity 4
def similarity(s1: str, s2: str) -> float:
    import difflib

    normalized1 = s1.lower()
    normalized2 = s2.lower()
    matcher = difflib.SequenceMatcher(None, normalized1, normalized2)
    return matcher.ratio()
# endregion FUNC_similarity


# region FUNC_similarity_levenshtein [DOMAIN(6): TextProcessing; CONCEPT(6): StringComparison; TECH(5): Levenshtein]
## @purpose To compute a case-insensitive Levenshtein ratio for high-quality fuzzy string comparison.
## @uses Levenshtein
## @io (str, str) -> float
## @complexity 4
def similarity_levenshtein(str1: str, str2: str) -> float:
    from Levenshtein import ratio

    str1 = str1.lower()
    str2 = str2.lower()
    return ratio(str1, str2)
# endregion FUNC_similarity_levenshtein


# region FUNC_convert_datetime [DOMAIN(8): DocumentProcessing; CONCEPT(7): TimestampParsing; TECH(6): dateutil]
## @purpose To parse ISO/IEC 8824 datetime strings (common in PDF metadata) into Unix timestamps, handling multiple format variants including UTC offsets.
## @uses datetime, dateutil, re
## @io str -> int
## @complexity 7
def convert_datetime(time_string: str) -> int:
    from dateutil.parser import parse

    date = str(time_string).replace("D:", "")
    if re.match(r"\d{14}(\+|-)\d{2}'?\d{2}'?", date):
        date_format = "%Y%m%d%H%M%S%z"
        d = datetime.datetime.strptime(date.replace("'", ""), date_format)
    elif re.match(r"\d{14}(Z|z)\d{2}'?\d{2}'?", date):
        date_format = "%Y%m%d%H%M%S"
        date = date.split("Z")[0]
        d = datetime.datetime.strptime(date.replace("'", ""), date_format)
    else:
        d = parse(date, fuzzy=True)

    timestamp = int(d.timestamp())
    logger.debug(f"[IMP:6][convert_datetime][PARSE] Input={time_string}, timestamp={timestamp}")
    return timestamp
# endregion FUNC_convert_datetime


# region FUNC_check_filename_length [DOMAIN(6): DocumentProcessing; CONCEPT(5): FileSystem; TECH(4): POSIX]
## @purpose To truncate filenames exceeding the POSIX 255-character limit, preserving the extension to maintain file type integrity.
## @uses splitext_
## @io str -> str
## @complexity 3
def check_filename_length(filename: str) -> str:
    max_filename_length = 255  # posix name limitation
    if len(filename) > max_filename_length:
        name, ext = splitext_(filename)
        filename = name[:max_filename_length - len(ext)] + ext
        logger.debug(f"[IMP:5][check_filename_length][TRUNCATE] Truncated to {len(filename)} chars")
    return filename
# endregion FUNC_check_filename_length


# region FUNC_send_file [DOMAIN(7): DocumentProcessing; CONCEPT(6): NetworkIO; TECH(6): requests]
## @purpose To send a file via HTTP POST multipart upload to a remote dedoc endpoint, enabling distributed document processing.
## @uses requests, json
## @io (str, str, str, dict) -> Dict[str, Any]
## @complexity 5
def send_file(host: str, file_name: str, file_path: str, parameters: dict) -> Dict[str, Any]:
    import requests

    logger.info(f"[IMP:7][send_file][SEND] Posting {file_name} to {host}/upload")
    with open(file_path, "rb") as file:
        files = {"file": (file_name, file)}
        r = requests.post(f"{host}/upload", files=files, data=parameters)
        assert r.status_code == 200
        result = json.loads(r.content.decode())
        logger.debug(f"[IMP:6][send_file][RESPONSE] Status 200, result keys: {list(result.keys())}")
        return result
# endregion FUNC_send_file
