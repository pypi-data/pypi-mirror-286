"""
Time profilers.
"""

from line_profiler import LineProfiler
from functools import wraps
from orsm.decorators.disabling import disable_decorator
from orsm.profilers._query_runtime_environment import is_in_debugger
from typing import Callable
time_profiler = LineProfiler()


@disable_decorator(is_in_debugger, reason="Time profiling disabled in debug mode.")  # The debugger used in e.g. Pycharm requires sys.settrace (cf. https://github.com/pyutils/line_profiler/issues/276), but that's what LineProfiler uses and it upsets everything, so we disable this in debug mode.
def profile_time(func: Callable) -> Callable:
    """
    Decorator for profiling the time inside a function.

    Parameters
    ----------
    func :
        The function to be decorated.

    Returns
    -------
    Callable :
        The decorated function.

    Notes
    -----
        Implementations using LineProfiler do not work in
        debug mode, so may be disabled in such cases.
    """
    @wraps(func)
    def profiled_function(*args, **kwargs):
        time_profiler.add_function(func)
        time_profiler.enable_by_count()
        return func(*args, **kwargs)

    return profiled_function
