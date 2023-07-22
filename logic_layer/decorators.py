__all__ = (
    "make_run",
    "run_subprocesses",
)

import typing
from functools import wraps

from . import context


def run_subprocesses(processor: typing.Callable, context_instance: "context.BaseProcessorContext"):
    kwargs = {}
    if getattr(processor, "allow_context", False):
        processor.context = context_instance  # type: ignore
        kwargs["context"] = context_instance
    return processor(**kwargs)


def make_run(run_func):
    @wraps(run_func)
    def run_wrapper(self, *args, **kwargs):
        for pre_proc in self.pre_run:
            self.results.pre_run[pre_proc] = run_subprocesses(pre_proc, self.context)
        self.results.run = run_func(self, *args, **kwargs)
        for post_proc in self.post_run:
            self.results.post_run[post_proc] = run_subprocesses(post_proc, self.context)
        return self.results.run

    return run_wrapper
