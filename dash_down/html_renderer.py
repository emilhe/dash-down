from dash_extensions import Purify
from dash_extensions.enrich import DashBlueprint, html
from mistune import AstRenderer

from dash_down.class_names import class_name


class DashHtmlRenderer(AstRenderer):
    """
    Render markdown into Dash HTML components.
    """

    def __init__(self, add_header_anchors=True):
        super().__init__()
        self.h_level_mapping = {
            1: html.H1,
            2: html.H2,
            3: html.H3,
            4: html.H4,
            5: html.H5,
            6: html.H6,
        }
        self.add_header_anchors = add_header_anchors
        self.blueprint = DashBlueprint()

    def text(self, text):
        return text

    @class_name
    def link(self, link, children=None, title=None):
        return html.A(children, title=title, href=link)

    @class_name
    def image(self, src, alt="", title=None):
        return html.Img(src=src, alt=alt, title=title)

    @class_name
    def emphasis(self, text):
        return html.Em(text)

    @class_name
    def strong(self, text):
        return html.Strong(text)

    @class_name
    def codespan(self, text):
        return html.Code(text)

    @class_name
    def linebreak(self):
        return html.Br()

    @class_name
    def paragraph(self, text):
        return html.P(text)

    @class_name
    def heading(self, children, level):
        return self.h_level_mapping[level](self.header_anchor(children))

    def newline(self):
        return ""

    @class_name
    def thematic_break(self):
        return html.Hr()

    def block_text(self, text):
        return text

    @class_name
    def block_code(self, children, info=None):
        class_name = None
        if info is not None:
            info = info.strip()
        if info:
            lang = info.split(None, 1)[0]
            class_name = f"language-{lang}"
        return html.Pre(html.Code(children, className=class_name))

    @class_name
    def block_quote(self, text):
        return html.Blockquote(text)

    @class_name
    def block_html(self, children):
        return Purify(children)

    @class_name
    def list(self, children, ordered, level, start=None):
        if not ordered:
            return html.Ul(children)
        return html.Ol(children, start=start)

    @class_name
    def list_item(self, text, level):
        return html.Li(text)

    def finalize(self, data):
        lst = list(data)
        if len(lst) == 1:
            return lst[0]
        return lst

    # strikethrough plugin

    @class_name
    def strikethrough(self, text):
        return html.Strike(text)

    # table plugin

    @class_name
    def table(self, text):
        return html.Table(text)

    @class_name
    def table_head(self, text):
        return html.Thead(html.Tr(text))

    @class_name
    def table_body(self, text):
        return html.Tbody(text)

    @class_name
    def table_row(self, text):
        return html.Tr(text)

    @class_name
    def table_cell(self, text, align=None, is_head=False):
        style = None
        if align:
            style = {"text-align": align}
        return html.Th(text, style=style) if is_head else html.Td(text, style=style)

    # custom stuff

    def header_anchor(self, children):
        if not self.add_header_anchors:
            return children
        string = str(children).lower()
        anchor = "".join(
            e if e.isalnum() else "" if i in [0, len(string) - 1] else "-"
            for i, e in enumerate(string)
        )
        anchor = f"a-{anchor}"  # add anchor prefix
        icon = html.Span(className="octicon octicon-link")
        return [
            html.A(className="anchor", href=f"#{anchor}", id=anchor, children=icon),
            children,
        ]
