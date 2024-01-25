from __future__ import annotations


__all__ = ("BaseProcessorContext",)

import dataclasses
import typing


if typing.TYPE_CHECKING:
    from .processors import BaseProcessor

ProcessT = typing.TypeVar("ProcessT", bound="BaseProcessor")


@dataclasses.dataclass(unsafe_hash=True)
class BaseProcessorContext(typing.Generic[ProcessT]):
    process: ProcessT = dataclasses.field(hash=False)
