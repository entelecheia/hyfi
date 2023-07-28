# Copyright (c) 2023 Massachusetts Institute of Technology
# SPDX-License-Identifier: MIT
import inspect
import sys
from typing import Any, Tuple

from typing_extensions import Final

UNKNOWN_NAME: Final[str] = "<unknown>"
COMMON_MODULES_WITH_OBFUSCATED_IMPORTS: Tuple[str, ...] = (
    "random",
    "numpy",
    "numpy.random",
    "jax.numpy",
    "jax",
    "torch",
)

# signature param-types
_POSITIONAL_ONLY: Final = inspect.Parameter.POSITIONAL_ONLY
_POSITIONAL_OR_KEYWORD: Final = inspect.Parameter.POSITIONAL_OR_KEYWORD
_VAR_POSITIONAL: Final = inspect.Parameter.VAR_POSITIONAL
_KEYWORD_ONLY: Final = inspect.Parameter.KEYWORD_ONLY
_VAR_KEYWORD: Final = inspect.Parameter.VAR_KEYWORD


def safe_name(obj: Any, repr_allowed: bool = True) -> str:
    """Tries to get a descriptive name for an object. Returns '<unknown>`
    instead of raising - useful for writing descriptive/dafe error messages."""

    if hasattr(obj, "__name__"):
        return obj.__name__

    return repr(obj) if repr_allowed and hasattr(obj, "__repr__") else UNKNOWN_NAME


def is_classmethod(obj: Any) -> bool:
    """
    Check if an object is a classmethod.

    https://stackoverflow.com/a/19228282/6592114

    Credit to: Martijn Pieters
    License: CC BY-SA 4.0 (free to copy/redistribute/remix/transform)
    """

    if not inspect.ismethod(obj):
        return False

    bound_to = getattr(obj, "__self__", None)
    if not isinstance(bound_to, type):
        # must be bound to a class
        return False
    name = safe_name(obj)

    if name == UNKNOWN_NAME:  # pragma: no cover
        return False

    for cls in bound_to.__mro__:
        descriptor = vars(cls).get(name)
        if descriptor is not None:
            return isinstance(descriptor, classmethod)
    return False  # pragma: no cover


def get_obj_path(obj: Any) -> str:
    name = safe_name(obj, repr_allowed=False)

    if name == UNKNOWN_NAME:
        raise AttributeError(f"{obj} does not have a `__name__` attribute")

    module = getattr(obj, "__module__", None)
    qualname = getattr(obj, "__qualname__", None)

    if (qualname is not None and "<" in qualname) or module is None:
        # NumPy's ufuncs do not have an inspectable `__module__` attribute, so we
        # check to see if the object lives in NumPy's top-level namespace.
        #
        # or..
        #
        # Qualname produced a name from a local namespace.
        # E.g. jax.numpy.add.__qualname__ is '_maybe_bool_binop.<locals>.fn'
        # Thus we defer to the name of the object and look for it in the
        # top-level namespace of the known suspects
        #
        # or...
        #
        # module is None, which is apparently a thing..:
        # __module__ is None for both numpy.random.rand and random.random
        #

        # don't use qualname for obfuscated paths
        for new_module in COMMON_MODULES_WITH_OBFUSCATED_IMPORTS:
            if getattr(sys.modules.get(new_module), name, None) is obj:
                module = new_module
                break
        else:
            raise ModuleNotFoundError(f"{name} is not importable")

    if not is_classmethod(obj):
        return f"{module}.{name}"
    else:
        # __qualname__ reflects name of class that originally defines classmethod.
        # Does not point to child in case of inheritance.
        #
        # obj.__self__ -> parent object
        # obj.__name__ -> name of classmethod
        return f"{get_obj_path(obj.__self__)}.{obj.__name__}"


def get_sig_obj(target):
    if not inspect.isclass(target):
        return target

    # This implements the same method prioritization as
    # `inspect.signature` for Python >= 3.9.1
    if "__new__" in target.__dict__:
        return target.__new__
    if "__init__" in target.__dict__:
        return target.__init__

    if len(target.__mro__) > 2:
        for parent in target.__mro__[1:-1]:
            if "__new__" in parent.__dict__:
                return target.__new__
            elif "__init__" in parent.__dict__:
                return target.__init__
    return getattr(target, "__init__", target)
