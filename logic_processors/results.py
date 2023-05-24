import dataclasses
import typing


@dataclasses.dataclass
class ProcessResult:
    pre_run: typing.Dict[typing.Callable, typing.Any] = dataclasses.field(default_factory=dict)
    run: typing.Any = None
    post_run: typing.Dict[typing.Callable, typing.Any] = dataclasses.field(default_factory=dict)
