from __future__ import annotations


__all__ = ("AttrCondition", "FunctionCondition", "OperatorCondition")

import typing

from ...context import BaseProcessorContext
from .operator_enums import OperatorEnum


if typing.TYPE_CHECKING:
    from ...protocols import CallableConditionProtocol
    from ..mappers import ProcessAttr

ContextT = typing.TypeVar("ContextT", bound=BaseProcessorContext)
OperatorCallablesT = typing.Callable[[typing.Iterable[typing.Any]], bool]
OperatorMapT = typing.Dict[OperatorEnum, OperatorCallablesT]


class OperatorCondition(typing.Generic[ContextT]):
    operator_map: typing.ClassVar[OperatorMapT] = {
        OperatorEnum.AND: all,
        OperatorEnum.OR: any,
        OperatorEnum.XOR: lambda conditions: sum(conditions) == 1,
    }

    def __init__(
        self,
        conditions: typing.Iterable[CallableConditionProtocol],
        *,
        operator: OperatorEnum = OperatorEnum.AND,
        negated: bool = False,
    ):
        self.conditions = conditions
        self.negated = negated
        self.operator = operator

    def __call__(self, context: ContextT) -> bool:
        operator_f = self.operator_map[self.operator]
        result = operator_f(condition(context) for condition in self.conditions)
        return not result if self.negated else result

    def __invert__(self) -> OperatorCondition:
        return OperatorCondition([self], operator=self.operator, negated=not self.negated)

    def __and__(self, other: CallableConditionProtocol) -> OperatorCondition:
        return OperatorCondition([self, other], operator=OperatorEnum.AND)

    def __or__(self, other: CallableConditionProtocol) -> OperatorCondition:
        return OperatorCondition([self, other], operator=OperatorEnum.OR)

    def __xor__(self, other):
        return OperatorCondition([self, other], operator=OperatorEnum.XOR)


class AttrCondition(OperatorCondition[ContextT]):
    def __init__(self, process_attr: ProcessAttr, *, negated: bool = False):
        self.process_attr = process_attr
        super().__init__(operator=OperatorEnum.AND, conditions=[self], negated=negated)

    def __call__(self, context: ContextT) -> bool:
        value = self.process_attr.get_value(context)
        result = bool(value)
        return not result if self.negated else result


class FunctionCondition(OperatorCondition[ContextT]):
    def __init__(self, func: CallableConditionProtocol, *, negated: bool = False):
        super().__init__(operator=OperatorEnum.AND, conditions=[func], negated=negated)
