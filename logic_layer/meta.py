__all__ = ("MetaProcessor",)

from .decorators import make_run


class MetaProcessor(type):
    def __new__(cls, name, bases, attrs):
        attrs["run"] = make_run(attrs["run"])
        attrs["pre_run"] = attrs.get("pre_run", [])
        attrs["post_run"] = attrs.get("post_run", [])
        return super().__new__(cls, name, bases, attrs)
