from __future__ import annotations

import pytest

from hexdump import hexdump, parse_hexdump


class TestRoundTripMatrix:
    @pytest.mark.parametrize("length", [0, 1, 2, 3, 15, 16, 17, 31, 32, 33, 255, 512])
    def test_canonical(self, length):
        p = bytes((i * 37 + 11) & 0xFF for i in range(length))
        assert parse_hexdump(hexdump(p)) == p

    @pytest.mark.parametrize("width", [1, 2, 4, 7, 8, 16, 32])
    def test_widths(self, width):
        p = bytes(range(64)); assert parse_hexdump(hexdump(p, width=width)) == p

    @pytest.mark.parametrize("group", [0, 1, 2, 4, 8, 16])
    def test_groups(self, group):
        p = bytes(range(64)); assert parse_hexdump(hexdump(p, group=group)) == p

    def test_full_byte_range(self):
        p = bytes(range(256)); assert parse_hexdump(hexdump(p)) == p
