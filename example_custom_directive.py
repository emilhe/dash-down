import plotly.express as px
from dash_extensions.enrich import DashBlueprint, DashProxy, dcc

from dash_down.express import md_to_blueprint_html


def graph(value: str, text: str, options: dict[str, str], blueprint: DashBlueprint):  # type: ignore
    """
    :param value: the directive value (optional)
    :param text: the markdown text (optional)
    :param options: a Box object containing all key value pairs (optional)
    :param blueprint: the DashBlueprint of the resulting Dash component tree, used e.g. for callback registration
    :return: a Dash component
    """
    df = getattr(px.data, options["dataset"])()
    fig = px.scatter(df, x=options["x"], y=options["y"])
    return dcc.Graph(figure=fig)


blueprint = md_to_blueprint_html("resources/custom_directive.md", directives=[graph])
app = DashProxy(blueprint=blueprint)

if __name__ == "__main__":
    app.run_server(port=7885)
