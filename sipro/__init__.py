from __future__ import annotations
 
from contextlib import contextmanager
from time import time
from typing import Callable
import json

class TimeEntry:
    sum: float = 0
    start_time: float | None = None
    children: dict[str, TimeEntry]
 
    def __init__(self):
        self.sum = 0
        self.children = {}
 
    def get(self, path: list[str]) -> TimeEntry:
        """
        Get the TimeEntry at the given path, creating it if it doesn't exist.

        Args:
            path (list[str]): The path to the TimeEntry to get.
        
        Returns:
            TimeEntry: The TimeEntry at the given path.
        """

        if not path:
            return self

        else:
            child_name = path[0]
            rest = path[1:]
 
            if child_name not in self.children:
                self.children[child_name] = TimeEntry()
 
            return self.children[child_name].get(rest)
 
    def start(self) -> None:
        """
        Start the timer for this TimeEntry.

        Returns:
            None
        """

        self.start_time = time()
 
    def stop(self) -> None:
        """
        Stop the timer for this TimeEntry.

        Returns:
            None
        """
        self.sum += time() - self.start_time
        self.start_time = None

    def commit(self) -> None:
        """
        Commit the current time to the sum without stopping the timer.

        Returns:
            None
        """

        if self.start_time is not None:
            now = time()
            self.sum += now - self.start_time
            self.start_time = now
    
    def str(self, whitespace = '', parent_time = None, total_time = None) -> str:
        """
        Get a string representation of the TimeEntry.

        Args:
            whitespace (str): The whitespace to use for indentation.
            parent_time (float): The time of the parent TimeEntry.
            total_time (float): The total time of the profiler.
        
        Returns:
            str: The string representation of the TimeEntry.
        """

        self.commit()
 
        # If parent_time is None, we are the root node
        if parent_time is None:
            parent_time = self.sum
            total_time = self.sum

        percent_of_parent = self.sum * 100 / parent_time
        percent_of_total = self.sum * 100 / total_time
        output = f'{percent_of_parent:2.1f}% ({percent_of_total:2.1f}%)\n'

        if not self.children:
            return output

        child_sum = 0.0
        child_whitespace = whitespace + "  "
        max_child_name_length = max(len(name) for name in self.children.keys())
        
        for name, child in self.children.items():
            child_output = child.str(child_whitespace, self.sum, total_time)
            extra_whitespace = ' ' * (max_child_name_length - len(name))
            output += f'{whitespace}{name}:{extra_whitespace} {child_output}'
            child_sum += child.sum

        rest_sum = max(0, self.sum - child_sum)
        rest_percent_of_parent = rest_sum * 100 / self.sum
        rest_percent_of_total = rest_sum * 100 / total_time
        extra_whitespace = ' ' * (max_child_name_length - 3)
        output += f'{whitespace}...:{extra_whitespace} {rest_percent_of_parent:2.1f}% ({rest_percent_of_total:2.1f}%)\n'

        return output
    
    def dict(self) -> dict:
        """
        Get a dictionary representation of the TimeEntry.

        Returns:
            dict: The dictionary representation of the TimeEntry.
        """

        self.commit()

        return dict(
            sum = self.sum,
            children = {
                name: child.dict() for name, child in self.children.items()
            }
        )

class Profiler:
    tree: TimeEntry
    current_path: list[str]
 
    def __init__(self) -> None:
        self.tree = TimeEntry()
        self.tree.start()
        self.current_path = []

    def clear(self) -> None:
        """
        Clear the profiler.

        Returns:
            None
        """

        self.tree = TimeEntry()
        
        for path_end in range(len(self.current_path) + 1):
            path = self.current_path[:path_end]
            self.tree.get(path).start()

    def wrap(self, fn: Callable, name: str | None = None):
        """
        Wrap a function with the profiler.

        Args:
            fn (Callable): The function to wrap.
            name (str): The name of the function.

        Returns:
            Callable: The wrapped function.
        """

        if name is None:
            name = fn.__name__
 
        def wrapped(*args, **kwargs):
            with self(name):
                return fn(*args, **kwargs)
            
        return wrapped
 
    @contextmanager
    def __call__(self, name: str):
        """
        Context manager for the profiler.

        Args:
            name (str): The name of the node.

        Yields:
            None
        """

        self.current_path.append(name)
        node = self.tree.get(self.current_path)
        node.start()
        yield
        node.stop()
        self.current_path.pop()
 
    def __str__(self) -> str:
        return self.tree.str()

    def dict(self) -> dict:
        return self.tree.dict()
    
    def toJSON(self) -> str:
        """
        Get a JSON representation of the profiler.

        Returns:
            str: The JSON representation of the profiler.
        """

        return json.dumps(self.dict())

default_profiler = Profiler()