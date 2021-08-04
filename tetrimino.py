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

    def update(self, cols, rows):
        self.board_pos[0] += cols
        self.board_pos[1] += rows
        self.rect = self.rect.move(cols * self.width, rows * self.width)
        # self.rect = pg.Rect(
        # board_col * self.width,
        # self.board_pos[1] + board_row * self.width,
        # self.width,
        # self.width,
        # )

    # def draw(self, surface):
    # pg.draw.rect(surface, self.color, self.rect)


class Tetrimino:
    BOARD = []
    BLOCK_PX_WIDTH = 10
    COLOR = colors[1]

    def __init__(self, *args, **kwargs) -> None:
        self.group = pg.sprite.Group()
        self.board_args = kwargs

        self.create_blocks(**kwargs)

    def create_blocks(self, **kwargs):
        board_rect = kwargs["rect"]
        board_cols = kwargs["cols"]
        board_rows = kwargs["rows"]
        block_px = int(board_rect.height / board_rows) # TODO: this isn't right
        for r_i, row in enumerate(self.BOARD):
            for c_i, val in enumerate(row):
                if val:
                    b = Block(c_i, r_i, 20, self.COLOR)
                    self.group.add(b)

    def can_move_by(self, cols, rows):
        board_rows = self.board_args["rows"]
        board_cols = self.board_args["cols"]
        board_sprites = self.board_args["cell_sprites"]

        def hits(b):
            pos = b.get_board_pos()
            new_col = pos[0] + cols
            new_row = pos[1] + rows
            print(f"New Col: {new_col}, New Row: {new_row}")

            try:
                return bool(board_sprites[new_row][new_col])
            except IndexError:
                # we hit the wall of the board
                return True

        return bool([b for b in self.group.sprites() if not hits(b)])

    def update(self, cols, rows):
        self.group.update(cols, rows)

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

    def __init__(self) -> None:
        super().__init__()


class O(Tetrimino):
    BOARD = [
        [1, 1],
        [1, 1],
    ]
    COLOR = colors[4]

    def __init__(self) -> None:
        super().__init__()


class S(Tetrimino):
    BOARD = [
        [0, 1, 1],
        [1, 1, 0],
    ]
    COLOR = colors[5]

    def __init__(self) -> None:
        super().__init__()


class T(Tetrimino):
    BOARD = [
        [0, 1, 0],
        [1, 1, 1],
    ]
    COLOR = colors[6]

    def __init__(self) -> None:
        super().__init__()


class Z(Tetrimino):
    BOARD = [
        [1, 1, 0],
        [0, 1, 1],
    ]
    COLOR = colors[7]

    def __init__(self) -> None:
        super().__init__()
