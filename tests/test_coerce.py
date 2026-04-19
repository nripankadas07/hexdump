from __future__ import annotations

import pytest

from hexdump import HexdumpError
from hexdump._coerce import coerce_bytes, validate_group, validate_offset, validate_width


class TestCoerceBytes:
    def test_accepts_bytes(self): assert coerce_bytes(b"hello") == b"hello"
    def test_accepts_bytearray(self): assert coerce_bytes(bytearray(b"abc")) == b"abc"
    def test_accepts_memoryview(self): assert coerce_bytes(memoryview(b"xyz")) == b"xyz"
    def test_accepts_iterable_of_ints(self): assert coerce_bytes([0x4E, 0x72, 0x69]) == b"Nri"
    def test_rejects_str(self):
        with pytest.raises(HexdumpError): coerce_bytes("hello")
    def test_rejects_non_iterable(self):
        with pytest.raises(HexdumpError): coerce_bytes(12345)
    def test_rejects_non_int(self):
        with pytest.raises(HexdumpError): coerce_bytes([0x41, "x", 0x43])
    def test_rejects_out_of_range(self):
        with pytest.raises(HexdumpError): coerce_bytes([256])
        with pytest.raises(HexdumpError): coerce_bytes([-1])


class TestValidateWidth:
    def test_ok(self): assert validate_width(16) == 16
    def test_zero(self):
        with pytest.raises(HexdumpError): validate_width(0)
    def test_negative(self):
        with pytest.raises(HexdumpError): validate_width(-1)


class TestValidateGroup:
    def test_zero(self): assert validate_group(0, 16) == 0
    def test_ok(self): assert validate_group(4, 16) == 4
    def test_clip(self): assert validate_group(32, 16) == 16
    def test_negative(self):
        with pytest.raises(HexdumpError): validate_group(-1, 16)


class TestValidateOffset:
    def test_zero(self): assert validate_offset(0) == 0
    def test_positive(self): assert validate_offset(4096) == 4096
    def test_negative(self):
        with pytest.raises(HexdumpError): validate_offset(-1)
