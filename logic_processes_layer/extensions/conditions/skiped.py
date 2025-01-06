from __future__ import annotations


__all__ = ["ConditionSkipped"]

import dataclasses
import typing

from ...processors import BaseProcessor


ProcessT = typing.TypeVar("ProcessT", bound=BaseProcessor)


@dataclasses.dataclass(unsafe_hash=True)
class ConditionSkipped(typing.Generic[ProcessT]):
    process: ProcessT

    def __str__(self):
        return f"Conditions skipped for {self.process}"
