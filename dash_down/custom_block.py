import logging
from typing import List, TypeVar
from mistletoe import BaseRenderer

""""
This module holds functionality related to mounting custom blocks, i.e. mark down syntax extensions.
"""


class CustomBlock:  # pragma: no cover
    """
    Custom block interface definition.
    """
    def render(self, renderer: BaseRenderer, inner: str):
        raise NotImplementedError


T = TypeVar('T', bound=BaseRenderer)
U = TypeVar('U', bound=CustomBlock)


def bind_custom_blocks(renderer: T, custom_blocks: List[CustomBlock]):
    """
    This function binds custom block definitions to a renderer using the following syntax,

    > [BLOCK_NAME]:arg1:arg2:..

    where BLOCK_NAME is the class name of the custom block stripped for 'Block'.
    :param renderer: the renderer (binding is performed in-place)
    :param custom_blocks: the custom blocks to bind
    :return: None
    """
    # Create token mapping.
    custom_block_map = {}
    for block in custom_blocks:
        custom_block_map[block.__class__.__name__.replace("Block", "")] = block
    # Prepare monkey patching.
    render_quote_original = renderer.render_map['Quote']

    def render_quote(token):
        # TODO: What about this block?
        inner = [renderer.render(child) for child in token.children]
        # Check for custom elements.
        custom_element = _detect_custom_block(inner)
        if custom_element:
            return custom_element
        # If not found, just return normal block.
        return render_quote_original(token)

    def _parse_args(line):
        # TODO: Add more elaborate parsing.
        args, kwargs = [], {}
        all_args = line.split(",")
        for arg in all_args:
            if "=" in arg:
                kwargs[arg.split("=")[0]] = "=".join(arg.split("=")[1:])
            else:
                args.append(arg)
        return args, kwargs

    def _detect_custom_block(inner):
        try:
            first_line = inner[0].children
            element_type = first_line.split(":")[0]
        except Exception as e:
            logging.warning(str(e))
            return None
        if element_type in custom_block_map:
            args, kwargs = _parse_args(first_line[len(element_type) + 1:])
            return custom_block_map[element_type].render(renderer, *args, **kwargs)
        return None

    renderer.render_map['Quote'] = render_quote
