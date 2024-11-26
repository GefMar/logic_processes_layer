from __future__ import annotations

import dataclasses
import random

from .examples.processors.process_with_nested_attrs import ProcessWithNestedAttributes


@dataclasses.dataclass
class TestData:
    some_attr_one: int = dataclasses.field(default_factory=lambda: random.randint(1, 100))
    some_attr_two: int = dataclasses.field(default_factory=lambda: random.randint(1, 100))


class TestProcessWithNestedAttributes:
    def setup_method(self):
        self.start_data = TestData()
        self.process: ProcessWithNestedAttributes = ProcessWithNestedAttributes(self.start_data)
        self.expected_result = {
            "post_run": (self.start_data.some_attr_one, self.start_data.some_attr_two),
        }

    def check_state(self, state_name):
        proc_state_instances = getattr(self.process, state_name)
        for idx, state_instance in enumerate(proc_state_instances):
            assert state_instance.call_result == sum(self.expected_result[state_name]), (state_name, idx)

    def test_process_composition(self):
        self.process()

        for state_name in self.expected_result:
            self.check_state(state_name)
