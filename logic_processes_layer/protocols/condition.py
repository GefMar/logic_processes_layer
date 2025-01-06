from __future__ import annotations


__all__ = ("ConditionProtocol",)

import typing

from ..context import BaseProcessorContext


ContextContravariantT_contra = typing.TypeVar(
    "ContextContravariantT_contra", bound=BaseProcessorContext, contravariant=True
)


class ConditionProtocol(typing.Protocol[ContextContravariantT_contra]):
    def __call__(self, context: ContextContravariantT_contra) -> bool: ...  # noqa: WPS220, WPS428
