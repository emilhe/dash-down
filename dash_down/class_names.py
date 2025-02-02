import inspect
from functools import wraps

"""
Util functions for generating / adding m2d class names to components.
"""


def create_class_name(text: str) -> str:
    return "m2d-" + "-".join(text.lower().split("_"))


def class_name(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        ret = func(*args, **kwargs)
        name = func.__name__ if inspect.isfunction(func) else func.__self__.block_name
        if ret is not None:
            ret.className = create_class_name(name)

        return ret

    return wrapper
