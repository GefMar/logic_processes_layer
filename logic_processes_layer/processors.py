__all__ = ("BaseProcessor",)

import typing

from .context import BaseProcessorContext
from .meta import MetaProcessor
from .results import ProcessorResult

ContextT = typing.TypeVar("ContextT", bound=BaseProcessorContext)
ResultsT = typing.TypeVar("ResultsT", bound=ProcessorResult)


class BaseProcessor(typing.Generic[ContextT, ResultsT], metaclass=MetaProcessor):
    _results: typing.Optional[ResultsT] = None
    _context: typing.Optional[ContextT] = None
    results_cls: typing.Type[ResultsT] = typing.cast(typing.Type[ResultsT], ProcessorResult)
    context_cls: typing.Type[ContextT] = typing.cast(typing.Type[ContextT], BaseProcessorContext)

    def __call__(self, *args, **kwargs):
        return self.run()

    @property
    def results(self) -> ResultsT:
        if self._results is None:
            self._results = self.results_cls()
        return self._results

    @property
    def context(self) -> ContextT:
        if self._context is None:
            self._context = self.context_cls(self)
        return self._context

    def run(self):
        raise NotImplementedError("Base process run method is required to be implemented")
