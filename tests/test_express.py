import os
import pytest

from dash_down.express import md_to_blueprint_html, md_to_blueprint_dmc


@pytest.fixture(autouse=True)
def change_cwd():
    os.chdir(os.path.join(os.getcwd(), ".."))


# TODO: Maybe add UI validation, e.g. using Percy
def test_render_markdown_html():
    blueprint = md_to_blueprint_html('tests/markdown_test.md')


# TODO: Maybe add UI validation, e.g. using Percy
def test_render_markdown_dmc():
    blueprint = md_to_blueprint_dmc('tests/markdown_test.md')
