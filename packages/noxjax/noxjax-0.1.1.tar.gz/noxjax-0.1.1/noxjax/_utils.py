import jax
import jax.numpy as jnp

from ._typecheck import typecheck

__all__ = ["array_summary"]


@typecheck
def array_summary(array: jax.Array, detailed: bool = True) -> str:
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
        if detailed and any_nan(array):
            body.append("nan")

        if any_neg_inf(array):
            body.append("-inf")

        if any_pos_inf(array):
            body.append("+inf")

        # check for constant values
        if is_constant(array):
            body.append(f"const={array.flatten()[0]}")

        if body:
            body = " ".join(body)
            head = f"{head} {body}"

    return head


@jax.jit
def any_nan(array: jax.Array):
    """
    Check if an array has any nan values.

    Parameters:
    ---
    array: jax.Array
        The array to check.

    Returns:
    ---
    bool
        True if the array has nan values, False otherwise.
    """
    return jnp.any(jnp.isnan(array))


@jax.jit
def any_pos_inf(array: jax.Array):
    """
    Check if an array has any positive infinity values.

    Parameters:
    ---
    array: jax.Array
        The array to check.

    Returns:
    ---
    bool
        True if the array has positive infinity values, False otherwise.
    """
    return jnp.any(jnp.isposinf(array))


@jax.jit
def any_neg_inf(array: jax.Array):
    """
    Check if an array has any negative infinity values.

    Parameters:
    ---
    array: jax.Array
        The array to check.

    Returns:
    ---
    bool
        True if the array has negative infinity values, False otherwise.
    """
    return jnp.any(jnp.isneginf(array))


@jax.jit
def is_constant(array: jax.Array):
    """
    Check if an array has constant values.

    Parameters:
    ---
    array: jax.Array
        The array to check.

    Returns:
    ---
    bool
        True if the array has constant values, False otherwise.
    """
    array = jnp.sort(array.flatten())
    return array[0] == array[-1]
