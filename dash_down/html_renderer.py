from itertools import chain
from dash_extensions import Purify
from dash_extensions.enrich import DashBlueprint, html
from mistletoe import BaseRenderer
from mistletoe.block_token import HTMLBlock


class DashHtmlRenderer(BaseRenderer):
    """
    Render markdown into Dash HTML components.
    """

    def __init__(self, *extras):
        super().__init__(*chain([HTMLBlock], extras))
        self._suppress_ptag_stack = [False]
        self.h_level_mapping = {
            1: html.H1,
            2: html.H2,
            3: html.H3,
            4: html.H4,
            5: html.H5,
            6: html.H6
        }
        self.blueprint = None

    def render_strong(self, token):
        return html.Strong(self.render_inner(token))

    def render_emphasis(self, token):
        return html.Em(self.render_inner(token))

    def render_inline_code(self, token):
        return html.Code(self.render_inner(token))

    def render_strikethrough(self, token):
        return html.Strike(self.render_inner(token))

    def render_image(self, token):
        if token.title:
            title = ' title="{}"'.format(token.title)
        else:
            title = ''
        return html.Img(src=token.src, alt=self.render_to_plain(token), title=title)

    def render_link(self, token):
        if token.title:
            title = ' title="{}"'.format(token.title)
        else:
            title = ''
        inner = self.render_inner(token)
        return html.A(children=inner, title=title, href=token.target)

    def render_escape_sequence(self, token):
        return self.render_inner(token)

    def render_raw_text(self, token):
        return token.content

    def render_heading(self, token):
        inner = self.render_inner(token)
        return self.h_level_mapping[token.level](inner)

    def render_quote(self, token):
        self._suppress_ptag_stack.append(False)
        inner = [self.render(child) for child in token.children]
        self._suppress_ptag_stack.pop()
        return html.Blockquote(inner)

    def render_paragraph(self, token):
        if self._suppress_ptag_stack[-1]:
            return '{}'.format(self.render_inner(token))
        return html.P(self.render_inner(token))

    @staticmethod
    def render_block_code(token):
        if token.language:
            class_name = 'language-{}'.format(token.language)
        else:
            class_name = ''
        inner = token.children[0].content
        return html.Pre(html.Code(inner, className=class_name))

    def render_list(self, token):
        self._suppress_ptag_stack.append(not token.loose)
        children = [self.render(child) for child in token.children]
        self._suppress_ptag_stack.pop()
        if token.start is None:
            return html.Ul(children)
        return html.Ol(children, start=token.start if token.start != 1 else '')

    def render_list_item(self, token):
        return html.Li([self.render(child) for child in token.children])

    @staticmethod
    def render_thematic_break(token):
        return html.Hr()

    @staticmethod
    def render_line_break(token):
        return html.Br()

    @staticmethod
    def render_html_block(token):
        return Purify(token.content)

    def render_inner(self, token):
        inner = list(map(self.render, token.children))
        # Unwrap one-element lists.
        if isinstance(inner, list) and len(inner) == 1:
            return inner[0]
        # Wrap children in a div.
        return html.Div(inner)

    def render_document(self, token):
        self.blueprint = DashBlueprint()
        self.blueprint.layout = self.render_inner(token)
        return self.blueprint
