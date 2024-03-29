from dataclasses import dataclass
from typing import ClassVar, Final, List, Tuple, Type, TypeAlias
import pygame as pg
import copy
import random

from .boad_args import BoardArgs
from .board_pos import BoardPos
from .block import Block

colors: Final[List[Tuple[int, int, int]]] = [
    (0, 0, 0),
    (255, 85, 85),
    (100, 200, 115),
    (120, 108, 245),
    (255, 140, 50),
    (50, 120, 52),
    (146, 202, 73),
    (150, 161, 218),
    (35, 35, 35),
]


Shape: TypeAlias = List[List[int | None | Block]]  # woa! weird types there, yo!


class Tetrimino:
    # the description of this tetrimino
    DESCRIPTION: ClassVar[Shape]
    # the color of this tetrimino
    COLOR: Tuple[int, int, int] = colors[1]

    # def __init__(self, pos: BoardPos, board_args: BoardArgs) -> None:
    def __init__(self, pos: BoardPos, ) -> None:
        self.group = pg.sprite.Group()
        # self.board_args: BoardArgs = board_args
        self.pos = pos

        # whether or not this Tetrimino is movable over the Board
        self.alive = True
        self.shape: Shape = self._create_blocks(pos.col, pos.row, board_args)

    def _create_blocks(self, init_col, init_row, board_args: BoardArgs) -> Shape:
        block_px = board_args.block_px_side
        shape = copy.deepcopy(self.DESCRIPTION)

        # create a block where self.BOARD has a 1 in it, otherwise None
        # overwrite the shape
        for r_i, row in enumerate(self.DESCRIPTION):
            for c_i, val in enumerate(row):
                if val:
                    b = Block(c_i + init_col, r_i + init_row, block_px, self.COLOR)
                    self.group.add(b)
                    # this is weird, because we are overwriting the int type with a Block
                    shape[r_i][c_i] = b
                else:
                    shape[r_i][c_i] = None

        return shape

    # def check_collision(self, col, row):
    #     """Return true if a collision with board sides or filled cell"""
    #     if col < 0 or row < 0:
    #         return True

    #     board_sprites = self.board_args.cell_sprites
    #     try:
    #         return bool(board_sprites[row][col])
    #     except IndexError:
    #         # we hit the wall of the board
    #         return True

    # def can_move_by(self, cols, rows):
    #     def hits(b):
    #         pos = b.get_board_pos()
    #         new_col = pos.col + cols
    #         new_row = pos.row + rows
    #         # print(f"Col: {pos["col"]} --> {new_col}, Row: {pos["row"]} --> {new_row}")
    #         return self.check_collision(new_col, new_row)

    #     can_move = all([not hits(b) for b in self.group.sprites()])
    #     # print(can_move)
    #     return can_move

    def move_by(self, cols, rows):
        for b in self.group.sprites():
            b.move_by(cols, rows)

        self.pos.row += rows
        self.pos.col += cols

    def rotate_clockwise(self):
        def rotate_okay(shape):
            """Return true if this shape can rotate, or False if there is something in the way"""
            for r, row in enumerate(shape):
                for c, blk in enumerate(row):
                    if blk:
                        # calc new board location for this block
                        new_col = self.pos.col + c
                        new_row = self.pos.row + r
                        # print(f"Col: {blk.get_board_pos()["col"]} --> "
                        # f"{new_col}, Row: {blk.get_board_pos()["row"]} --> {new_row}")
                        if self.check_collision(new_col, new_row):
                            return False
            return True

        print("rotating")
        shape = [
            [self.shape[y][x] for y in range(len(self.shape))]
            for x in range(len(self.shape[0]) - 1, -1, -1)
        ]
        print(f"new shape {shape}")
        if rotate_okay(shape):
            print("rotate was okay")
            for r, row in enumerate(shape):
                for c, blk in enumerate(row):
                    if blk:
                        new_col = self.pos.col + c
                        new_row = self.pos.row + r
                        blk.set_board_pos(col=new_col, row=new_row)
            self.shape = shape

    def update(self):
        self.group.update()

    def draw(self, surface):
        self.group.draw(surface)

    def set_alive(self, b):
        self.alive = b

    def is_alive(self):
        return self.alive


class I(Tetrimino):
    DESCRIPTION = [
        [1, 1, 1, 1],
    ]
    COLOR = colors[1]


class J(Tetrimino):
    DESCRIPTION = [
        [1, 0, 0],
        [1, 1, 1],
    ]
    COLOR = colors[2]


class L(Tetrimino):
    DESCRIPTION = [
        [0, 0, 1],
        [1, 1, 1],
    ]
    COLOR = colors[3]


class O(Tetrimino):
    DESCRIPTION = [
        [1, 1],
        [1, 1],
    ]
    COLOR = colors[4]


class S(Tetrimino):
    DESCRIPTION = [
        [0, 1, 1],
        [1, 1, 0],
    ]
    COLOR = colors[5]


class T(Tetrimino):
    DESCRIPTION = [
        [0, 1, 0],
        [1, 1, 1],
    ]
    COLOR = colors[6]


class Z(Tetrimino):
    DESCRIPTION = [
        [1, 1, 0],
        [0, 1, 1],
    ]
    COLOR = colors[7]


_tets = [I, J, L, O, S, T, Z]


def random_tetrimino(icol: int, irow: int, board_args: BoardArgs):
    n = int(random.randrange(0, len(_tets)))
    return _tets[n](BoardPos(col=icol, row=irow), board_args)
