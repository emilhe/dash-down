import dash_mantine_components as dmc

from itertools import chain
from mistletoe.block_token import HTMLBlock
from dash_down.html_renderer import DashHtmlRenderer


class DashMantineRenderer(DashHtmlRenderer):
    """
    Render markdown into Dash Mantine components.
    """

    def __init__(self, *extras):
        super().__init__(*chain([HTMLBlock], extras))
        self._suppress_ptag_stack = [False]
        self.blueprint = None

    # # TODO: Change to dmc.Code
    # def render_inline_code(self, token):
    #     return html.Code(self.render_inner(token))

    def render_image(self, token):
        return dmc.Image(src=token.src, alt=self.render_to_plain(token), caption=token.title)

    def render_heading(self, token):
        inner = self.render_inner(token)
        return dmc.Title(inner, order=token.level)

    def render_quote(self, token):
        self._suppress_ptag_stack.append(False)
        inner = [self.render(child) for child in token.children]
        self._suppress_ptag_stack.pop()
        return dmc.Blockquote(inner)

    def render_paragraph(self, token):
        if self._suppress_ptag_stack[-1]:
            return '{}'.format(self.render_inner(token))
        return dmc.Text(self.render_inner(token))

    @staticmethod
    def render_block_code(token):
        inner = token.children[0].content
        return dmc.Prism(inner, language=token.language if token.language else "markup")
