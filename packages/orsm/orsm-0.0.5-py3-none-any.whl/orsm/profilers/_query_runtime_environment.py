"""
Tools for querying the runtime environment.
"""

import inspect


def is_in_debugger() -> bool:
    """
    Queries if a debugger being used.

    Returns
    -------
    bool

    """
    # Taken from https://stackoverflow.com/a/338391/5134817
    for frame in inspect.stack():
        if frame[1].endswith("pydevd.py"):
            return True
    return False
