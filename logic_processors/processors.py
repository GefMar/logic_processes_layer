__all__ = ("BaseProcess",)

import typing

from .context import BaseProcessContext
from .meta import MetaProcessor
from .results import ProcessResult


class BaseProcess(metaclass=MetaProcessor):
    _context: typing.Optional["BaseProcessContext"] = None
    process_result = ProcessResult()
    context_cls = BaseProcessContext

    def __call__(self, *args, **kwargs):
        return self.run()

    @property
    def context(self):
        if self._context is None:
            self._context = self.context_cls(self)
        return self._context

    def run(self):
        raise NotImplementedError("Base process run method is required to be implemented")
