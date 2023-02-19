from dataclasses import dataclass
from typing import List, Tuple, Final
import pygame as pg

from .boad_args import BoardArgs


class BoardSprite(pg.sprite.Sprite):
    """Represents image of the Board on the screen"""

    def __init__(self, board_args: BoardArgs) -> None:
        super().__init__()
        self.board_args = board_args

        self.image: pg.Surface = pg.Surface((board_args.rect.width, board_args.rect.height))
        self.image.fill(board_args.color)
        self.rect: pg.Rect = self.image.get_rect()

        pg.draw.rect(self.image, (255, 255, 255), self.rect, width=1)


class Board:
    def __init__(self, board_args: BoardArgs) -> None:
        self.board_args: Final[BoardArgs] = board_args
        self.board_sprite = BoardSprite(board_args=board_args)
        # blocks that are not part of a tet anymore. after a tetrimino has
        # been deemed unable to move down anymore it's blocks are copied into
        # this group.
        self.frozen_blocks_group = pg.sprite.Group()
        # the group also has the boardsprite rectangular outline in it...
        # TODO: rename frozen_blocks_group to more appropriate name
        self.frozen_blocks_group.add(self.board_sprite)

    def draw(self, surface):
        self.frozen_blocks_group.draw(surface)

    def update(self):
        self.frozen_blocks_group.update()

    def take_blocks(self, tetrimino):
        print("taking blocks")
        # pdb.set_trace()
        group_sprites = tetrimino.group.sprites()
        for b in group_sprites:
            pos = b.get_board_pos()
            # self.cell_sprites[pos["row"]][pos["col"]] = b
            self.board_args.cell_sprites[pos.row][pos.col] = b

        # add these two the group so we can have pygame manage them
        self.frozen_blocks_group.add(group_sprites)
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
