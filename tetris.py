import dataclasses
from sys import exit
from typing import Callable, ClassVar, Dict
from enum import Enum, auto, unique

import pygame as pg
from pygame.locals import *
from board import Board, BoardArgs

import tetrimino


SCREENRECT = pg.Rect(0, 0, 720, 1280)
FPS = 60
DOWN_SPEED_MS = 1000

_BOARD_COLS = 10
_BOARD_ROWS = 20
_BLOCK_PX_SIDE = 20
_BOARD_DEFAULTS = {
    "n_cols": _BOARD_COLS,
    "n_rows": _BOARD_ROWS,
    "block_px_side": _BLOCK_PX_SIDE,
    "color": (0, 0, 0),
    "cell_sprites": [[None for i in range(_BOARD_COLS)] for j in range(_BOARD_ROWS)],
    "rect": pg.Rect(10, 10, _BLOCK_PX_SIDE * _BOARD_COLS, _BLOCK_PX_SIDE * _BOARD_ROWS),
}

board_args = dataclasses.replace(BoardArgs, **_BOARD_DEFAULTS)



@unique
class MoveNames(Enum):
    DOWN = auto()
    UP = auto()
    LEFT = auto()
    RIGHT = auto()

class Keyboard:
    def __init__(self) -> None:
        self.since_move_events = {
            MoveNames.DOWN: 0.0,
            MoveNames.UP: 0.0,
            MoveNames.LEFT: 0.0,
            MoveNames.RIGHT: 0.0,
        }

    def update_time(self, move: MoveNames, tm: float):
        prev = self.since_move_events[move]
        self.since_move_events[move] = tm - prev

    def clear_time(self, move: MoveNames):
        self.since_move_events[move] = 0.0

class Tetris:
    initial_key_repeat_delay_ms: ClassVar[int] = 100
    key_repeat_delay_ms: ClassVar[int] = 50

    def __init__(self, screen, board_args) -> None:
        self.screen = screen
        self.clock = pg.time.Clock()
        self.board = Board(board_args)

        self.since_last_down_move = 0

        self.event_handlers: Dict[int, Callable[[tetrimino.Tetrimino], None]] = {
            pg.K_d: self.move_right,
            pg.K_a: self.move_left,
            pg.K_s: self.move_down,
            pg.K_w: self.rotate_clockwise,
            pg.KEYDOWN: self.handle_key_down,
            pg.KEYUP: self.handle_key_up,
        }


    def copy_tetrimino_to_board(self, tetrimino):
        self.board.take_blocks(tetrimino)
        tetrimino.set_alive(False)
        lines_found = self.board.find_and_kill_lines()
        print(f"found {lines_found} lines")

    def move_right(self, tetrimino):
        # pg.key.set_repeat(self.initial_key_repeat_delay_ms, self.key_repeat_delay_ms)
        if tetrimino.can_move_by(1, 0):
            tetrimino.move_by(1, 0)

    def move_left(self, tetrimino):
        # pg.key.set_repeat(self.initial_key_repeat_delay_ms, self.key_repeat_delay_ms)
        if tetrimino.can_move_by(-1, 0):
            tetrimino.move_by(-1, 0)

    def move_down(self, tetrimino):
        # pg.key.set_repeat(self.initial_key_repeat_delay_ms, self.key_repeat_delay_ms)
        if tetrimino.can_move_by(0, 1):
            tetrimino.move_by(0, 1)
            self.since_last_down_move = 0
        else:
            print("tet couldn't move")
            self.copy_tetrimino_to_board(tetrimino)

    def rotate_clockwise(self, tetrimino):
        tetrimino.rotate_clockwise()

    def handle_key_down(self, ev, tet):
        print("key down event")
        # pg.key.set_repeat(self.initial_key_repeat_delay_ms, self.key_repeat_delay_ms)
        if func := self.event_handlers.get(ev.key, None):
            func(tet)

    def handle_key_up(self, ev, tet):
        # pg.key.set_repeat(0)
        pass

    def next_tet(self):
        return tetrimino.random_tetrimino(0, 0, board_args)

    def loop(self):
        tet = self.next_tet()
        while True:
            if not tet.is_alive():
                tet = self.next_tet()

            if self.since_last_down_move > DOWN_SPEED_MS:
                if tet.can_move_by(0, 1):
                    tet.move_by(0, 1)
                    self.since_last_down_move = 0
                else:
                    self.copy_tetrimino_to_board(tet)

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


def init_pygame():
    pg.init()
    if not pg.get_init():
        print("oh no! pygame not init'd")
        exit(1)

    screen = pg.display.set_mode(SCREENRECT.size)
    pg.display.set_caption("Tetris")
    pg.key.set_repeat(100, 50)

    return screen


def main():
    scrn = init_pygame()
    tetris = Tetris(scrn)
    tetris.loop()
    exit(0)


if __name__ == "__main__":
    main()
