"""Utility functions for PyTenno."""

import re
from datetime import datetime
from typing import Any, Callable, Optional, TypeVar

T = TypeVar("T")

_CAMEL_TO_SNAKE_RE = re.compile(r"(?<!^)(?=[A-Z])")


def camel_to_snake(name: str) -> str:
    """Converts a camelCase string to snake_case.

    Parameters
    ----------
    name : str
        The camelCase identifier.

    Returns
    -------
    str
        The snake_case identifier.
    """
    return _CAMEL_TO_SNAKE_RE.sub("_", name).lower()


def snake_to_camel(name: str) -> str:
    """Converts a snake_case string to camelCase.

    Parameters
    ----------
    name : str
        The snake_case identifier.

    Returns
    -------
    str
        The camelCase identifier.
    """
    parts = name.split("_")
    return parts[0] + "".join(word.capitalize() for word in parts[1:])


def get_or_none(item: Any,Converter: Callable[[Any], T]) -> Optional[T]:
    """Applies ``Converter`` to ``item`` if ``item`` is not ``None``.

    Parameters
    ----------
    item : Any
        The value to convert.
    Converter : Callable[[Any], T]
        The conversion function or enum/class constructor.

    Returns
    -------
    Optional[T]
    """
    return None if item is None else Converter(item)


def parse_iso_datetime(value: Optional[str]) -> Optional[datetime]:
    """Parses an ISO-8601 datetime string from Warframe.market (including trailing ``Z``).

    Parameters
    ----------
    value : Optional[str]
        The ISO-8601 string (e.g., ``"2026-11-07T21:11:22Z"``).

    Returns
    -------
    Optional[datetime]
    """
    if not value:
        return None
    if isinstance(value, datetime):
        return value
    normalized = value.replace("Z", "+00:00")
    try:
        return datetime.fromisoformat(normalized)
    except ValueError:
        return None


def enum_or_raw(enum_cls: Any, value: Any) -> Any:
    """Attempts to resolve ``value`` as a member of ``enum_cls``, falling back to ``value``.

    Parameters
    ----------
    enum_cls : EnumMeta
        The target Enum class.
    value : Any
        The string or value to look up.

    Returns
    -------
    Any
    """
    if value is None or isinstance(value, enum_cls):
        return value
    if isinstance(value, str):
        if value in enum_cls.__members__:
            return enum_cls[value]
        lower = value.lower()
        if lower in enum_cls.__members__:
            return enum_cls[lower]
        for member in enum_cls:
            if str(member.value).lower() == lower:
                return member
    return value
