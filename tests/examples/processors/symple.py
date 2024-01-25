from __future__ import annotations


__all__ = ("SympleProcessor",)

from logic_processes_layer import BaseProcessor


class SympleProcessor(BaseProcessor):
    def run(self):
        return self.__class__.__name__
