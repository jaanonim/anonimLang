from enum import Enum


class TokenType(Enum):
    INT = 1
    FLOAT = 2
    PLUS = 3
    MINUS = 4
    MUL = 5
    DIV = 6
    LPAREN = 7
    RPAREN = 8
    EOF = 9


class Token:
    DIGITS = "0123456789"

    def __init__(self, type_, value=None, pos_start=None, pos_end=None):
        self.type = type_
        self.value = value
        if pos_start:
            self.pos_start = pos_start.copy()
            self.pos_end = pos_start.copy()
            self.pos_end.advance()
        if pos_end:
            self.pos_end = pos_end.copy()

    def __repr__(self):
        if self.value:
            return f"{self.type.name}:{self.value}"
        return f"{self.type.name}"
