from dataclasses import dataclass
from typing import Final


@dataclass(frozen=True)
class BoardPos:
    """Represents a position on the game board using column and row coordinates."""
    col: Final[int]
    row: Final[int]

    def __post_init__(self) -> None:
        if not isinstance(self.col, int) or not isinstance(self.row, int):
            raise TypeError("Column and row must be integers")
        if self.col < 0 or self.row < 0:
            raise ValueError("Column and row must be non-negative")

    def __repr__(self) -> str:
        return f"BoardPos(col={self.col}, row={self.row})"