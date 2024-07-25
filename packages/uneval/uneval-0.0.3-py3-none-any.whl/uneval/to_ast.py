import ast
from functools import singledispatch
from collections.abc import Hashable


@singledispatch
def to_ast(node):
    raise TypeError(f"Unsupported type: {type(node)}")


@to_ast.register
def _(node: ast.AST):
    return node


@to_ast.register
def _(node: Hashable):
    return ast.Constant(node)


@to_ast.register
def _(node: tuple):
    return ast.Tuple(elts=[to_ast(x) for x in node], ctx=ast.Load())


@to_ast.register
def _(node: list):
    return ast.List(elts=[to_ast(x) for x in node], ctx=ast.Load())


@to_ast.register
def _(node: set):
    return ast.Set(node)


@to_ast.register
def _(node: dict):
    return ast.Dict(keys=[to_ast(k) for k in node.keys()],
                    values=[to_ast(v) for v in node.values()])


@to_ast.register
def _(node: range):
    args = [to_ast(node.start), to_ast(node.stop), to_ast(node.step)]
    return ast.Call(ast.Name('range', ctx=ast.Load()), args=args, keywords=[])
