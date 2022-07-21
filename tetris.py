from sys import exit
from typing import ClassVar
from enum import Enum, unique

import pygame as pg
from pygame.locals import *

import tetrimino


SCREENRECT = pg.Rect(0, 0, 720, 1280)
BOARD_COLS = 10
BOARD_ROWS = 20
BLOCK_PX_SIDE = 20
BOARD = {
    "cols": BOARD_COLS,
    "rows": BOARD_ROWS,
    "block_px_side": BLOCK_PX_SIDE,
    "color": (0, 0, 0),
    "cell_sprites": [[None for i in range(BOARD_COLS)] for j in range(BOARD_ROWS)],
    "rect": pg.Rect(10, 10, BLOCK_PX_SIDE * BOARD_COLS, BLOCK_PX_SIDE * BOARD_ROWS),
}
FPS = 60
DOWN_SPEED_MS = 1000

import pdb


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
        self.cell_sprites = board["cell_sprites"]

    def draw(self, surface):
        self.group.draw(surface)

    def update(self):
        self.group.update()

    def take_blocks(self, tetrimino):
        print("taking blocks")
        # pdb.set_trace()
        group_sprites = tetrimino.group.sprites()
        for b in group_sprites:
            pos = b.get_board_pos()
            self.cell_sprites[pos["row"]][pos["col"]] = b

        # add these two the group so we can have pygame manage them
        self.group.add(group_sprites)
        tetrimino.group.remove(group_sprites)
        print("taking blocks done")

    def find_and_kill_lines(self):
        dead_rows = []
        for row in self.cell_sprites[::-1]:
            if all(row):
                print("found dead row")
                dead_rows.append(row)

        for row in dead_rows:
            for b in row:
                b.kill()
            # remove this row from cell_sprites
            self.cell_sprites.remove(row)
            # pre-pend a new row to cell_sprites
            self.cell_sprites.insert(0, [None for i in range(len(row))])

        # update each block's cell position so it matches the board
        if dead_rows:
            for ri, row in enumerate(self.cell_sprites):
                for block in row:
                    if block:
                        block.set_board_pos(col=block.col, row=ri)

        return len(dead_rows)


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

    def __init__(self, screen) -> None:
        self.screen = screen
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
        # pass

    def next_tet(self):
        return tetrimino.random_tetrimino(0, 0, **BOARD)

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
