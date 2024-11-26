from __future__ import annotations

from logic_processes_layer import BaseSubprocessor


__all__ = ("SimpleSubprocessor",)


class SimpleSubprocessor(BaseSubprocessor):
    def __call__(self):
        return self.__class__.__name__
