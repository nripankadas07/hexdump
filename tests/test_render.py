from __future__ import annotations

import pytest

from hexdump import HexdumpError, hexdump, iter_hexdump


class TestHexdumpCanonical:
    def test_empty(self): assert hexdump(b"") == ""
    def test_single_line(self):
        r = hexdump(b"Hello, World!")
        assert r == "00000000  48 65 6c 6c 6f 2c 20 57  6f 72 6c 64 21           |Hello, World!|"
    def test_non_printable_gutter(self):
        assert hexdump(bytes([0x00, 0x7F, 0x80, 0xFF, 0x41])).endswith("|....A|")
    def test_full_16_bytes(self):
        assert hexdump(bytes(range(16))) == "00000000  00 01 02 03 04 05 06 07  08 09 0a 0b 0c 0d 0e 0f  |................|"
    def test_offset_advances(self):
        lines = hexdump(bytes(range(48))).splitlines()
        assert lines[0].startswith("00000000"); assert lines[1].startswith("00000010"); assert lines[2].startswith("00000020")
    def test_explicit_offset(self):
        assert hexdump(b"abcd", offset=0x1000).startswith("00001000")
    def test_uppercase(self):
        assert "AB CD" in hexdump(bytes([0xAB, 0xCD]), uppercase=True)
    def test_ascii_false(self):
        assert "|" not in hexdump(b"abcd", ascii=False)
    def test_custom_group(self):
        assert "00 01 02 03  04 05 06 07  08 09 0a 0b  0c 0d 0e 0f" in hexdump(bytes(range(16)), group=4)
    def test_group_zero(self):
        assert "00 01 02 03 04 05 06 07 08 09 0a 0b 0c 0d 0e 0f" in hexdump(bytes(range(16)), group=0)
    def test_custom_width(self):
        lines = hexdump(b"abcdef", width=4).splitlines()
        assert lines[0].startswith("00000000"); assert len(lines) == 2
    def test_invalid_width(self):
        with pytest.raises(HexdumpError): hexdump(b"ab", width=0)
    def test_str_input(self):
        with pytest.raises(HexdumpError): hexdump("abc")


class TestIterHexdump:
    def test_empty(self): assert list(iter_hexdump(b"")) == []
    def test_matches_hexdump(self):
        d = b"The quick brown fox jumps over the lazy dog."
        assert "\n".join(iter_hexdump(d)) == hexdump(d)
