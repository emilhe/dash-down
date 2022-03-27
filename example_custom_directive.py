import plotly.express as px
from box import Box

from dash_extensions.enrich import DashProxy, dcc, DashBlueprint
from dash_down.directives import DashDirective
from dash_down.express import md_to_blueprint_dmc


class GraphDirective(DashDirective):

    def render_directive(self, value: str, text: str, options: Box[str, str], blueprint: DashBlueprint):
        df = getattr(px.data, options.dataset)()
        fig = px.scatter(df, x=options.x, y=options.y)
        return dcc.Graph(figure=fig)


blueprint = md_to_blueprint_dmc('resources/custom_directive.md', plugins=[GraphDirective()])

if __name__ == '__main__':
    DashProxy(blueprint=blueprint).run_server(port=7777)
