from .error import InvalidSyntaxError
from .nodes import BinOpNode, NumberNode, UnaryOpNode
from .token import TokenType


class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.t_id = -1
        self.advance()

    def advance(self):
        self.t_id += 1
        if self.t_id < len(self.tokens):
            self.current_token = self.tokens[self.t_id]
        return self.current_token

    def parse(self):
        res = self.expr()
        if not res.error and self.current_token.type != TokenType.EOF:
            return res.failure(
                InvalidSyntaxError(
                    self.current_token.pos_start,
                    self.current_token.pos_end,
                    "Excepted '+', '-', '*', '/'",
                )
            )
        return res

    def atom(self):
        res = ParserResult()
        t = self.current_token

        if t.type in (TokenType.INT, TokenType.FLOAT):
            res.register(self.advance())
            return res.success(NumberNode(t))
        elif t.type == TokenType.LPAREN:
            res.register(self.advance())
            expr = res.register(self.expr())
            if res.error:
                return res
            if self.current_token.type == TokenType.RPAREN:
                res.register(self.advance())
                return res.success(expr)
            else:
                return res.failure(
                    InvalidSyntaxError(
                        self.current_token.pos_start,
                        self.current_token.pos_end,
                        "Expected ')'",
                    )
                )

        return res.failure(
            InvalidSyntaxError(
                t.pos_start,
                t.pos_end,
                "Excepted number or '+', '-', '('",
            )
        )

    def power(self):
        return self.bin_op(self.atom, (TokenType.POW,), self.factor)

    def factor(self):
        res = ParserResult()
        t = self.current_token

        if t.type in (TokenType.PLUS, TokenType.MINUS):
            res.register(self.advance())
            factor = res.register(self.factor())
            if res.error:
                return res
            return res.success(UnaryOpNode(t, factor))

        return self.power()

    def term(self):
        return self.bin_op(self.factor, (TokenType.MUL, TokenType.DIV))

    def expr(self):
        return self.bin_op(self.term, (TokenType.PLUS, TokenType.MINUS))

    def bin_op(self, func_a, ops, func_b=None):
        if func_b == None:
            func_b = func_a

        res = ParserResult()
        left = res.register(func_a())
        if res.error:
            return res

        while self.current_token.type in ops:
            op = self.current_token
            res.register(self.advance())
            rigth = res.register(func_b())
            if res.error:
                return res
            left = BinOpNode(op, left, rigth)

        return res.success(left)


class ParserResult:
    def __init__(self):
        self.error = None
        self.node = None

    def register(self, res):
        if isinstance(res, ParserResult):
            if res.error:
                self.error = res.error
            return res.node
        return res

    def success(self, node):
        self.node = node
        return self

    def failure(self, error):
        self.error = error
        return self
