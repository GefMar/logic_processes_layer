__all__ = ("BaseProcessor",)

import typing

from .context import BaseProcessorContext
from .meta import MetaProcessor
from .results import ProcessorResult


class BaseProcessor(metaclass=MetaProcessor):
    _context: typing.Optional["BaseProcessorContext"] = None
    results = ProcessorResult()
    context_cls = BaseProcessorContext

    def __call__(self, *args, **kwargs):
        return self.run()

    @property
    def context(self):
        if self._context is None:
            self._context = self.context_cls(self)
        return self._context

    def run(self):
        raise NotImplementedError("Base process run method is required to be implemented")
