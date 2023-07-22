# logic_processors

A set of classes is provided for implementing business logic with a shared context.

The base class BaseProcess provides a convenient way to execute logic before and after the main process.

example:

use simple functions for pre_run and post_run
In this case, the context is not available for the auxiliary functions.

```python
import dataclasses
from logic_layer import BaseProcessor

def sub_process():
    return "run sub_process"

@dataclasses.dataclass
class MyClass(BaseProcessor):
    some: int
    pre_run = [lambda: "Return pre_run unit result", sub_process]

    def run(self):
        return "Result"

process = MyClass(some=1)
process.run()

```

To pass the context, use objects with a specific class where the allow_context attribute is defined as True.
Additionally, all child classes of BaseProcess are callable.

```python
import dataclasses
from logic_layer import BaseProcessor
from logic_layer.context import BaseProcessorContext


class BaseSubProcess:
    allow_context = True

    def __call__(self, context: BaseProcessorContext):
        return "return result BaseSubProcess"


@dataclasses.dataclass
class MyClass(BaseProcessor):
    some: int
    post_run = [BaseSubProcess(), ]
    pre_run = [lambda: "Return pre_run unit result", BaseSubProcess()]

    def run(self):
        return "Result"
process = MyClass(some=1)
process()
```

each child of `BaseProcessor` has a `results` attribute which is an instance of the `ProcessorResult` class
also you can override the context class by setting the `context_class` attribute

```python
import dataclasses
from logic_layer import BaseProcessor
from logic_layer.context import BaseProcessorContext


class CustomContext(BaseProcessorContext):
    def some_method(self):
        return "some_method"


class BaseSubProcess:
    allow_context = True

    def __call__(self, context: BaseProcessorContext):
        return "return result BaseSubProcess"


@dataclasses.dataclass
class MyClass(BaseProcessor):
    some: int
    post_run = [BaseSubProcess(), ]
    pre_run = [lambda: "Return pre_run unit result", BaseSubProcess()]
    context_class = CustomContext

    def run(self):
        return "Result"


process = MyClass(some=1)
process()
results = process.results
```
