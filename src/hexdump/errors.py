"""Single error class raised for every invalid input or malformed parse."""

from __future__ import annotations


class HexdumpError(ValueError):
    """Raised when hexdump input or parse target is invalid.

    Subclasses :class:`ValueError` so existing ``except ValueError`` handlers
    still catch misuse, while a dedicated class lets callers catch library
    errors specifically without swallowing unrelated exceptions.
    """
