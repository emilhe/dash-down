from dash_down.express import md_to_blueprint_html, md_to_blueprint_dmc


# TODO: Maybe add UI validation, e.g. using Percy
def test_render_markdown_html():
    blueprint = md_to_blueprint_html('resources/test.md', plugins=[])


# TODO: Maybe add UI validation, e.g. using Percy
def test_render_markdown_dmc():
    blueprint = md_to_blueprint_dmc('resources/test.md')
