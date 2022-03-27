import plotly.express as px

from dash_extensions.enrich import DashProxy, dcc
from dash_down.directives import DashDirective
from dash_down.express import md_to_blueprint_dmc


class GraphDirective(DashDirective):

    def __init__(self):
        super().__init__("graph", render=self.render_graph)

    @staticmethod
    def render_graph(value, text, options, blueprint):
        df = getattr(px.data, options.dataset)()
        fig = px.scatter(df, x=options.x, y=options.y)
        return dcc.Graph(figure=fig)


blueprint = md_to_blueprint_dmc('resources/custom_directive.md', plugins=[GraphDirective()])

if __name__ == '__main__':
    DashProxy(blueprint=blueprint).run_server(port=7777)
