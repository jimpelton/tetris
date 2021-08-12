import pygame as pg

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
        return self.board_pos

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
        ic = args[0]
        ir = args[1]
        self.create_blocks(ic, ir, **kwargs
        )

    def create_blocks(self, init_col, init_row, **kwargs):
        block_px = kwargs["block_px_side"]
        for r_i, row in enumerate(self.BOARD):
            for c_i, val in enumerate(row):
                if val:
                    b = Block(c_i + init_col, r_i + init_row, block_px, self.COLOR)
                    self.group.add(b)

    def can_move_by(self, cols, rows):
        board_sprites = self.board_args["cell_sprites"]

        def hits(b):
            pos = b.get_board_pos()
            new_col = pos[0] + cols
            new_row = pos[1] + rows
            print(f"Col: {pos[0]} --> {new_col}, Row: {pos[1]} --> {new_row}")

            if new_col < 0 or new_row < 0:
                return False

            try:
                return bool(board_sprites[new_row][new_col])
            except IndexError:
                # we hit the wall of the board
                return True

        can_move = all([not hits(b) for b in self.group.sprites()])
        print(can_move)
        return can_move

    def move_by(self, cols, rows):
        for b in self.group.sprites():
            b.move_by(cols, rows)

    def update(self):
        self.group.update()

    def draw(self, surface):
        self.group.draw(surface)


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
