from __future__ import annotations

from hexdump import HexdumpError


def test_hexdump_error_is_a_valueerror():
    assert issubclass(HexdumpError, ValueError)


def test_hexdump_error_carries_message():
    assert str(HexdumpError("boom")) == "boom"


def test_hexdump_error_can_be_caught_as_valueerror():
    try: raise HexdumpError("x")
    except ValueError as e: assert isinstance(e, HexdumpError)
