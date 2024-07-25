"""
Nullifying decorators.
"""

from functools import wraps
from typing import Callable

def null_decorator(func: Callable) -> Callable:
    """
    A decorator that does nothing.

    Parameters
    ----------
    func :
        The function to be decorated.

    Returns
    -------
    None

    """


    @wraps(func)
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)

    return wrapper


def nullify_decorator(decorator: Callable) -> Callable:
    """
    Nullifies a decorator.

    Parameters
    ----------
    decorator :
        The decorator to be nullified.

    Returns
    -------
    Callable :
        A null decorator.

    """
    return null_decorator
