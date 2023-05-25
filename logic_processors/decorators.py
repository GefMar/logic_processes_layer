__all__ = (
    "make_run",
    "run_subprocesses",
)

import typing
from functools import wraps

from . import context


def run_subprocesses(process: typing.Callable, context_instance: "context.BaseProcessContext"):
    kwargs = {}
    if getattr(process, "allow_context", False):
        kwargs["context"] = context_instance
    return process(**kwargs)


def make_run(run_func):
    @wraps(run_func)
    def run_wrapper(self, *args, **kwargs):
        for pre_proc in self.pre_run:
            self.process_result.pre_run[pre_proc] = run_subprocesses(pre_proc, self.context)
        self.process_result.run = run_func(self, *args, **kwargs)
        for post_proc in self.post_run:
            self.process_result.post_run[post_proc] = run_subprocesses(post_proc, self.context)
        return self.process_result.run

    return run_wrapper
