[![Unit tests](https://github.com/emilhe/dash-down/actions/workflows/python-test.yml/badge.svg)](https://github.com/emilhe/dash-down/actions/workflows/python-test.yml)
[![codecov](https://codecov.io/gh/emilhe/dash-down/branch/main/graph/badge.svg?token=kZXx2N1QGY)](https://codecov.io/gh/emilhe/dash-down)

The `dash-down` module provides tools to convert markdown files into a Plotly Dash application.

## Getting started

Make sure that you have setup [poetry](https://python-poetry.org/). Then run

    poetry install

to install dependencies.

### Running the example

    poetry run python example.py

### Running the tests

    poetry run pytest

## Syntax extension(s)

Custom content is rendered via a **block** markdown syntax extension. A block has the following syntax,

> BLOCK_NAME:ARG,KEY=VALUE

where `BLOCK_NAME` denotes the name of the custom block, while `ARG` is a block argument, and the (`KEY`,`VALUE`) pair denotes a keyword argument. Any number of arguments/keyword arguments can be specified (separated by `,`). All arguments are passed to the block `render` function.

### What blocks are bundled?

Currently, the bundled blocks are

* **ApiDocBlock** - a block for rendering api documentation for a component
* **DashProxyBlock** - a block for rendering dash apps (including interactivity)

### How to create custom blocks?

To create a new block, make a subclass of `CustomBlock` and implement the `render` function. Say we want to make a new block that yields a plot of the `iris` dataset. The code would be along the lines of,

```
class GraphBlock(CustomBlock):
    def render(self, renderer, dataset_name, x, y):
        df = getattr(px.data, dataset_name)()
        fig = px.scatter(df, x=x, y=y)
        return dcc.Graph(figure=fig)
```

With this block defined, you could now create a graph similar to [the one in the Dash docs](https://dash.plotly.com/dash-core-components/graph) with the following syntax,

> Graph:iris,x=petal_width,y=petal_length

To render a markdown file using your new, shiny block, the syntax would be along the line of,

```
path_to_your_md_file = "..."
blueprint = md_to_blueprint_dmc(path_to_your_md_file, custom_blocks=[GraphBlock()])

if __name__ == '__main__':
    DashProxy(blueprint=blueprint).run_server()
```

A working example is bundled in the repo (see `example_custom_block.py`).

### How to customize the way code is rendered with the DashProxyBlock?

The `DashProxyBlock` takes optional arguments to customize code rendering. A working example is bundled in the repo (see `example_code_renderer.py`).

### How to customize the markdown rendering itself?

Just make a subclass of `DashMantineRenderer` (or `DashHtmlRenderer`, if you prefer to start from raw HTML) and override the render function for any element that you want to change.