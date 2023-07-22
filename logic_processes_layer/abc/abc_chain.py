import typing
from abc import ABC, abstractmethod

from ..structures import AttrsData
from .abc_pipeline import AbstractPipelineStep


class AbstractChainPipeline(ABC):
    def __call__(self):
        return self.run()

    @property
    @abstractmethod
    def step_classes(self) -> typing.List[typing.Type[AbstractPipelineStep]]:
        ...

    @property
    @abstractmethod
    def start_attrs(self) -> AttrsData:
        ...

    def run(self):
        result = None
        for step_cls in self.step_classes:
            step: AbstractPipelineStep = step_cls(start_attrs=self.start_attrs)
            result = step(result)
        return result
