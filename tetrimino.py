import pygame as pg
import copy
import random

colors = [
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


class Block(pg.sprite.Sprite):
    def __init__(self, board_col, board_row, width, color) -> None:
        super().__init__()
        self.board_pos = [board_col, board_row]
        self.width = width
        self.color = color
        # use the board-relative x, y (col, row)
        self.rect = pg.Rect(board_col * width, board_row * width, width, width)
        self.image = pg.Surface([width, width])
        self.image.fill(color)

    def get_board_pos(self):
        return {"col": self.board_pos[0], "row": self.board_pos[1]}

    def set_board_pos(self, col, row):
        self.board_pos[0] = col
        self.board_pos[1] = row

    def move_by(self, cols, rows):
        self.board_pos[0] += cols
        self.board_pos[1] += rows

    def update(self):
        self.rect = pg.Rect(
            self.board_pos[0] * self.width,
            self.board_pos[1] * self.width,
            self.width,
            self.width,
        )


class Tetrimino:
    BOARD = []
    COLOR = colors[1]

    def __init__(self, *args, **kwargs) -> None:
        self.group = pg.sprite.Group()
        self.board_args = kwargs
        self.board_col = args[0]
        self.board_row = args[1]
        self.alive = True
        self.shape = self.create_blocks(self.board_col, self.board_row, **kwargs)

    def create_blocks(self, init_col, init_row, **kwargs):
        block_px = kwargs["block_px_side"]
        shape = copy.deepcopy(self.BOARD)
        for r_i, row in enumerate(self.BOARD):
            for c_i, val in enumerate(row):
                if val:
                    b = Block(c_i + init_col, r_i + init_row, block_px, self.COLOR)
                    self.group.add(b)
                    shape[r_i][c_i] = b
                else:
                    shape[r_i][c_i] = None

        return shape

    def check_collision(self, col, row):
        """Return true if a collision with board sides or filled cell"""
        if col < 0 or row < 0:
            return True

        board_sprites = self.board_args["cell_sprites"]
        try:
            return bool(board_sprites[row][col])
        except IndexError:
            # we hit the wall of the board
            return True

    def can_move_by(self, cols, rows):
        def hits(b):
            pos = b.get_board_pos()
            new_col = pos["col"] + cols
            new_row = pos["row"] + rows
            # print(f"Col: {pos["col"]} --> {new_col}, Row: {pos["row"]} --> {new_row}")
            return self.check_collision(new_col, new_row)

        can_move = all([not hits(b) for b in self.group.sprites()])
        # print(can_move)
        return can_move

    def move_by(self, cols, rows):
        for b in self.group.sprites():
            b.move_by(cols, rows)

        self.board_row += rows
        self.board_col += cols

    def rotate_clockwise(self):
        def rotate_okay(shape):
            for r, row in enumerate(shape):
                for c, blk in enumerate(row):
                    if blk:
                        # calc new board location for this block
                        new_col = self.board_col + c
                        new_row = self.board_row + r
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
                        new_col = self.board_col + c
                        new_row = self.board_row + r
                        blk.set_board_pos(new_col, new_row)
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
    BOARD = [
        [1, 1, 1, 1],
    ]
    COLOR = colors[1]

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)


class J(Tetrimino):
    BOARD = [
        [1, 0, 0],
        [1, 1, 1],
    ]
    COLOR = colors[2]

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)


class L(Tetrimino):
    BOARD = [
        [0, 0, 1],
        [1, 1, 1],
    ]
    COLOR = colors[3]

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)


class O(Tetrimino):
    BOARD = [
        [1, 1],
        [1, 1],
    ]
    COLOR = colors[4]

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)


class S(Tetrimino):
    BOARD = [
        [0, 1, 1],
        [1, 1, 0],
    ]
    COLOR = colors[5]

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)


class T(Tetrimino):
    BOARD = [
        [0, 1, 0],
        [1, 1, 1],
    ]
    COLOR = colors[6]

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)


class Z(Tetrimino):
    BOARD = [
        [1, 1, 0],
        [0, 1, 1],
    ]
    COLOR = colors[7]

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)


_tets = [
    I, J, L, O, S, T, Z
]


def random_tetrimino(icol, irow, **board):
    n = int(random.randrange(0, len(_tets)))
    return _tets[n](icol, irow, **board)
