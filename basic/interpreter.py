from .error import RunTimeError
from .runtime import RuntimeResult
from .token import TokenKeywords, TokenType
from .values.function import Function
from .values.list import List
from .values.number import Number
from .values.string import String


class Interpreter:
    def visit(self, node, context):
        method_name = f"visit_{type(node).__name__}"
        method = getattr(self, method_name, self.no_visit_method)
        return method(node, context)

    def no_visit_method(self, node, context):
        raise Exception(f"No visit_{type(node).__name__} method defined.")

    def visit_NumberNode(self, node, context):
        return RuntimeResult().success(
            Number(node.token.value)
            .set_context(context)
            .set_pos(node.pos_start, node.pos_end)
        )

    def visit_VarAccessNode(self, node, context):
        res = RuntimeResult()
        var_name = node.token.value
        value = context.symbol_table.get(var_name)

        if not value:
            return res.failure(
                RunTimeError(
                    node.pos_start,
                    node.pos_end,
                    f"'{var_name}' is not defined",
                    context,
                )
            )

        value = value.copy().set_pos(node.pos_start, node.pos_end).set_context(context)
        return res.success(value)

    def visit_VarAssignNode(self, node, context):
        res = RuntimeResult()
        var_name = node.token.value
        value = res.register(self.visit(node.value, context))
        if res.error:
            return res
        context.symbol_table.set(var_name, value)
        return res.success(value)

    def visit_BinOpNode(self, node, context):
        res = RuntimeResult()
        left = res.register(self.visit(node.left, context))
        if res.error:
            return res
        rigth = res.register(self.visit(node.rigth, context))
        if res.error:
            return res

        if node.token.type == TokenType.PLUS:
            r, e = left.added_to(rigth)
        elif node.token.type == TokenType.MINUS:
            r, e = left.subbed_by(rigth)
        elif node.token.type == TokenType.MUL:
            r, e = left.multed_by(rigth)
        elif node.token.type == TokenType.DIV:
            r, e = left.divided_by(rigth)
        elif node.token.type == TokenType.POW:
            r, e = left.powed_to(rigth)
        elif node.token.type == TokenType.EE:
            r, e = left.get_comparison_eq(rigth)
        elif node.token.type == TokenType.NE:
            r, e = left.get_comparison_ne(rigth)
        elif node.token.type == TokenType.LT:
            r, e = left.get_comparison_lt(rigth)
        elif node.token.type == TokenType.GT:
            r, e = left.get_comparison_gt(rigth)
        elif node.token.type == TokenType.LTE:
            r, e = left.get_comparison_lte(rigth)
        elif node.token.type == TokenType.GTE:
            r, e = left.get_comparison_gte(rigth)
        elif node.token.isKeword(TokenKeywords._and):
            r, e = left.anded_by(rigth)
        elif node.token.isKeword(TokenKeywords._or):
            r, e = left.ored_by(rigth)

        if e:
            return res.failure(e)
        else:
            return res.success(r.set_pos(node.pos_start, node.pos_end))

    def visit_UnaryOpNode(self, node, context):
        res = RuntimeResult()
        num = res.register(self.visit(node.node, context))
        if res.error:
            return res
        if node.token.type == TokenType.MINUS:
            num, e = num.multed_by(Number(-1))
        elif node.token.isKeword(TokenKeywords._not):
            num, e = num.notted()

        if e:
            return res.failure(e)
        else:
            return res.success(num.set_pos(node.pos_start, node.pos_start))

    def visit_IfNode(self, node, context):
        res = RuntimeResult()

        for condition, expr in node.cases:
            condition_value = res.register(self.visit(condition, context))
            if res.error:
                return res

        if condition_value.is_true():
            expr_value = res.register(self.visit(expr, context))
            if res.error:
                return res
            return res.success(expr_value)

        if node.else_case:
            else_value = res.register(self.visit(node.else_case, context))
            if res.error:
                return res
            return res.success(else_value)

        return res.success(None)

    def visit_ForNode(self, node, context):
        res = RuntimeResult()
        elements = []

        start_value = res.register(self.visit(node.start_value_node, context))
        if res.error:
            return res

        end_value = res.register(self.visit(node.end_value_node, context))
        if res.error:
            return res

        if node.step_value_node:
            step_value = res.register(self.visit(node.step_value_node, context))
            if res.error:
                return res
        else:
            step_value = Number(1)

        i = start_value.value

        if step_value.value >= 0:
            condition = lambda: i < end_value.value
        else:
            condition = lambda: i > end_value.value

        while condition():
            context.symbol_table.set(node.var_name_tok.value, Number(i))
            i += step_value.value

            elements.append(res.register(self.visit(node.body_node, context)))
            if res.error:
                return res

        return res.success(
            List(elements).set_context(context).set_pos(node.pos_start, node.pos_end)
        )

    def visit_WhileNode(self, node, context):
        res = RuntimeResult()
        elements = []

        while True:
            condition = res.register(self.visit(node.condition_node, context))
            if res.error:
                return res

            if not condition.is_true():
                break

            elements.append(res.register(self.visit(node.body_node, context)))
            if res.error:
                return res

        return res.success(
            List(elements).set_context(context).set_pos(node.pos_start, node.pos_end)
        )

    def visit_FuncDefNode(self, node, context):
        res = RuntimeResult()

        func_name = node.var_name_tok.value if node.var_name_tok else None
        body_node = node.body_node
        arg_names = [arg_name.value for arg_name in node.arg_names_toks]

        func_value = (
            Function(func_name, body_node, arg_names)
            .set_context(context)
            .set_pos(node.pos_start, node.pos_end)
        )

        if node.var_name_tok:
            context.symbol_table.set(func_name, func_value)

        return res.success(func_value)

    def visit_CallNode(self, node, context):
        res = RuntimeResult()
        args = []
        value_to_call = res.register(self.visit(node.node_to_call, context))
        if res.error:
            return res
        value_to_call = value_to_call.copy().set_pos(node.pos_start, node.pos_end)

        for arg in node.arg_nodes:
            args.append(res.register(self.visit(arg, context)))
            if res.error:
                return res

        return_value = res.register(value_to_call.execute(args))
        if res.error:
            return res

        return_value = (
            return_value.copy()
            .set_pos(node.pos_start, node.pos_end)
            .set_context(context)
        )
        return res.success(return_value)

    def visit_StringNode(self, node, context):
        return RuntimeResult().success(
            String(node.token.value)
            .set_context(context)
            .set_pos(node.pos_start, node.pos_end)
        )

    def visit_ListNode(self, node, context):
        res = RuntimeResult()
        elements = []

        for element in node.element_nodes:
            elements.append(res.register(self.visit(element, context)))
            if res.error:
                return res

        return res.success(
            List(elements).set_context(context).set_pos(node.pos_start, node.pos_end)
        )
