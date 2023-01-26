from typing import Tuple

import pygame as pg

from .board_pos import BoardPos

class Block(pg.sprite.Sprite):
    def __init__(
        self, board_col: int, board_row: int, width: int, color: Tuple[int, int, int]
    ) -> None:
        super().__init__()
        self.board_pos = BoardPos(board_col, board_row)
        self.width = width
        self.color = color
        # use the board-relative x, y (col, row)
        self.rect = pg.Rect(board_col * width, board_row * width, width, width)
        self.image = pg.Surface([width, width])
        self.image.fill(color)

    def get_board_pos(self) -> BoardPos:
        return self.board_pos

    def set_board_pos(self, col: int, row: int):
        self.board_pos.col = col
        self.board_pos.row = row

    def move_by(self, cols: int, rows: int):
        self.board_pos.col += cols
        self.board_pos.row += rows

    def update(self):
        self.rect = pg.Rect(
            self.board_pos.col * self.width,
            self.board_pos.row * self.width,
            self.width,
            self.width,
        )

    @property
    def col(self) -> int:
        return self.board_pos.col

    @property
    def row(self) -> int:
        return self.board_pos.row
