![SiPro Logo](./imgs/logo_small.png)

Nothing to see here...

...just a very simple python profiler

## Examples

### With context manager

#### Code

```python
# Use default profiler
from sipro import default_profiler as profiler

# Create your own profiler
from sipro import Profiler

my_profiler = Profiler()

with profiler('my loop'):
    for i in range(1000):
        pass

with profiler('nested parent'):
    for i in range(50):
        pass

    with profiler('nested child 1'):
        for i in range(50):
            pass

    with profiler('nested child 2'):
        for i in range(50):
            pass

print(profiler)
```

#### Output
```
100.0% (100.0%)
my loop:       37.4% (37.4%)
nested parent: 17.6% (17.6%)
  nested child 1: 14.5% (2.5%)
  nested child 2: 11.3% (2.0%)
  ...:            74.2% (13.0%)
...:           45.0% (45.0%)
```

### With functions

#### Code
```python
from sipro import default_profiler as profiler


@profiler.wrap
def inherit_name():
    for i in range(1000):
        pass

from functools import partial

@partial(profiler.wrap, name='custom_name')
def dont_use_fn_name():
    for i in range(1000):
        pass

    # Functions also nest properly
    inherit_name()

dont_use_fn_name()

print(profiler)
```

#### Output
```
100.0% (100.0%)
custom_name: 71.4% (71.4%)
  inherit_name: 42.2% (30.1%)
  ...:          57.8% (41.3%)
...:         28.6% (28.6%)
```

## Output

There are two ways of getting the output:

1. Cast to string `str(profiler)` - Output same as above
2. Get `dict`, by `profiler.dict()` - Structure:
    ```
    {
        'sum': <time in seconds, float>,
        'children': {
            '<child_name>': {
                ...child values
            }
        }
    }
    ```
