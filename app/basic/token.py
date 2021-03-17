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


class Token:
    DIGITS = "0123456789"

    def __init__(self, type_, value=None):
        self.type = type_
        self.value = value

    def __repr__(self):
        if self.value:
            return f"{self.type.name}:{self.value}"
        return f"{self.type.name}"
