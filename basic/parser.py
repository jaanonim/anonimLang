from .error import InvalidSyntaxError
from .nodes import (
    BinOpNode,
    BreakNode,
    CallNode,
    ContinueNode,
    ForNode,
    FuncDefNode,
    IfNode,
    ListNode,
    NumberNode,
    ReturnNode,
    StringNode,
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
        self.update_token()
        return self.current_token

    def parse(self):
        res = self.statments()
        if not res.error and self.current_token.type != TokenType.EOF:
            return res.failure(
                InvalidSyntaxError(
                    self.current_token.pos_start,
                    self.current_token.pos_end,
                    "Excepted '+', '-', '*', '/', '^'",
                )
            )
        return res

    def reverse(self, to_reverse_count):
        self.t_id -= to_reverse_count
        self.update_token()
        return self.current_token

    def update_token(self):
        if self.t_id >= 0 and self.t_id < len(self.tokens):
            self.current_token = self.tokens[self.t_id]

    def statments(self):
        res = ParserResult()
        statments = []
        pos_start = self.current_token.pos_start.copy()

        while self.current_token.type == TokenType.NEWLINE:
            res.register_advance()
            self.advance()

        statment = res.register(self.statment())
        if res.error:
            return res
        statments.append(statment)

        more_statments = True
        while True:
            new_line_count = 0
            while self.current_token.type == TokenType.NEWLINE:
                res.register_advance()
                self.advance()
                new_line_count += 1
            if new_line_count == 0:
                more_statments = False

            if not more_statments:
                break
            statment = res.try_register(self.statment())
            if not statment:
                self.reverse(res.to_reverse_count)
                more_statments = False
                continue
            statments.append(statment)
        return res.success(
            ListNode(statments, pos_start, self.current_token.pos_end.copy())
        )

    def statment(self):
        res = ParserResult()
        pos_start = self.current_token.pos_start.copy()

        if self.current_token.isKeword(TokenKeywords._return):
            res.register_advance()
            self.advance()

            expr = res.try_register(self.expr())
            if not expr:
                self.reverse(res.to_reverse_count)
            return res.success(
                ReturnNode(expr, pos_start, self.current_token.pos_start.copy())
            )

        if self.current_token.isKeword(TokenKeywords._continue):
            res.register_advance()
            self.advance()

            return res.success(
                ContinueNode(pos_start, self.current_token.pos_start.copy())
            )

        if self.current_token.isKeword(TokenKeywords._break):
            res.register_advance()
            self.advance()
            return res.success(
                BreakNode(pos_start, self.current_token.pos_start.copy())
            )

        expr = res.register(self.expr())
        if res.error:
            return res.failure(
                InvalidSyntaxError(
                    self.current_token.pos_start,
                    self.current_token.pos_end,
                    f"Excepted number, variable, '{TokenKeywords._return.value}', '{TokenKeywords._break.value}', '{TokenKeywords._continue.value}', '{TokenKeywords._if.value}', '{TokenKeywords._for.value}', '{TokenKeywords._while.value}', '{TokenKeywords._func.value}', '{TokenKeywords._var.value}', '+', '-', '(', '[', '{TokenKeywords._not.value}'",
                )
            )

        return res.success(expr)

    def if_expr(self):
        res = ParserResult()
        all_cases = res.register(self.if_expr_cases(TokenKeywords._if))
        if res.error:
            return res
        cases, else_cases = all_cases
        return res.success(IfNode(cases, else_cases))

    def elif_expr(self):
        return self.if_expr_cases(TokenKeywords._elif)

    def else_expr(self):
        res = ParserResult()
        else_case = None

        if self.current_token.isKeword(TokenKeywords._else):
            res.register_advance()
            self.advance()

            if self.current_token.type == TokenType.LCURBRA:
                res.register_advance()
                self.advance()

                statements = res.register(self.statments())
                if res.error:
                    return res
                else_case = (statements, True)

                if self.current_token.type != TokenType.RCURBRA:
                    return res.failure(
                        InvalidSyntaxError(
                            self.current_token.pos_start,
                            self.current_token.pos_end,
                            "Expected '}'",
                        )
                    )

                res.register_advance()
                self.advance()
            else:
                statment = res.register(self.statment())
                if res.error:
                    return res
                else_case = (statment, False)

        return res.success(else_case)

    def elif_or_else_expr(self, new_line):
        res = ParserResult()
        cases, else_case = [], None

        if new_line:
            while self.current_token.type == TokenType.NEWLINE:
                res.register_advance()
                self.advance()

        if self.current_token.isKeword(TokenKeywords._elif):
            all_cases = res.register(self.elif_expr())
            if res.error:
                return res
            cases, else_case = all_cases
        else:
            else_case = res.register(self.else_expr())
            if res.error:
                return res

        return res.success((cases, else_case))

    def if_expr_cases(self, keyword):
        res = ParserResult()
        cases = []
        else_case = None

        if not self.current_token.isKeword(keyword):
            return res.failure(
                InvalidSyntaxError(
                    self.current_token.pos_start,
                    self.current_token.pos_end,
                    f"Expected '{keyword.value}'",
                )
            )

        res.register_advance()
        self.advance()

        condition = res.register(self.expr())

        if res.error:
            return res

        if self.current_token.type == TokenType.LCURBRA:
            res.register_advance()
            self.advance()

            statments = res.register(self.statments())
            if res.error:
                return res
            cases.append((condition, statments, True))

            if self.current_token.type != TokenType.RCURBRA:
                return res.failure(
                    InvalidSyntaxError(
                        self.current_token.pos_start,
                        self.current_token.pos_end,
                        "Expected ''",
                    )
                )
            res.register_advance()
            self.advance()

            all_cases = res.register(self.elif_or_else_expr(False))
            if res.error:
                return res
            new_cases, else_case = all_cases
            cases.extend(new_cases)
        else:
            statment = res.register(self.statment())
            if res.error:
                return res
            cases.append((condition, statment, False))
            all_cases = res.register(self.elif_or_else_expr(True))
            if res.error:
                return res
            new_cases, else_case = all_cases
            cases.extend(new_cases)

        return res.success((cases, else_case))

    def for_expr(self):
        res = ParserResult()
        if not self.current_token.isKeword(TokenKeywords._for):
            return res.failure(
                InvalidSyntaxError(
                    self.current_token.pos_start,
                    self.current_token.pos_end,
                    f"Expected '{TokenKeywords._for.value}'",
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
                    f"Expected '{TokenKeywords._to.value}'",
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

        if self.current_token.type == TokenType.LCURBRA:
            res.register_advance()
            self.advance()

            body = res.register(self.statments())
            if res.error:
                return res

            if not self.current_token.type == TokenType.RCURBRA:
                return res.failure(
                    InvalidSyntaxError(
                        self.current_token.pos_start,
                        self.current_token.pos_end,
                        "Expected '}'",
                    )
                )

            res.register_advance()
            self.advance()

            return res.success(
                ForNode(var_name, start_value, end_value, step_value, body, True)
            )

        else:
            body = res.register(self.statment())
            if res.error:
                return res
            return res.success(
                ForNode(var_name, start_value, end_value, step_value, body, False)
            )

    def while_expr(self):
        res = ParserResult()

        if not self.current_token.isKeword(TokenKeywords._while):
            return res.failure(
                InvalidSyntaxError(
                    self.current_token.pos_start,
                    self.current_token.pos_end,
                    f"Expected '{TokenKeywords._while.value}'",
                )
            )

        res.register_advance()
        self.advance()

        condition = res.register(self.expr())
        if res.error:
            return res

        if self.current_token.type == TokenType.LCURBRA:
            res.register_advance()
            self.advance()

            body = res.register(self.statments())
            if res.error:
                return res

            print(self.current_token)

            if not self.current_token.type == TokenType.RCURBRA:
                return res.failure(
                    InvalidSyntaxError(
                        self.current_token.pos_start,
                        self.current_token.pos_end,
                        "Expected '}'",
                    )
                )

            res.register_advance()
            self.advance()
            return res.success(WhileNode(condition, body, True))

        else:
            body = res.register(self.statment())
            if res.error:
                return res
            return res.success(WhileNode(condition, body, False))

    def atom(self):
        res = ParserResult()
        t = self.current_token

        if t.type in (TokenType.INT, TokenType.FLOAT):
            res.register_advance()
            self.advance()
            return res.success(NumberNode(t))
        elif t.type == TokenType.STRING:
            res.register_advance()
            self.advance()
            return res.success(StringNode(t))
        elif t.type == TokenType.IDENTIFIRER:
            res.register_advance()
            self.advance()
            obj = VarAccessNode(t)
            value = t
            if self.current_token.type == TokenType.DOT:
                res.register_advance()
                self.advance()
                if self.current_token.type != TokenType.IDENTIFIRER:
                    return res.failure(
                        InvalidSyntaxError(
                            self.current_token.pos_start,
                            self.current_token.pos_end,
                            "Expected identifirer",
                        )
                    )
                value = self.current_token
                res.register_advance()
                self.advance()
                while self.current_token.type == TokenType.DOT:
                    obj = VarAccessNode(value, obj)
                    res.register_advance()
                    self.advance()
                    if self.current_token.type != TokenType.IDENTIFIRER:
                        return res.failure(
                            InvalidSyntaxError(
                                self.current_token.pos_start,
                                self.current_token.pos_end,
                                "Expected identifirer",
                            )
                        )
                    value = self.current_token
                    res.register_advance()
                    self.advance()
            return res.success(VarAccessNode(value, obj))
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

        elif t.type == TokenType.LSQUARE:
            list_expr = res.register(self.list_expr())
            if res.error:
                return res
            return res.success(list_expr)

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

        elif t.isKeword(TokenKeywords._func):
            func_def = res.register(self.func_def())
            if res.error:
                return res
            return res.success(func_def)

        return res.failure(
            InvalidSyntaxError(
                t.pos_start,
                t.pos_end,
                f"Excepted number, variable, '+', '-', '(', '[', '{TokenKeywords._if.value}', '{TokenKeywords._for.value}', '{TokenKeywords._while.value}', '{TokenKeywords._func.value}'",
            )
        )

    def list_expr(self):
        res = ParserResult()
        element_nodes = []
        pos_start = self.current_token.pos_start.copy()

        if self.current_token.type != TokenType.LSQUARE:
            return res.failure(
                InvalidSyntaxError(
                    self.current_token.pos_start,
                    self.current_token.pos_end,
                    f"Excepted '['",
                )
            )

        res.register_advance()
        self.advance()

        if self.current_token.type == TokenType.RSQUARE:
            res.register_advance()
            self.advance()
        else:
            element_nodes.append(res.register(self.expr()))
            if res.error:
                return res.failure(
                    InvalidSyntaxError(
                        self.current_token.pos_start,
                        self.current_token.pos_end,
                        f"Excepted '[', ']', '{TokenKeywords._var.value}', '{TokenKeywords._for.value}', '{TokenKeywords._while.value}', '{TokenKeywords._func.value}', number, identifier",
                    )
                )

            while self.current_token.type == TokenType.COMMA:
                res.register_advance()
                self.advance()

                element_nodes.append(res.register(self.expr()))
                if res.error:
                    return res

            if self.current_token.type != TokenType.RSQUARE:
                return res.failure(
                    InvalidSyntaxError(
                        self.current_token.pos_start,
                        self.current_token.pos_end,
                        f"Excepted ']', ','",
                    )
                )

            res.register_advance()
            self.advance()
        return res.success(
            ListNode(element_nodes, pos_start, self.current_token.pos_end.copy())
        )

    def call(self):
        res = ParserResult()
        atom = res.register(self.atom())
        if res.error:
            return res

        if self.current_token.type == TokenType.LPAREN:
            res.register_advance()
            self.advance()
            arg_nodes = []

            if self.current_token.type == TokenType.RPAREN:
                res.register_advance()
                self.advance()
            else:
                arg_nodes.append(res.register(self.expr()))
                if res.error:
                    return res.failure(
                        InvalidSyntaxError(
                            self.current_token.pos_start,
                            self.current_token.pos_end,
                            f"Excepted ')', '[', '{TokenKeywords._var.value}', '{TokenKeywords._for.value}', '{TokenKeywords._while.value}', '{TokenKeywords._func.value}', number, identifier",
                        )
                    )

                while self.current_token.type == TokenType.COMMA:
                    res.register_advance()
                    self.advance()

                    arg_nodes.append(res.register(self.expr()))
                    if res.error:
                        return res

                if self.current_token.type != TokenType.RPAREN:
                    return res.failure(
                        InvalidSyntaxError(
                            self.current_token.pos_start,
                            self.current_token.pos_end,
                            f"Excepted ')', ','",
                        )
                    )

                res.register_advance()
                self.advance()
            return res.success(CallNode(atom, arg_nodes))
        return res.success(atom)

    def power(self):
        return self.bin_op(self.call, (TokenType.POW,), self.factor)

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
        return self.bin_op(self.factor, (TokenType.MUL, TokenType.DIV, TokenType.MOD))

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
                    "Excepted number, variable, '+', '-', '(', '['",
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
                        self.current_token.pos_start,
                        self.current_token.pos_end,
                        "Expected identifier",
                    )
                )
            var_name = self.current_token
            obj = VarAccessNode(var_name)
            value = var_name

            res.register_advance()
            self.advance()
            if self.current_token.type == TokenType.DOT:
                res.register_advance()
                self.advance()
                if self.current_token.type != TokenType.IDENTIFIRER:
                    return res.failure(
                        InvalidSyntaxError(
                            self.current_token.pos_start,
                            self.current_token.pos_end,
                            "Expected identifirer",
                        )
                    )
                value = self.current_token
                res.register_advance()
                self.advance()
                while self.current_token.type == TokenType.DOT:
                    obj = VarAccessNode(value, obj)
                    res.register_advance()
                    self.advance()
                    if self.current_token.type != TokenType.IDENTIFIRER:
                        return res.failure(
                            InvalidSyntaxError(
                                self.current_token.pos_start,
                                self.current_token.pos_end,
                                "Expected identifirer",
                            )
                        )
                    value = self.current_token
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
            return res.success(VarAssignNode(value, exp, obj))

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
                    f"Excepted number, variable,'{TokenKeywords._if.value}', '{TokenKeywords._for.value}', '{TokenKeywords._while.value}', '{TokenKeywords._func.value}', '{TokenKeywords._var.value}', '+', '-', '(', '[', '{TokenKeywords._not.value}'",
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

    def func_def(self):
        res = ParserResult()

        if not self.current_token.isKeword(TokenKeywords._func):
            return res.failure(
                InvalidSyntaxError(
                    self.current_token.pos_start,
                    self.current_token.pos_end,
                    f"Expected '{TokenKeywords._func.value}'",
                )
            )

        res.register_advance()
        self.advance()

        if self.current_token.type == TokenType.IDENTIFIRER:
            var_name_tok = self.current_token
            res.register_advance()
            self.advance()
            if self.current_token.type != TokenType.LPAREN:
                return res.failure(
                    InvalidSyntaxError(
                        self.current_token.pos_start,
                        self.current_token.pos_end,
                        f"Expected '('",
                    )
                )
        else:
            var_name_tok = None
            if self.current_token.type != TokenType.LPAREN:
                return res.failure(
                    InvalidSyntaxError(
                        self.current_token.pos_start,
                        self.current_token.pos_end,
                        f"Expected identifier, '('",
                    )
                )

        res.register_advance()
        self.advance()

        arg_name_toks = []
        if self.current_token.type == TokenType.IDENTIFIRER:
            arg_name_toks.append(self.current_token)
            res.register_advance()
            self.advance()

            while self.current_token.type == TokenType.COMMA:
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

                arg_name_toks.append(self.current_token)
                res.register_advance()
                self.advance()

            if self.current_token.type != TokenType.RPAREN:
                return res.failure(
                    InvalidSyntaxError(
                        self.current_token.pos_start,
                        self.current_token.pos_end,
                        f"Expected ',', ')'",
                    )
                )
        else:
            if self.current_token.type != TokenType.RPAREN:
                return res.failure(
                    InvalidSyntaxError(
                        self.current_token.pos_start,
                        self.current_token.pos_end,
                        f"Expected identifier, ')'",
                    )
                )

        res.register_advance()
        self.advance()

        if self.current_token.type == TokenType.ARROW:
            res.register_advance()
            self.advance()

            node_to_return = res.register(self.expr())
            if res.error:
                return res

            return res.success(
                FuncDefNode(var_name_tok, arg_name_toks, node_to_return, True)
            )

        elif self.current_token.type == TokenType.LCURBRA:
            res.register_advance()
            self.advance()

            node_to_return = res.register(self.statments())
            if res.error:
                return res

            if not self.current_token.type == TokenType.RCURBRA:
                return res.failure(
                    InvalidSyntaxError(
                        self.current_token.pos_start,
                        self.current_token.pos_end,
                        "Expected '}'",
                    )
                )

            res.register_advance()
            self.advance()

            return res.success(
                FuncDefNode(var_name_tok, arg_name_toks, node_to_return, False)
            )

        else:
            return res.failure(
                InvalidSyntaxError(
                    self.current_token.pos_start,
                    self.current_token.pos_end,
                    "Expected '->','{'",
                )
            )


class ParserResult:
    def __init__(self):
        self.error = None
        self.node = None
        self.adv_count = 0
        self.to_reverse_count = 0

    def register(self, res):
        self.adv_count += res.adv_count
        if res.error:
            self.error = res.error
        return res.node

    def try_register(self, res):
        if res.error:
            self.to_reverse_count = res.adv_count
            return None
        return self.register(res)

    def register_advance(self):
        self.adv_count += 1

    def success(self, node):
        self.node = node
        return self

    def failure(self, error):
        if not self.error or self.adv_count == 0:
            self.error = error
        return self
