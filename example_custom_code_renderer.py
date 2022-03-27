import dash_mantine_components as dmc

from dash_extensions.enrich import DashProxy
from dash_down.directives import DashProxyDirective
from dash_down.express import md_to_blueprint_dmc
from dash_down.plugins import PluginBlueprint


def custom_layout(children):
    return dmc.MantineProvider(dmc.Group(children, direction="column", grow=True), withNormalizeCSS=True, withGlobalStyles=True)


def custom_code_renderer(source, layout):
    return dmc.Grid([
        dmc.Col(dmc.Prism("".join(source), language="python"), span=1),
        dmc.Col(layout, span=1),
    ], columns=2)


pb = PluginBlueprint(layout=custom_layout)
dpd = DashProxyDirective(custom_render=custom_code_renderer)
blueprint = md_to_blueprint_dmc('resources/custom_renderer.md', plugins=[pb, dpd])

if __name__ == '__main__':
    DashProxy(blueprint=blueprint).run_server()
