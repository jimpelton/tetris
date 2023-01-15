from sys import exit
from typing import Callable, ClassVar, Dict

import pygame as pg
from pygame.locals import *
from lib import Board, BoardArgs

from lib import tetrimino

SCREENRECT = pg.Rect(0, 0, 720, 720)
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


class Tetris:
    initial_key_repeat_delay_ms: ClassVar[int] = 100
    key_repeat_delay_ms: ClassVar[int] = 50

    def __init__(self, screen: pg.display, board_args: BoardArgs) -> None:
        self.screen: pg.display = screen
        self.clock: pg.time.Clock = pg.time.Clock()
        self.board_args: BoardArgs = board_args
        self.board: Board = Board(board_args)

        self.since_last_down_move: float = 0

        self.event_handlers: Dict[int, Callable[[tetrimino.Tetrimino], None]] = {
            pg.KEYDOWN: self.handle_key_down,
            pg.KEYUP: self.handle_key_up,
            # pg.VIDEORESIZE: self.handle_video_resize,
        }

        self.key_down_event_handlers: Dict[int, Callable] = {
            pg.K_d: self.move_right,
            pg.K_a: self.move_left,
            pg.K_s: self.move_down,
            pg.K_w: self.rotate_clockwise,
        }

    def copy_tetrimino_to_board(self, tet: tetrimino.Tetrimino):
        self.board.take_blocks(tet)
        tet.set_alive(False)
        lines_found = self.board.find_and_kill_lines()
        print(f"found {lines_found} lines")

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
            print("tet couldn't move")
            self.copy_tetrimino_to_board(tet)

    def rotate_clockwise(self, tet: tetrimino.Tetrimino):
        tet.rotate_clockwise()

    def handle_key_down(self, ev, tet: tetrimino.Tetrimino):
        print("key down event")
        # pg.key.set_repeat(self.initial_key_repeat_delay_ms, self.key_repeat_delay_ms)
        if func := self.key_down_event_handlers.get(ev.key, None):
            func(tet)

    def handle_key_up(self, ev, tet: tetrimino.Tetrimino):
        # pg.key.set_repeat(0)
        pass

    def handle_resize_event(self, ev, tet:tetrimino.Tetrimino ):
        pass

    def next_tet(self):
        return tetrimino.random_tetrimino(0, 0, self.board_args)

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


def init_pygame() -> pg.display:
    pg.init()
    if not pg.get_init():
        print("oh no! pygame not init'd")
        exit(1)

    screen: pg.display = pg.display.set_mode(SCREENRECT.size, pg.RESIZABLE)
    pg.display.set_caption("Tetris")
    pg.key.set_repeat(100, 50)

    return screen


def main():
    scrn: pg.display = init_pygame()
    board_args: BoardArgs = BoardArgs(**_BOARD_DEFAULTS)
    tetris = Tetris(screen=scrn, board_args=board_args)
    tetris.loop()
    exit(0)


if __name__ == "__main__":
    main()
