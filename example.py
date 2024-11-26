from dash_extensions.enrich import DashProxy
from dash_down.express import md_to_blueprint_html, GITHUB_MARKDOWN_CSS_LIGHT

blueprint = md_to_blueprint_html("resources/test.md")
app = DashProxy(blueprint=blueprint, external_stylesheets=[GITHUB_MARKDOWN_CSS_LIGHT])

if __name__ == "__main__":
    app.run_server(port=9657)
