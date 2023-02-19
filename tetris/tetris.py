import sys
from typing import Callable, ClassVar, Dict,  Final
import logging
import argparse

import pygame as pg
from pygame.locals import *
from lib import BoardArgs, Tetris


logger = None

SCREENRECT: Final = pg.Rect(0, 0, 720, 720)
FPS: Final = 60
DOWN_SPEED_MS: Final = 1000


def init_pygame() -> pg.surface.Surface:
    pg.init()
    if not pg.get_init():
        print("oh no! pygame not init'd")
        exit(1)

    screen: pg.surface.Surface = pg.display.set_mode(SCREENRECT.size, pg.RESIZABLE)
    pg.display.set_caption("Tetris")
    pg.key.set_repeat(100, 50)

    return screen


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--debug", action="store_true", help="print debug logeroos")

    return parser.parse_args()


def main():
    args = parse_args()
    if args.debug:
        logging.basicConfig(level=logging.DEBUG)
    else:
        logging.basicConfig(level=logging.INFO)
    
    global logger
    logger = logging.getLogger(__name__)

    scrn: pg.surface.Surface = init_pygame()
    board_args: BoardArgs = BoardArgs.make_default()
    tetris = Tetris(screen=scrn, board_args=board_args)
    tetris.loop()
    pg.quit()
    sys.exit(0)


if __name__ == "__main__":
    main()
