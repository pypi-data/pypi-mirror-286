"""
Variable mangling.
"""


from varname.helpers import jsobj
from functools import wraps
from typing import Iterable

def return_dict_items(func, *func_args, **func_kwargs):
    @wraps(func)
    def wrapper(*args, **kwargs):
        # Keywords specified in the function take precedence over those in the wrapper is they clash, so some might need to be dropped.
        _func_kwargs = func_kwargs
        for k in kwargs.keys():
            if k in _func_kwargs:
                _func_kwargs = {i:j for i,j in func_kwargs.items() if i != k}
        return func(*func_args, *args, **kwargs, **_func_kwargs).items()

    return wrapper

def variable_names_and_objects(*args) -> Iterable:
    """
    Will return the names of the variables as entered
    and their underlying objects.

    Examples
    --------

        >>> a, b, c = 1, 2, 3
        >>> for k, v in variable_names_and_objects(a, b, c): print(k, v)
        ("a", 1)
        ("b", 2)
        ("c", 3)


    Parameters
    ----------
    args :
        Variables.

    Returns
    -------
    Iterable:
        The names of the variables and their underlying objects.

    """
    ...

variable_names_and_objects = return_dict_items(jsobj, vars_only=False, frame=2)
