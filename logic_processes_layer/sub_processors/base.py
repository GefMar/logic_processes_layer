from __future__ import annotations


__all__ = ("BaseSubprocessor",)

import dataclasses
import typing

from ..context import BaseProcessorContext
from .meta import MetaSubprocessor


ContextT = typing.TypeVar("ContextT", bound=BaseProcessorContext)
CallResultT = typing.TypeVar("CallResultT", bound=typing.Any)


@dataclasses.dataclass(unsafe_hash=True)
class BaseSubprocessor(typing.Generic[ContextT, CallResultT], metaclass=MetaSubprocessor):
    context: ContextT = dataclasses.field(init=False, hash=False)
    call_result: CallResultT = dataclasses.field(init=False, hash=False)

    def __call__(self) -> CallResultT:
        msg = "Base subprocess call method is required to be implemented"
        raise NotImplementedError(msg)
