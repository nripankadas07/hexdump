"""Zero-dependency hexdump formatter and parser."""

from __future__ import annotations

from ._parse import parse_hexdump
from ._render import hexdump, iter_hexdump
from .errors import HexdumpError

__all__ = ["HexdumpError", "hexdump", "iter_hexdump", "parse_hexdump", "__version__"]
__version__ = "1.0.0"
