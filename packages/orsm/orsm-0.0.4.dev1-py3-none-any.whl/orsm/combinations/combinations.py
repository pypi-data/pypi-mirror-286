"""
Handling combinations.
"""

import itertools
from orsm.variables.variables import variable_names_and_objects
from typing import Iterable, List


def all_combinations(iterable: Iterable, *, min_length: int = None, max_length: int = None) -> List[Iterable]:
    """
    Generates the possible cross product of combinations.

    Example
    -------
        >>> all_combinations(["a","b","c"])
        [(),
         ('a',),
         ('b',),
         ('c',),
         ('a', 'b'),
         ('a', 'c'),
         ('b', 'c'),
         ('a', 'b', 'c')]

    Parameters
    ----------
    iterable :
        Object to iterate over.
    min_length :
        Minimum length of combinations.
    max_length :
        Maximum length of combinations.

    Returns
    -------
    List[Iterable]:
        The cross product of combinations.
    """
    for variable, value in variable_names_and_objects(max_length, min_length):
        if value is not None:
            assert isinstance(value, int) and value >= 0, f"The {variable = } needs to be a positive integer, not {value = }"
    if all([i is not None for i in [min_length, max_length]]):
        assert min_length <= max_length, f"The bounding lengths contradict: {max_length = } and {min_length = }"
    size = 0
    reached_max_size = False

    while (max_length is not None and size <= max_length) or (max_length is None and not reached_max_size):
        if max_length is None:
            # We will have to determine when to stop
            iterable_size = len(iterable)
            reached_max_size = (size == iterable_size)
        if min_length is None or size >= min_length:
            yield from itertools.combinations(iterable, size)
        size += 1


def all_kwarg_combinations(*, keys: List, values: List, min_length:int=None, max_length:int=None) -> List[Iterable]:
    """
    For a list of keys and values it produces
    all the unique combinations of key-value pairings.

    Notes
    -----
    This is quite useful in unit tests for combinations of possible
    combinations.

    Example
    -------
        >>> all_kwarg_combinations(keys=["a", "b"], values=[1, 2])
        [{},
         {'a': 1},
         {'a': 2},
         {'b': 1},
         {'b': 2},
         {'a': 1, 'b': 1},
         {'a': 1, 'b': 2},
         {'a': 2, 'b': 1},
         {'a': 2, 'b': 2}]



    Parameters
    ----------
    keys :
        The keys to use.
    values :
        The values to use.
    min_length :
        The minimum length of combinations.
    max_length :
        The maximum length of combinations.

    Returns
    -------
    List[Iterable]:
        The cross product of keys and values.
    """
    individual_pairings = [list(itertools.product([key], values)) for key in keys]
    combinations = all_combinations(individual_pairings, min_length=min_length, max_length=max_length)
    yield from (dict(kwarg) for combination in combinations for kwarg in itertools.product(*combination))
