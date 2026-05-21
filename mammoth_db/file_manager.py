from mammoth_db.constant import BLOCK_SIZE
from io import BytesIO
from pathlib import Path
from mammoth_db.utils import ensure_dir
from typing import IO
from dataclasses import dataclass

from mammoth_db.page import Page
from mammoth_db.block_id import BlockID

@dataclass
class FileManager:
    """File manager used for block-level storage.

    Manages database files within given directory so that all of database
    files are managed in-memory. This handles in-memory read/write IO using
    in-memory buffer called page.

    Attributes:
        directory: directory where database files are managed
        block_size: size of each block
        current_open_files: Handles database files in-memory
    """
    directory: Path
    block_size: int
    current_open_files: dict[str, Path]

    @classmethod
    def from_directory_path(cls, *, dir_path: Path, block_size: int) -> "FileManager":
        directory = ensure_dir(dir_path)

        current_open_files = {}
        for entry in directory.iterdir():
            if entry.name.startswith("temp"):
                entry.unlink()
            else:
                current_open_files[entry.name] = entry

        return FileManager(
            directory=directory,
            block_size=block_size,
            current_open_files=current_open_files
        )


    def read(self, block: BlockID, page: Page):
        """Read contents from block and overwrites to page

        Args:
            block: implies relative position for database file
            page: in-memory buffer to be overwritten
        """
        file = self.get_file(block.filename)
        with open(file, "rb") as f:
            f.seek(block.number * self.block_size)
            page.byte_buffer = BytesIO(f.read(self.block_size))

    def write(self, block: BlockID, page: Page):
        """Write contents of page to given database file's block

        Args:
            block: implies relative position for database file
            page: in-memory data to write
        """
        file = self.get_file(block.filename)
        with open(file, "wb") as f:
            f.seek(block.number * self.block_size)
            f.write(page.byte_buffer.getvalue())

    def append(self, filename: str):
        """Append additional block to database file

        Args:
            filename: Name of database file to be appended
        """
        new_blknum = self.blk_count(filename)
        blk = BlockID(filename=filename, number=new_blknum)
        content = b"\00" * self.block_size

        file = self.get_file(filename)
        with open(file, "wb") as f:
            f.seek(blk.number * self.block_size)
            f.write(content)

    def blk_count(self, filename: str) -> int:
        """Measure number of block for specific file

        Args:
            filename: Existing file to measure # of block

        Returns:
            # of blocks
        """
        f = self.get_file(filename)
        count = int(len(f.read_bytes()) / self.block_size)
        return count

    def get_file(self, filename: str) -> Path:
        """Get database file for given name

        Args:
            filename: Name of database file

        Returns:
            Path of database file within db directory
        """
        f = self.current_open_files.get(filename)
        if f is None:
            db_table = Path(self.directory / filename)
            self.current_open_files[filename] = db_table
            f = db_table

        return f
