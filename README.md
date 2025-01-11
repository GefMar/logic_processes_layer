# logic_processes_layer

The `logic_processes_layer` package provides a framework for structuring the logic of your Python programs in a flexible and maintainable way. It allows you to divide your program logic into separate processes, each of which can be easily modified or replaced without affecting the others.

## Features

- **Separation of concerns**: Each process in your program can be developed and tested independently.
- **Flexibility**: Processes can be easily added, removed, or modified without affecting the rest of your program.
- **Ease of testing**: By isolating each process, you can write more focused and effective unit tests.

## Installation

You can install the `logic_processes_layer` package via pip:

```bash
pip install logic-processes-layer
```

## New Features

- **ProcessAsSubprocess**: Use any process as a subprocess.
- **InitMapper**: Simplifies process initialization by mapping attributes from the context to processor arguments.
- **ProcessAttr**: Retrieve attributes from the process context or directly from the process.
- **Conditions Support**: Add logical conditions to control the execution of processes.
  - **AttrCondition**: Define conditions based on attributes of the process or context.
  - **FunctionCondition**: Wrap custom functions as conditions.
  - **Logical Operators**: Combine conditions with `&` (AND), `|` (OR), `~` (NOT), and `^` (XOR) for advanced logic.
- [Examples](tests/examples) of how to use the `logic_processes_layer` package.

### Using `ProcessAttr` and `InitMapper`

In many cases, you may want to initialize your process with specific values drawn from the current context or from the process itself. To simplify this, the package provides two utilities: `ProcessAttr` and `InitMapper`.

#### `ProcessAttr`

`ProcessAttr` makes it easy to fetch required attributes from the context or from the process. This class can be declared as generic (i.e., `Generic[AttrResultT]`) to enable strict typing if needed:

```python
import dataclasses
from operator import attrgetter
import typing


AnyTupleT = typing.Tuple[typing.Any, ...]
DictStrAnyT = typing.Dict[str, typing.Any]
AttrResultT = typing.TypeVar("AttrResultT")


@dataclasses.dataclass
class ProcessAttr(typing.Generic[AttrResultT]):
    attr_name: str
    from_context: bool = dataclasses.field(default=False)
    cast: typing.Callable[[typing.Any], AttrResultT] = dataclasses.field(default=lambda arg: arg)

    def get_value(self, context: typing.Any) -> AttrResultT:  # noqa: ANN401
        source = (context.process, context)[self.from_context]
        source_value = attrgetter(self.attr_name)(source)
        return self.cast(source_value)

```

- **`attr_name`**: The attribute name to retrieve.
- **`from_context`**: A flag indicating whether to take the attribute from `context.process` (default) or directly from `context`.
- **`cast`**: A callable to cast (transform) the retrieved value into a desired type (default simply returns the original value).

#### `InitMapper`

`InitMapper` helps you gather the needed `args` and `kwargs` for initializing a process or any other object. If certain values should come from the context, you can use `ProcessAttr` objects for those parameters.

Example:

```python
from typing import Any
import dataclasses

AnyTupleT = tuple[Any, ...]
DictStrAnyT = dict[str, Any]

@dataclasses.dataclass
class InitMapper:
    _init_attrs: tuple[Any, ...] = ()
    _init_kwargs: dict[str, Any] = dataclasses.field(default_factory=dict)

    def __call__(self, context: Any) -> tuple[AnyTupleT, DictStrAnyT]:
        args = self._load_args(context)
        kwargs = self._load_kwargs(context)
        return args, kwargs

    def _load_args(self, context: Any) -> AnyTupleT:
        args = []
        for init_attr in self._init_attrs:
            value = init_attr
            if isinstance(init_attr, ProcessAttr):
                value = init_attr.get_value(context)
            args.append(value)
        return tuple(args)

    def _load_kwargs(self, context: Any) -> DictStrAnyT:
        kwargs = {}
        for key, value in self._init_kwargs.items():
            init_value = value
            if isinstance(value, ProcessAttr):
                init_value = value.get_value(context)
            kwargs[key] = init_value
        return kwargs
```

- **`_init_attrs`**: A tuple of positional arguments to be passed to the constructor.
- **`_init_kwargs`**: A dictionary of keyword arguments (key is the argument name, value is either a fixed value or a `ProcessAttr` to load from the context).

##### Usage Example

```python
# Suppose we have a class MyProcessor that needs two arguments: name (str) and age (int).

class MyProcessor:
    def __init__(self, name: str, age: int) -> None:
        self.name = name
        self.age = age

    def run(self):
        print(f"Name: {self.name}, Age: {self.age}")

# Assume the required values are stored in context.process, for example:
# context.process.name = "Alice", context.process.age = 30

mapper = InitMapper(
    _init_attrs=(),
    _init_kwargs={
        "name": ProcessAttr[str]("name"),
        "age": ProcessAttr[int]("age")
    }
)

# When mapper(context) is called, it will build (args, kwargs),
# where args is an empty tuple and kwargs is {"name": "Alice", "age": 30}.

args, kwargs = mapper(context)
processor = MyProcessor(*args, **kwargs)
processor.run()  # Prints: Name: Alice, Age: 30
```

In this way, `InitMapper` provides a flexible mechanism for assembling parameters for object initialization, while `ProcessAttr` enables you to reference attributes from either the context or the process.

---

## Basic Usage

Below is a basic example of how to use the `logic_processes_layer` package, creating a process with pre- and post-run steps:

```python
import dataclasses
from logic_processes_layer import BaseProcessor, BaseSubprocessor

class MyPreProcess(BaseSubprocessor):

    def __call__(self):
        print("This is the pre-run step.")
        self.context.data['message'] = "Hello, World!"

class MyPostProcess(BaseSubprocessor):
    allow_context = True

    def __call__(self):
        print("This is the post-run step.")
        print(self.context.data['message'])

@dataclasses.dataclass
class MyClass(BaseProcessor):
    pre_run = (MyPreProcess(), )
    post_run = (MyPostProcess(), )

    def run(self):
        print("This is the run step.")

process = MyClass()
process()
```

## Advanced Example: Processing Data from Multiple APIs

This example demonstrates how to use the `logic_processes_layer` package to process data from multiple APIs. The process is divided into three steps: pre-run, run, and post-run.

### Pre-run

```python
class PreProcess1(BaseSubprocessor):
    def __call__(self):
        # Assuming a GET request to the first API
        response1 = requests.get('http://api1.com')
        return response1.json()

class PreProcess2(BaseSubprocessor):
    def __call__(self):
        # Assuming a GET request to the second API
        response2 = requests.get('http://api2.com')
        return response2.json()
```

### Run

```python
def run(self):
    # Retrieve and process the data from the pre_run step
    api1_response = self.results.pre_run[self.pre_run[0]]
    api2_response = self.results.pre_run[self.pre_run[1]]
    result = process_data(api1_response, api2_response)  # process_data is hypothetical
    return result
```

### Post-run

```python
class PostProcess(BaseSubprocessor):
    def __call__(self):
        result = context.process.results.run
        # Send the result to another API
        response3 = requests.post('http://api3.com', data=result)
        return response3.json()
```

## Advanced Example: ChainPipeline with Custom Mapper and Steps

In this example, we dive deeper into how `ChainPipeline`, `AbstractMapper`, and `AbstractPipelineStep` can be used to create more complex processes:

1. **Processors**: Three processors (`ProcessorOne`, `ProcessorTwo`, `ProcessorThree`), each performing a certain task and returning a result.
2. **Mappers**: Three mappers (`MapperOne`, `MapperTwo`, `MapperThree`) to build attribute dictionaries to be passed into the processors.
3. **Steps**: Three steps (`StepOne`, `StepTwo`, `StepThree`), each using one of the processors and one of the mappers.
4. **ChainPipeline**: A `ChainPipeline` that combines all three steps into a sequence.

```python
import dataclasses

from logic_processes_layer import BaseProcessor
from logic_processes_layer.abc.abc_chain import AbstractChainPipeline
from logic_processes_layer.abc.abc_mapper import AbstractMapper
from logic_processes_layer.abc.abc_pipeline import AbstractPipelineStep
from logic_processes_layer.structures import AttrsData


@dataclasses.dataclass
class ProcessorOne(BaseProcessor):
    data_for_init: str

    def run(self):
        return {"one": 1}


@dataclasses.dataclass
class ProcessorTwo(BaseProcessor):
    data_for_init: str
    data_for_init_two: int

    def run(self):
        return None


class ProcessorThree(BaseProcessor):
    def run(self):
        return "RESULT THREE"


class MapperOne(AbstractMapper):
    def build_attrs_strategy(self, prev_results):
        return self.start_attrs


class MapperTwo(AbstractMapper):
    def build_attrs_strategy(self, prev_results):
        return AttrsData(
            args=self.start_attrs.args,
            kwargs={"data_for_init_two": prev_results["one"]}
        )


class MapperThree(AbstractMapper):
    def build_attrs_strategy(self, prev_results):
        return AttrsData(
            args=tuple(),
            kwargs={}
        )


class StepOne(AbstractPipelineStep):
    processor = ProcessorOne
    attr_mapper_cls = MapperOne


class StepTwo(AbstractPipelineStep):
    processor = ProcessorTwo
    attr_mapper_cls = MapperTwo


class StepThree(AbstractPipelineStep):
    processor = ProcessorThree
    attr_mapper_cls = MapperThree


class ChainPipeline(AbstractChainPipeline):
    step_classes = (StepOne, StepTwo, StepThree)
    start_attrs = AttrsData(args=("DATA FOR INIT",), kwargs={})


pipeline = ChainPipeline()
result = pipeline()
print(result)
```
