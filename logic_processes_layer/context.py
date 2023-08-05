__all__ = ("BaseProcessorContext",)

import dataclasses
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from . import processors


@dataclasses.dataclass
class BaseProcessorContext:
    process: "processors.BaseProcessor"
