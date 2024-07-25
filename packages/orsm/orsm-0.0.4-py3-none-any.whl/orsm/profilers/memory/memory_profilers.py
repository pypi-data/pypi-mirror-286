"""
Memory profiler.
"""
from functools import wraps
import tracemalloc
from orsm.logger.logger import log as logging
from typing import Callable


class MemoryProfiler:
    # A memory profiler to give a similar interface to LineProfiler

    def __init__(self):
        self.max_usages = {}

    def store(self, *, name: str, peak: int):
        self.max_usages[name] = max(peak, self.max_usages[name]) if name in self.max_usages else peak

    def print_stats(self):
        print(f"\n\nMemory Usage\n" + "=" * 80)
        for name, peak in sorted(self.max_usages.items(), key=lambda i: i[1]):
            print(f"Maximal memory usage for {name}: Peak={peak / 10 ** 6}MB")


memory_profiler = MemoryProfiler()


def profile_memory(func: Callable) -> Callable:
    """
    Decorator to profile a function's memory usage.

    Parameters
    ----------
    func :
        The function to be profiled.

    Returns
    -------
    Callable:
        The decorated function.

    """

    @wraps(func)
    def wrapper(*args, **kwargs):
        tracemalloc.start()
        result = func(*args, **kwargs)
        current, peak = tracemalloc.get_traced_memory()
        tracemalloc.stop()
        logging.debug(f'Memory usage for {func.__name__}: Current={current / 10 ** 6}MB, Peak={peak / 10 ** 6}MB')
        memory_profiler.store(name=func.__name__, peak=peak)
        return result

    return wrapper
