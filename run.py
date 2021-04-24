from basic.context import Context
from basic.interpreter import Interpreter
from basic.lexer import Lexer
from basic.parser import Parser
from basic.symbols import SymbolTable

global_symbol_table = SymbolTable()
"""
global_symbol_table.set(
    "null",
)
global_symbol_table.set("true")
global_symbol_table.set("false")
"""
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
