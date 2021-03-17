from basic.lexer import Lexer
from basic.parser import Parser


def run(fn, text):
    l = Lexer(fn, text)
    t, e = l.make_tokens()
    if e:
        return None, e

    p = Parser(t)
    ast = p.parse()

    return ast.node, ast.error
