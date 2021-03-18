from basic.context import Context
from basic.interpreter import Interpreter
from basic.lexer import Lexer
from basic.parser import Parser


def run(fn, text):
    l = Lexer(fn, text)
    t, e = l.make_tokens()
    if e:
        return None, e

    p = Parser(t)
    ast = p.parse()
    if ast.error:
        return None, ast.error

    i = Interpreter()
    c = Context("<program>")
    res = i.visit(ast.node, c)

    return res.value, res.error
