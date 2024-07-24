import json
from types import MappingProxyType
from typing import Any, Mapping, overload

import jax
import jax.numpy as jnp
import jax.tree_util as jtu
import numpy as onp

from ._module import Module, get_module_name
from ._trees import MODULE_REGISTRY
from ._typecheck import typecheck

__all__ = [
    "save",
    "load",
]


@typecheck
def _treedef_to_dict(treedef, /) -> dict[str, Any] | None:
    """
    Convert a PyTree tree definition into a nested dictionary. This uses the
    global module registry to convert types to unique names.
    """
    if treedef.node_data() is None:
        return None

    node_data = treedef.node_data()
    name = get_module_name(node_data[0])

    if name not in MODULE_REGISTRY:
        error = f"Module '{node_data[0]}' is not registered."
        raise ValueError(error)

    return {
        "__noxname": name,
        "aux_data": node_data[1],
        "children": [_treedef_to_dict(child) for child in treedef.children()],
    }


@typecheck
def _dict_to_treedef(data: Mapping | None, /) -> jtu.PyTreeDef:
    """
    Convert a nested dictionary created by 'treedef_to_dict' back into a PyTree.
    All types used in the tree definition must be registered in the global
    module registry.
    """
    if data is None:
        return jtu.PyTreeDef.make_from_node_data_and_children(
            jtu.default_registry, None, []
        )

    if data["__noxname"] not in MODULE_REGISTRY:
        error = f"Module with name '{data['__noxname']}' is not registered."
        raise ValueError(error)

    cls = MODULE_REGISTRY[data["__noxname"]]

    return jtu.PyTreeDef.make_from_node_data_and_children(
        jtu.default_registry,
        (cls, data["aux_data"]),
        (_dict_to_treedef(child) for child in data["children"]),
    )


@typecheck
def _ismapping(obj: Any) -> bool:
    """
    Check whether an object can be used as a mapping.
    """
    try:
        _ = (lambda **kwargs: kwargs)(**obj)  # type: ignore
        return True
    except TypeError:
        return False


@typecheck
def _issequence(obj: Any) -> bool:
    """
    Check whether an object can be used as a sequence.
    """
    try:
        _ = (lambda *args: args)(*obj)  # type: ignore
        return True
    except TypeError:
        return False


@typecheck
class ConfigEncoder(json.JSONEncoder):
    """
    Encodes json like data by converting mappings to dictionaries and sequences
    to lists.
    """

    def default(self, obj) -> dict[str, Any] | list[Any] | Any:
        # first check if the object is coercible to a mapping,
        # since mappings are also sequences of their keys
        if _ismapping(obj):
            return dict(obj)

        if _issequence(obj):
            return list(obj)

        return super().default(obj)


@typecheck
def save(path: str, tree: Module | list | dict | tuple | None) -> None:
    """
    Save a pytree to a file in a format that can be loaded later.
    """

    flat, treedef = jtu.tree_flatten(tree)
    arrays = {}

    # leaves with primitive-type values are stored in a separate dictionary
    primis = {}

    for i, value in enumerate(flat):
        if isinstance(value, (jax.Array, onp.ndarray)):
            arrays[str(i)] = value
            continue

        if isinstance(value, (bool, int, float, str)):
            primis[str(i)] = value
            continue

        error = f"Invalid value type: {value}"
        raise TypeError(error)

    treedef = _treedef_to_dict(treedef)
    jsondat = {"treedef": treedef, "primis": primis}

    jsonstr = json.dumps(jsondat, indent=2, cls=ConfigEncoder)
    arrays["json"] = jsonstr

    jnp.savez(path, **arrays)


@overload
def convert_json_immutable(obj: dict) -> MappingProxyType: ...


@overload
def convert_json_immutable(obj: list) -> tuple: ...


@typecheck
def convert_json_immutable(obj: Any) -> MappingProxyType | tuple | Any:
    """
    Convert a json like object to an immutable object, by recursively converting
    dictionaries to MappingProxyType and lists to tuples.
    """
    if isinstance(obj, dict):
        new = {}
        for k, v in obj.items():
            new[k] = convert_json_immutable(v)

        return MappingProxyType(new)

    if isinstance(obj, list):
        new = []
        for v in obj:
            new.append(convert_json_immutable(v))

        return tuple(new)

    return obj


@typecheck
def load(path: str) -> Module | list | dict | tuple | None:
    """
    Load a pytree from a file that was saved with 'save'.
    """
    arrays = dict(jnp.load(path))
    jsondat = json.loads(str(arrays.pop("json")))

    # convert to immutable, since noxjax expects immutable types in some places
    # for instance in the aux_data of the treedef of modules
    jsondat = convert_json_immutable(jsondat)
    assert isinstance(jsondat, Mapping)

    # merge the arrays and the primitive types, which come from the json file
    arrays = arrays | jsondat["primis"]
    flat = [jnp.array(arrays[k]) for k in sorted(arrays, key=int)]

    treedef = _dict_to_treedef(jsondat["treedef"])
    return jtu.tree_unflatten(treedef, flat)
