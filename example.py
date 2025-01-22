from dash import _dash_renderer
from dash_extensions.enrich import DashProxy

from dash_down.express import md_to_blueprint_html

_dash_renderer._set_react_version("18.2.0")
blueprint = md_to_blueprint_html("resources/test.md")
app = DashProxy(blueprint=blueprint)

if __name__ == "__main__":
    app.run_server(port=9657)
