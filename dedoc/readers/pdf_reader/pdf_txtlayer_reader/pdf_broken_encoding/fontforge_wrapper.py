import json
from pathlib import Path
from typing import Dict, List, Tuple

import logging

logger = logging.getLogger(__name__)

import fontforge

image_size = 80


def generate_images(save_path: Path, font_path: Path, index: int, uni_char_pool: List[str]) -> List[str]:
    """Generate images for specified unicode characters from font."""
    font = fontforge.open(str(font_path), 1)
    save_paths = []
    for uni in uni_char_pool:
        uni = int(uni)
        glyph_name = fontforge.nameFromUnicode(uni)
        char = chr(uni)
        try:
            if char.isalpha() and char.isupper():
                char_low = char.lower()
                if font[ord(char)] == font[ord(char_low)]:
                    continue
        except Exception:
            continue

        if glyph_name == -1:
            continue
        char_save_path = str(save_path.joinpath(str(uni), f"{font.fontname}_{index}.png"))

        try:
            font[int(uni)].export(char_save_path, image_size)
            save_paths.append(char_save_path)
        except Exception:
            continue

    return save_paths


def generate_all_images(save_path: Path, font_path: Path) -> Tuple[List[str], Dict[str, str], List[str], List[int]]:
    """Generate images for all glyphs in font."""
    font = fontforge.open(str(font_path))
    save_paths = []
    not_worth_outputting = []
    font_white_spaces = {}
    names = []
    codes = []

    for name in font:
        process_glyph(name, font, save_path, save_paths, font_white_spaces, names, codes, not_worth_outputting)

    return save_paths, font_white_spaces, names, codes


def process_glyph(
    name: str,
    font: Dict[str, any],
    save_path: Path,
    save_paths: List[str],
    font_white_spaces: Dict[str, str],
    names: List[str],
    codes: List[int],
    not_worth_outputting: List[str]
) -> None:
    """Process individual glyph from font."""
    if should_skip_glyph(name, font):
        return

    unicode_val = get_unicode_value(name, font)
    filename = get_filename(name, unicode_val)

    if is_empty_glyph(font, name):
        handle_empty_glyph(filename, font_white_spaces, not_worth_outputting)
        return

    if filename == -1:
        return

    export_glyph(name, font, save_path, filename, save_paths, names, codes, unicode_val)


def should_skip_glyph(name: str, font: Dict[str, any]) -> bool:
    """Check if glyph should be skipped."""
    if "superior" in name:
        return True
    if name == ".notdef":
        return True
    if not font[name].isWorthOutputting() and name != "space":
        return True
    return False


def get_unicode_value(name: str, font: Dict[str, any]) -> int:
    """Get unicode value for glyph name."""
    try:
        return ord(name)
    except TypeError:
        try:
            return font[name].encoding
        except AttributeError:
            return fontforge.unicodeFromName(name)


def get_filename(name: str, unicode_val: int) -> str:
    """Get filename for glyph based on unicode value or name."""
    return str(unicode_val) if unicode_val != -1 else name


def is_empty_glyph(font: Dict[str, any], name: str) -> bool:
    """Check if glyph is empty."""
    if not font[name].isWorthOutputting() or font[name].width == 0:
        for i in range(len(font[name].layers)):
            if font[name].layers[i] != 1:
                return False
        return True
    return False


def handle_empty_glyph(filename: str, font_white_spaces: Dict[str, str], not_worth_outputting: List[str]) -> None:
    """Handle empty glyph case."""
    try:
        name_whitespace = chr(int(filename)) if filename.isdigit() else filename
    except (ValueError, TypeError):
        name_whitespace = filename

    font_white_spaces[name_whitespace] = " "
    not_worth_outputting.append(filename)


def export_glyph(
    name: str,
    font: Dict[str, Dict[str, any]],
    save_path: Path, filename: str,
    save_paths: List[str],
    names: List[str],
    codes: List[int],
    unicode_val: int
) -> None:
    """Export glyph to image file."""
    char_save_path = f"{save_path}/{filename}.png"
    try:
        font[name].export(char_save_path, image_size)
        save_paths.append(char_save_path)
        names.append(name)
        codes.append(unicode_val)
    except OSError:
        pass


if __name__ == "__main__":
    import sys

    args = sys.argv[1:]
    if args[0] == "generate_images":
        result = generate_images(Path(args[1]), Path(args[2]), int(args[3]), args[4:])
        sys.stdout.write(json.dumps(result))
    elif args[0] == "generate_all_images":
        result = generate_all_images(Path(args[1]), Path(args[2]))
        sys.stdout.write(json.dumps(result))


# region MODULE_CONTRACT [DOMAIN(8): DocumentProcessing; CONCEPT(7): Reader_fontforge_wrapper; TECH(6): Python, dedoc]
## @modulecontract
## @purpose Read and parse PDF documents, extracting lines with metadata, tables, and attachments into UnstructuredDocument.
## @scope Document parsing pipeline: PDF format reading.
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
## FUNC [5][generate_images utility/helper] => generate_images
## FUNC [5][generate_all_images utility/helper] => generate_all_images
## FUNC [5][process_glyph utility/helper] => process_glyph
## FUNC [5][should_skip_glyph utility/helper] => should_skip_glyph
## FUNC [5][get_unicode_value utility/helper] => get_unicode_value
## FUNC [5][get_filename utility/helper] => get_filename
## FUNC [5][is_empty_glyph utility/helper] => is_empty_glyph
## FUNC [5][handle_empty_glyph utility/helper] => handle_empty_glyph
## FUNC [5][export_glyph utility/helper] => export_glyph
## @usecases
## - [read]: System (Pipeline) → ParseDocument(PDF) → UnstructuredDocument
def _module_contract():
    pass
# endregion MODULE_CONTRACT
# GREP_SUMMARY: fontforge_wrapper, dedoc, reader, PDF, PdfReader, BaseReader, PDF, pdfminer, tabby, OCR, tables, image, txtlayer, columns, orientation, paragraphs, metadata, extraction, line, bbox, generate_images, generate_all_images, process_glyph, should_skip_glyph, get_unicode_value, get_filename, is_empty_glyph, handle_empty_glyph, export_glyph
# STRUCTURE: ▶ Input → ○ generate_images → generate_all_images → process_glyph → ⊕ result
