# Noxjax
Simple pytree module classes for Jax, _strongly inspired_ by [Equinox](https://github.com/patrick-kidger/equinox).
- Referential transparency via strict immutability
- Safe serialization including hyperparameters
- Bound methods and function transformations are also modules
- Auxillary information in key paths for filtered transformations

## Quick Examples
Modules work similar to dataclasses, but with the added benefit of being pytrees. Making them compatible with all Jax function transformations.
```python
import noxjax as nox

class Linear(nox.Module):
    # The __init__ method is automatically generated
    w: jax.Array
    b: jax.Array

    # additional intialization methods via classmethods
    @classmethod
    def init(cls, key, dim_in, dim):
        w = jax.random.normal(key, (dim, dim_in)) * 0.02
        b = jax.numpy.zeros((dim,))
        return cls(w=w, b=b)

    def __call__(self, x):
        return self.w @ x + self.b

key = jax.random.PRNGKey(42)
key1, key2 = jax.random.split(key)

model = fj.Sequential(
    (
        Linear.init(key1, 3, 2),
        Linear.init(key2, 2, 5),
    )
)
```

The model can be serialized and deserialized using `fj.save` and `fj.load`.
```python
nox.save("model.npz", model)
model = nox.load("model.npz")
```

Noxjax includes wrappers of the Jax function transformations, which return callable modules.
```python
model = nox.VMap(model)
model = nox.Jit(model)
```

## Installation
Memmpy can be installed directly from PyPI using `pip`. It requires Python 3.10+ and Jax 0.4.26+.
```bash
pip install Noxjax
```

## Design
Noxjax modules sacrifice some flexibility for the sake of a unified interface and safety. Noxjax code should alway be easy to reason about and should not contain any footguns from using python magic.
1. Everything is immutable and 
2. module fields can be either jax arrays, other modules or json-like data.

This makes it harder to use other jax libraries in Noxjax modules. It is recommended to wrap the needed functionality in a module.
Most jax libraries should be compatible with Noxjax modules, since they are simply callable pytrees.

## Roadmap
- [ ] Filtered grad transformation based on key paths
- [ ] Pretty printing for modules
- [ ] Rule to infer static arguments in jitted functions, possibly everything except JAX arrays

## See also
- The beautiful [Equinox](https://github.com/patrick-kidger/equinox) library
