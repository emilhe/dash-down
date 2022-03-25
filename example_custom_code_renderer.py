import dash_mantine_components as dmc

from dash_extensions.enrich import DashProxy
from dash_down.blocks import DashProxyBlock
from dash_down.express import md_to_blueprint_dmc


def code_renderer(renderer, source, layout):
    return dmc.Grid([
        dmc.Col(dmc.Prism("".join(source), language="python"), span=1),
        dmc.Col(layout, span=1),
    ], columns=2)


blueprint = md_to_blueprint_dmc('resources/custom_code_renderer.md',
                                custom_blocks=[DashProxyBlock(code_renderer)])

if __name__ == '__main__':
    DashProxy(blueprint=blueprint).run_server(port=9999)
