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
    COMMA = 20
    ARROW = 21
    STRING = 22
    LSQUARE = 23
    RSQUARE = 23


class TokenKeywords(Enum):
    _var = "var"
    _and = "and"
    _or = "or"
    _not = "not"
    _if = "if"
    _else = "else"
    _then = "then"
    _elif = "elif"
    _for = "for"
    _to = "to"
    _step = "step"
    _while = "while"
    _func = "def"


"""
Polish wersion for noobs

class TokenKeywords(Enum):
    _var = "zmienna"
    _and = "and"
    _or = "lub"
    _not = "nie"
    _if = "jezeli"
    _else = "inaczej"
    _then = "wtedy"
    _elif = "inaczej_jesli"
    _for = "powtazaj"
    _to = "do"
    _step = "co"
    _while = "dopuki"

"""


class Token:
    DIGITS = "0123456789"
    LETTERS = string.ascii_letters
    LETTERS_DIGITS = LETTERS + DIGITS + "_"

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

    def isKeword(self, keyword):
        return self.type == TokenType.KEYWORD and self.value == keyword.value
