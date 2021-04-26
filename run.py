from basic.context import Context
from basic.interpreter import Interpreter
from basic.lexer import Lexer
from basic.parser import Parser
from basic.symbols import SymbolTable
from basic.values.build_in_functions import BuiltInFunction
from basic.values.number import Number

global_symbol_table = SymbolTable()
global_symbol_table.set("NULL", Number.null)
global_symbol_table.set("TRUE", Number.true)
global_symbol_table.set("FALSE", Number.false)
global_symbol_table.set("print", BuiltInFunction.print)
global_symbol_table.set("input", BuiltInFunction.input)
global_symbol_table.set("input_int", BuiltInFunction.input_int)
global_symbol_table.set("is_number", BuiltInFunction.is_number)
global_symbol_table.set("is_string", BuiltInFunction.is_string)
global_symbol_table.set("is_list", BuiltInFunction.is_list)
global_symbol_table.set("is_function", BuiltInFunction.is_function)
global_symbol_table.set("exit", BuiltInFunction.exit)
global_symbol_table.set("run", BuiltInFunction.run)
global_symbol_table.set("len", BuiltInFunction.len)

debug = True


def run(fn, text):
    l = Lexer(fn, text)
    t, e = l.make_tokens()
    if e:
        return None, e

    if debug:
        print(f"DEBUG: {t}")

    p = Parser(t)
    ast = p.parse()
    if ast.error:
        return None, ast.error

    i = Interpreter()
    c = Context("<program>")
    c.symbol_table = global_symbol_table
    res = i.visit(ast.node, c)

    return res.value, res.error
