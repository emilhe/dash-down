import dash_mantine_components as dmc
from dash_extensions.enrich import DashProxy

from dash_down.express import md_to_blueprint_dmc


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


blueprint = md_to_blueprint_dmc(
    "resources/custom_renderer.md",
    shell=blueprint_shell,
    dash_proxy_shell=dash_proxy_shell,
)
app = DashProxy()
app.layout = dmc.MantineProvider(blueprint.embed(app))

if __name__ == "__main__":
    app.run(port=7979)
