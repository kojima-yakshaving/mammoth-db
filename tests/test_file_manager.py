from pathlib import Path
from tempfile import TemporaryDirectory
import pytest

from mammoth_db.page import Page
from mammoth_db.block_id import BlockID
from mammoth_db.file_manager import FileManager
from mammoth_db.constant import BLOCK_SIZE


def test_compatibility_with_temporary_file_system():
    with TemporaryDirectory() as tmp_dir:
        tmp_file_path = Path(Path(tmp_dir) / "temp1")
        tmp_file2_path = Path(Path(tmp_dir) / "temp2")
        file_path = Path(Path(tmp_dir) / "members.db")

        files = [
            tmp_file_path,
            tmp_file2_path,
            file_path
        ]
        for path in files:
            with open(path, "w") as f:
                f.write("")

        file_manager = \
            FileManager.from_directory_path(dir_path=Path(tmp_dir), block_size=BLOCK_SIZE)

        assert len(file_manager.current_open_files) == 1


def test_append_operation_adds_blank_contents():
    content = "hello world"
    block_size = 1
    with TemporaryDirectory() as tmp_dir:
        filename = "helloworld.db"
        file_path = Path(Path(tmp_dir) / filename)

        with open(file_path, "w") as f:
            f.write(content)

        file_manager = FileManager \
            .from_directory_path(
                dir_path=Path(tmp_dir),
                block_size=block_size
            )

        assert file_manager.blk_count(filename) == len(content)

        file_manager.append(filename)
        assert file_manager.blk_count(filename) == len(content) + 1


def test_page_read():
    content = "hello world"
    block_size = 4
    with TemporaryDirectory() as tmp_dir:
        filename = "helloworld.db"
        file_path = Path(Path(tmp_dir) / filename)

        with open(file_path, "w") as f:
            f.write(content)

        file_manager = FileManager \
            .from_directory_path(
                dir_path=Path(tmp_dir),
                block_size=block_size
            )

        first_block = BlockID(filename=filename, number=0)
        second_block = BlockID(filename=filename, number=1)

        page = Page.from_blocksize(block_size)
        file_manager.read(first_block, page)
        assert page.contents() == b"hell"

        file_manager.read(second_block, page)
        assert page.contents() == b"o wo"


def test_page_write():
    content = "hello world"
    block_size = 6
    with TemporaryDirectory() as tmp_dir:
        filename = "helloworld.db"
        file_path = Path(Path(tmp_dir) / filename)

        with open(file_path, "w") as f:
            f.write(content)

        file_manager = FileManager \
            .from_directory_path(
                dir_path=Path(tmp_dir),
                block_size=block_size
            )

        first_block = BlockID(filename=filename, number=0)
        second_block = BlockID(filename=filename, number=1)

        page = Page.from_blocksize(block_size)
        page.byte_buffer.write(b"Holla ")
        file_manager.write(first_block, page)

        page.byte_buffer.write(b"mundo!")
        file_manager.write(second_block, page)

        with open(Path(tmp_dir) / filename, 'rb') as f:
            assert b"Holla mundo" in f.read()
