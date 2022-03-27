from dash_extensions.enrich import DashProxy
from dash_down.express import md_to_blueprint_dmc

blueprint = md_to_blueprint_dmc('resources/test0.md')

if __name__ == '__main__':
    app = DashProxy(blueprint=blueprint)
    app.run_server(port=9998)
