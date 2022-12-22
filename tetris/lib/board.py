from dataclasses import dataclass
from typing import List, Tuple
import pygame as pg


@dataclass
class BoardArgs:
    n_cols: int
    n_rows: int
    block_px_side: int
    color: Tuple[int, int, int]
    cell_sprites: List[List[None | pg.sprite.Sprite]]
    rect: pg.Rect


class BoardSprite(pg.sprite.Sprite):
    """Represents image of the Board on the screen"""

    def __init__(self, board_args) -> None:
        super().__init__()
        self.board_args = board_args

        self.image = pg.Surface((board_args.rect.width, board_args.rect.height))
        self.image.fill(board_args.color)
        self.rect = self.image.get_rect()

        pg.draw.rect(self.image, (255, 255, 255), self.rect, width=1)

class Board:
    def __init__(self, board_args: BoardArgs) -> None:
        self.board_args = board_args
        self.board_sprite = BoardSprite(board_args=board_args)
        self.group = pg.sprite.Group()
        self.group.add(self.board_sprite)

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
            # self.cell_sprites[pos["row"]][pos["col"]] = b
            self.board_args.cell_sprites[pos.row][pos.col] = b

        # add these two the group so we can have pygame manage them
        self.group.add(group_sprites)
        tetrimino.group.remove(group_sprites)
        print("taking blocks done")

    def find_and_kill_lines(self):
        dead_rows = []
        for row in self.board_args.cell_sprites[::-1]:
            if all(row):
                print("found dead row")
                dead_rows.append(row)

        for row in dead_rows:
            for b in row:
                b.kill()
            # remove this row from cell_sprites
            self.board_args.cell_sprites.remove(row)
            # pre-pend a new row to cell_sprites
            self.board_args.cell_sprites.insert(0, [None for i in range(len(row))])

        # update each block's cell position so it matches the board
        if dead_rows:
            for ri, row in enumerate(self.board_args.cell_sprites):
                for block in row:
                    if block:
                        block.set_board_pos(col=block.board_pos.col, row=ri)

        return len(dead_rows)
