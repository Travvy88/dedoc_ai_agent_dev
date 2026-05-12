# region MODULE_CONTRACT [DOMAIN(8): DocumentProcessing, HTMLRendering; CONCEPT(7): FormatConversion, JSON2Display; TECH(8): HTML, TreeTraversal]
## @modulecontract
## @purpose Convert parsed document structures (TreeNode, Table, ParsedDocument) from JSON/tree representation into display formats: HTML (tree, collapsed tree), plain text, and annotated HTML with tables/attachments.
## @scope Output format rendering — JSON → HTML/plain_text/tree conversion.
## @input TreeNode, List[Table], List[ParsedDocument], annotation data.
## @output HTML strings (tree, collapsed tree, annotated HTML), plain text.
## @links [USES_API(8): dedoc.api.schema (TreeNode, Table, LineMetadata, ParsedDocument); READS_DATA_FROM(7): dedoc.data_structures.concrete_annotations, dedoc.extensions]
## @invariants
## - json2html always returns valid HTML fragment.
## - All rendering functions are pure (no side effects on input data).
## @rationale
## Q: Why manual HTML generation instead of a template engine?
## A: The tree-to-HTML logic is algorithmic (depth-based indentation, annotation tag injection) — direct string construction is more efficient and self-contained than template rendering.
## @changes
## LAST_CHANGE: [v1.0.0 – Initial creation with semantic markup]
## @modulemap
## FUNC 7[Prettifies text with line wrapping at 60 chars] => __prettify_text
## FUNC 8[Recursively renders TreeNode as collapsible HTML details] => _node2tree
## FUNC 8[Wraps _node2tree result in full HTML document] => json2collapsed_tree
## FUNC 9[Renders TreeNode as flat HTML tree with vertical lines] => json2tree
## FUNC 4[Adds vertical line symbols for tree depth] => __add_vertical_line
## FUNC 10[Main conversion: TreeNode + Tables + Attachments → annotated HTML] => json2html
## FUNC 6[Maps annotation name+value to HTML tag] => __value2tag
## FUNC 9[Injects annotation HTML tags into text at character positions] => __annotations2html
## FUNC 7[Renders Table as HTML table element] => table2html
## FUNC 5[Recursively extracts plain text from TreeNode] => json2txt
## @usecases
## - [json2html]: ApiEndpoint => ConvertParsedResult => ReturnHTMLResponse
## - [json2txt]: ApiEndpoint => ConvertParsedResult => ReturnPlainTextResponse
def _module_contract():
    pass
# endregion MODULE_CONTRACT
# GREP_SUMMARY: HTML, rendering, tree, json2html, json2tree, json2txt, annotations, tables, attachments, format conversion, text prettify
# STRUCTURE: ▶ Input ┌TreeNode, Tables, Attachments┐ → ◇ json2html/json2tree/json2collapsed_tree/json2txt → ⊕ HTML/text → ⎋ output

import logging
from typing import Dict, Iterator, List, Optional, Set

from dedoc.api.schema import LineMetadata, ParsedDocument, Table, TreeNode
from dedoc.data_structures.concrete_annotations.attach_annotation import AttachAnnotation
from dedoc.data_structures.concrete_annotations.bold_annotation import BoldAnnotation
from dedoc.data_structures.concrete_annotations.italic_annotation import ItalicAnnotation
from dedoc.data_structures.concrete_annotations.reference_annotation import ReferenceAnnotation
from dedoc.data_structures.concrete_annotations.strike_annotation import StrikeAnnotation
from dedoc.data_structures.concrete_annotations.subscript_annotation import SubscriptAnnotation
from dedoc.data_structures.concrete_annotations.superscript_annotation import SuperscriptAnnotation
from dedoc.data_structures.concrete_annotations.table_annotation import TableAnnotation
from dedoc.data_structures.concrete_annotations.underlined_annotation import UnderlinedAnnotation
from dedoc.data_structures.hierarchy_level import HierarchyLevel
from dedoc.extensions import converted_mimes, recognized_mimes

logger = logging.getLogger(__name__)

# region FUNC___prettify_text [DOMAIN(6): TextProcessing; CONCEPT(5): LineWrapping; TECH(5): StringIteration]
## @purpose Wrap text into lines of approximately 60 characters for display, yielding chunks without breaking words.
## @io str -> Iterator[str]
## @complexity 4
def __prettify_text(text: str) -> Iterator[str]:
    res = []
    for word in text.split():
        if len(word) == 0:
            continue
        res.append(word)
        if sum(map(len, res)) >= 60:
            yield " ".join(res)
            res = []
    if len(res) > 0:
        yield " ".join(res)
# endregion FUNC___prettify_text

# region FUNC__node2tree [DOMAIN(7): HTMLRendering; CONCEPT(8): TreeToHTML, Recursive; TECH(7): HTML, Recursion]
## @purpose Recursively render a TreeNode as nested HTML `<details>` elements for an interactive collapsible tree view.
## @uses __prettify_text
## @io (TreeNode, int, Set[int]) -> str
## @complexity 7
def _node2tree(paragraph: TreeNode, depth: int, depths: Set[int] = None) -> str:
    if depths is None:
        depths = set()

    space_symbol = "&nbsp"
    space = [space_symbol] * 4 * (depth - 1) + 4 * ["-"]
    space = "".join(space)
    node_result = []

    node_result.append(f"  {space} {paragraph.metadata.paragraph_type}&nbsp{paragraph.node_id} ")
    for text in __prettify_text(paragraph.text):
        space = [space_symbol] * 4 * (depth - 1) + 4 * [space_symbol]
        space = "".join(space)
        node_result.append(f"<p>  {space} {text}  </p>")
    if len(paragraph.subparagraphs) > 0:
        sub_nodes = "\n".join([_node2tree(sub_node, depth=depth + 1, depths=depths.union({depth})) for sub_node in paragraph.subparagraphs])
        return f"""
        <details>
            <summary> <tt> {"".join(node_result)} </tt> </summary>
            {sub_nodes}
        </details>
        """
    else:
        return f"""
                <p>
                     {"".join(node_result)}
                </p>
                """
# endregion FUNC__node2tree

# region FUNC_json2collapsed_tree [DOMAIN(7): HTMLRendering; CONCEPT(8): CollapsibleTree, HTMLDocument; TECH(6): HTMLTemplate]
## @purpose Wrap the collapsible tree HTML from _node2tree in a full HTML document with charset and styling.
## @uses _node2tree
## @io TreeNode -> str
## @complexity 4
def json2collapsed_tree(paragraph: TreeNode) -> str:
    logger.debug(f"[IMP:4][json2collapsed_tree][INIT] Rendering collapsed tree for node_id={paragraph.node_id}")
    result = f"""
    <!DOCTYPE html>
    <html>
     <head>
      <meta charset="utf-8">
      <title>details</title>
     </head>
     <body>
     <tt>
      {_node2tree(paragraph, depth=0)}
      </tt>
     </body>
    </html>
    """
    return result
# endregion FUNC_json2collapsed_tree

# region FUNC_json2tree [DOMAIN(8): HTMLRendering; CONCEPT(8): FlatTree, BreadthFirst; TECH(7): StackTraversal, TreeSorting]
## @purpose Render a TreeNode as a flat indented HTML tree using stack-based traversal, node sorting by ID, and vertical line markers for hierarchy depth.
## @uses __prettify_text, __add_vertical_line
## @io TreeNode -> str
## @complexity 8
def json2tree(paragraph: TreeNode) -> str:
    logger.debug(f"[IMP:4][json2tree][INIT] Rendering flat tree for node_id={paragraph.node_id}")
    stack = [paragraph]
    nodes = []
    while len(stack) > 0:
        element = stack.pop()
        nodes.append(element)
        stack.extend(element.subparagraphs)
    nodes.sort(key=lambda node: tuple(map(int, node.node_id.split("."))))
    root, *nodes = nodes
    result = []
    space_symbol = "&nbsp"
    depths = set()
    for node in reversed(nodes):
        node_result = []
        depth = len(node.node_id.split(".")) - 1
        depths.add(depth)
        depths = {d for d in depths if d <= depth}
        space = [space_symbol] * 4 * (depth - 1) + 4 * ["-"]
        space = __add_vertical_line(depths, space)
        node_result.append(f"<p> <tt> <em>  {space} {node.metadata.paragraph_type}&nbsp{node.node_id} </em> </tt> </p>")
        for text in __prettify_text(node.text):
            space = [space_symbol] * 4 * (depth - 1) + 4 * [space_symbol]
            space = __add_vertical_line(depths, space)
            node_result.append(f"<p> <tt> {space} {text} </tt> </p>")
        result.extend(reversed(node_result))
    result.append(f"<h3>{root.text}</h3>")
    return "".join(reversed(result))
# endregion FUNC_json2tree

# region FUNC___add_vertical_line [DOMAIN(5): HTMLStyling; CONCEPT(4): TreeVisualization; TECH(4): ListMutation]
## @purpose Insert vertical line pipe characters at depth positions in the indentation space list for tree visualization.
## @io (Set[int], List[str]) -> str
## @complexity 3
def __add_vertical_line(depths: Set[int], space: List[str]) -> str:
    for d in depths:
        space[(d - 1) * 4] = "|"
    return "".join(space)
# endregion FUNC___add_vertical_line

# region FUNC_json2html [DOMAIN(9): HTMLRendering; CONCEPT(9): FullDocumentHTML, AnnotationInjection; TECH(8): RecursiveTraversal, HTMLGeneration]
## @purpose Main conversion function: recursively renders TreeNode with tables and attachments into a full annotated HTML document with page breaks, inline annotations, and external links.
## @uses __annotations2html, table2html, json2html (recursive)
## @io (str, TreeNode, Optional[List[Table]], Optional[List[ParsedDocument]], int, Dict, Dict, Optional[List[int]]) -> str
## @complexity 10
def json2html(text: str,
              paragraph: TreeNode,
              tables: Optional[List[Table]],
              attachments: Optional[List[ParsedDocument]],
              tabs: int = 0,
              table2id: Dict[str, int] = None,
              attach2id: Dict[str, int] = None,
              prev_page_id: Optional[List[int]] = None) -> str:
    if prev_page_id is None:
        prev_page_id = [0]

    tables = [] if tables is None else tables
    attachments = [] if attachments is None else attachments
    table2id = {table.metadata.uid: table_id for table_id, table in enumerate(tables)} if table2id is None else table2id
    attach2id = {attachment.metadata.uid: attachment_id for attachment_id, attachment in enumerate(attachments)} if attach2id is None else attach2id

    if paragraph.metadata.page_id != prev_page_id[0]:
        text += f"<center><small><b>Page {prev_page_id[0] + 1}</b></small></center><hr>"
        prev_page_id[0] = paragraph.metadata.page_id

    ptext = __annotations2html(paragraph=paragraph, table2id=table2id, attach2id=attach2id, tabs=tabs)

    if paragraph.metadata.paragraph_type in [HierarchyLevel.header, HierarchyLevel.root]:
        ptext = f"<strong>{ptext.strip()}</strong>"
    elif paragraph.metadata.paragraph_type == HierarchyLevel.list_item:
        ptext = f"<em>{ptext.strip()}</em>"
    else:
        ptext = ptext.strip()

    ptext = f'<p> {"&nbsp;" * tabs} {ptext}     <sub> id = {paragraph.node_id} ; type = {paragraph.metadata.paragraph_type} </sub></p>'
    if hasattr(paragraph.metadata, "uid"):
        ptext = f'<div id="{paragraph.metadata.uid}">{ptext}</div>'
    text += ptext

    for subparagraph in paragraph.subparagraphs:
        text = json2html(text=text, paragraph=subparagraph, tables=None, attachments=None, tabs=tabs + 4, table2id=table2id, attach2id=attach2id,
                         prev_page_id=prev_page_id)

    if tables is not None and len(tables) > 0:
        text += "<h3> Tables: </h3>"
        for table in tables:
            text += table2html(table, table2id)
            text += "<p>&nbsp;</p>"

    image_mimes = recognized_mimes.image_like_format.union(converted_mimes.image_like_format)

    if attachments is not None and len(attachments) > 0:
        text += "<h3> Attachments: </h3>"
        for attachment_id, attachment in enumerate(attachments):
            attachment_text = json2html(text="", paragraph=attachment.content.structure, tables=attachment.content.tables, attachments=attachment.attachments)
            attachment_base64 = f'data:{attachment.metadata.file_type};base64,{attachment.metadata.base64}"'
            attachment_link = f'<a href="{attachment_base64}" download="{attachment.metadata.file_name}">{attachment.metadata.file_name}</a>'
            is_image = attachment.metadata.file_type in image_mimes
            attachment_image = f'<img src="{attachment_base64}">' if is_image else ""

            text += f"""<div id="{attachment.metadata.uid}">
                <h4>attachment {attachment_id} ({attachment_link}):</h4>
                {attachment_image}
                {attachment_text}
            </div>"""

    return text
# endregion FUNC_json2html

# region FUNC___value2tag [DOMAIN(5): AnnotationMapping; CONCEPT(5): TagDispatch; TECH(4): StringMapping]
## @purpose Map annotation name and value to the corresponding HTML tag (e.g., BoldAnnotation → "b", heading → "h1"-"h6").
## @io (str, str) -> str
## @complexity 4
def __value2tag(name: str, value: str) -> str:
    if name == BoldAnnotation.name:
        return "b"

    if name == ItalicAnnotation.name:
        return "i"

    if name == StrikeAnnotation.name:
        return "strike"

    if name == SuperscriptAnnotation.name:
        return "sup"

    if name == SubscriptAnnotation.name:
        return "sub"

    if name == UnderlinedAnnotation.name:
        return "u"

    if name in (AttachAnnotation.name, TableAnnotation.name, ReferenceAnnotation.name):
        return "a"

    if value.startswith("heading "):
        level = value[len("heading "):]
        return "h" + level if level.isdigit() and int(level) < 7 else "strong"

    return value
# endregion FUNC___value2tag

# region FUNC___annotations2html [DOMAIN(8): AnnotationProcessing; CONCEPT(8): CharacterLevelTagInjection; TECH(7): IndexTracking, StringMutation]
## @purpose Inject HTML tags into paragraph text at annotation character positions (start/end), handling bool annotations, links, and table/attachment references.
## @uses __value2tag
## @io (TreeNode, Dict[str,int], Dict[str,int], int) -> str
## @complexity 9
def __annotations2html(paragraph: TreeNode, table2id: Dict[str, int], attach2id: Dict[str, int], tabs: int = 0) -> str:
    indexes = dict()

    for annotation in paragraph.annotations:
        name = annotation.name
        value = annotation.value

        bool_annotations = [
            BoldAnnotation.name, ItalicAnnotation.name, StrikeAnnotation.name, SubscriptAnnotation.name, SuperscriptAnnotation.name, UnderlinedAnnotation.name
        ]
        check_annotations = bool_annotations + [TableAnnotation.name, ReferenceAnnotation.name, AttachAnnotation.name]
        if name not in check_annotations and not value.startswith("heading "):
            continue
        elif name in bool_annotations and annotation.value == "False":
            continue

        tag = __value2tag(name, value)
        indexes.setdefault(annotation.start, "")
        indexes.setdefault(annotation.end, "")
        if name == TableAnnotation.name:
            indexes[annotation.end] += f' (<{tag} href="#{value}">table {table2id[value]}</{tag}>)'
        elif name == AttachAnnotation.name:
            indexes[annotation.end] += f' (<{tag} href="#{value}">attachment {attach2id[value]}</{tag}>)'
        elif name == ReferenceAnnotation.name:
            indexes[annotation.start] += f'<{tag} href="#{value}">'
            indexes[annotation.end] = f"</{tag}>" + indexes[annotation.end]
        else:
            indexes[annotation.start] += f"<{tag}>"
            indexes[annotation.end] = f"</{tag}>" + indexes[annotation.end]

    insert_tags = sorted([(index, tag) for index, tag in indexes.items()], reverse=True)
    text = paragraph.text

    for index, tag in insert_tags:
        text = text[:index] + tag + text[index:]

    return text.replace("\n", f'<br>{"&nbsp;" * tabs}')
# endregion FUNC___annotations2html

# region FUNC_table2html [DOMAIN(7): HTMLRendering; CONCEPT(7): TableToHTML; TECH(7): HTMLTable, CellRendering]
## @purpose Render a Table schema object as an HTML `<table>` element with border styling, merged cells (colspan/rowspan), and inline annotations.
## @uses __annotations2html
## @io (Table, Dict[str,int]) -> str
## @complexity 7
def table2html(table: Table, table2id: Dict[str, int]) -> str:
    logger.debug(f"[IMP:4][table2html][INIT] Rendering table uid={table.metadata.uid} with {len(table.cells)} rows")
    uid = table.metadata.uid
    table_title = f" {table.metadata.title}" if table.metadata.title else ""
    text = f"<h4> table {table2id[uid]}:{table_title}</h4>"
    text += f'<table border="1" id={uid} style="border-collapse: collapse; width: 100%;">\n<tbody>\n'
    for row in table.cells:
        text += "<tr>\n"
        for cell in row:
            text += "<td"
            if cell.invisible:
                text += ' style="display: none" '
            cell_node = TreeNode(
                node_id="0",
                text="\n".join([line.text for line in cell.lines]),
                annotations=cell.lines[0].annotations if cell.lines else [],
                metadata=LineMetadata(page_id=0, line_id=0, paragraph_type=HierarchyLevel.raw_text),
                subparagraphs=[]
            )
            text += f' colspan="{cell.colspan}" rowspan="{cell.rowspan}">{__annotations2html(cell_node, {}, {})}</td>\n'

        text += "</tr>\n"
    text += "</tbody>\n</table>"
    return text
# endregion FUNC_table2html

# region FUNC_json2txt [DOMAIN(5): TextExtraction; CONCEPT(5): TreeToText; TECH(4): RecursiveStringJoin]
## @purpose Recursively extract plain text content from a TreeNode, joining paragraph text with subparagraph text via newlines.
## @io TreeNode -> str
## @complexity 3
def json2txt(paragraph: TreeNode) -> str:
    subparagraphs_text = "\n".join([json2txt(subparagraph) for subparagraph in paragraph.subparagraphs])
    text = f"{paragraph.text}\n{subparagraphs_text}"
    return text
# endregion FUNC_json2txt
