from __future__ import annotations


__all__ = ("ProcessAsSubprocess",)

import dataclasses
import typing

from ..processors import BaseProcessor
from ..sub_processors import BaseSubprocessor


if typing.TYPE_CHECKING:
    from .mappers import InitMapper

ProcessT = typing.TypeVar("ProcessT", bound=BaseProcessor)


@dataclasses.dataclass(unsafe_hash=True)
class ProcessAsSubprocess(BaseSubprocessor, typing.Generic[ProcessT]):
    process_cls: type[ProcessT]
    init_mapper: None | InitMapper = dataclasses.field(hash=False, default=None)

    def __call__(self):
        args = ()
        kwargs: dict[str, typing.Any] = {}
        if self.init_mapper is not None:
            args, kwargs = self.init_mapper(self.context)
        return self.process_cls(*args, **kwargs)()
