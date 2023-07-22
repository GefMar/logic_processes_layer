
# logic_processes_layer

The logic_processes_layer package provides a framework for structuring the logic of your Python programs in a flexible and maintainable way. It allows you to divide your program logic into separate processes, each of which can be easily modified or replaced without affecting the others.

## Features

- **Separation of concerns**: Each process in your program can be developed and tested independently.

- **Flexibility**: Processes can be easily added, removed, or modified without affecting the rest of your program.

- **Ease of testing**: By isolating each process, you can write more focused and effective unit tests.

## Installation

You can install the logic_processes_layer package via pip:


## Basic Usage

Here is a basic example of how to use the logic_processes_layer package:

```python
import dataclasses
from logic_processes_layer import BaseProcessor, BaseProcessorContext

class MyPreProcess:
    allow_context = True

    def __call__(self, context: BaseProcessorContext):
        print("This is the pre-run step.")
        context.data['message'] = "Hello, World!"

class MyPostProcess:
    allow_context = True

    def __call__(self, context: BaseProcessorContext):
        print("This is the post-run step.")
        print(context.data['message'])

@dataclasses.dataclass
class MyClass(BaseProcessor):
    pre_run = [MyPreProcess()]
    post_run = [MyPostProcess()]

    def run(self):
        print("This is the run step.")

process = MyClass()
process()
```

In this example, `MyClass` is a processor that has a pre-run step, a run step, and a post-run step. The pre-run step is performed by `MyPreProcess`, which saves a message in the context. The run step is defined in `MyClass` itself. The post-run step is performed by `MyPostProcess`, which retrieves the message from the context and prints it.

## Advanced Example: Processing Data from Multiple APIs

This example demonstrates how to use the logic_processes_layer package to process data from multiple APIs. The process is divided into three steps: pre-run, run, and post-run.

### Pre-run

In the pre-run step, we have two subprocesses, each making a GET request to a different API. The responses from these requests are stored in `self.results.pre_run`, and will be used in the main run step.

```python
class PreProcess1:
    allow_context = True

    def __call__(self, context: BaseProcessorContext):
        # Assuming that we are making a GET request to the first API
        response1 = requests.get('http://api1.com')
        # Return the response
        return response1.json()

class PreProcess2:
    allow_context = True

    def __call__(self, context: BaseProcessorContext):
        # Assuming that we are making a GET request to the second API
        response2 = requests.get('http://api2.com')
        # Return the response
        return response2.json()
```

### Run

In the run step, we process the data from the pre-run step. The results from the two pre-run subprocesses are retrieved from `self.results.pre_run`, and we assume that these results are combined in some way by a hypothetical function `process_data`.

```python
def run(self):
    # Process the data from the pre_run step
    api1_response = self.results.pre_run[self.pre_run[0]]
    api2_response = self.results.pre_run[self.pre_run[1]]
    # Assume that we are combining the data from the two APIs in some way
    result = process_data(api1_response, api2_response)  # process_data is a hypothetical function
    # Return the result
    return result
```

### Post-run

In the post-run step, we have a subprocess that sends the result from the run step to another API. The response from this POST request is stored in `self.results.post_run`.

```python
class PostProcess:
    allow_context = True

    def __call__(self, context: BaseProcessorContext):
        result = context.process.results.run
        # Send the result to another API
        response3 = requests.post('http://api3.com', data=result)
        # Return the response
        return response3.json()
```

Finally, we create an instance of our class and call it to execute the process:

```python
process = MyClass()
process()
```

Please note that you need to replace `'http://api1.com'`, `'http://api2.com'`, and `'http://api3.com'` with the actual API URLs, and implement the `process_data` function that processes the data from the first two APIs.

## Advanced Example: ChainPipeline with Custom Mapper and Steps

In this example, we delve deeper into the use of `logic_processes_layer` and demonstrate how `ChainPipeline`, `AbstractMapper`, and `AbstractPipelineStep` can be used to create more complex processes.

1. **Processors**: We have three processors, `ProcessorOne`, `ProcessorTwo`, and `ProcessorThree`. Each of these processors performs a certain task and returns a result.

2. **Mappers**: We then have three mappers, `MapperOne`, `MapperTwo`, and `MapperThree`. These mappers are used to build attribute dictionaries that are passed into the processors.

3. **Steps**: We then have three steps, `StepOne`, `StepTwo`, and `StepThree`. Each of these steps uses one of the processors and one of the mappers.

4. **ChainPipeline**: Finally, we have a `ChainPipeline` that combines all three steps into one sequence.

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
In this example, we create an instance of `ChainPipeline` and call it to execute the whole process.
The result of each step is passed to the next step via the mapper,
allowing each step to use the result of the previous step when building its attributes.
