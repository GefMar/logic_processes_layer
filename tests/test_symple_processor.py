from __future__ import annotations

from tests.examples.processors.symple import SympleProcessor


class TestSympleProcessor:
    def setup_method(self):
        self.processor = SympleProcessor()

    def test_run(self):
        assert self.processor.run() == self.processor.__class__.__name__

    def test_call(self):
        assert self.processor() == self.processor.__class__.__name__

    def test_results(self):
        result = self.processor()
        assert self.processor.results.run == result
        assert isinstance(self.processor.results.pre_run, dict)
        assert isinstance(self.processor.results.post_run, dict)
        assert not self.processor.results.pre_run
        assert not self.processor.results.post_run
