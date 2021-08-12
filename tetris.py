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
    # "cells": [[0] * BOARD_COLS] * BOARD_ROWS,
    "cols": BOARD_COLS,
    "rows": BOARD_ROWS,
    "block_px_side": BLOCK_PX_SIDE,
    "rect": pg.Rect(10, 10, BLOCK_PX_SIDE * BOARD_COLS, BLOCK_PX_SIDE * BOARD_ROWS),
    "cell_sprites": [[None] * BOARD_COLS] * BOARD_ROWS,
    "color": (0, 0, 0),
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


def move_right(tetrimino):
    if tetrimino.can_move_by(1, 0):
        tetrimino.move_by(1, 0)


def move_left(tetrimino):
    if tetrimino.can_move_by(-1, 0):
        tetrimino.move_by(-1, 0)


def move_down(tetrimino):
    if tetrimino.can_move_by(0, 1):
        tetrimino.move_by(0, 1)


def rotate_clockwise(tetrimino):
    pass


event_handlers = {
    pg.K_d: move_right,
    pg.K_a: move_left,
    pg.K_s: move_down,
    pg.K_w: rotate_clockwise,
}


def main():
    screen = pg.display.set_mode(SCREENRECT.size)
    clock = pg.time.Clock()
    group = pg.sprite.Group()
    tet = tetrimino.J(1, 1, **BOARD)
    board_sprite = BoardSprite(**BOARD)
    group.add(board_sprite)

    # initial_key_repeat_delay_ms = 1000
    # key_repeat_delay_ms = 500
    # pygame.key.set_repeat(initial_key_repeat_delay_ms, key_repeat_delay_ms)
    since_last_move = 0
    while True:
        if since_last_move > DOWN_SPEED_MS:
            since_last_move = 0
            move_down(tet)

        for ev in pg.event.get():
            if ev.type == pg.KEYDOWN:
                if func := event_handlers.get(ev.key, None):
                    func(tet)

        screen.fill(tetrimino.colors[0])
        group.draw(screen)
        tet.update()
        tet.draw(screen)

        pg.display.flip()
        since_last_move += clock.tick(FPS)


if __name__ == "__main__":
    main()
