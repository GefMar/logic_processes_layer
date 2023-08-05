from typing import TYPE_CHECKING, Optional

if TYPE_CHECKING:
    from .context import BaseProcessorContext


class BaseSubprocessor:
    context: Optional["BaseProcessorContext"]
    allow_context: bool = True

    def __call__(self, context: "BaseProcessorContext"):
        raise NotImplementedError("Base process run method is required to be implemented")
