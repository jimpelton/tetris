from sys import exit
from typing import Callable, ClassVar, Dict,  Final
import logging

import pygame as pg
from pygame.locals import *
from lib import Board, BoardArgs

from lib import tetrimino


logger = None

SCREENRECT: Final = pg.Rect(0, 0, 720, 720)
FPS: Final = 60
DOWN_SPEED_MS: Final = 1000



class Tetris:
    initial_key_repeat_delay_ms: ClassVar[int] = 100
    key_repeat_delay_ms: ClassVar[int] = 50

    def __init__(self, screen: pg.surface.Surface, board_args: BoardArgs) -> None:
        self.screen: pg.surface.Surface = screen
        self.clock: pg.time.Clock = pg.time.Clock()
        self.board_args: BoardArgs = board_args
        self.board: Board = Board(board_args)

        self.since_last_down_move: float = 0

        self.event_handlers: Dict[int, Callable[[pg.event.Event, tetrimino.Tetrimino], None]] = {
            pg.KEYDOWN: self.handle_key_down,
            pg.KEYUP: self.handle_key_up,
            # pg.VIDEORESIZE: self.handle_video_resize,
        }

        self.key_down_event_handlers: Dict[int, Callable] = {
            pg.K_d: self.move_right,
            pg.K_a: self.move_left,
            pg.K_s: self.move_down,
            pg.K_w: self.rotate_clockwise,
            pg.K_SPACE: self.drop_piece,
            pg.K_ESCAPE: self.quit,
        }

    def copy_tetrimino_to_board(self, tet: tetrimino.Tetrimino):
        self.board.take_blocks(tet)
        tet.set_alive(False)
        lines_found = self.board.find_and_kill_lines()
        logger.debug("Found %s lines", lines_found)

    def move_right(self, tet: tetrimino.Tetrimino):
        # pg.key.set_repeat(self.initial_key_repeat_delay_ms, self.key_repeat_delay_ms)
        if tet.can_move_by(1, 0):
            tet.move_by(1, 0)

    def move_left(self, tet: tetrimino.Tetrimino):
        # pg.key.set_repeat(self.initial_key_repeat_delay_ms, self.key_repeat_delay_ms)
        if tet.can_move_by(-1, 0):
            tet.move_by(-1, 0)

    def move_down(self, tet: tetrimino.Tetrimino):
        # pg.key.set_repeat(self.initial_key_repeat_delay_ms, self.key_repeat_delay_ms)
        if tet.can_move_by(0, 1):
            tet.move_by(0, 1)
            self.since_last_down_move = 0
        else:
            logger.debug("Tet couldn't move")
            self.copy_tetrimino_to_board(tet)

    def rotate_clockwise(self, tet: tetrimino.Tetrimino):
        tet.rotate_clockwise()

    def drop_piece(self, tet: tetrimino.Tetrimino):
        while tet.can_move_by(0, 1):
            logger.debug("dropping piece")
            tet.move_by(0, 1)

    def handle_key_down(self, ev: pg.event.Event, tet: tetrimino.Tetrimino):
        logger.debug("key down event")
        # pg.key.set_repeat(self.initial_key_repeat_delay_ms, self.key_repeat_delay_ms)
        if func := self.key_down_event_handlers.get(ev.key, None):
            func(tet)

    def handle_key_up(self, ev: pg.event.Event, tet: tetrimino.Tetrimino):
        # pg.key.set_repeat(0)
        pass

    def handle_resize_event(self, ev: pg.event.Event, tet:tetrimino.Tetrimino ):
        pass

    def next_tet(self):
        return tetrimino.random_tetrimino(0, 0, self.board_args)

    def quit(self, _: tetrimino.Tetrimino):
        pg.event.post(pg.event.Event(pg.QUIT))

    def loop(self):
        tet = self.next_tet()
        while True:
            if not tet.is_alive():
                tet = self.next_tet()

            if self.since_last_down_move > DOWN_SPEED_MS:
                self.move_down(tet)

            for ev in pg.event.get():
                if ev.type == pg.QUIT:
                    pg.quit()
                    return
                if func := self.event_handlers.get(ev.type, None):
                    func(ev, tet)

            self.screen.fill(tetrimino.colors[0])
            self.board.update()
            self.board.draw(self.screen)
            tet.update()
            tet.draw(self.screen)

            pg.display.flip()
            self.since_last_down_move += self.clock.tick(FPS)


def init_pygame() -> pg.surface.Surface:
    pg.init()
    if not pg.get_init():
        print("oh no! pygame not init'd")
        exit(1)

    screen: pg.surface.Surface = pg.display.set_mode(SCREENRECT.size, pg.RESIZABLE)
    pg.display.set_caption("Tetris")
    pg.key.set_repeat(100, 50)

    return screen

import argparse

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--debug", action="store_true", help="print debug logeroos")

    return parser.parse_args()

def main():
    args = parse_args()
    if args.debug:
        logging.basicConfig(level=logging.DEBUG)
    
    global logger
    logger = logging.getLogger(__name__)

    scrn: pg.surface.Surface = init_pygame()
    board_args: BoardArgs = BoardArgs.make_default()
    tetris = Tetris(screen=scrn, board_args=board_args)
    tetris.loop()
    exit(0)


if __name__ == "__main__":
    main()
