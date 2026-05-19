from io import BytesIO

import pytest

from mammoth_db.page import Page


def test_from_blocksize_creates_zero_filled_page():
    page = Page.from_blocksize(8)

    assert page.contents() == b"\x00" * 8


def test_from_bytes_uses_provided_buffer():
    buffer = BytesIO(b"abcd")

    page = Page.from_bytes(buffer)

    assert page.byte_buffer is buffer
    assert page.contents() == b"abcd"


def test_get_int_reads_four_bytes_from_offset():
    page = Page.from_bytes(BytesIO(b"\x00\x00\x00*\xff\xff\xff\xff"))

    assert page.get_int(0) == 42
    assert page.get_int(4) == 4_294_967_295


def test_set_int_writes_four_bytes_at_offset():
    page = Page.from_blocksize(8)

    page.set_int(2, 42)
    assert page.contents() == b"\x00\x00\x00\x00\x00*\x00\x00"

    page.set_int(4, 4_294_967_295)
    assert page.contents() == b"\x00\x00\x00\x00\xff\xff\xff\xff"


def test_read_and_write_reset_buffer_position():
    page = Page.from_blocksize(4)

    page.byte_buffer.seek(3)
    page.get_int(0)
    assert page.byte_buffer.tell() == 0

    page.byte_buffer.seek(3)
    page.set_int(0, 1)
    assert page.byte_buffer.tell() == 0
