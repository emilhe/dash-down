[![Unit tests](https://github.com/emilhe/dash-down/actions/workflows/python-test.yml/badge.svg)](https://github.com/emilhe/dash-down/actions/workflows/python-test.yml)
[![codecov](https://codecov.io/gh/emilhe/dash-down/branch/main/graph/badge.svg?token=kZXx2N1QGY)](https://codecov.io/gh/emilhe/dash-down)

The `dash-down` module provides tools to convert markdown files into Plotly Dash applications.

## Getting started

Make sure that you have setup [poetry](https://python-poetry.org/). Then run

    poetry install

to install dependencies.

#### Running the example

    poetry run python example.py

#### Running the tests

    poetry run pytest

## Custom content

Custom content is rendered the markdown [directive syntax extension](https://mistune.readthedocs.io/en/latest/directives.html). A directive has the following syntax,

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

To create a new directive, simply make a subclass of `DashDirective` and implement the `render_directive` function. Say you want to make a new directive that yields a plot of the `iris` dataset. The code would be along the lines of,

```
import plotly.express as px
from dash_down.directives import DashDirective
from dash_extensions.enrich import dcc

class GraphDirective(DashDirective):
    def render_directive(self, value, text, options, blueprint):
        df = getattr(px.data, options.dataset)()
        fig = px.scatter(df, x=options.x, y=options.y)
        return dcc.Graph(figure=fig)
```

The directive name is derived from the class name by dropping `Directive`, and converting to kebab-case (or you can override the `get_directive_name` function). With this directive defined, you can now create a graph similar to [the one in the Dash docs](https://dash.plotly.com/dash-core-components/graph) with the following syntax,

    .. graph::
       :dataset: iris
       :x: sepal_width
       :y: sepal_length

To render a markdown file using your new, shiny directive, the syntax would be,

```
from dash_extensions.enrich import DashProxy
from dash_down.express import md_to_blueprint_dmc

path_to_your_md_file = "..."
blueprint = md_to_blueprint_dmc(path_to_your_md_file, plugins=[GraphDirective()])

if __name__ == '__main__':
    DashProxy(blueprint=blueprint).run_server()
```

A working example is bundled in the repo (see `example_custom_directive.py`).

#### How to customize the layout of the rendered blueprint?

The layout of the blueprint returned by the renderer can be customized by passing a custom layout function to the `PluginBlueprint`. A working example is bundled in the repo (see `example_code_renderer.py`).

#### How to customize the markdown rendering itself?

Make a subclass of `DashMantineRenderer` (or `DashHtmlRenderer`, if you prefer to start from raw HTML) and override the render function(s) for any element that you want to change.

#### How to customize the way code is rendered with the DashProxyDirective?

The `DashProxyDirective` takes optional arguments to customize code rendering. A working example is bundled in the repo (see `example_code_renderer.py`).
