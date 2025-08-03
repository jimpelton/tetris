from abc import ABC

import pygame as pg


class EventHandler(ABC):
    def on_event(self, ev: pg.event.Event, game_time: float):
        raise NotImplementedError("on_event must be implemented")

