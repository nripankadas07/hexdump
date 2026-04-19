"""Line-level formatting primitives for the canonical hexdump style."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class FormatOptions:
    width: int
    group: int
    uppercase: bool
    ascii_gutter: bool
    sep: str


def format_offset(offset: int, uppercase: bool) -> str:
    spec = "08X" if uppercase else "08x"
    return format(offset, spec)


def format_hex_section(chunk: bytes, options: FormatOptions) -> str:
    width = options.width
    group = options.group
    byte_spec = "02X" if options.uppercase else "02x"
    per_byte = 3
    cells: list[str] = []
    for index in range(width):
        if index < len(chunk):
            cells.append(format(chunk[index], byte_spec) + " ")
        else:
            cells.append("   ")
        if group and index != width - 1 and (index + 1) % group == 0:
            cells.append(" ")
    rendered = "".join(cells).rstrip(" ")
    expected_width = width * per_byte - 1
    if group:
        gap_count = width // group - (1 if width % group == 0 else 0)
        expected_width += max(0, gap_count)
    return rendered.ljust(expected_width)


def format_ascii_gutter(chunk: bytes, width: int) -> str:
    del width
    chars: list[str] = []
    for byte in chunk:
        if 0x20 <= byte <= 0x7E:
            chars.append(chr(byte))
        else:
            chars.append(".")
    return "|" + "".join(chars) + "|"


def format_line(offset: int, chunk: bytes, options: FormatOptions) -> str:
    hex_section = format_hex_section(chunk, options)
    offset_col = format_offset(offset, options.uppercase)
    if options.ascii_gutter:
        return f"{offset_col}{options.sep}{hex_section}{options.sep}{format_ascii_gutter(chunk, options.width)}"
    return f"{offset_col}{options.sep}{hex_section}"
