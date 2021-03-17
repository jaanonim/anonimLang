from .error import IllegalCharError
from .position import Position
from .token import Token, TokenType


class Lexer:
    def __init__(self, fn, text):
        self.fn = fn
        self.text = text
        self.pos = Position(-1, 0, -1, fn, text)
        self.char = None
        self.advance()

    def advance(self):
        self.pos.advance(self.char)
        self.char = self.text[self.pos.id] if self.pos.id < len(self.text) else None

    def make_tokens(self):
        tokens = []

        while self.char != None:
            if self.char in " \t":
                self.advance()
            elif self.char in Token.DIGITS:
                tokens.append(self.make_number())
            elif self.char == "+":
                tokens.append(Token(TokenType.PLUS))
            elif self.char == "-":
                tokens.append(Token(TokenType.MINUS))
            elif self.char == "*":
                tokens.append(Token(TokenType.MUL))
            elif self.char == "/":
                tokens.append(Token(TokenType.DIV))
            elif self.char == "(":
                tokens.append(Token(TokenType.LPAREN))
            elif self.char == ")":
                tokens.append(Token(TokenType.RPAREN))
            else:
                pos_start = self.pos.copy()
                char = self.char
                self.advance()
                return [], IllegalCharError(pos_start, self.pos, "'" + char + "'")

        return tokens, None

    def make_number(self):
        num_str = ""
        dot_count = 0

        while self.char != None and self.char in Token.DIGITS + ".":
            if self.char == ".":
                if dot_count == 1:
                    break
                dot_count += 1
                num_str += "."
            else:
                num_str += self.char
            self.advance()

        if dot_count == 0:
            return Token(TokenType.INT, int(num_str))
        else:
            return Token(TokenType.FLOAT, float(num_str))


def run(fn, text):
    l = Lexer(fn, text)
    t, error = l.make_tokens()

    return t, error
