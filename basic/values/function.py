from ..context import Context
from ..error import RunTimeError
from ..runtime import RuntimeResult
from ..symbols import SymbolTable
from .number import Number
from .value import Value


class BaseFunction(Value):
    def __init__(self, name):
        super().__init__()
        self.name = name or "<anonymus>"

    def check_args(self, arg_names, args):
        res = RuntimeResult()

        if len(args) != len(arg_names):
            return res.failure(
                RunTimeError(
                    self.pos_start,
                    self.pos_end,
                    f"The function {self.name} can only take {len(arg_names)} arguments but has received {len(args)}.",
                    self.context,
                )
            )

        return res.success(None)

    def populate_args(self, arg_names, args, exec_context):
        for i in range(len(args)):
            arg_name = arg_names[i]
            arg_value = args[i]
            arg_value.set_context(exec_context)
            exec_context.symbol_table.set(arg_name, arg_value)

    def check_and_populate_args(self, arg_names, args, exec_context):
        res = RuntimeResult()
        res.register(self.check_args(arg_names, args))
        if res.should_return():
            return res
        self.populate_args(arg_names, args, exec_context)
        return res.success(None)


class Function(BaseFunction):
    def __init__(self, name, body_node, arg_names, auto_return):
        super().__init__(name)
        self.body_node = body_node
        self.arg_names = arg_names
        self.auto_return = auto_return

    def __repr__(self):
        return f"<function {self.name}>"

    def copy(self):
        copy = Function(self.name, self.body_node, self.arg_names, self.auto_return)
        copy.set_context(self.context)
        copy.set_pos(self.pos_start, self.pos_end)
        return copy

    def execute(self, args):
        res = RuntimeResult()
        exec_context = self.context.generate_new_context(self.name, self.pos_start)

        from ..interpreter import Interpreter

        interpreter = Interpreter()

        self.check_and_populate_args(self.arg_names, args, exec_context)
        if res.should_return():
            return res

        value = res.register(interpreter.visit(self.body_node, exec_context))
        if res.should_return() and res.return_value == None:
            return res

        return_value = (
            (value if self.auto_return else None) or res.return_value or Number.null
        )
        return res.success(return_value)
