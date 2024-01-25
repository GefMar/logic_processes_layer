from __future__ import annotations


__all__ = ("MetaSubprocessor",)

from .decorators import call_subprocess


class MetaSubprocessor(type):
    def __new__(cls, name, bases, attrs):
        if "__call__" in attrs:
            attrs["__call__"] = call_subprocess(attrs["__call__"])  # noqa: WPS529
        return super().__new__(cls, name, bases, attrs)
