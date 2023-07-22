import dataclasses
import typing


@dataclasses.dataclass
class AttrsData:
    args: typing.Tuple
    kwargs: typing.Dict
