from dash_extensions.enrich import DashBlueprint, html
from mistune import Markdown


class PluginBlueprint:
    """
    This plugin injects a DashBlueprint as part of the rendering state. It's needed by e.g. the DashProxy directive.
    """

    def __init__(self, shell=None):
        self.shell = shell if shell is not None else lambda x: html.Div(x, className="markdown-body")

    def __call__(self, md: Markdown):
        def setup_blueprint(ctx, tokens, state):
            state["blueprint"] = DashBlueprint()
            return tokens, state

        def collect_blueprint(ctx, result, state):
            blueprint: DashBlueprint = state["blueprint"]
            blueprint.layout = self.shell(result)
            return blueprint

        md.before_parse_hooks.append(setup_blueprint)
        md.after_render_hooks.append(collect_blueprint)
