# Create your own profiler

from sipro import Profiler

my_profiler = Profiler()

# Import the default profiler

from sipro import default_profiler as profiler

# Context based profiling

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

# Function based profiling
profiler.clear()

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

# Print the results

print(profiler)

# Get python dict representation of the profiler

print(profiler.dict())

# Clear the profiler

profiler.clear()
