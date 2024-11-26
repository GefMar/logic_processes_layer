from __future__ import annotations

import dataclasses
from typing import TYPE_CHECKING

from logic_processes_layer import BaseProcessor
from logic_processes_layer.extensions import InitMapper, ProcessAttr

from .multy_process import ProcessWithInitalData, SubProc


if TYPE_CHECKING:
    from ..protocols.supports_get_attribute import SupportsGetAttribute


@dataclasses.dataclass
class ProcessWithNestedAttributes(BaseProcessor):
    attr: SupportsGetAttribute

    post_run = (
        SubProc(
            process_cls=ProcessWithInitalData,
            init_mapper=InitMapper(
                some_attr_one=ProcessAttr("attr.some_attr_one"),
                some_attr_two=ProcessAttr("attr.some_attr_two"),
            ),
        ),
    )

    def run(self):
        return self.attr.some_attr_one + self.attr.some_attr_two
