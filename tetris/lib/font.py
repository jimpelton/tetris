import pathlib
from typing import List, Tuple, Iterable, Final

import pygame


# Heavily inspired by DaFluffyPotato's video:
# https://www.youtube.com/watch?v=Lh-cc5qzDqk
# The clip() logic is pretty much verbatim.


def _clip(surf: pygame.Surface, x: int, y: int, x_size: int, y_size: int) -> pygame.Surface:
    handle_surf = surf.copy()
    clip_r = pygame.Rect(x, y, x_size, y_size)
    handle_surf.set_clip(clip_r)
    image = surf.subsurface(handle_surf.get_clip())
    return image.copy()


class Font:
    def __init__(
            self,
            path: pathlib.Path,
            c_order: List[str] | str,
            c_width: Tuple[int, int] | int,
    ):
        sheet = pygame.image.load(path)
        self._chars = self._cut_sprites(sheet, c_order, c_width)

        self._char_spacing: int = 1
        self._char_width = c_width
        self._white_space_width = c_width[0]

    def render(self, surf: pygame.Surface, text: str, loc: Tuple[int, int]):
        """Blit the text onto the surface at location in loc."""
        x_offset = 0
        for c in text:
            if c != ' ':
                surf.blit(self._chars[c], (loc[0] + x_offset, loc[1]))
                x_offset += self._chars[c].get_width() + self._char_spacing
            else:
                x_offset += self._white_space_width + self._char_spacing

    def _cut_sprites(
            self,
            img: pygame.Surface,
            order: Iterable[str] | str,
            width: Tuple[int, int]
    ):
        """Cut sprites out of the sprite sheet given by img."""
        chars = {}
        x_w, y_w = width[0], width[1]
        start_x = 0
        start_y: Final = 0
        for c in order:
            char_img = _clip(img, start_x, start_y, x_w, y_w)
            chars[c] = char_img.copy()
            start_x += x_w

        return chars
