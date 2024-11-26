from __future__ import annotations

import random

from tests.examples.processors.multy_process import ProcessComposition


class TestProcessComposition:
    def setup_method(self):
        self.start_data = (random.randint(1, 10), random.randint(1, 10))
        self.process: ProcessComposition = ProcessComposition(*self.start_data)
        self.expected_result = {
            "pre_run": ("SimpleSubprocessor", 3, sum(self.start_data)),
            "post_run": (333, 333),
        }

    def check_state(self, state_name):
        proc_state_instances = getattr(self.process, state_name)
        for idx, state_instance in enumerate(proc_state_instances):
            assert state_instance.call_result == self.expected_result[state_name][idx]

    def test_process_composition(self):
        self.process()

        for state_name in self.expected_result:
            self.check_state(state_name)
