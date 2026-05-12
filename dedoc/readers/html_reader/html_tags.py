# region CLASS_HtmlTags [DOMAIN(7): DocumentProcessing; CONCEPT(8): HTMLTags, HtmlParsing; TECH(6): Python, BeautifulSoup]
## @purpose Define canonical HTML tag categories (block, inline, list, table, styled) for use by the HTML reader pipeline — serves as a lookup dictionary for tag classification.
## @uses None (pure data class with no external dependencies)
## @complexity 2
class HtmlTags:
    service_tags = ["script", "style"]

    list_items = ["li", "dd", "dt"]
    block_tags = ["aside", "article", "body", "div", "blockquote", "footer", "header", "html", "main", "nav", "section", "form", *list_items]
    unordered_list = ["ul", "dl", "dir"]
    ordered_list = ["ol"]
    list_tags = unordered_list + ordered_list
    header_tags = ["h1", "h2", "h3", "h4", "h5", "h6"]

    strike_tags = ["del", "strike", "s"]
    bold_tags = ["strong", "b"]
    underlined_tags = ["ins", "u"]
    italic_tags = ["em", "i", "dfn", "var", "address"]
    subscript_tags = ["sub"]
    superscript_tags = ["sup"]
    link_tags = ["a"]

    paragraphs = ["p"] + block_tags + list_items + header_tags

    styled_tag = bold_tags + italic_tags + underlined_tags + strike_tags + superscript_tags + subscript_tags
    simple_text_tags = [
        "a", "abbr", "acronym", "applet", "area", "article", "aside", "bdi", "bdo", "big", "canvas", "caption", "center", "cite", "code", "data",
        "font", "kbd", "mark", "output", "p", "pre", "q", "samp", "small", "span", "tt", "wbr"
    ]
    text_tags = simple_text_tags + styled_tag

    table_tags = ["table"]
    table_rows = ["tr"]
    table_cells = ["td", "th"]

    special_symbol_tags = {"br": "\n"}
    available_tags = block_tags + list_tags + header_tags + text_tags + list(special_symbol_tags.keys()) + paragraphs
    available_tags = sorted(set(available_tags))
# endregion CLASS_HtmlTags

# region MODULE_CONTRACT [DOMAIN(7): DocumentProcessing; CONCEPT(8): HTMLTags; TECH(6): Python]
## @modulecontract
## @purpose Define canonical HTML tag categories (block, inline, list, table, styled, text) as a lookup dictionary for the HTML reader pipeline.
## @scope HTML tag classification — semantic role assignment for each HTML tag.
## @input None (pure data class evaluated at import time).
## @output Module-level class_html_tags with categorized tag name sets.
## @links [USES_API(8): dedoc.readers.html_reader]
## @invariants
## - available_tags ALWAYS contains sorted unique tag names.
## @rationale
## Q: Why a class with class-level constants instead of a plain dict?
## A: Class-level constants provide autocomplete-friendly, namespaced access for IDE and grep navigation.
## @changes
## LAST_CHANGE: [v1.0.0 – Added SEMANTIC TEMPLATE markup.]
## @modulemap
## CLASS [10][HTML tag semantic categories] => HtmlTags
## @usecases
## - [HtmlTags]: HtmlReader (Parse) → LookupTagCategory(tag_name) → SemanticRole
def _module_contract():
    pass
# endregion MODULE_CONTRACT
# GREP_SUMMARY: html_tags, HtmlTags, HTML, tag_categories, block_tags, inline_tags, list_tags, table_tags, styled_tags, text_tags, dedoc, reader
# STRUCTURE: ▶ HtmlTags ∋ {service, block, list, header, styled, table, text, symbol, special} → ○ available_tags = ∪ all → ⊕ sorted set
