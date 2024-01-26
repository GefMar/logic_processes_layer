from __future__ import annotations


__all__ = ("BaseProcessor",)

import typing

from ..context import BaseProcessorContext
from ..results import ProcessorResult
from .meta import MetaProcessor


if typing.TYPE_CHECKING:
    from ..sub_processors import BaseSubprocessor


ContextT = typing.TypeVar("ContextT", bound=BaseProcessorContext)
ResultsT = typing.TypeVar("ResultsT", bound=ProcessorResult)


class BaseProcessor(typing.Generic[ContextT, ResultsT], metaclass=MetaProcessor):
    _results: ResultsT | None = None
    _context: ContextT | None = None
    results_cls: type[ResultsT] = typing.cast(typing.Type[ResultsT], ProcessorResult)
    context_cls: type[ContextT] = typing.cast(typing.Type[ContextT], BaseProcessorContext)
    pre_run: tuple[BaseSubprocessor, ...] = ()
    post_run: tuple[BaseSubprocessor, ...] = ()

    def __call__(self):
        return self.run()

    @property
    def results(self) -> ResultsT:
        if self._results is None:
            self._results = self.results_cls()  # noqa: WPS601
        return self._results

    @property
    def context(self) -> ContextT:
        if self._context is None:
            self._context = self.context_cls(self)  # noqa: WPS601
        return self._context

    def run(self):
        msg = "Base process run method is required to be implemented"
        raise NotImplementedError(msg)
