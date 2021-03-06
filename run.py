from basic.context import Context
from basic.interpreter import Interpreter
from basic.lexer import Lexer
from basic.parser import Parser
from basic.symbols import SymbolTable
from basic.values.build_in_functions import BuiltInFunction
from basic.values.number import Number
from basic.values.object import Object

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
global_symbol_table.set("is_object", BuiltInFunction.is_object)
global_symbol_table.set("isset", BuiltInFunction.isset)
global_symbol_table.set("exit", BuiltInFunction.exit)
global_symbol_table.set("run", BuiltInFunction.run)
global_symbol_table.set("append", BuiltInFunction.append)
global_symbol_table.set("pop", BuiltInFunction.pop)
global_symbol_table.set("extend", BuiltInFunction.extend)
global_symbol_table.set("len", BuiltInFunction.len)
global_symbol_table.set("clear", BuiltInFunction.clear)
global_symbol_table.set("random", BuiltInFunction.random)

debug = False


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


def run_with_context(fn, text, context):
    l = Lexer(fn, text)
    t, e = l.make_tokens()
    if e:
        return None, e, None

    if debug:
        print(f"DEBUG: {t}")

    p = Parser(t)
    ast = p.parse()
    if ast.error:
        return None, ast.error, None
    c = context.generate_new_context(fn)
    c.symbol_table.set("self", Object(c))

    i = Interpreter()
    res = i.visit(ast.node, c)

    return res.value, res.error, c
