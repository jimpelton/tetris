from .move_names import MoveNames

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