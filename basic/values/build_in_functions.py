import os

from ..error import RunTimeError
from ..runtime import RuntimeResult
from .function import BaseFunction
from .list import List
from .number import Number
from .string import String


class BuiltInFunction(BaseFunction):
    def __init__(self, name):
        super().__init__(name)

    def __repr__(self):
        return f"<build-in function {self.name}>"

    def copy(self):
        copy = BuiltInFunction(self.name)
        copy.set_context(self.context)
        copy.set_pos(self.pos_start, self.pos_end)
        return copy

    def execute(self, args):
        res = RuntimeResult()
        exec_context = self.generate_new_context()

        method_name = f"execute_{self.name}"
        method = getattr(self, method_name, self.no_execute_method)

        res.register(self.check_and_populate_args(method.arg_names, args, exec_context))
        if res.should_return():
            return res

        return_value = res.register(method(exec_context))
        if res.should_return():
            return res

        return res.success(return_value)

    def no_execute_method(self):
        raise Exception(f"No execute_{self.name} method defined")

    #########################################

    def execute_print(self, exec_context):
        print(str(exec_context.symbol_table.get("value")))
        return RuntimeResult().success(Number.null)

    execute_print.arg_names = ["value"]

    def execute_input(self, exec_context):
        arg = exec_context.symbol_table.get("value")
        if arg:
            arg = str(arg)
        else:
            arg = ""
        text = input(arg)
        return RuntimeResult().success(String(text))

    execute_input.arg_names = ["value"]

    def execute_input_int(self, exec_context):
        arg = exec_context.symbol_table.get("value")
        if arg:
            arg = str(arg)
        else:
            arg = ""
        text = input(arg)
        try:
            num = int(text)
        except ValueError:
            print(f"'{text}' must be an intiger.")
            return RuntimeResult().success(Number.null)
        return RuntimeResult().success(Number(num))

    execute_input_int.arg_names = ["value"]

    def execute_clear(self, exec_context):
        os.system("cls" if os.name == "nt" else "clear")
        return RuntimeResult().success(Number.null)

    execute_clear.arg_names = []

    def execute_is_number(self, exec_context):
        is_number = isinstance(exec_context.symbol_table.get("value"), Number)
        return RuntimeResult().success(Number.true if is_number else Number.false)

    execute_is_number.arg_names = ["value"]

    def execute_is_string(self, exec_context):
        is_number = isinstance(exec_context.symbol_table.get("value"), String)
        return RuntimeResult().success(Number.true if is_number else Number.false)

    execute_is_string.arg_names = ["value"]

    def execute_is_list(self, exec_context):
        is_number = isinstance(exec_context.symbol_table.get("value"), List)
        return RuntimeResult().success(Number.true if is_number else Number.false)

    execute_is_list.arg_names = ["value"]

    def execute_is_function(self, exec_context):
        is_number = isinstance(exec_context.symbol_table.get("value"), BaseFunction)
        return RuntimeResult().success(Number.true if is_number else Number.false)

    execute_is_function.arg_names = ["value"]

    def execute_exit(self, exec_context):
        exit()

    execute_exit.arg_names = []


BuiltInFunction.print = BuiltInFunction("print")
BuiltInFunction.input = BuiltInFunction("input")
BuiltInFunction.input_int = BuiltInFunction("input_int")
BuiltInFunction.clear = BuiltInFunction("clear")
BuiltInFunction.is_number = BuiltInFunction("is_number")
BuiltInFunction.is_string = BuiltInFunction("is_string")
BuiltInFunction.is_list = BuiltInFunction("is_list")
BuiltInFunction.is_function = BuiltInFunction("is_function")
BuiltInFunction.exit = BuiltInFunction("exit")
