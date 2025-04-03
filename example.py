from dash_extensions.enrich import DashProxy

from dash_down.express import md_to_blueprint_html

blueprint = md_to_blueprint_html("resources/test.md")
app = DashProxy(blueprint=blueprint)

if __name__ == "__main__":
    app.run(port=9657)
