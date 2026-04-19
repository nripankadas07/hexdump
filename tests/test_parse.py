from __future__ import annotations

import pytest

from hexdump import HexdumpError, hexdump, parse_hexdump


class TestParseCanonical:
    def test_empty(self): assert parse_hexdump("") == b""
    def test_roundtrip_single(self):
        d = b"Hello, World!"; assert parse_hexdump(hexdump(d)) == d
    def test_roundtrip_multi(self):
        d = bytes(range(256)); assert parse_hexdump(hexdump(d)) == d
    def test_roundtrip_upper(self):
        d = bytes([0xDE, 0xAD, 0xBE, 0xEF]); assert parse_hexdump(hexdump(d, uppercase=True)) == d
    def test_roundtrip_no_ascii(self):
        d = b"no gutter here"; assert parse_hexdump(hexdump(d, ascii=False)) == d


class TestParseErrors:
    def test_non_string(self):
        with pytest.raises(HexdumpError): parse_hexdump(b"00000000: 41")
    def test_no_offset(self):
        with pytest.raises(HexdumpError): parse_hexdump("hello world\n")
    def test_mismatched_offset(self):
        with pytest.raises(HexdumpError): parse_hexdump("00000010  41 42 43\n")
