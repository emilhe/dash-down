from dash_extensions.enrich import DashBlueprint
from mistune import create_markdown
from dash_down.directives import ApiDocDirective
from dash_down.html_renderer import DashHtmlRenderer
from dash_down.mantine_renderer import DmcRenderer
from dash_down.plugins import PluginBlueprint


def _render_markdown(renderer, md_path, plugins=None):
    default_plugins = ['table', 'strikethrough', PluginBlueprint(), ApiDocDirective()]
    if plugins is not None:
        plugins = default_plugins + plugins
    markdown = create_markdown(renderer=renderer(), plugins=plugins)
    with open(md_path) as f:
        blueprint = markdown.parse(f.read())
    return blueprint


def md_to_blueprint_html(md_path: str, plugins=None) -> DashBlueprint:
    return _render_markdown(DashHtmlRenderer, md_path, plugins)


def md_to_blueprint_dmc(md_path: str, plugins=None) -> DashBlueprint:
    return _render_markdown(DmcRenderer, md_path, plugins)
