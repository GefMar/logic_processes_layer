from __future__ import annotations


__all__ = ("CallableConditionProtocol",)

import typing

from ..context import BaseProcessorContext


ContextT_contra = typing.TypeVar("ContextT_contra", bound=BaseProcessorContext, contravariant=True)


@typing.runtime_checkable
class CallableConditionProtocol(typing.Protocol[ContextT_contra]):
    def __call__(self, context: ContextT_contra) -> bool: ...  # noqa: WPS220, WPS428
