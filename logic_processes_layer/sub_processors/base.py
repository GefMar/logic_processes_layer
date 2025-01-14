from __future__ import annotations


__all__ = ("BaseSubprocessor", "CallResultT", "ContextT")

import typing

from ..context import BaseProcessorContext
from .meta import MetaSubprocessor


ContextT = typing.TypeVar("ContextT", bound=BaseProcessorContext)
CallResultT = typing.TypeVar("CallResultT", bound=typing.Any)


class BaseSubprocessor(typing.Generic[ContextT, CallResultT], metaclass=MetaSubprocessor):
    _context: ContextT | None = None
    _call_result: CallResultT | None = None

    def __call__(self) -> CallResultT:
        msg = "Base subprocess call method is required to be implemented"
        raise NotImplementedError(msg)

    @property
    def context(self) -> ContextT | None:
        return self._context

    @context.setter
    def context(self, value: ContextT) -> None:
        self._context = value  # noqa: WPS601

    @property
    def call_result(self) -> CallResultT | None:
        return self._call_result

    @call_result.setter
    def call_result(self, value: CallResultT) -> None:
        self._call_result = value  # noqa: WPS601

    def __repr__(self):
        context_str = f"{self.context!r}"
        call_result_str = f"{self.call_result!r}"
        return f"{self.__class__.__name__}({context_str=}, {call_result_str=})"

    def __hash__(self):
        return hash(f"{self.__class__.__name__}{id(self)}")
