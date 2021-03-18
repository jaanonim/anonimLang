from .number import Number
from .runtime import RuntimeResult
from .token import TokenType


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

        if e:
            return res.failure(e)
        else:
            return res.success(num.set_pos(node.pos_start, node.pos_start))
