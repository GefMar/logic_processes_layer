from __future__ import annotations


__all__ = ["AndCondition", "Condition", "OrCondition"]

import typing

from ...context import BaseProcessorContext


if typing.TYPE_CHECKING:
    from ...protocols import ConditionProtocol
    from ..mappers import ProcessAttr


ContextT = typing.TypeVar("ContextT", bound=BaseProcessorContext)


class AndCondition:
    def __init__(self, conditions: typing.Iterable[ConditionProtocol]):
        self.conditions = conditions

    def __call__(self, context: ContextT) -> bool:
        return all(condition(context) for condition in self.conditions)


class OrCondition:
    def __init__(self, conditions: typing.Iterable[ConditionProtocol]):
        self.conditions = conditions

    def __call__(self, context: ContextT) -> bool:
        return any(condition(context) for condition in self.conditions)


class Condition(typing.Generic[ContextT]):
    def __init__(self, process_attr: ProcessAttr):
        self.process_attr = process_attr

    def __call__(self, context: ContextT) -> bool:
        value = self.process_attr.get_value(context)
        return bool(value)

    def __and__(self, other: ConditionProtocol) -> ConditionProtocol:
        return AndCondition([self, other])

    def __or__(self, other: ConditionProtocol) -> ConditionProtocol:
        return OrCondition([self, other])
