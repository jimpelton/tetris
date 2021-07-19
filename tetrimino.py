import pygame as pg


class Block(pg.sprite.Sprite):
    pass


class Tetrimino:
    BOARD = []
    def __init__(self) -> None:
        pass


class I(Tetrimino):
    BOARD = [
        [0, 0, 1, 0, 0],
        [0, 0, 1, 0, 0],
        [0, 0, 1, 0, 0],
        [0, 0, 1, 0, 0],
        [0, 0, 0, 0, 0],
    ]

    def __init__(self) -> None:
        super().__init__()


class J(Tetrimino):
    BOARD = [
        [],
        [],
        [],
        [],
        [],
        [],
    ]

    def __init__(self) -> None:
        super().__init__()


class L(Tetrimino):
    BOARD = [
        [],
        [],
        [],
        [],
        [],
        [],
    ]

    def __init__(self) -> None:
        super().__init__()


class O(Tetrimino):
    BOARD = [
        [],
        [],
        [],
        [],
        [],
        [],
    ]

    def __init__(self) -> None:
        super().__init__()


class S(Tetrimino):
    BOARD = [
        [],
        [],
        [],
        [],
        [],
        [],
    ]

    def __init__(self) -> None:
        super().__init__()


class T(Tetrimino):
    BOARD = [
        [],
        [],
        [],
        [],
        [],
        [],
    ]

    def __init__(self) -> None:
        super().__init__()


class Z(Tetrimino):
    BOARD = [
        [],
        [],
        [],
        [],
        [],
        [],
    ]

    def __init__(self) -> None:
        super().__init__()
