import dash_mantine_components as dmc
from dash_extensions.enrich import DashProxy
from dash_down.express import md_to_blueprint_dmc, GITHUB_MARKDOWN_CSS_LIGHT


def blueprint_shell(children):
    return dmc.MantineProvider(dmc.Group(children, direction="column", grow=True),
                               withNormalizeCSS=True, withGlobalStyles=True)


def dash_proxy_shell(source, layout, caption):
    return dmc.Grid([
        dmc.Col(dmc.Prism("".join(source), language="python"), span=1),
        dmc.Col(layout, span=1),
        dmc.Col(dmc.Text(caption), span=2),
    ], columns=2)


blueprint = md_to_blueprint_dmc('resources/custom_renderer.md',
                                shell=blueprint_shell,
                                dash_proxy_shell=dash_proxy_shell)
app = DashProxy(blueprint=blueprint, external_stylesheets=[GITHUB_MARKDOWN_CSS_LIGHT])

if __name__ == '__main__':
    app.run_server(port=7979)
