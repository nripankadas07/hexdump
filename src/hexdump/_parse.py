"""Parse canonical-style hexdump text back to ``bytes``."""

from __future__ import annotations

import re
from typing import List

from .errors import HexdumpError

_HEX_PAIR_RE = re.compile(r"[0-9A-Fa-f]{2}")
_OFFSET_RE = re.compile(r"^([0-9A-Fa-f]+)[:\s]")


def parse_hexdump(text: str) -> bytes:
    if not isinstance(text, str):
        raise HexdumpError("text must be a string")
    collected: List[int] = []
    for ln, raw in enumerate(text.splitlines(), start=1):
        s = raw.strip()
        if not s: continue
        collected.extend(_parse_line(s, ln, len(collected)))
    return bytes(collected)


def _parse_line(line, line_number, running_offset):
    m = _OFFSET_RE.match(line)
    if not m: raise HexdumpError(f"line {line_number}: expected hex offset at start of line")
    off = int(m.group(1), 16)
    if off != running_offset:
        raise HexdumpError(f"line {line_number}: offset mismatch (got 0x{off:x}, expected 0x{running_offset:x})")
    body = line[m.end():]
    hex_portion = _strip_ascii_gutter(body)
    pairs = _HEX_PAIR_RE.findall(hex_portion)
    if not pairs and hex_portion.strip():
        raise HexdumpError(f"line {line_number}: could not find any hex byte pairs")
    return [int(p, 16) for p in pairs]


def _strip_ascii_gutter(body):
    pipe_index = body.rfind("|")
    if pipe_index > 0 and body.count("|") >= 2:
        open_index = body.rfind("|", 0, pipe_index)
        if open_index != -1 and open_index < pipe_index:
            return body[:open_index]
    return body
