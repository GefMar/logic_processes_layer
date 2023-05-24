__all__ = ("MetaProcessor",)

from .decorators import make_run
from .results import ProcessResult


class MetaProcessor(type):
    def __new__(cls, name, bases, attrs):
        if not attrs.get("run"):
            raise NotImplementedError("run method is required")
        attrs["run"] = make_run(attrs["run"])
        attrs["pre_run"] = attrs.get("pre_run", [])
        attrs["post_run"] = attrs.get("post_run", [])
        attrs["process_result"] = ProcessResult()
        return super().__new__(cls, name, bases, attrs)
