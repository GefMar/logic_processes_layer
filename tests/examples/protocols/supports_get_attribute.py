from __future__ import annotations


__all__ = ("SupportsGetAttribute",)

import typing


class SupportsGetAttribute(typing.Protocol):
    some_attr_one: int
    some_attr_two: int

    def __getattribute__(self, name: str) -> typing.Any:  # noqa: ANN401
        ...  # noqa: WPS428
