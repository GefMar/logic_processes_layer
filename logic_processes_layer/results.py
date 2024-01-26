from __future__ import annotations

import dataclasses
import typing
import warnings


if typing.TYPE_CHECKING:
    from logic_processes_layer import BaseSubprocessor

warnings.warn("Module ProcessorResult is deprecated", DeprecationWarning, stacklevel=2)


@dataclasses.dataclass
class ProcessorResult:
    pre_run: dict[BaseSubprocessor, typing.Any] = dataclasses.field(default_factory=dict)
    run: typing.Any = None
    post_run: dict[BaseSubprocessor, typing.Any] = dataclasses.field(default_factory=dict)
