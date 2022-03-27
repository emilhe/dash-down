from dash_extensions.enrich import DashBlueprint
from mistune import create_markdown
from dash_down.directives import ApiDocDirective, DashProxyDirective
from dash_down.html_renderer import DashHtmlRenderer
from dash_down.mantine_renderer import DmcRenderer
from dash_down.plugins import PluginBlueprint

_default_plugins_str = ['table', 'strikethrough']
_default_plugins_class = [PluginBlueprint(), ApiDocDirective(), DashProxyDirective()]
_default_plugins = _default_plugins_str + _default_plugins_class


def _resolve_plugins(plugins):
    if plugins is None:
        return _default_plugins
    all_plugins = list(_default_plugins)
    for plugin in plugins:
        # String plugins.
        if isinstance(plugin, str):
            if plugin not in _default_plugins_str:
                all_plugins.append(plugin)
            continue
        # Class-based plugins.
        try:
            class_names = [p.__class__.__name__ for p in all_plugins]
            match = class_names.index(plugin.__class__.__name__)
            all_plugins.pop(match)
        except ValueError:
            pass
        all_plugins.append(plugin)
    return all_plugins


def md_to_blueprint(renderer, md_path, plugins=None):
    """
    Render a markdown file into a DashBlueprint using the provided renderer class
    :param renderer: renderer class, e.g. DashHtmlRenderer
    :param md_path: path to markdown file
    :param plugins: extra plugins to load
    :return: DashBlueprint
    """
    markdown = create_markdown(renderer=renderer(), plugins=_resolve_plugins(plugins))
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
