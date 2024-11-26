import dash_mantine_components as dmc
from dash_extensions.enrich import DashProxy
from dash_down.express import md_to_blueprint_dmc, GITHUB_MARKDOWN_CSS_LIGHT
from dash import _dash_renderer


def blueprint_shell(children):
    return dmc.Group(children, grow=True)


def dash_proxy_shell(source, layout, caption):
    return dmc.Grid(
        [
            dmc.GridCol(dmc.CodeHighlight("".join(source), language="python"), span=1),
            dmc.GridCol(layout, span=1),
            dmc.GridCol(dmc.Text(caption), span=2),
        ],
        columns=2,
    )


_dash_renderer._set_react_version("18.2.0")
blueprint = md_to_blueprint_dmc(
    "resources/custom_renderer.md",
    shell=blueprint_shell,
    dash_proxy_shell=dash_proxy_shell,
)
app = DashProxy(external_stylesheets=[GITHUB_MARKDOWN_CSS_LIGHT])
app.layout = dmc.MantineProvider(blueprint.embed(app))

if __name__ == "__main__":
    app.run_server(port=7979)
