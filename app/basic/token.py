import string
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
    POW = 10
    IDENTIFIRER = 11
    KEYWORD = 12
    EQ = 13
    EE = 14
    NE = 15
    LT = 15
    GT = 17
    GTE = 18
    LTE = 19


class Token:
    DIGITS = "0123456789"
    LETTERS = string.ascii_letters
    LETTERS_DIGITS = LETTERS + DIGITS
    KEYWORDS = ["var", "and", "or", "not"]

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

    def maches(self, type_, value):
        return self.type == type_ and self.value == value
