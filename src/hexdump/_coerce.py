"""Input coercion helpers shared by the public API."""

from __future__ import annotations

from typing import Iterable, Union

from .errors import HexdumpError

BytesInput = Union[bytes, bytearray, memoryview, Iterable[int]]


def coerce_bytes(data: BytesInput) -> bytes:
    if isinstance(data, (bytes, bytearray)):
        return bytes(data)
    if isinstance(data, memoryview):
        return data.tobytes()
    if isinstance(data, str):
        raise HexdumpError("data must be bytes-like, not str (encode first)")
    try:
        iterator = iter(data)
    except TypeError:
        raise HexdumpError("data must be bytes, bytearray, memoryview, or an iterable of ints") from None
    values: list[int] = []
    for index, value in enumerate(iterator):
        if not isinstance(value, int) or isinstance(value, bool):
            raise HexdumpError(f"element at index {index} must be an int in [0, 255], got {type(value).__name__}")
        if value < 0 or value > 0xFF:
            raise HexdumpError(f"element at index {index} must be in [0, 255], got {value}")
        values.append(value)
    return bytes(values)


def validate_width(width: int) -> int:
    if isinstance(width, bool) or not isinstance(width, int):
        raise HexdumpError("width must be an int")
    if width <= 0:
        raise HexdumpError("width must be a positive integer")
    return width


def validate_group(group: int, width: int) -> int:
    if isinstance(group, bool) or not isinstance(group, int):
        raise HexdumpError("group must be an int")
    if group < 0:
        raise HexdumpError("group must be >= 0")
    if group > width:
        return width
    return group


def validate_offset(offset: int) -> int:
    if isinstance(offset, bool) or not isinstance(offset, int):
        raise HexdumpError("offset must be an int")
    if offset < 0:
        raise HexdumpError("offset must be >= 0")
    return offset
