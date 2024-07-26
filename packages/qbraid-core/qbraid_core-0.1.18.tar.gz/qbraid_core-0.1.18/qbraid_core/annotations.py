# Copyright (c) 2024, qBraid Development Team
# All rights reserved.

"""
Module defining function annotations (e.g. decorators) used in qbraid-core.

"""
import functools
import warnings
from typing import Any, Callable, Optional


def deprecated(func: Any) -> Any:
    """
    This decorator is used to mark functions as deprecated.
    It will result in a warning being emitted when the function is used.

    """

    @functools.wraps(func)
    def new_func(*args, **kwargs):
        warnings.simplefilter("always", DeprecationWarning)
        warnings.warn(
            f"Call to deprecated function {func.__name__}.",
            category=DeprecationWarning,
            stacklevel=2,
        )
        warnings.simplefilter("default", DeprecationWarning)
        return func(*args, **kwargs)

    return new_func


def deprecated_message(message: Optional[str] = None) -> Callable:
    """
    Decorator to mark functions as deprecated with an optional custom message.

    This decorator emits a warning when the decorated function is used, optionally
    including a specific guidance message.

    Args:
        message (Optional[str]): A custom message to include in the deprecation warning,
            providing specific guidance or alternatives.

    Returns:
        Callable: A decorator that wraps the function and shows a deprecation warning when
            the function is called.
    """

    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def new_func(*args, **kwargs) -> Any:
            warnings.simplefilter("always", DeprecationWarning)
            warning_message = f"Call to deprecated function {func.__name__}."
            if message:
                warning_message += " " + message
            warnings.warn(
                warning_message,
                category=DeprecationWarning,
                stacklevel=2,
            )
            warnings.simplefilter("default", DeprecationWarning)
            return func(*args, **kwargs)

        return new_func

    return decorator
