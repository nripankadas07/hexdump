"""Top-level rendering: iterate lines over a bytes payload."""

from __future__ import annotations

from typing import Iterator

from ._coerce import BytesInput, coerce_bytes, validate_group, validate_offset, validate_width
from ._format import FormatOptions, format_line


def iter_hexdump(data, *, width=16, group=8, offset=0, uppercase=False, ascii=True, sep="  "):
    vw = validate_width(width); vg = validate_group(group, vw); vo = validate_offset(offset)
    if not isinstance(sep, str): raise TypeError("sep must be a string")
    payload = coerce_bytes(data)
    opts = FormatOptions(width=vw, group=vg, uppercase=uppercase, ascii_gutter=bool(ascii), sep=sep)
    if not payload: return
    for i in range(0, len(payload), vw):
        yield format_line(vo + i, payload[i:i+vw], opts)


def hexdump(data, *, width=16, group=8, offset=0, uppercase=False, ascii=True, sep="  "):
    return "\n".join(iter_hexdump(data, width=width, group=group, offset=offset, uppercase=uppercase, ascii=ascii, sep=sep))
