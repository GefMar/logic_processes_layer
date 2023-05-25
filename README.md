# logic_processors

A set of classes is provided for implementing business logic with a shared context.

The base class BaseProcess provides a convenient way to execute logic before and after the main process.

example:

use simple functions for pre_run and post_run
In this case, the context is not available for the auxiliary functions.

```python
import dataclasses
from logic_processors import BaseProcess

def sub_process():
    return "run sub_process"

@dataclasses.dataclass
class MyClass(BaseProcess):
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
from logic_processors import BaseProcess
from logic_processors.context import BaseProcessContext


class BaseSubProcess:
    allow_context = True

    def __call__(self, context: BaseProcessContext):
        return "return result BaseSubProcess"


@dataclasses.dataclass
class MyClass(BaseProcess):
    some: int
    post_run = [BaseSubProcess(), ]
    pre_run = [lambda: "Return pre_run unit result", BaseSubProcess()]

    def run(self):
        return "Result"
process = MyClass(some=1)
process()
```

each child of `BaseProcess` has a `process_result` attribute which is an instance of the `ProcessResult` class
also you can override the context class by setting the `context_class` attribute

```python
import dataclasses
from logic_processors import BaseProcess
from logic_processors.context import BaseProcessContext

class CustomContext(BaseProcessContext):
    def some_method(self):
        return "some_method"

class BaseSubProcess:
    allow_context = True

    def __call__(self, context: BaseProcessContext):
        return "return result BaseSubProcess"


@dataclasses.dataclass
class MyClass(BaseProcess):
    some: int
    post_run = [BaseSubProcess(), ]
    pre_run = [lambda: "Return pre_run unit result", BaseSubProcess()]
    context_class = CustomContext

    def run(self):
        return "Result"
process = MyClass(some=1)
process()
results = process.process_result
```
