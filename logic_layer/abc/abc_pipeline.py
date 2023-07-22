import dataclasses
import typing
from abc import ABC, abstractmethod

from ..processors import BaseProcessor
from ..structures import AttrsData
from .abc_mapper import AbstractMapper


@dataclasses.dataclass
class AbstractPipelineStep(ABC):
    start_attrs: AttrsData

    def __call__(self, prev_results=None):
        attrs = self.get_mapping_attrs(prev_results)
        return self.processor(*attrs.args, **attrs.kwargs)()

    @property
    @abstractmethod
    def processor(self) -> typing.Type[BaseProcessor]:
        ...

    @property
    @abstractmethod
    def attr_mapper_cls(self) -> typing.Type[AbstractMapper]:
        ...

    @property
    def step_attrs_mapper(self) -> AbstractMapper:
        return self.attr_mapper_cls(start_attrs=self.start_attrs)

    def get_mapping_attrs(self, prev_results) -> AttrsData:
        return self.step_attrs_mapper(prev_results)
