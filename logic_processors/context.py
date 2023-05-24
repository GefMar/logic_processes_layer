__all__ = ("BaseProcessContext",)

import dataclasses

from . import processors


@dataclasses.dataclass
class BaseProcessContext:
    process: "processors.BaseProcess"
