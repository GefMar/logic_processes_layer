from __future__ import annotations

from logic_processes_layer import BaseSubprocessor


__all__ = ("SympleSubprocessor",)


class SympleSubprocessor(BaseSubprocessor):
    def __call__(self):
        return self.__class__.__name__
