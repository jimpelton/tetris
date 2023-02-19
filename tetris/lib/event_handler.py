import pygame as pg


class EventHandler:
    def on_event(self, ev: pg.event.Event, game_time: float):
        raise NotImplementedError("on_event must be implemented")

