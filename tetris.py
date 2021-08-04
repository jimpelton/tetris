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
BOARD = {
    "cells": [[0] * BOARD_COLS] * BOARD_ROWS,
    "cols": BOARD_COLS,
    "rows": BOARD_ROWS,
    "rect": pg.Rect(10, 10, SCREENRECT.width * 0.75, SCREENRECT.height * 0.95),
    "cell_sprites": [[None] * BOARD_COLS] * BOARD_ROWS,
    "color": (0, 0, 0),
}


class BoardSprite(pg.sprite.Sprite):
    def __init__(self, **board) -> None:
        super().__init__()
        self.board = board

        self.image = pg.Surface((board["rect"].width, board["rect"].height))
        self.image.fill(board["color"])
        self.rect = self.image.get_rect()

        pg.draw.rect(self.image, (255, 255, 255), self.rect, width=1)


def main():
    screen = pg.display.set_mode(SCREENRECT.size)
    clock = pg.time.Clock()
    group = pg.sprite.Group()
    tet = tetrimino.J(**BOARD)
    board_sprite = BoardSprite(**BOARD)
    group.add(board_sprite)

    while True:
        clock.tick(1)
        if tet.can_move_by(0, 1):
            tet.update(0, 1)
        else:
            print("tet can't move there")

        screen.fill(tetrimino.colors[0])
        group.draw(screen)
        tet.draw(screen)

        pg.display.flip()


def rotate(tetrimino):
    pass


if __name__ == "__main__":
    main()
