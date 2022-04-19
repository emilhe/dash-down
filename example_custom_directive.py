import plotly.express as px
from box import Box
from dash_extensions.enrich import DashProxy, dcc, DashBlueprint
from dash_down.express import md_to_blueprint_dmc


def graph(value: str, text: str, options: Box[str, str], blueprint: DashBlueprint):
    df = getattr(px.data, options.dataset)()
    fig = px.scatter(df, x=options.x, y=options.y)
    return dcc.Graph(figure=fig)


blueprint = md_to_blueprint_dmc('resources/custom_directive.md', directives=[graph])

if __name__ == '__main__':
    DashProxy(blueprint=blueprint).run_server(port=7885)
