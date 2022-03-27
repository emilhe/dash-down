from dash_extensions import Purify
from dash_extensions.enrich import DashBlueprint, html
from mistune import AstRenderer


class DashHtmlRenderer(AstRenderer):
    """
    Render markdown into Dash HTML components.
    """

    def __init__(self):
        super().__init__()
        self.h_level_mapping = {
            1: html.H1,
            2: html.H2,
            3: html.H3,
            4: html.H4,
            5: html.H5,
            6: html.H6
        }
        self.blueprint = DashBlueprint()

    def text(self, text):
        return text

    def link(self, link, children=None, title=None):
        return html.A(children, title=title, href=link)

    def image(self, src, alt="", title=None):
        return html.Img(src=src, alt=alt, title=title)

    def emphasis(self, text):
        return html.Em(text)

    def strong(self, text):
        return html.Strong(text)

    def codespan(self, text):
        return html.Code(text)

    def linebreak(self):
        return html.Br()

    def paragraph(self, text):
        return html.P(text)

    def heading(self, children, level):
        return self.h_level_mapping[level](children)

    def newline(self):
        return ''

    def thematic_break(self):
        return html.Hr()

    def block_text(self, text):
        return text

    def block_code(self, children, info=None):
        class_name = None
        if info is not None:
            info = info.strip()
        if info:
            lang = info.split(None, 1)[0]
            class_name = f"language-{lang}"
        return html.Pre(html.Code(children, className=class_name))

    def block_quote(self, text):
        return html.Blockquote(text)

    def block_html(self, children):
        return Purify(children)

    def list(self, children, ordered, level, start=None):
        if not ordered:
            return html.Ul(children)
        return html.Ol(children, start=start)

    def list_item(self, text, level):
        return html.Li(text)

    def finalize(self, data):
        lst = list(data)
        if len(lst) == 1:
            return lst[0]
        return lst

    # strikethrough plugin

    def strikethrough(self, text):
        return html.Strike(text)

    # table plugin

    def table(self, text):
        return html.Table(text)

    def table_head(self, text):
        return html.Thead(html.Tr(text))

    def table_body(self, text):
        return html.Tbody(text)

    def table_row(self, text):
        return html.Tr(text)

    def table_cell(self, text, align=None, is_head=False):
        style = None
        if align:
            style = {"text-align": align}
        return html.Th(text, style=style) if is_head else html.Td(text, style=style)