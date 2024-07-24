import abc
import dataclasses
from types import MappingProxyType
from typing import Any, Callable, Hashable, Self, Sequence, dataclass_transform

import jax
import jax.tree_util as jtu
from oryx.core.interpreters.harvest import nest

from ._trees import MODULE_REGISTRY
from ._typecheck import typecheck
from ._utils import array_summary

__all__ = [
    "field",
    "get_module_name",
    "Module",
    "BoundMethod",
    "BoundMethodWrap",
]


@typecheck
def field(*, static: bool = False, **kwargs):
    """
    Dataclass field with additional metadata for static pytree leaves.
    Static pytree leaves are used as considered part of the tree structure
    instead of the tree content. The values of static leaves should be hashable,
    since changing the value of a static leaf usually triggers a recompilation
    of all JAX transformations.

    Parameters:
    ---
    static: bool
        Whether the field is a static pytree leaf.

    **kwargs: Any
        Additional arguments to pass to 'dataclasses.field'.

    Returns:
    ---
    dataclasses.Field
        A dataclass field with additional metadata for static pytree leaves.

    """
    metadata = kwargs.pop("metadata", {})

    # perform copy and make mutable
    metadata = dict(metadata)
    metadata["static"] = static

    # make immutable again
    metadata = MappingProxyType(metadata)
    return dataclasses.field(metadata=metadata, **kwargs)


@typecheck
def get_module_name(cls: type) -> str:
    """
    Get the name of a given module class. This is the class name by default,
    but can be overridden by setting a '__noxname' attribute on the class.

    The double underscore invokes python's name mangling which makes sure,
    that the same name is not used for two modules, just because one inherits
    from the other.

    Parameters:
    ---
    cls: type
        The class to get the module name for.

    Returns:
    ---
    str
        The name of the module class.
    """
    # attribute name of '__noxname' after private name mangling
    mangled_name = f"_{cls.__name__}__noxname"

    if hasattr(cls, mangled_name):
        name = getattr(cls, mangled_name)

        if not isinstance(name, str):
            error = f"Expected __noxname to be a string, but got: {name}"
            raise TypeError(error)

        return name

    return cls.__name__


@typecheck
@dataclass_transform(
    frozen_default=True,
    field_specifiers=(
        dataclasses.Field,
        dataclasses.field,
        field,
    ),
)
class FrozenDataclassMeta(abc.ABCMeta, type):
    """
    This metaclass makes all its subclasses frozen dataclasses and registers
    them as JAX PyTrees. The fields of the dataclass are the pytree leaves.

    Parameters:
    ---
    register: bool
        Whether to register the class in the global module registry.

    replace: bool
        Whether to replace an existing module with the same name in the
        global module registry.
    """

    def __new__(
        cls,
        name: str,
        bases: tuple[type, ...],
        attrs: dict[str, Any],
        **kwargs: Any,
    ):
        for key, value in attrs.items():
            if name in ["FrozenDataclassBase", "Module", "BoundMethod"]:
                break

            if key in ["tree_flatten_with_keys", "tree_unflatten"]:
                continue

            if key != "__call__":
                if key.startswith("__") and key.endswith("__"):
                    continue

            if not callable(value):
                continue

            attrs[key] = BoundMethodWrap(value)

        cls_new = super().__new__(cls, name, bases, attrs)
        cls_new = dataclasses.dataclass(frozen=True, repr=False)(cls_new)

        cls_new.__init__ = typecheck(cls_new.__init__)

        if not kwargs.get("register", True):
            return cls_new

        module_name = get_module_name(cls_new)

        if module_name in MODULE_REGISTRY and not kwargs.get("replace", False):
            error = (
                f"Module with name '{module_name}' is already registered. "
                "Consider using a different name for the module or adding a"
                "'__noxname' class attribute to the module definition. "
                "In case you want to replace the existing module, set the "
                "'replace' keyword argument to 'True'."
            )
            raise ValueError(error)

        MODULE_REGISTRY[module_name] = cls_new
        return cls_new

    def __init__(
        cls,
        name: str,
        bases: tuple[type, ...],
        attrs: dict[str, Any],
        **_: Any,
    ) -> None:
        super().__init__(name, bases, attrs)
        jtu.register_pytree_with_keys_class(cls)


@typecheck
class FrozenDataclassBase(metaclass=FrozenDataclassMeta, register=False):
    @abc.abstractmethod
    def tree_flatten_with_keys(self: Self):
        error = "Abstract method 'tree_flatten_with_keys' must be implemented."
        raise NotImplementedError(error)

    @classmethod
    @abc.abstractmethod
    def tree_unflatten(cls, aux_data, children: tuple[Any, ...]):
        error = "Abstract method 'tree_unflatten' must be implemented."
        raise NotImplementedError(error)


@typecheck
class Module(FrozenDataclassBase):
    """
    The base class for all modules. Modules are frozen dataclasses that can
    be used to define modular parametric functions like neural networks.

    Modules are JAX pytrees, which means they can be used with JAX
    transformations like 'jax.jit', 'jax.grad', 'jax.vmap', 'jax.pmap', etc.

    The attributes of a module are the pytree leaves, which can also be other
    modules. Attributes annotated with '= field(static=True)' are considered
    part of the tree structure.

    The '__noxname' attribute can be set to set the name that is used when
    serializing the module. By default, the class name is used.
    """

    __noxname = "noxjax.Module"

    def tree_flatten_with_keys(
        self: Self,
    ) -> tuple[
        tuple[tuple[jtu.GetAttrKey, Any], ...],
        tuple[tuple[str, Hashable], ...],
    ]:
        children = []
        aux_data = []

        # fixed order for the fields
        for field in sorted(dataclasses.fields(self), key=lambda f: f.name):
            # static fields are part of the tree structure
            # if there is not 'static' key, assume it is not a static field
            if field.metadata.get("static", False):
                value = getattr(self, field.name)

                if not isinstance(value, Hashable):
                    error = f"Non-hashable static data '{field.name}: {value}'"
                    raise ValueError(error)

                aux_data.append((field.name, value))
                continue

            # Use the key path api to indicate the address of the fields
            v = getattr(self, field.name)
            k = jtu.GetAttrKey(field.name)
            children.append((k, v))

        return tuple(children), tuple(aux_data)

    @classmethod
    def tree_unflatten(
        cls,
        aux_data: Sequence[tuple[str, Hashable]],
        children: Sequence[Any],
    ):
        aux_data_dict = dict(aux_data)
        children_dict = {}

        # use the same order
        fields = sorted(dataclasses.fields(cls), key=lambda f: f.name)

        # pointer to the element in the children list
        i = 0

        for field in fields:
            # check whether the current field is a static field
            if field.name in aux_data_dict:
                continue

            children_dict[field.name] = children[i]
            i += 1

        return cls(**children_dict, **aux_data_dict)

    def __repr__(self: Self) -> str:
        head = f"{self.__class__.__name__}("

        # do not use linebreaks if there are no fields
        if len(dataclasses.fields(self)) == 0:
            return head + ")"

        body = []

        for field in dataclasses.fields(self):
            value = getattr(self, field.name)

            if isinstance(value, jax.Array):
                # do not print the whole array, just a summary
                value = array_summary(value)
            else:
                value = repr(value)

            body.append(f"{field.name}={value}")

        body = ",\n".join(body)
        body = "\n" + body

        # add indentation
        body = body.replace("\n", "\n  ")
        body = body + "\n"

        tail = ")"
        return head + body + tail


@typecheck
class BoundMethod(Module):
    """
    Make a callable module out of a method of a module. This allows the method
    to be used with JAX transformatiosn like 'jax.jit', 'jax.grad' in the same
    way a module with the '__call__' method might be used.

    Attributes:
    ---
    module: Module
        The module the method is bound to.

    method: str
        The name of the method of the module.
    """

    __noxname = "noxjax.BoundMethod"

    module: Module
    method: str = field(static=True)

    @classmethod
    def init(cls, module_method) -> Self:
        if not hasattr(module_method, "__self__"):
            error = f"Method {module_method} is not bound to a module."
            raise ValueError(error)

        module = module_method.__self__

        if not callable(module_method):
            error = f"Method {module_method} is not callable."
            raise ValueError(error)

        if not isinstance(module, Module):
            error = f"Object {module} is not a Module."
            raise ValueError(error)

        return cls(
            module=module,
            method=module_method.__name__,
        )

    # maintain compatibility with the original python bound method type
    @property
    def __self__(self: Self) -> Module:
        return self.module

    @property
    def _scope(self: Self) -> str:
        scope = get_module_name(type(self.module))

        if self.method != "__call__":
            scope = f"{scope}.{self.method}"

        return scope

    def __call__(self: Self, *args, **kwargs):
        method = getattr(type(self.module), self.method)
        method = jax.named_scope(self._scope)(method)
        method = nest(method, scope=self._scope)
        return method(self.module, *args, **kwargs)


@typecheck
@dataclasses.dataclass(frozen=True)
class BoundMethodWrap:
    """
    A descriptor that wraps a method of a module into a 'BoundMethod' instance.
    This allows all methods of a module to automatically be wrapped into
    'BoundMethod' instances when the module is created.

    Attributes:
    ---
    method: Callable
        The method to wrap into a 'BoundMethod' instance.
    """

    __noxname = "noxjax.BoundMethodWrap"

    method: Callable

    def __get__(self: Self, instance, owner=None) -> Callable | BoundMethod:
        if instance is None:
            return self.method

        method = self.method.__get__(instance, owner)
        return BoundMethod.init(method)
