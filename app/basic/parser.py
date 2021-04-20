from .error import InvalidSyntaxError
from .nodes import (
    BinOpNode,
    ForNode,
    IfNode,
    NumberNode,
    UnaryOpNode,
    VarAccessNode,
    VarAssignNode,
    WhileNode,
)
from .token import TokenKeywords, TokenType


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
                    "Excepted '+', '-', '*', '/', '^'",
                )
            )
        return res

    def if_expr(self):
        res = ParserResult()
        cases = []
        else_case = None

        if not self.current_token.isKeword(TokenKeywords._if):
            return res.failure(
                InvalidSyntaxError(
                    self.current_token.pos_start,
                    self.current_token.pos_end,
                    f"Expected 'if'",
                )
            )

        res.register_advance()
        self.advance()

        condition = res.register(self.expr())
        if res.error:
            return res

        if not self.current_token.isKeword(TokenKeywords._then):
            return res.failure(
                InvalidSyntaxError(
                    self.current_token.pos_start,
                    self.current_token.pos_end,
                    f"Expected 'then'",
                )
            )

        res.register_advance()
        self.advance()

        expr = res.register(self.expr())
        if res.error:
            return res
        cases.append((condition, expr))

        while self.current_token.isKeword(TokenKeywords._elif):
            res.register_advance()
            self.advance()

            condition = res.register(self.expr())
            if res.error:
                return res

            if not self.current_token.isKeword(TokenKeywords._then):
                return res.failure(
                    InvalidSyntaxError(
                        self.current_token.pos_start,
                        self.current_token.pos_end,
                        f"Expected 'then'",
                    )
                )

            res.register_advance()
            self.advance()

            expr = res.register(self.expr())
            if res.error:
                return res
            cases.append((condition, expr))

        if self.current_token.isKeword(TokenKeywords._else):
            res.register_advance()
            self.advance()

            else_case = res.register(self.expr())
            if res.error:
                return res

        return res.success(IfNode(cases, else_case))

    def for_expr(self):
        res = ParserResult()
        if not self.current_token.isKeword(TokenKeywords._for):
            return res.failure(
                InvalidSyntaxError(
                    self.current_token.pos_start,
                    self.current_token.pos_end,
                    f"Expected 'for'",
                )
            )

        res.register_advance()
        self.advance()

        if self.current_token.type != TokenType.IDENTIFIRER:
            return res.failure(
                InvalidSyntaxError(
                    self.current_token.pos_start,
                    self.current_token.pos_end,
                    f"Expected identifier",
                )
            )

        var_name = self.current_token
        res.register_advance()
        self.advance()

        if self.current_token.type != TokenType.EQ:
            return res.failure(
                InvalidSyntaxError(
                    self.current_token.pos_start,
                    self.current_token.pos_end,
                    f"Expected '='",
                )
            )

        res.register_advance()
        self.advance()

        start_value = res.register(self.expr())
        if res.error:
            return res

        if not self.current_token.isKeword(TokenKeywords._to):
            return res.failure(
                InvalidSyntaxError(
                    self.current_token.pos_start,
                    self.current_token.pos_end,
                    f"Expected 'to'",
                )
            )

        res.register_advance()
        self.advance()

        end_value = res.register(self.expr())
        if res.error:
            return res

        if self.current_token.isKeword(TokenKeywords._step):
            res.register_advance()
            self.advance()

            step_value = res.register(self.expr())
            if res.error:
                return res
        else:
            step_value = None

        if not self.current_token.isKeword(TokenKeywords._then):
            return res.failure(
                InvalidSyntaxError(
                    self.current_token.pos_start,
                    self.current_token.pos_end,
                    f"Expected 'then'",
                )
            )

        res.register_advance()
        self.advance()

        body = res.register(self.expr())
        if res.error:
            return res

        return res.success(ForNode(var_name, start_value, end_value, step_value, body))

    def while_expr(self):
        res = ParserResult()

        if not self.current_token.isKeword(TokenKeywords._while):
            return res.failure(
                InvalidSyntaxError(
                    self.current_token.pos_start,
                    self.current_token.pos_end,
                    f"Expected 'WHILE'",
                )
            )

        res.register_advance()
        self.advance()

        condition = res.register(self.expr())
        if res.error:
            return res

        if not self.current_token.isKeword(TokenKeywords._then):
            return res.failure(
                InvalidSyntaxError(
                    self.current_token.pos_start,
                    self.current_token.pos_end,
                    f"Expected 'THEN'",
                )
            )

        res.register_advance()
        self.advance()

        body = res.register(self.expr())
        if res.error:
            return res

        return res.success(WhileNode(condition, body))

    def atom(self):
        res = ParserResult()
        t = self.current_token

        if t.type in (TokenType.INT, TokenType.FLOAT):
            res.register_advance()
            self.advance()
            return res.success(NumberNode(t))
        elif t.type == TokenType.IDENTIFIRER:
            res.register_advance()
            self.advance()
            return res.success(VarAccessNode(t))
        elif t.type == TokenType.LPAREN:
            res.register_advance()
            self.advance()
            expr = res.register(self.expr())
            if res.error:
                return res
            if self.current_token.type == TokenType.RPAREN:
                res.register_advance()
                self.advance()
                return res.success(expr)
            else:
                return res.failure(
                    InvalidSyntaxError(
                        self.current_token.pos_start,
                        self.current_token.pos_end,
                        "Expected ')'",
                    )
                )
        elif t.isKeword(TokenKeywords._if):
            if_exp = res.register(self.if_expr())
            if res.error:
                return res
            return res.success(if_exp)

        elif t.isKeword(TokenKeywords._for):
            for_exp = res.register(self.for_expr())
            if res.error:
                return res
            return res.success(for_exp)

        elif t.isKeword(TokenKeywords._while):
            for_while = res.register(self.while_expr())
            if res.error:
                return res
            return res.success(for_while)

        return res.failure(
            InvalidSyntaxError(
                t.pos_start,
                t.pos_end,
                "Excepted number, variable, '+', '-', '('",
            )
        )

    def power(self):
        return self.bin_op(self.atom, (TokenType.POW,), self.factor)

    def factor(self):
        res = ParserResult()
        t = self.current_token

        if t.type in (TokenType.PLUS, TokenType.MINUS):
            res.register_advance()
            self.advance()
            factor = res.register(self.factor())
            if res.error:
                return res
            return res.success(UnaryOpNode(t, factor))

        return self.power()

    def term(self):
        return self.bin_op(self.factor, (TokenType.MUL, TokenType.DIV))

    def arith_exp(self):
        return self.bin_op(self.term, (TokenType.PLUS, TokenType.MINUS))

    def comp_expr(self):
        res = ParserResult()
        if self.current_token.isKeword(TokenKeywords._not):
            op_tok = self.current_token
            res.register_advance()
            self.advance()

            node = res.register(self.comp_expr())
            if res.error:
                return res
            return res.success(UnaryOpNode(op_tok, node))

        node = res.register(
            self.bin_op(
                self.arith_exp,
                (
                    TokenType.EE,
                    TokenType.NE,
                    TokenType.LTE,
                    TokenType.LT,
                    TokenType.GT,
                    TokenType.GTE,
                ),
            )
        )

        if res.error:
            return res.failure(
                InvalidSyntaxError(
                    self.current_token.pos_start,
                    self.current_token.pos_end,
                    "Excepted number, variable, '+', '-', '('",
                )
            )
        return res.success(node)

    def expr(self):
        res = ParserResult()

        if self.current_token.isKeword(TokenKeywords._var):
            res.register_advance()
            self.advance()

            if self.current_token.type != TokenType.IDENTIFIRER:
                return res.failure(
                    InvalidSyntaxError(
                        self.current_tok.pos_start,
                        self.current_tok.pos_end,
                        "Expected identifier",
                    )
                )

            var_name = self.current_token
            res.register_advance()
            self.advance()
            t = self.current_token
            if t.type != TokenType.EQ:
                return res.failure(
                    InvalidSyntaxError(
                        t.pos_start,
                        t.pos_end,
                        "Excepted '='",
                    )
                )
            res.register_advance()
            self.advance()
            exp = res.register(self.expr())
            if res.error:
                return res
            return res.success(VarAssignNode(var_name, exp))

        node = res.register(
            self.bin_op(
                self.comp_expr,
                (
                    (TokenType.KEYWORD, TokenKeywords._and),
                    (TokenType.KEYWORD, TokenKeywords._or),
                ),
            )
        )
        if res.error:
            return res.failure(
                InvalidSyntaxError(
                    self.current_token.pos_start,
                    self.current_token.pos_end,
                    "Excepted number, variable, variable declaration '+', '-', '(', 'not'",
                )
            )
        return res.success(node)

    def bin_op(self, func_a, ops, func_b=None):
        if func_b == None:
            func_b = func_a

        res = ParserResult()
        left = res.register(func_a())
        if res.error:
            return res

        while (
            self.current_token.type in ops
            or (self.current_token.type, self.current_token.value) in ops
        ):
            op = self.current_token
            res.register_advance()
            self.advance()
            rigth = res.register(func_b())
            if res.error:
                return res
            left = BinOpNode(op, left, rigth)

        return res.success(left)


class ParserResult:
    def __init__(self):
        self.error = None
        self.node = None
        self.adv_count = 0

    def register(self, res):
        self.adv_count += res.adv_count
        if res.error:
            self.error = res.error
        return res.node

    def register_advance(self):
        self.adv_count += 1

    def success(self, node):
        self.node = node
        return self

    def failure(self, error):
        if not self.error or self.adv_count == 0:
            self.error = error
        return self
