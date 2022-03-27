import importlib
import re
from typing import List
from dash import html
from dash_extensions.enrich import DashProxy, PrefixIdTransform, DashBlueprint
from mistune.directives import Directive
from box import Box


# region Utils

# https://stackoverflow.com/questions/1175208/elegant-python-function-to-convert-camelcase-to-snake-case
def camel_to_snake(name):
    name = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
    return re.sub('([a-z0-9])([A-Z])', r'\1_\2', name).lower()

# https://stackoverflow.com/questions/11273282/whats-the-name-for-hyphen-separated-case
def camel_to_kebab(name):
    return camel_to_snake(name).replace("_", "-")


# endregion

class DashDirective(Directive):
    """
    Class intended to use as base class for Dash component directives. See 'ApiDocDirective' for a simple example.
    """

    def __init__(self):
        self.md = None

    def __call__(self, md):
        self.md = md
        self.register_directive(md, self.get_directive_name())
        md.renderer.register(self.get_directive_name(),
                             lambda raw: self.render_directive(**raw))

    def parse(self, block, m, state):
        value = m.group('value')
        text = self.parse_text(m)
        options = self.parse_options(m)
        options = Box({item[0]: item[1] for item in options})
        blueprint = state.get("blueprint", None)
        return dict(type=self.get_directive_name(),
                    raw=dict(value=value, text=text, options=options, blueprint=blueprint))

    def get_directive_name(self):
        return camel_to_kebab(self.__class__.__name__.replace("Directive", ""))

    def render_directive(self, value: str, text: str, options: Box[str, str], blueprint: DashBlueprint):
        raise NotImplementedError()  # pragma: no cover


class ApiDocDirective(DashDirective):
    """
    Directive that yields API documentation. The following syntax,

        .. api-doc:: dash_extensions.Purify

    yields API docs for the 'Purify' component from the 'dash_extensions' module.
    """

    def __init__(self, custom_render=None):
        super().__init__()
        self.custom_render = custom_render

    def render_directive(self, value: str, text: str, options: Box[str, str], blueprint: DashBlueprint):
        # Parse api doc.
        module_name, component_name = ".".join(value.split(".")[:-1]), value.split(".")[-1]
        module = importlib.import_module(module_name)
        component = getattr(module, component_name)
        component_doc = component.__doc__
        docs = component_doc.split("Keyword arguments:")[-1]
        docs = docs.lstrip("\n\n")
        # Invoke render function.
        if self.custom_render:
            return self.custom_render(docs)
        return self._default_renderer(docs)

    def _default_renderer(self, docs):
        return html.Div([
            self.md.renderer.heading("Keyword arguments:", 5),
            self.md.renderer.block_code(docs, info='git')
        ])


class DashProxyDirective(DashDirective):
    """
    Directive that enables mounting of Dash apps that use the 'DashProxy' object from the 'dash-extensions' pakcage.
    The following syntax,

        .. dash-proxy:: resources.test

    loads the 'app' variable (must be a 'DashProxy' object) from the 'resources.test' module, renders the app
    (including callbacks), with the code next to it.
    """

    def __init__(self, custom_render=None, custom_code_transform=None, hide_tag="no-show"):
        super().__init__()
        self.custom_render = custom_render
        self.custom_code_transform = custom_code_transform
        self.hide_tag = hide_tag

    def render_directive(self, value: str, text: str, options: Box[str, str], blueprint: DashBlueprint):
        module_name = value
        # Parse app name.
        app_name = "app"
        if "app-name" in options:
            app_name = options["app-name"]
        # Get the app.
        module = importlib.import_module(module_name)
        app: DashProxy = getattr(module, app_name)
        # Add prefix.
        prefix = module_name.replace(".", "_")
        prefix_transform = PrefixIdTransform(prefix)  # TODO: Maybe do some escaping?
        app.blueprint.transforms.append(prefix_transform)
        # Register on blueprint.
        app.blueprint.register_callbacks(blueprint)
        # Extract values for rendering.
        layout = app._layout_value()
        with open(f"{module_name.replace('.', '/')}.py", 'r') as f:
            source = f.readlines()
            if self.custom_code_transform:
                source = self.custom_code_transform(source)
            else:
                source = self._default_code_transform(source)
        # Invoke render function.
        if self.custom_render:
            return self.custom_render(source, layout)
        return self._default_renderer(source, layout)

    def _default_code_transform(self, source: List[str]):
        return "".join([line for line in source if self.hide_tag not in line])

    def _default_renderer(self, source, layout):
        return html.Div([
            self.md.renderer.block_code(source, "python"),
            layout
        ])
