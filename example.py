from dash_extensions.enrich import DashProxy
from dash_down.express import md_to_blueprint_dmc

blueprint = md_to_blueprint_dmc('resources/test.md')

if __name__ == '__main__':
    DashProxy(blueprint=blueprint).run_server(port=9657)