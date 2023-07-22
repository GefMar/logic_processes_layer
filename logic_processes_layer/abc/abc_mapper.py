import dataclasses
import typing
from abc import ABC, abstractmethod

from logic_layer.structures import AttrsData


@dataclasses.dataclass
class AbstractMapper(ABC):
    start_attrs: AttrsData

    def __call__(self, prev_results) -> AttrsData:
        return self.build_attrs_strategy(prev_results)

    @abstractmethod
    def build_attrs_strategy(self, prev_results: typing.Any) -> AttrsData:
        ...
