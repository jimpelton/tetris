from dataclasses import dataclass
from typing import Tuple, List, Final, Self

import pygame as pg


_BOARD_COLS: Final = 10
_BOARD_ROWS: Final = 20
_BLOCK_PX_SIDE: Final = 20

_BOARD_DEFAULTS = {
    "n_cols": _BOARD_COLS,
    "n_rows": _BOARD_ROWS,
    "block_px_side": _BLOCK_PX_SIDE,
    "color": (0, 0, 0),
    "cell_sprites": [[None for _ in range(_BOARD_COLS)] for _ in range(_BOARD_ROWS)],
    "rect": pg.Rect(10, 10, _BLOCK_PX_SIDE * _BOARD_COLS, _BLOCK_PX_SIDE * _BOARD_ROWS),
}

@dataclass(frozen=True)
class BoardArgs:
    """Represents details/config about the board."""
    n_cols: int
    n_rows: int
    block_px_side: int
    color: Tuple[int, int, int]
    cell_sprites: List[List[None | pg.sprite.Sprite]]
    rect: pg.Rect


    @classmethod
    def make_default(cls) -> Self:
        return cls(**_BOARD_DEFAULTS)
