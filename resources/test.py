from dash_extensions.enrich import DashProxy, html, Output, Input

app = DashProxy()
app.layout = html.Div([
    html.Button("Click me!", id="btn"), html.Div(id="log")
])

@app.callback(Output("log", "children"), Input("btn", "n_clicks"))
def update(n_clicks):
    return f"You clicked {n_clicks} times!"
# no-show
if __name__ == '__main__':  # no-show
    app.run_server()  # no-show
