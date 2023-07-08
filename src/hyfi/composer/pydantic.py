import inspect
from typing import Any, Callable, TypeVar, cast

from pydantic import ConfigDict, validate_call

_T = TypeVar("_T", bound=Callable[..., Any])

__all__ = ["validates_with_pydantic"]


_default_validator = validate_call(
    config=ConfigDict(arbitrary_types_allowed=True),
)


def validates_with_pydantic(
    obj: _T, *, validator: Callable[[_T], _T] = _default_validator
) -> _T:
    """Enables runtime type-checking of values, via the library ``pydantic``.

    If the input object is a class, this function wraps the class's __init__ method
    with the provided validator. If the input object is a function, this function
    wraps the function with the provided validator. If the input object has already
    been decorated with pydantic's validation decorator, this function returns the
    input object unchanged.

    I.e. ``obj = validates_with_pydantic(obj)`` adds runtime type-checking
    to all calls of ``obj(*args, **kwargs)``, based on the type-annotations specified
    in the signature of ``obj``.

    Arguments:
        obj (Callable):
            The function or class to be decorated with runtime type-checking.

        validator (Type[pydantic.validate_arguments], optional):
            A configured instance of pydantic's validation decorator.

            The default validator that we provide specifies:
               - arbitrary_types_allowed: True

    Returns:
        Callable: A wrapped function or a class whose init-method has been wrapped in-place

    """
    if inspect.isclass(obj) and hasattr(type, "__init__"):
        if hasattr(obj.__init__, "validate"):
            # already decorated by pydantic
            return cast(_T, obj)
        obj.__init__ = validator(obj.__init__)  # type: ignore
    elif hasattr(obj, "validate"):
        # already decorated by pydantic
        return cast(_T, obj)
    else:
        obj = cast(_T, validator(obj))

    return cast(_T, obj)
