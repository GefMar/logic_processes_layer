from __future__ import annotations

from unittest.mock import Mock

from logic_processes_layer import BaseProcessor, BaseProcessorContext

from .examples.sub_processors import SimpleSubprocessor


class TestSimpleSubprocessor:
    def setup_method(self):
        self.context = BaseProcessorContext(process=Mock(spec=BaseProcessor))
        self.subprocessor = SimpleSubprocessor()
        self.subprocessor.context = self.context

    def test_call(self):
        result = self.subprocessor()
        assert result == self.subprocessor.__class__.__name__
        assert self.subprocessor.call_result == result
