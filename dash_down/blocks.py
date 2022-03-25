import importlib
from typing import List

import mistletoe

from dash_extensions.enrich import DashProxy, DashBlueprint, PrefixIdTransform
from mistletoe import BaseRenderer
from dash import html
from mistletoe.block_token import BlockCode
from dash_down.custom_block import CustomBlock

""""
This module holds examples of custom block defnitions. Use them as you please, either as-they-are or as inspiration.
"""


class ApiDocBlock(CustomBlock):
    """
    Block used to automate api documentation generation.
    """

    def render(self, renderer: BaseRenderer, inner: str):
        # Parse api doc.
        module_name, component_name = ".".join(inner.split(".")[:-1]), inner.split(".")[-1]
        module = importlib.import_module(module_name)
        component = getattr(module, component_name)
        component_doc = component.__doc__
        docs = component_doc.split("Keyword arguments:")[-1]
        docs = docs.lstrip("\n\n")
        # Create tokens.
        heading_token = mistletoe.block_token.Heading((0, "Keyword Arguments"))
        heading_token.level = 5
        code_token = mistletoe.block_token.BlockCode(docs)
        code_token.language = "git"
        return html.Div([
            renderer.render_heading(heading_token),
            renderer.render_block_code(code_token)
        ])


class DashProxyBlock(CustomBlock):
    """
    Block used to render Dash apps.
    """

    def __init__(self, renderer = None, code_transform = None, hide_tag="no-show"):
        self.renderer = self._default_renderer if renderer is None else renderer
        self.code_transform = self._default_code_transform if code_transform is None else code_transform
        self.hide_tag = hide_tag

    @staticmethod
    def _default_renderer(renderer: BaseRenderer, code, layout):
        token = BlockCode(code)
        token.language = "python"
        return html.Div([
            renderer.render_block_code(token),
            layout
        ])

    def _default_code_transform(self, source: List[str]):
        return [line for line in source if self.hide_tag not in line]

    def render(self, renderer: BaseRenderer, module_name, app_name="app"):
        # Get the app.
        module = importlib.import_module(module_name)
        app: DashProxy = getattr(module, app_name)
        # Add prefix.
        prefix = module_name.replace(".", "_")
        prefix_transform = PrefixIdTransform(prefix)  # TODO: Maybe do some escaping?
        app.blueprint.transforms.append(prefix_transform)
        # Register on blueprint.
        blueprint: DashBlueprint = renderer.blueprint
        app.blueprint.register_callbacks(blueprint)
        # Extract values for rendering.
        layout = app._layout_value()
        with open(f"{module_name.replace('.', '/')}.py", 'r') as f:
            source = self._default_code_transform(f.readlines())
        return self.renderer(renderer, source, layout)
