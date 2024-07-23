import functools
from typing import Callable, ParamSpec, TypeVar

import jax
import jax.numpy as jnp

from ._typecheck import typecheck

__all__ = [
    "array_summary",
    "wraps_with_hints",
]


T = TypeVar("T")
P = ParamSpec("P")


@typecheck
def array_summary(array: jax.Array, detailed: bool = False) -> str:
    """
    Summarize an array with its dtype and shape. If detailed is True, it will
    include additional information like the presence of nan, inf and constant
    values.

    Parameters:
    ---
    array: jax.Array
        The array to summarize.

    detailed: bool
        If True, additional information will be included in the summary.
        This includes
        - Presence of nan, inf, -inf, +inf
        - Constant values

    Returns:
    ---
    str
        The summary of the array.
    """
    dtype = array.dtype.str[1:]
    shape = list(array.shape)

    head = f"{dtype}{shape}"
    body = []

    if detailed:
        if detailed and jnp.any(jnp.isnan(array)):
            body.append("nan")

        if jnp.any(jnp.isneginf(array)):
            body.append("-inf")

        if jnp.any(jnp.isposinf(array)):
            body.append("+inf")

        # check for constant values
        if len(jnp.unique(array)) == 1:
            body.append(f"const={array.flatten()[0]}")

        if body:
            body = " ".join(body)
            head = f"{head} {body}"

    return head


def wraps_with_hints(f: Callable[P, T]) -> Callable[
    [Callable[P, T]],
    Callable[P, T],
]:
    """
    Wraps a function with the same signature as the input function. It also
    keeps the docstring and the name of the input function.
    """

    def decorator(g: Callable[P, T]) -> Callable[P, T]:
        return functools.wraps(f)(g)

    return decorator
