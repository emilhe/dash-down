from dash_extensions.enrich import DashBlueprint
from mistletoe import Document
from dash_down.blocks import ApiDocBlock, DashProxyBlock
from dash_down.custom_block import bind_custom_blocks
from dash_down.mantine_renderer import DashMantineRenderer
from dash_down.html_renderer import DashHtmlRenderer


def _render_markdown(renderer, md_path: str, custom_blocks=None) -> DashBlueprint:
    custom_blocks = [ApiDocBlock(), DashProxyBlock()] if custom_blocks is None else custom_blocks
    with open(md_path, 'r') as f:
        with renderer() as r:
            bind_custom_blocks(r, custom_blocks=custom_blocks)
            blueprint = r.render(Document(f))
    return blueprint


def md_to_blueprint_html(md_path: str, custom_blocks=None) -> DashBlueprint:
    return _render_markdown(DashHtmlRenderer, md_path, custom_blocks)


def md_to_blueprint_dmc(md_path: str, custom_blocks=None) -> DashBlueprint:
    return _render_markdown(DashMantineRenderer, md_path, custom_blocks)
