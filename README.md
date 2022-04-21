[![Unit tests](https://github.com/emilhe/dash-down/actions/workflows/python-test.yml/badge.svg)](https://github.com/emilhe/dash-down/actions/workflows/python-test.yml)
[![codecov](https://codecov.io/gh/emilhe/dash-down/branch/main/graph/badge.svg?token=kZXx2N1QGY)](https://codecov.io/gh/emilhe/dash-down)

The `dash-down` module provides tooling to convert markdown files into Plotly Dash applications. 

## Getting started

Make sure that you have setup [poetry](https://python-poetry.org/). Then run

    poetry install

to install dependencies.

#### Running the example

    poetry run python example.py

#### Running the tests

    poetry run pytest

## Custom content

Custom content is rendered via the markdown [directive syntax extension](https://mistune.readthedocs.io/en/latest/directives.html). A directive has the following syntax,

    .. directive-name:: directive value
       :option-key: option value
       :option-key: option value
    
       full featured markdown text here

where the `directive-name` is mandatory, while the `value`, the `options` (specified as key value pairs), and the `text` are optional. 

#### What directives are bundled?

Currently, the bundled directives are

* **api-doc** - a directive for rendering api documentation for a component
* **dash-proxy** - a block for rendering dash apps (including interactivity)

#### How to create custom directives?

The easiest way to create a custom directive is to create a function with the following signature,

```python
def directive_name(value: str, text: str, options: Box[str, str], blueprint: DashBlueprint):
    """
    :param value: the directive value (optional)
    :param text: the markdown text (optional)
    :param options: a Box object containing all key value pairs (optional)
    :param blueprint: the DashBlueprint of the resulting Dash component tree, used e.g. for callback registration
    :return: a Dash component
    """
    ...
```

Say, we want to make a new directive that yields a plot of the `iris` dataset. The code would then be along the lines of,

```
def graph(value: str, text: str, options: Box[str, str], blueprint: DashBlueprint):
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
```
from dash_extensions.enrich import DashProxy
from dash_down.express import md_to_blueprint_dmc

path_to_your_md_file = "..."
blueprint = md_to_blueprint_dmc(path_to_your_md_file, directives=[graph])

if __name__ == '__main__':
    DashProxy(blueprint=blueprint).run_server()
```

A working example is bundled in the repo (see `example_custom_directive.py`).

#### How to customize the layout of the rendered blueprint?

The layout of the blueprint returned by the renderer can be customized by passing a custom app sheel via the `shell` keyword of the `md_to_blueprint_dmc` function. A working example is bundled in the repo (see `example_code_renderer.py`).

Per default, the app shell is a `Div` element with `className="markdown-body"`. This class makes it possibly to use GitHub CSS for styling.

#### How to customize the way code is rendered with the DashProxyDirective?

The layout of the Dash apps rendered via the `DashProxyDirective` can be customized via the `dash_proxy_shell` keyword of the `md_to_blueprint_dmc` function. A working example is bundled in the repo (see `example_code_renderer.py`).

Per default, the app shell `Div` element with the code rendered as the first child and the resulting app rendered as the second.

#### How to customize the markdown rendering itself?

Make a subclass of `DashMantineRenderer` (or `DashHtmlRenderer`, if you prefer to start from raw HTML) and override the render function(s) for any element that you want to change. A good place to start would be to look at the `DashMantineRenderer` class itself for inspiration.
