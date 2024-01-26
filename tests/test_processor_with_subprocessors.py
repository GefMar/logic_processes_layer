from __future__ import annotations

from tests.examples.processors.symple import SympleProcessor
from tests.examples.sub_processors import SympleSubprocessor


def make_symple_subprocessor(cls_name):
    return type(cls_name, (SympleSubprocessor,), {})


class ProcessorWithSubprocess(SympleProcessor):
    pre_run = tuple(make_symple_subprocessor(f"Subprocessor{idx}")() for idx in range(2))  # noqa: WPS221
    post_run = tuple(make_symple_subprocessor(f"Subprocessor{idx}")() for idx in range(2, 5))  # noqa: WPS221


class TestProcessorWithSubprocess:
    def setup_method(self):
        self.processor = ProcessorWithSubprocess()

    def check_state(self, results, state_name):
        proc_state_instances = getattr(self.processor, state_name)
        result_state = getattr(results, state_name)
        assert isinstance(result_state, dict), state_name
        assert len(proc_state_instances) == len(result_state), state_name
        for state_itm in proc_state_instances:
            assert result_state[state_itm] == state_itm.__class__.__name__, state_name

    def test_process_result(self):
        self.processor()
        results = self.processor.results
        assert results.run == self.processor.__class__.__name__
        for state_name in ("pre_run", "post_run"):
            self.check_state(results, state_name)
