import os
import random

from ..error import RunTimeError
from ..runtime import RuntimeResult
from .function import BaseFunction
from .list import List
from .number import Number
from .object import Object
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
        exec_context = self.context.generate_new_context(self.name, self.pos_start)

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
            return RuntimeResult().failure(
                RunTimeError(
                    self.pos_start,
                    self.pos_end,
                    f"'{text}' must be an intiger.",
                    exec_context,
                )
            )
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

    def execute_is_object(self, exec_context):
        is_number = isinstance(exec_context.symbol_table.get("value"), Object)
        return RuntimeResult().success(Number.true if is_number else Number.false)

    execute_is_object.arg_names = ["value"]

    def execute_isset(self, exec_context):
        v_name = exec_context.symbol_table.get("value")
        if not isinstance(v_name, String):
            return RuntimeResult().failure(
                RunTimeError(
                    self.pos_start,
                    self.pos_end,
                    "Argument must be String",
                    exec_context,
                )
            )

        return RuntimeResult().success(
            Number(1) if exec_context.symbol_table.get(v_name.value) else Number(0)
        )

    execute_isset.arg_names = ["value"]

    def execute_random(self, exec_context):
        return RuntimeResult().success(Number(random.random()))

    execute_random.arg_names = []

    def execute_exit(self, exec_context):
        exit()

    execute_exit.arg_names = []

    def execute_append(self, exec_context):
        list_ = exec_context.symbol_table.get("list")
        value = exec_context.symbol_table.get("value")

        if not isinstance(list_, List):
            return RuntimeResult().failure(
                RunTimeError(
                    self.pos_start,
                    self.pos_end,
                    "First argument must be list",
                    exec_context,
                )
            )

        list_.elements.append(value)
        return RuntimeResult().success(Number.null)

    execute_append.arg_names = ["list", "value"]

    def execute_pop(self, exec_context):
        list_ = exec_context.symbol_table.get("list")
        index = exec_context.symbol_table.get("index")

        if not isinstance(list_, List):
            return RuntimeResult().failure(
                RunTimeError(
                    self.pos_start,
                    self.pos_end,
                    "First argument must be list",
                    exec_context,
                )
            )

        if not isinstance(index, Number):
            return RuntimeResult().failure(
                RunTimeError(
                    self.pos_start,
                    self.pos_end,
                    "Second argument must be number",
                    exec_context,
                )
            )

        try:
            element = list_.elements.pop(index.value)
        except:
            return RuntimeResult().failure(
                RunTimeError(
                    self.pos_start,
                    self.pos_end,
                    "Element at this index could not be removed from list because index is out of bounds",
                    exec_context,
                )
            )
        return RuntimeResult().success(element)

    execute_pop.arg_names = ["list", "index"]

    def execute_extend(self, exec_context):
        listA = exec_context.symbol_table.get("listA")
        listB = exec_context.symbol_table.get("listB")

        if not isinstance(listA, List):
            return RuntimeResult().failure(
                RunTimeError(
                    self.pos_start,
                    self.pos_end,
                    "First argument must be list",
                    exec_context,
                )
            )

        if not isinstance(listB, List):
            return RuntimeResult().failure(
                RunTimeError(
                    self.pos_start,
                    self.pos_end,
                    "Second argument must be list",
                    exec_context,
                )
            )

        listA.elements.extend(listB.elements)
        return RuntimeResult().success(Number.null)

    execute_extend.arg_names = ["listA", "listB"]

    def execute_len(self, exec_context):
        _list = exec_context.symbol_table.get("list")

        if not isinstance(_list, List):
            return RuntimeResult().failure(
                RunTimeError(
                    self.pos_start,
                    self.pos_end,
                    "Argument must be List",
                    exec_context,
                )
            )
        return RuntimeResult().success(Number(len(_list.elements)))

    execute_len.arg_names = ["list"]

    def execute_run(self, exec_context):
        fn = exec_context.symbol_table.get("value")

        if not isinstance(fn, String):
            return RuntimeResult().failure(
                RunTimeError(
                    self.pos_start,
                    self.pos_end,
                    "Argument must be string",
                    exec_context,
                )
            )

        fn = fn.value

        try:
            with open(fn, "r") as f:
                s = f.read()
        except Exception as e:
            return RuntimeResult().failure(
                RunTimeError(
                    self.pos_start,
                    self.pos_end,
                    f'Failed to load script"{fn}"\n' + str(e),
                    exec_context,
                )
            )
        from run import run_with_context

        _, error, context = run_with_context(fn, s, exec_context)
        if error:
            return RuntimeResult().failure(
                RunTimeError(
                    self.pos_start,
                    self.pos_end,
                    f'Failed to load script"{fn}"\n' + error.as_str(),
                    exec_context,
                )
            )
        return RuntimeResult().success(Object(context))

    execute_run.arg_names = ["value"]


BuiltInFunction.print = BuiltInFunction("print")
BuiltInFunction.input = BuiltInFunction("input")
BuiltInFunction.input_int = BuiltInFunction("input_int")
BuiltInFunction.clear = BuiltInFunction("clear")
BuiltInFunction.is_number = BuiltInFunction("is_number")
BuiltInFunction.is_string = BuiltInFunction("is_string")
BuiltInFunction.is_list = BuiltInFunction("is_list")
BuiltInFunction.is_function = BuiltInFunction("is_function")
BuiltInFunction.is_object = BuiltInFunction("is_object")
BuiltInFunction.isset = BuiltInFunction("isset")
BuiltInFunction.exit = BuiltInFunction("exit")
BuiltInFunction.run = BuiltInFunction("run")
BuiltInFunction.append = BuiltInFunction("append")
BuiltInFunction.pop = BuiltInFunction("pop")
BuiltInFunction.extend = BuiltInFunction("extend")
BuiltInFunction.len = BuiltInFunction("len")
BuiltInFunction.random = BuiltInFunction("random")
