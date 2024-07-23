import os

from .base import PythonResolver


def get_resolver(config):
    if os.environ.get("NRP_USE_UV"):
        from .uv import UVResolver
        return UVResolver(config)
    else:
        from .pdm import PDMResolver
        return PDMResolver(config)


__all__ = (
    "PythonResolver",
    "get_resolver",
)
