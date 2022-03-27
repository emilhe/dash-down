from dash_extensions.enrich import DashBlueprint
from mistune import create_markdown
from dash_down.directives import ApiDocDirective, DashProxyDirective
from dash_down.html_renderer import DashHtmlRenderer
from dash_down.mantine_renderer import DmcRenderer
from dash_down.plugins import PluginBlueprint


def md_to_blueprint(renderer, md_path, plugins=None):
    """
    Render a markdown file into a DashBlueprint using the provided renderer class
    :param renderer: renderer class, e.g. DashHtmlRenderer
    :param md_path: path to markdown file
    :param plugins: extra plugins to load
    :return: DashBlueprint
    """
    all_plugins = ['table', 'strikethrough', PluginBlueprint(), ApiDocDirective(), DashProxyDirective()]
    if plugins is not None:
        all_plugins = all_plugins + plugins
    markdown = create_markdown(renderer=renderer(), plugins=all_plugins)
    with open(md_path) as f:
        blueprint = markdown.parse(f.read())
    return blueprint


def md_to_blueprint_html(md_path: str, plugins=None) -> DashBlueprint:
    """
    Render a markdown file into a DashBlueprint using html components.
    :param md_path: path to markdown file
    :param plugins: extra plugins to load
    :return: DashBlueprint
    """
    return md_to_blueprint(DashHtmlRenderer, md_path, plugins)


def md_to_blueprint_dmc(md_path: str, plugins=None) -> DashBlueprint:
    """
    Render a markdown file into a DashBlueprint using dmc components.
    :param md_path: path to markdown file
    :param plugins: extra plugins to load
    :return: DashBlueprint
    """
    return md_to_blueprint(DmcRenderer, md_path, plugins)
