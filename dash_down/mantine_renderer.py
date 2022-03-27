import dash_mantine_components as dmc
from dash_down.html_renderer import DashHtmlRenderer


class DmcRenderer(DashHtmlRenderer):
    """
    Render markdown into Dash Mantine components.
    """

    def text(self, text):
        return text

    def paragraph(self, text):
        return dmc.Text(text)

    def link(self, link, children=None, title=None):
        return dmc.Anchor(children, href=link)

    def image(self, src, alt="", title=None):
        return dmc.Image(src=src, alt=alt, caption=title)

    def heading(self, children, level):
        return dmc.Title(children, order=level)

    def thematic_break(self):
        return dmc.Divider()

    def block_text(self, text):
        return dmc.Text(text)

    def block_code(self, children, info=None):
        lang = None
        if info is not None:
            info = info.strip()
        if info:
            lang = info.split(None, 1)[0]
        return dmc.Prism(children, language=lang)

    def block_quote(self, text):
        return dmc.Blockquote(text)

    def table(self, text):
        return dmc.Table(text, striped=True, highlightOnHover=True)