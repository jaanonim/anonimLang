from ..context import Context
from ..error import RunTimeError
from ..runtime import RuntimeResult
from ..symbols import SymbolTable
from .value import Value


class Function(Value):
    def __init__(self, name, body_node, arg_names):
        super().__init__()
        self.name = name or "<anonymus>"
        self.body_node = body_node
        self.arg_names = arg_names

    def __repr__(self):
        return f"<function {self.name}>"

    def copy(self):
        copy = Function(self.name, self.body_node, self.arg_names)
        copy.set_context(self.context)
        copy.set_pos(self.pos_start, self.pos_end)
        return copy

    def execute(self, args):
        res = RuntimeResult()
        from ..interpreter import Interpreter

        interpreter = Interpreter()

        new_context = Context(self.name, self.context, self.pos_start)
        new_context.symbol_table = SymbolTable(new_context.parent.symbol_table)

        if len(args) != len(self.arg_names):
            return res.failure(
                RunTimeError(
                    self.pos_start,
                    self.pos_end,
                    f"The function {self.name} can only take {len(self.arg_names)} arguments but has received {len(args)}.",
                    self.context,
                )
            )

        for i in range(len(args)):
            arg_name = self.arg_names[i]
            arg_value = args[i]
            arg_value.set_context(new_context)
            new_context.symbol_table.set(arg_name, arg_value)

        value = res.register(interpreter.visit(self.body_node, new_context))
        if res.error:
            return res

        return res.success(value)
