import pygame as pg

from .tetrimino import Tetrimino

class Screen():
    def __init__(self, surf: pg.surface.Surface) -> None:
        super().__init__()
        self._cur_tet: Tetrimino | None = None
        self._group: pg.sprite.Group = pg.sprite.Group()
        self._screen_surf: pg.surface.Surface = surf

    def update(self, *args, **kwargs):
        self._group.update(*args, **kwargs)

    def draw(self, *args, **kwargs):
        self._group.draw(*args, **kwargs)
