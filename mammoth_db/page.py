from io import BytesIO
from dataclasses import dataclass

@dataclass
class Page:
    """Fixed-size byte page used for block-level storage

    A page wraps an in-memory byte buffer and provides helpers for reading and
    writing primitive values at byte offsets. Methods reset the buffer position
    to the beginning after each operation

    Attributes:
        byte_buffer: Underlying byte buffer that stores the page contents
    """
    byte_buffer: BytesIO

    @classmethod
    def from_bytes(cls, bytes: BytesIO) -> "Page":
        """Create a page from an existing byte buffer

        Args:
            bytes: Existing byte buffer to wrap.

        Returns:
            A page backed by the provided buffer
        """
        return Page(
            byte_buffer=bytes
        )

    @classmethod
    def from_blocksize(cls, block_size: int) -> "Page":
        """Create a zero-filled page with the given block size.

        Args:
            block_size: Number of bytes in the page.

        Returns:
            A zero-filled page.
        """
        return Page(
            byte_buffer=BytesIO(bytes(block_size))
        )

    def get_int(self, offset: int) -> int:
        """Read an unsigned 4-byte integer from the page.

        Args:
            offset: Byte offset where the integer starts.

        Returns:
            The integer decoded from four bytes.
        """
        self.byte_buffer.seek(offset)
        result = int.from_bytes(self.byte_buffer.read(4))
        self.byte_buffer.seek(0)
        return result

    def set_int(self, offset: int, n: int) -> None:
        """Write an unsigned 4-bytes integer to the page

        Args:
            offset: Byte offset where the integer starts
            n: Integer to write. Must fit in four unsigned bytes.

        Raises:
            OverflowError: If ``n`` cannot fit in four unsigned bytes.
        """  # noqa: DOC502 -- propagates from int.to_bytes, not raised directly here
        self.byte_buffer.seek(offset)
        self.byte_buffer.write(n.to_bytes(4))
        self.byte_buffer.seek(0)

    def contents(self) -> bytes:
        """Returns the full contents of byte buffer

        Returns:
            The page contents from the beginning of the buffer
        """
        self.byte_buffer.seek(0)
        return self.byte_buffer.read()
