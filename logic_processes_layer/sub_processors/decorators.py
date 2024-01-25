from __future__ import annotations


__all__ = ("call_subprocess",)

from functools import wraps
import typing


def call_subprocess(sub_process_call: typing.Callable) -> typing.Callable:
    @wraps(sub_process_call)
    def sub_process_call_wrapper(self):
        self.call_result = sub_process_call(self)
        return self.call_result

    return sub_process_call_wrapper
