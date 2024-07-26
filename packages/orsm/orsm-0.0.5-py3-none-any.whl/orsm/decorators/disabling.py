"""
Decorators and things.
"""

from orsm.logger.logger import log as logging
from functools import wraps
import traceback
from typing import Callable
from orsm.decorators.nullifying import nullify_decorator, null_decorator


def disable_decorator(should_disable: bool | Callable, /, *predicate_args, reason: str = None, notify: bool = True, **predicate_kwargs) -> Callable:
    """
    Disable a decorator if a condition is met.

    Parameters
    ----------
    should_disable :
        A bool or predicate function to determine if the decorator should be disabled.
    predicate_args :
        Positional combinations to provide to the predicate function.
    reason :
        An reason to explain why the predicate might have been disabled.
    notify :
        Whether we should notify the user when the predicate has been disabled.
    predicate_kwargs :
        Keyword combinations to provide to the predicate function.

    Returns
    -------
    Callable:
        The conditional decorator.
    """
    location = traceback.extract_stack()[-2]

    def notification(decorator):
        if notify:
            logging.debug(f"Disabling the decorator: {decorator.__name__} (decoration at {location.filename}:{location.lineno}) because: {reason}")

    def _nullify_decorator(decorator):
        notification(decorator)
        return nullify_decorator(null_decorator)

    # For "static" condition checking.
    if isinstance(should_disable, bool):
        return _nullify_decorator if should_disable else null_decorator

    # For "runtime" condition checking.
    assert callable(should_disable), f"Require a callable predicate: {should_disable =}"

    def conditionally_null_decorator(decorator):
        enabled_decorator = disable_decorator(False, reason=reason, notify=False)(decorator)
        disabled_decorator = disable_decorator(True, reason=reason, notify=False)(decorator)

        def conditional_decorator(func):
            @wraps(func)
            def wrapper(*args, **kwargs):
                logging.debug("Inside the conditional decorator")
                runtime_disable = should_disable(*predicate_args, **predicate_kwargs)
                if runtime_disable:
                    notification(decorator)
                dec_func = disabled_decorator(func) if runtime_disable else enabled_decorator(func)
                return dec_func(*args, **kwargs)

            return wrapper

        return conditional_decorator

    return conditionally_null_decorator
