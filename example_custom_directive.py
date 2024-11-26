import plotly.express as px
from box import Box
from dash_extensions.enrich import DashProxy, dcc, DashBlueprint
from dash_down.express import GITHUB_MARKDOWN_CSS_LIGHT, md_to_blueprint_html


def graph(value: str, text: str, options: Box[str, str], blueprint: DashBlueprint):  # type: ignore
    """
    :param value: the directive value (optional)
    :param text: the markdown text (optional)
    :param options: a Box object containing all key value pairs (optional)
    :param blueprint: the DashBlueprint of the resulting Dash component tree, used e.g. for callback registration
    :return: a Dash component
    """
    df = getattr(px.data, options.dataset)()
    fig = px.scatter(df, x=options.x, y=options.y)
    return dcc.Graph(figure=fig)


blueprint = md_to_blueprint_html("resources/custom_directive.md", directives=[graph])
app = DashProxy(blueprint=blueprint, external_stylesheets=[GITHUB_MARKDOWN_CSS_LIGHT])

if __name__ == "__main__":
    app.run_server(port=7885)
