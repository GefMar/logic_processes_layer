from __future__ import annotations


__all__ = ("InitMapper", "ProcessAttr")

import dataclasses
from operator import attrgetter
import typing


AnyTupleT = typing.Tuple[typing.Any, ...]
DictStrAnyT = typing.Dict[str, typing.Any]


@dataclasses.dataclass
class ProcessAttr:
    attr_name: str
    from_context: bool = dataclasses.field(default=False)
    cast: typing.Callable[[typing.Any], typing.Any] = dataclasses.field(default=lambda arg: arg)

    def get_value(self, context: typing.Any) -> typing.Any:  # noqa: ANN401
        source = (context.process, context)[self.from_context]
        source_value = attrgetter(self.attr_name)(source)
        return self.cast(source_value)


class InitMapper:
    def __init__(self, *args, **kwargs):
        self._init_attrs = args
        self._init_kwargs = kwargs

    def __call__(self, context: typing.Any) -> tuple[AnyTupleT, DictStrAnyT]:  # noqa: ANN401
        args = self._load_args(context)
        kwargs = self._load_kwargs(context)
        return args, kwargs

    def _load_args(self, context: typing.Any) -> AnyTupleT:  # noqa: ANN401
        args = []
        for init_attr in self._init_attrs:
            value = init_attr
            if isinstance(init_attr, ProcessAttr):
                value = init_attr.get_value(context)
            args.append(value)
        return tuple(args)

    def _load_kwargs(self, context: typing.Any) -> DictStrAnyT:  # noqa: ANN401
        kwargs = {}
        for key, value in self._init_kwargs.items():
            init_value = value
            if isinstance(value, ProcessAttr):
                init_value = value.get_value(context)
            kwargs[key] = init_value
        return kwargs
