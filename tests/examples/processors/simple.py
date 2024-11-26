from __future__ import annotations


__all__ = ("SimpleProcessor",)

from logic_processes_layer import BaseProcessor


class SimpleProcessor(BaseProcessor):
    def run(self):
        return self.__class__.__name__
