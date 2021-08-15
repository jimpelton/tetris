import pygame as pg
from pygame.locals import *

import tetrimino

pg.init()
if not pg.get_init():
    print("oh no! pygame not init'd")
    exit(1)

SCREENRECT = pg.Rect(0, 0, 720, 1280)
BOARD_COLS = 10
BOARD_ROWS = 20
BLOCK_PX_SIDE = 20
BOARD = {
    "cols": BOARD_COLS,
    "rows": BOARD_ROWS,
    "block_px_side": BLOCK_PX_SIDE,
    "color": (0, 0, 0),
    "cell_sprites": [[None] * BOARD_COLS] * BOARD_ROWS,
    "rect": pg.Rect(10, 10, BLOCK_PX_SIDE * BOARD_COLS, BLOCK_PX_SIDE * BOARD_ROWS),
}
FPS = 60
DOWN_SPEED_MS = 1000


class BoardSprite(pg.sprite.Sprite):
    def __init__(self, **board) -> None:
        super().__init__()
        self.board = board

        self.image = pg.Surface((board["rect"].width, board["rect"].height))
        self.image.fill(board["color"])
        self.rect = self.image.get_rect()

        pg.draw.rect(self.image, (255, 255, 255), self.rect, width=1)


class Board:
    def __init__(self, **board) -> None:
        self.board_sprite = BoardSprite(**board)
        self.group = pg.sprite.Group()
        self.group.add(self.board_sprite)

    def draw(self, surface):
        self.group.draw(surface)


class Tetris:
    initial_key_repeat_delay_ms = 500
    key_repeat_delay_ms = 100

    def __init__(self) -> None:
        self.screen = pg.display.set_mode(SCREENRECT.size)
        self.clock = pg.time.Clock()
        self.board = Board(**BOARD)

        self.since_last_down_move = 0

        self.event_handlers = {
            pg.K_d: self.move_right,
            pg.K_a: self.move_left,
            pg.K_s: self.move_down,
            pg.K_w: self.rotate_clockwise,
            pg.KEYDOWN: self.handle_key_down,
            pg.KEYUP: self.handle_key_up,
        }

    def move_right(self, tetrimino):
        if tetrimino.can_move_by(1, 0):
            tetrimino.move_by(1, 0)

    def move_left(self, tetrimino):
        if tetrimino.can_move_by(-1, 0):
            tetrimino.move_by(-1, 0)

    def move_down(self, tetrimino):
        if tetrimino.can_move_by(0, 1):
            tetrimino.move_by(0, 1)
        self.since_last_down_move = 0

    def rotate_clockwise(self, tetrimino):
        tetrimino.rotate_clockwise()

    def handle_key_down(self, ev, tet):
        if func := self.event_handlers.get(ev.key, None):
            func(tet)

    def handle_key_up(self, ev, tet):
        pass

    def next_tet(self):
        return tetrimino.J(1, 1, **BOARD)

    def loop(self):
        pg.key.set_repeat(self.initial_key_repeat_delay_ms, self.key_repeat_delay_ms)
        tet = self.next_tet()

        while True:
            if self.since_last_down_move > DOWN_SPEED_MS:
                self.move_down(tet)

            for ev in pg.event.get():
                if ev.type == pg.QUIT:
                    return
                if func := self.event_handlers.get(ev.type, None):
                    func(ev, tet)

            self.screen.fill(tetrimino.colors[0])
            self.board.draw(self.screen)
            tet.update()
            tet.draw(self.screen)

            pg.display.flip()
            self.since_last_down_move += self.clock.tick(FPS)

def main():
    tetris = Tetris()
    tetris.loop()


if __name__ == "__main__":
    main()
