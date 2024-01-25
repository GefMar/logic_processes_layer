from __future__ import annotations


__all__ = ("MetaProcessor",)

from .decorators import make_run


class MetaProcessor(type):
    def __new__(cls, name, bases, attrs):
        if "run" in attrs:
            attrs["run"] = make_run(attrs["run"])  # noqa: WPS529
        return super().__new__(cls, name, bases, attrs)
