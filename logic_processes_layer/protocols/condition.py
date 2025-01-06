from __future__ import annotations


__all__ = ("ConditionProtocol",)

import typing

from ..context import BaseProcessorContext


ContextT_contra = typing.TypeVar("ContextT_contra", bound=BaseProcessorContext, contravariant=True)


class ConditionProtocol(typing.Protocol[ContextT_contra]):
    def __call__(self, context: ContextT_contra) -> bool: ...  # noqa: WPS220, WPS428
