from dataclasses import dataclass
from typing import Tuple, List

import pygame as pg

@dataclass
class BoardArgs:
    n_cols: int
    n_rows: int
    block_px_side: int
    color: Tuple[int, int, int]
    cell_sprites: List[List[None | pg.sprite.Sprite]]
    rect: pg.Rect
