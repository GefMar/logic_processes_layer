from __future__ import annotations


__all__ = ("ProcessAsSubprocess",)

import dataclasses
import typing

from ..processors import BaseProcessor
from ..sub_processors import BaseSubprocessor, ContextT
from .conditions import ConditionSkipped


if typing.TYPE_CHECKING:
    from .mappers import InitMapper

ProcessT = typing.TypeVar("ProcessT", bound=BaseProcessor)


@dataclasses.dataclass(unsafe_hash=True)
class ProcessAsSubprocess(BaseSubprocessor, typing.Generic[ProcessT]):
    process_cls: type[ProcessT]
    init_mapper: InitMapper | None = dataclasses.field(hash=False, default=None)
    conditions: typing.Iterable[typing.Callable[[ContextT], bool]] = dataclasses.field(
        hash=False, default_factory=tuple
    )

    def __call__(self):
        args = ()
        kwargs: dict[str, typing.Any] = {}
        if self.init_mapper is not None:
            args, kwargs = self.init_mapper(self.context)

        subprocessor = self.process_cls(*args, **kwargs)
        if not self.check_conditions():
            return ConditionSkipped(subprocessor)
        return subprocessor()

    def check_conditions(self) -> bool:
        return all(condition(self.context) for condition in self.conditions)
