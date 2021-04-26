from .error import ExceptedCharError, IllegalCharError
from .position import Position
from .token import Token, TokenKeywords, TokenType


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
            elif self.char in Token.LETTERS:
                tokens.append(self.make_identifier())
            elif self.char == '"':
                tokens.append(self.make_string())
            elif self.char == "+":
                tokens.append(Token(TokenType.PLUS, pos_start=self.pos))
                self.advance()
            elif self.char == "-":
                tokens.append(self.make_arrow())
            elif self.char == "*":
                tokens.append(Token(TokenType.MUL, pos_start=self.pos))
                self.advance()
            elif self.char == "/":
                token = self.make_comment()
                if token:
                    tokens.append(token)
            elif self.char == "^":
                tokens.append(Token(TokenType.POW, pos_start=self.pos))
                self.advance()
            elif self.char == "(":
                tokens.append(Token(TokenType.LPAREN, pos_start=self.pos))
                self.advance()
            elif self.char == ")":
                tokens.append(Token(TokenType.RPAREN, pos_start=self.pos))
                self.advance()
            elif self.char == "[":
                tokens.append(Token(TokenType.LSQUARE, pos_start=self.pos))
                self.advance()
            elif self.char == "]":
                tokens.append(Token(TokenType.RSQUARE, pos_start=self.pos))
                self.advance()
            elif self.char == "{":
                tokens.append(Token(TokenType.LCURBRA, pos_start=self.pos))
                self.advance()
            elif self.char == "}":
                tokens.append(Token(TokenType.RCURBRA, pos_start=self.pos))
                self.advance()
            elif self.char in ";\n":
                tokens.append(Token(TokenType.NEWLINE, pos_start=self.pos))
                self.advance()
            elif self.char == "!":
                t, e = self.make_not_equals()
                if e:
                    return [], e
                tokens.append(t)
                self.advance()
            elif self.char == "=":
                tokens.append(self.make_equals())
            elif self.char == ">":
                tokens.append(self.make_greader())
            elif self.char == "<":
                tokens.append(self.make_less())
            elif self.char == ",":
                tokens.append(Token(TokenType.COMMA, pos_start=self.pos))
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

    def make_identifier(self):
        id_str = ""
        pos_start = self.pos.copy()

        while self.char != None and self.char in Token.LETTERS_DIGITS:
            id_str += self.char
            self.advance()

        tok_type = (
            TokenType.KEYWORD
            if id_str in [e.value for e in TokenKeywords]
            else TokenType.IDENTIFIRER
        )
        return Token(tok_type, id_str, pos_start, self.pos)

    def make_not_equals(self):
        pos_start = self.pos.copy()
        self.advance()
        if self.char == "=":
            return Token(TokenType.NE, pos_start=pos_start, pos_end=self.pos), None

        return None, ExceptedCharError(pos_start, self.pos, "'=' after '!'")

    def make_equals(self):
        type_ = TokenType.EQ
        pos_start = self.pos.copy()
        self.advance()
        if self.char == "=":
            type_ = TokenType.EE
            self.advance()
        return Token(type_, pos_start=pos_start, pos_end=self.pos)

    def make_less(self):
        type_ = TokenType.LT
        pos_start = self.pos.copy()
        self.advance()
        if self.char == "=":
            type_ = TokenType.LTE
            self.advance()
        return Token(type_, pos_start=pos_start, pos_end=self.pos)

    def make_greader(self):
        type_ = TokenType.GT
        pos_start = self.pos.copy()
        self.advance()
        if self.char == "=":
            type_ = TokenType.GTE
            self.advance()
        return Token(type_, pos_start=pos_start, pos_end=self.pos)

    def make_arrow(self):
        type_ = TokenType.MINUS
        pos_start = self.pos.copy()
        self.advance()
        if self.char == ">":
            type_ = TokenType.ARROW
            self.advance()
        return Token(type_, pos_start=pos_start, pos_end=self.pos)

    def make_string(self):
        string = ""
        pos_start = self.pos.copy()
        escape_char = False
        self.advance()

        escape_chars = {"n": "\n", "t": "\t"}

        while self.char != None and self.char != '"' or escape_char:
            if escape_char:
                string += escape_chars.get(self.char, self.char)
                escape_char = False
            else:
                if self.char == "\\":
                    escape_char = True
                else:
                    string += self.char
            self.advance()

        self.advance()
        return Token(TokenType.STRING, string, pos_start=pos_start, pos_end=self.pos)

    def make_comment(self):
        pos_start = self.pos.copy()
        self.advance()
        if self.char == "/":
            self.advance()
            while self.char != "\n":
                if self.char == None:
                    break
                self.advance()
            self.advance()
        elif self.char == "*":
            self.advance()
            while True:
                if self.char == None:
                    break
                if self.char == "*":
                    self.advance()
                    if self.char == "/":
                        break
                self.advance()
            self.advance()
        else:
            return Token(TokenType.DIV, pos_start=self.pos)
