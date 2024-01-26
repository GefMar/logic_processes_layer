from __future__ import annotations

import dataclasses

from logic_processes_layer import BaseProcessor, BaseProcessorContext
from logic_processes_layer.extensions import InitMapper, ProcessAsSubprocess, ProcessAttr
from logic_processes_layer.processors.base import ResultsT

from ..sub_processors import SympleSubprocessor


class CompositionContext(BaseProcessorContext["ProcessComposition"]):
    @property
    def attr_one(self):
        return 111  # noqa: WPS432

    @property
    def attr_two(self):
        return 222  # noqa: WPS432


@dataclasses.dataclass(unsafe_hash=True)
class ProcessWithInitalData(BaseProcessor):
    some_attr_one: int
    some_attr_two: int

    def run(self):
        return self.some_attr_one + self.some_attr_two


SubProc = ProcessAsSubprocess[ProcessWithInitalData]


@dataclasses.dataclass(unsafe_hash=True)
class ProcessComposition(BaseProcessor[CompositionContext, ResultsT]):
    attr_one: int
    attr_two: int
    context_cls = CompositionContext

    pre_run = (
        SympleSubprocessor(),
        SubProc(
            process_cls=ProcessWithInitalData,
            init_mapper=InitMapper(1, 2),
        ),
        SubProc(
            process_cls=ProcessWithInitalData,
            init_mapper=InitMapper(
                ProcessAttr("attr_one"),
                ProcessAttr("attr_two"),
            ),
        ),
    )

    post_run = (
        SubProc(
            process_cls=ProcessWithInitalData,
            init_mapper=InitMapper(
                ProcessAttr("attr_one", from_context=True),
                ProcessAttr("attr_two", from_context=True),
            ),
        ),
        SubProc(
            process_cls=ProcessWithInitalData,
            init_mapper=InitMapper(
                some_attr_one=ProcessAttr("attr_one", from_context=True),
                some_attr_two=ProcessAttr("attr_two", from_context=True),
            ),
        ),
    )

    def run(self):
        return self.attr_one + self.attr_two
