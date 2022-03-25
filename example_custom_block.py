import plotly.express as px

from dash_extensions.enrich import DashProxy, dcc
from dash_down.custom_block import CustomBlock
from dash_down.express import md_to_blueprint_dmc


class GraphBlock(CustomBlock):
    def render(self, renderer, dataset_name, x, y):
        df = getattr(px.data, dataset_name)()
        fig = px.scatter(df, x=x, y=y)
        return dcc.Graph(figure=fig)


blueprint = md_to_blueprint_dmc('resources/custom.md', custom_blocks=[GraphBlock()])

if __name__ == '__main__':
    app = DashProxy(blueprint=blueprint)
    app.run_server(port=9999)
