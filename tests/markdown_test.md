# Heading level 1

## Heading level 2

### Heading level 3

#### Heading level 4

##### Heading level 5

###### Heading level 6

![Tux, the Linux mascot](assets/lena_color.png)

~~strike through~~, `inline code`, *italic*, **bold**, ***bold and italic***, [link](https://google.com), [link](https://google.com, "link title")

> Dorothy followed her through many of the beautiful rooms in her castle.

```python
from dash import Dash, html
from dash_extensions import BeforeAfter

app = Dash()
app.layout = html.Div([
    BeforeAfter(before="assets/lena_bw.png", after="assets/lena_color.png", width=512, height=512)
])

if __name__ == '__main__':
    app.run_server()
```

```
unkown code
```

1. First item
2. Second item
3. Third item
4. Fourth item

* Item
* Another item

***

Text on a line
and text on another link

<p>Hello from <em>html</em> world!</p>

\* Without the backslash, this would be a bullet in an unordered list.

> ApiDoc:dash_extensions.Purify

> DashProxy:module_name=tests.example_app,app_name=app