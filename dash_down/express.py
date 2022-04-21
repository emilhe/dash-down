from dash_extensions.enrich import DashBlueprint
from mistune import create_markdown
from dash_down.directives import ApiDocDirective, DashProxyDirective, FunctionDirective
from dash_down.html_renderer import DashHtmlRenderer
from dash_down.mantine_renderer import DmcRenderer
from dash_down.plugins import PluginBlueprint
from dash_down import GITHUB_MARKDOWN_CSS, GITHUB_MARKDOWN_CSS_DARK, GITHUB_MARKDOWN_CSS_LIGHT

_default_plugins_str = ['table', 'strikethrough']


def _default_plugins_class(shell, api_doc_shell, dash_proxy_shell):
    return [PluginBlueprint(shell=shell), ApiDocDirective(api_doc_shell), DashProxyDirective(shell=dash_proxy_shell)]


def _default_plugins(shell, api_doc_shell, dash_proxy_shell):
    return _default_plugins_str + _default_plugins_class(shell, api_doc_shell, dash_proxy_shell)


def _resolve_plugins(plugins, directives=None, shell=None, api_doc_shell=None, dash_proxy_shell=None):
    if directives is not None:
        d_plugins = [FunctionDirective(d) for d in directives]
        plugins = d_plugins if plugins is None else plugins + d_plugins
    if plugins is None:
        return _default_plugins(shell, api_doc_shell, dash_proxy_shell)
    all_plugins = list(_default_plugins(shell, api_doc_shell, dash_proxy_shell))
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


def md_to_blueprint(renderer, md_path, plugins=None, directives=None, shell=None, api_doc_shell=None, dash_proxy_shell=None):
    """
    Render a markdown file into a DashBlueprint using the provided renderer class
    :param renderer: renderer class, e.g. DashHtmlRenderer
    :param md_path: path to markdown file
    :param plugins: extra plugins to load
    :param shell: shell for the blueprint layout rendering
    :param api_doc_shell: shell for rendering of api doc directives
    :param dash_proxy_shell: shell for rendering of dash proxy directives
    :return: DashBlueprint
    """
    plugins = _resolve_plugins(plugins, directives, shell, api_doc_shell, dash_proxy_shell)
    markdown = create_markdown(renderer=renderer(), plugins=plugins)
    with open(md_path) as f:
        blueprint = markdown.parse(f.read())
    return blueprint


def md_to_blueprint_html(md_path: str, plugins=None, directives=None, shell=None, api_doc_shell=None, dash_proxy_shell=None) -> DashBlueprint:
    """
    Render a markdown file into a DashBlueprint using html components.
    :param md_path: path to markdown file
    :param plugins: extra plugins to load
    :param shell: shell for the blueprint layout rendering
    :param api_doc_shell: shell for rendering of api doc directives
    :param dash_proxy_shell: shell for rendering of dash proxy directives
    """
    return md_to_blueprint(DashHtmlRenderer, md_path, plugins, directives, shell, api_doc_shell, dash_proxy_shell)


def md_to_blueprint_dmc(md_path: str, plugins=None, directives=None, shell=None, api_doc_shell=None, dash_proxy_shell=None) -> DashBlueprint:
    """
    Render a markdown file into a DashBlueprint using dmc components.
    :param md_path: path to markdown file
    :param plugins: extra plugins to load
    :param shell: shell for the blueprint layout rendering
    :param api_doc_shell: shell for rendering of api doc directives
    :param dash_proxy_shell: shell for rendering of dash proxy directives
    :return: DashBlueprint
    """
    return md_to_blueprint(DmcRenderer, md_path, plugins, directives, shell, api_doc_shell, dash_proxy_shell)
