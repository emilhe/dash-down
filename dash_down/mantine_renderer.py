import dash_mantine_components as dmc

from dash_down.class_names import class_name
from dash_down.html_renderer import DashHtmlRenderer


class DmcRenderer(DashHtmlRenderer):
    """
    Render markdown into Dash Mantine components.
    """

    def __init__(self, add_header_anchors=True):
        super().__init__(add_header_anchors)

    # Basic

    @class_name
    def link(self, link, children=None, title=None):
        return dmc.Anchor(children, href=link)

    @class_name
    def heading(self, children, level):
        return dmc.Title(super().header_anchor(children), order=level)

    @class_name
    def paragraph(self, text):
        return dmc.Text(text)

    @class_name
    def image(self, src, alt="", title=None):
        # TODO: Review render (!)
        return dmc.Stack([dmc.Image(src=src, alt=alt), dmc.Text(title)])

    @class_name
    def thematic_break(self):
        return dmc.Divider()

    # Block

    @class_name
    def block_code(self, children, info=None):
        lang = None
        if info is not None:
            info = info.strip()
        if info:
            lang = info.split(None, 1)[0]
        return dmc.CodeHighlight(children, language=lang)

    @class_name
    def block_quote(self, text):
        return dmc.Blockquote(text)

    # List

    @class_name
    def list(self, children, ordered, level, start=None):
        return dmc.List(children, type="ordered" if ordered else "unordered")

    @class_name
    def list_item(self, text, level):
        return dmc.ListItem(text)

    # Formatting

    @class_name
    def codespan(self, text):
        return dmc.Code(text)

    @class_name
    def strong(self, text):
        return dmc.Text(text, fw=700, display="inline")

    @class_name
    def emphasis(self, text):
        return dmc.Text(text, fs="italic", display="inline")

    @class_name
    def strikethrough(self, text):
        return dmc.Text(text, td="line-through", display="inline")

    # Table

    @class_name
    def table(self, text):
        return dmc.Table(text, striped=True, highlightOnHover=True)

    @class_name
    def table_head(self, text):
        return dmc.TableThead(self.table_row(text))

    @class_name
    def table_body(self, text):
        return dmc.TableTbody(text)

    @class_name
    def table_row(self, text: str):
        return dmc.TableTr(text)

    @class_name
    def table_cell(self, text: str, align=None, head=False):
        return dmc.TableTh(text) if head else dmc.TableTd(text)
