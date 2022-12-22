
from enum import Enum, auto, unique

@unique
class MoveNames(Enum):
    DOWN = auto()
    UP = auto()
    LEFT = auto()
    RIGHT = auto()