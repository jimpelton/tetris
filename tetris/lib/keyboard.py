from typing import Dict, Callable, Final, Set

import pygame as pg
from .move_names import MoveNames

from . import event_handler

KEY_REPEAT_DELAY: Final[int] = 100


KEY_MAP: Dict[int, MoveNames] = {
    pg.K_d: MoveNames.RIGHT,
    pg.K_a: MoveNames.LEFT,
    pg.K_s: MoveNames.DOWN,
    pg.K_w: MoveNames.ROTATE,
    pg.K_SPACE: MoveNames.DROP,
}


class Keyboard(event_handler.EventHandler):
    def __init__(self) -> None:
        self.since_last_key_event: Dict[MoveNames, float] = {
            MoveNames.RIGHT: 0.0,
            MoveNames.LEFT: 0.0,
            MoveNames.DOWN: 0.0,
            MoveNames.ROTATE: 0.0,
            MoveNames.DROP: 0.0,
        }

        # keys that ignore the key repeat (must be released)
        self.not_repeatable_keys = (MoveNames.DROP, MoveNames.ROTATE)
        self.key_was_down_previously: Set[MoveNames] = set()

        self.event_handlers: Dict[int, Callable[[pg.event.Event, float], None]] = {
            pg.KEYDOWN: self.handle_key_down,
            pg.KEYUP: self.handle_key_up,
        }

        self._keys_down: Set[MoveNames] = set()

    @property
    def keys_down(self) -> Set[MoveNames]:
        rval = self._keys_down.copy()
        self._keys_down.clear()
        return rval

    def on_event(self, ev: pg.event.Event, game_time: float):
        if handler := self.event_handlers.get(ev.type):
            handler(ev, game_time)

    def handle_key_down(self, ev: pg.event.Event, game_time: float):
        if ev.key not in KEY_MAP:
            return

        key = KEY_MAP[ev.key]
        
        if key in self.not_repeatable_keys:
            # check if eligible to register as a press
            if key not in self.key_was_down_previously:
                self.key_was_down_previously.add(key)
                self._keys_down.add(key)
            
            return

        now = game_time
        current_diff = now - self.since_last_key_event[key]
        if current_diff >= KEY_REPEAT_DELAY:
            self._keys_down.add(key)
            self.since_last_key_event[key] = 0.0
        else:
            self.since_last_key_event[key] = current_diff
        
    def handle_key_up(self, ev: pg.event.Event, game_time: float):
        if ev.key not in KEY_MAP:
            return
        
        key = KEY_MAP[ev.key]
        self.key_was_down_previously.discard(key)
        self.since_last_key_event[key] = 0.0

