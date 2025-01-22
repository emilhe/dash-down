from dash_extensions.enrich import DashProxy, html

from dash_down.express import md_to_blueprint_html

app = DashProxy()
app.layout = html.Div(
    [
        md_to_blueprint_html(md="# This is a heading").embed(app),
        md_to_blueprint_html(md="Here is some **bold** text").embed(app),
    ]
)

if __name__ == "__main__":
    app.run_server(port=9658)
