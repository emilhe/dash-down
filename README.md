[![Unit tests](https://github.com/emilhe/dash-down/actions/workflows/python-test.yml/badge.svg)](https://github.com/emilhe/dash-down/actions/workflows/python-test.yml)
[![codecov](https://codecov.io/gh/emilhe/dash-down/branch/main/graph/badge.svg?token=kZXx2N1QGY)](https://codecov.io/gh/emilhe/dash-down)

The `dash-down` package provides tools to render markdown files into Plotly Dash component trees. Besides standard markdown syntax, a custom interpretation of the [directive syntax extension](https://mistune.readthedocs.io/en/latest/directives.html) makes it possible to embed Dash code blocks and/or applications (including callbacks). For a live demo, please take look at the [`dash-extensions` documentation](https://www.dash-extensions.com/sections/installation).

## Getting started

Make sure that you have setup [uv](https://docs.astral.sh/uv/). Then run

    uv venv && source .venv/bin/activate && uv sync --all-extras --dev

to create a new virtual environment with all dependencies installed.

#### Running the examples

    uv run python example.py
    uv run python example_inline.py
    uv run python example_custom_directive.py
    uv run python example_custom_code_renderer.py

#### Running the tests

    uv run pytest

## Inline content

In addition to rendering markdown from files, you can also render inline markdown,

    md_to_blueprint_html(md="# This is a heading").embed(app)

A complete example can be found in `example_inline.py`.

## Custom content

Custom content is rendered via the markdown [directive syntax extension](https://mistune.readthedocs.io/en/latest/directives.html). A directive has the following syntax,

    .. directive-name:: directive value
       :option-key: option value
       :option-key: option value

       full featured markdown text here

where the `directive-name` is mandatory, while the `value`, the `options` (specified as key value pairs), and the `text` are optional.

#### What directives are bundled?

Currently, the bundled directives are

- **api-doc** - a directive for rendering api documentation for a component
- **dash-proxy** - a directive for rendering dash apps (including interactivity)

#### How to create custom directives?

The easiest way to create a custom directive is to create a function with the following signature,

```python
from dash_extensions.enrich import DashBlueprint

def directive_name(value: str, text: str, options: dict[str, str], blueprint: DashBlueprint):
    """
    :param value: the directive value (optional)
    :param text: the markdown text (optional)
    :param options: a dict containing all key value pairs (optional)
    :param blueprint: the DashBlueprint of the resulting Dash component tree, used e.g. for callback registration
    :return: a Dash component
    """
    ...
```

Say, we want to make a new directive that yields a plot of the `iris` dataset. The code would then be along the lines of,

```python
import plotly.express as px
from dash_extensions.enrich import dcc, DashBlueprint

def graph(value: str, text: str, options: dict[str, str], blueprint: DashBlueprint):
    df = getattr(px.data, options.dataset)()
    fig = px.scatter(df, x=options.x, y=options.y)
    return dcc.Graph(figure=fig)
```

With this directive defined, it is now possible to create a graph similar to [the one in the Dash docs](https://dash.plotly.com/dash-core-components/graph) with the following syntax,

    .. graph::
       :dataset: iris
       :x: sepal_width
       :y: sepal_length

To render a markdown file using the new, shiny directive, the syntax would be,

```python
from dash_extensions.enrich import DashProxy
from dash_down.express import md_to_blueprint_dmc

...

blueprint = md_to_blueprint_html('path_to_your_md_file', directives=[graph])
app = DashProxy(blueprint=blueprint)

if __name__ == '__main__':
    app.run()
```

A working example is bundled in the repo (see `example_custom_directive.py`).

#### How to customize the layout of the rendered blueprint?

The layout of the blueprint returned by the renderer can be customized by passing a custom app shell via the `shell` keyword of the `md_to_blueprint_html` function. A working example is bundled in the repo (see `example_code_renderer.py`).

#### How to customize the way code is rendered with the DashProxyDirective?

The layout of the Dash apps rendered via the `DashProxyDirective` can be customized via the `dash_proxy_shell` keyword of the `md_to_blueprint_html` function. A working example is bundled in the repo (see `example_code_renderer.py`).

Per default, the app shell `Div` element with the code rendered as the first child and the resulting app rendered as the second.

#### How to customize the markdown rendering itself?

Make a subclass of `DashMantineRenderer` (or `DashHtmlRenderer`, if you prefer to start from raw HTML) and override the render function(s) for any element that you want to change. A good place to start would be to look at the `DashMantineRenderer` class itself for inspiration.

#### How to style the rendered markdown?

The bundled renderers ( `DashHtmlRenderer`, `DashMantineRenderer`) add CSS classes to the rendered elements with the following naming structure,

```
m2d-{DIRECTIVE NAME}
```

Hence, you can target all paragraphs via the `m2d-paragraph` class, or all bold text via the `m2d-strong` class.
