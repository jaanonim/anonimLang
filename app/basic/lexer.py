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
                tokens.append(Token(TokenType.PLUS, pos_start=self.pos))
                self.advance()
            elif self.char == "-":
                tokens.append(Token(TokenType.MINUS, pos_start=self.pos))
                self.advance()
            elif self.char == "*":
                tokens.append(Token(TokenType.MUL, pos_start=self.pos))
                self.advance()
            elif self.char == "/":
                tokens.append(Token(TokenType.DIV, pos_start=self.pos))
                self.advance()
            elif self.char == "(":
                tokens.append(Token(TokenType.LPAREN, pos_start=self.pos))
                self.advance()
            elif self.char == ")":
                tokens.append(Token(TokenType.RPAREN, pos_start=self.pos))
                self.advance()
            else:
                pos_start = self.pos.copy()
                char = self.char
                self.advance()
                return [], IllegalCharError(pos_start, self.pos, "'" + char + "'")

        tokens.append(Token(TokenType.EOF, pos_start=self.pos))
        return tokens, None

    def make_number(self):
        num_str = ""
        dot_count = 0
        pos_start = self.pos.copy()

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
            return Token(TokenType.INT, int(num_str), pos_start, self.pos.copy())
        else:
            return Token(TokenType.FLOAT, float(num_str), pos_start, self.pos.copy())
