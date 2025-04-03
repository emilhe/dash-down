from dash_down.express import _resolve_plugins, md_to_blueprint_dmc, md_to_blueprint_html

# TODO: Maybe add UI validation, e.g. using Percy
from dash_down.plugins import PluginBlueprint


def test_render_markdown_html():
    blueprint = md_to_blueprint_html("resources/test.md", plugins=[])


# TODO: Maybe add UI validation, e.g. using Percy
def test_render_markdown_dmc():
    blueprint = md_to_blueprint_dmc("resources/test.md")


def test_resolve_plugins():
    class DummyPlugin:
        def dummy(self):
            return None

    plugins = _resolve_plugins(None)
    assert len(plugins) == 5
    plugins = _resolve_plugins(["awesome_plugin"])
    assert len(plugins) == 6
    plugins = _resolve_plugins(["table"])
    assert len(plugins) == 5
    plugins = _resolve_plugins([PluginBlueprint()])
    assert len(plugins) == 5
    plugins = _resolve_plugins([DummyPlugin()])
    assert len(plugins) == 6
