__all__ = ("BaseProcessorContext",)

import dataclasses

from . import processors


@dataclasses.dataclass
class BaseProcessorContext:
    process: "processors.BaseProcessor"
