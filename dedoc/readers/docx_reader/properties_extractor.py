from typing import Union

from bs4 import Tag

import logging

logger = logging.getLogger(__name__)

from dedoc.readers.docx_reader.data_structures.base_props import BaseProperties


def spacing_to_float(spacing: Union[str, int, float]) -> float:
    if str(spacing).endswith("pt"):
        return float(spacing[:-2])
    return float(spacing)


def check_if_true(value: str) -> bool:
    if value == "1" or value == "True" or value == "true":
        return True
    return False


def change_paragraph_properties(old_properties: BaseProperties, tree: Tag) -> None:
    """
    Changes old properties indent, size, jc, spacing_before, spacing_after if they were found in tree.
    :param old_properties: Paragraph
    :param tree: BeautifulSoup tree with properties
    """
    change_indent(old_properties, tree)
    change_size(old_properties, tree)
    change_jc(old_properties, tree)
    change_spacing(old_properties, tree)


def change_run_properties(old_properties: BaseProperties, tree: Tag) -> None:
    """
    Changes old properties: bold, italic, underlined, size if they were found in tree.
    :param old_properties: Run
    :param tree: BeautifulSoup tree with properties
    """
    change_size(old_properties, tree)
    change_caps(old_properties, tree)

    if tree.b:
        b_tag = tree.b.get("w:val", True)
        old_properties.bold = check_if_true(b_tag) if isinstance(b_tag, str) else b_tag

    if tree.i:
        i_tag = tree.i.get("w:val", True)
        old_properties.italic = check_if_true(i_tag) if isinstance(i_tag, str) else i_tag

    if tree.u:
        u_tag = tree.u.get("w:val", False)
        if u_tag == "none":
            old_properties.underlined = False
        elif isinstance(u_tag, str):
            old_properties.underlined = True

    if tree.strike:
        strike_tag = tree.strike.get("w:val", True)
        old_properties.strike = check_if_true(strike_tag) if isinstance(strike_tag, str) else strike_tag

    if tree.vertAlign:
        sub_super_script = tree.vertAlign.attrs.get("w:val")
        if sub_super_script == "superscript":
            old_properties.superscript = True
        elif sub_super_script == "subscript":
            old_properties.subscript = True


def change_indent(old_properties: BaseProperties, tree: Tag) -> None:
    """
    Changes old properties: indentation if it was found in tree.
    Indentation is changed according to the following attributes in paragraph properties:
    - firstLine describes additional indentation to current indentation, if hanging is present firstLine is ignored
    - firstLineChars differs from firstLine only in measurement (one hundredths of a character unit)
    - hanging removes indentation from current indentation (analogous hangingChars)
    - start (startChars) describes classical indentation
    - left isn't specified in the documentation, F
    Main measurement 1/1440 of an inch: 1 inch is 12 char units, 1/100 char unit = 1/1200 inch = 1.2 * (1/1440 of an inch)

    :param old_properties: Paragraph
    :param tree: BeautifulSoup tree with properties
    """
    if not tree.ind:
        return

    attributes = {
        attribute: 0 for attribute in
        ["firstLine", "firstLineChars", "hanging", "hangingChars", "start", "startChars", "left"]
    }
    for attribute in attributes:
        attributes[attribute] = spacing_to_float(tree.ind.get(f"w:{attribute}", 0))

    indentation = 0
    if attributes["left"] != 0:
        indentation = attributes["left"]
    elif attributes["start"] != 0:
        indentation = attributes["start"]
    elif attributes["startChars"] != 0:
        indentation = attributes["startChars"] / 1.2

    if attributes["firstLine"] != 0 and attributes["hanging"] == 0:
        indentation += attributes["firstLine"]
    if attributes["firstLineChars"] != 0 and attributes["hangingChars"] == 0:
        indentation += attributes["firstLineChars"] / 1.2

    if attributes["hanging"] != 0:
        indentation -= attributes["hanging"]
    elif attributes["hangingChars"] != 0:
        indentation -= attributes["hangingChars"] / 1.2

    old_properties.indentation = indentation


def change_size(old_properties: BaseProperties, tree: Tag) -> None:
    """
    Changes old properties: size if it was found in tree.
    :param old_properties: Paragraph or Run
    :param tree: BeautifulSoup tree with properties
    """
    if tree.sz:
        new_size = spacing_to_float(tree.sz.get("w:val", old_properties.size))
        old_properties.size = int(new_size)


def change_jc(old_properties: BaseProperties, tree: Tag) -> None:
    """
    Changes old_properties: jc (alignment) if tag jc was found in tree.
    Alignment values: left, right, center, both, left is default.
    :param old_properties: Paragraph
    :param tree: BeautifulSoup tree with properties
    """
    if not tree.jc:
        return

    if tree.bidi:
        bidi_tag = tree.bidi.get("w:val", True)
        right_to_left = check_if_true(bidi_tag) if isinstance(bidi_tag, str) else bidi_tag
    else:
        right_to_left = False

    jc_tag = tree.jc.get("w:val", old_properties.jc)

    if jc_tag == "both":
        old_properties.jc = "both"
    elif jc_tag == "center":
        old_properties.jc = "center"
    elif jc_tag == "right":
        old_properties.jc = "right"
    elif jc_tag == "end" and not right_to_left:
        old_properties.jc = "right"
    elif jc_tag == "start" and right_to_left:
        old_properties.jc = "right"


def change_caps(old_properties: BaseProperties, tree: Tag) -> None:
    """
    Changes old_properties: caps if tag caps was found in tree.
    :param old_properties: Paragraph or Run
    :param tree: BeautifulSoup tree with properties
    """
    if not tree.caps:
        return

    caps_tag = tree.caps.get("w:val", True)
    old_properties.caps = check_if_true(caps_tag) if isinstance(caps_tag, str) else caps_tag


def change_spacing(old_properties: BaseProperties, tree: Tag) -> None:
    """
    Changes old_properties: spacing_before, spacing_after if tag spacing was found in tree.
    Spacing is changed according to the following attributes of tag <spacing>:
    - after / before (measured in twentieths of a point), ignored if afterLines or afterAutospacing are specified
    - afterAutospacing / beforeAutospacing (we set 0 if specified) if is specified, other attributes are ignored
    - afterLines / beforeLines (measured in one hundredths of a line)
    If we have spacing "after" for the previous paragraph and spacing "before" for the next paragraph, we choose maximum between these two values.

    :param old_properties: Paragraph
    :param tree: BeautifulSoup tree with properties
    """
    if not tree.spacing:
        return

    before, after = 0, 0
    before_autospacing = tree.spacing.get("w:beforeAutospacing", False)
    before_autospacing = check_if_true(before_autospacing) if before_autospacing else before_autospacing

    after_autospacing = tree.spacing.get("w:afterAutospacing", False)
    after_autospacing = check_if_true(after_autospacing) if after_autospacing else after_autospacing

    if not before_autospacing:
        before_lines = tree.spacing.get("w:beforeLines", False)
        before_lines = int(spacing_to_float(before_lines)) if before_lines else before_lines
        if not before_lines:
            before_tag = tree.spacing.get("w:before", False)
            before = int(spacing_to_float(before_tag)) if before_tag else before
        else:
            before = before_lines

    if not after_autospacing:
        after_lines = tree.spacing.get("w:afterLines", False)
        after_lines = int(spacing_to_float(after_lines)) if after_lines else after_lines
        if not after_lines:
            after_tag = tree.spacing.get("w:after", False)
            after = int(spacing_to_float(after_tag)) if after_tag else after
        else:
            after = after_lines

    old_properties.spacing_before = before
    old_properties.spacing_after = after


# region MODULE_CONTRACT [DOMAIN(8): DocumentProcessing; CONCEPT(7): Reader_properties_extractor; TECH(6): Python, dedoc]
## @modulecontract
## @purpose Read and parse DOCX documents, extracting lines with metadata, tables, and attachments into UnstructuredDocument.
## @scope Feature and metadata extraction from documents.
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
## FUNC [5][spacing_to_float utility/helper] => spacing_to_float
## FUNC [5][check_if_true utility/helper] => check_if_true
## FUNC [5][change_paragraph_properties utility/helper] => change_paragraph_properties
## FUNC [5][change_run_properties utility/helper] => change_run_properties
## FUNC [5][change_indent utility/helper] => change_indent
## FUNC [5][change_size utility/helper] => change_size
## FUNC [5][change_jc utility/helper] => change_jc
## FUNC [5][change_caps utility/helper] => change_caps
## FUNC [5][change_spacing utility/helper] => change_spacing
## @usecases
## - [read]: System (Pipeline) → ParseDocument(DOCX) → UnstructuredDocument
def _module_contract():
    pass
# endregion MODULE_CONTRACT
# GREP_SUMMARY: properties_extractor, dedoc, reader, DOCX, DocxReader, BaseReader, DOCX, Word, UnstructuredDocument, LineWithMeta, attachments, numbering, styles, properties, paragraph, footnote, spacing_to_float, check_if_true, change_paragraph_properties, change_run_properties, change_indent, change_size, change_jc, change_caps, change_spacing
# STRUCTURE: ▶ Input → ○ spacing_to_float → check_if_true → change_paragraph_properties → ⊕ result
