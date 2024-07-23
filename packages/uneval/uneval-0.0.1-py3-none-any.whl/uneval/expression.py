import ast
import operator
from types import CodeType
from typing import Hashable, List, Set, Dict, Sequence, Mapping, TypeVar, Iterable

TExpression = TypeVar("TExpression", bound="Expression")


class Expression:
    """Represents a python expression."""
    def __init__(self, node: ast.AST):
        self._node = node

    def _unop(op, node_cls):
        def unary(self) -> TExpression:
            node = self._node
            return Expression(ast.UnaryOp(node_cls(), node))
        unary.__name__ = "__" + op.__name__ + "__"
        unary.__doc__ = f"""Generate a new expression applying {op.__name__}"""
        return unary

    def _binop(op, node_cls):
        def forward(self, other) -> TExpression:
            left, right = self._node, to_ast(other)
            return Expression(ast.BinOp(left, node_cls(), right))
        forward.__name__ = "__" + op.__name__ + "__"
        forward.__doc__ = f"""Generate a new expression applying {op.__name__}"""

        def backward(self, other) -> TExpression:
            left, right = self._node, to_ast(other)
            return Expression(ast.BinOp(right, node_cls(), left))
        backward.__name__ = "__" + op.__name__ + "__"
        backward.__doc__ = f"""Generate a new expression applying {op.__name__}"""

        return forward, backward

    def _compare(op, node_cls):
        def compare(self, other) -> TExpression:
            left, right = self._node, to_ast(other)
            return Expression(ast.Compare(left, [node_cls()], [right]))
        compare.__name__ = "__" + op.__name__ + "__"
        compare.__doc__ = f"""Generate a new expression applying {op.__name__}"""
        return compare

    __pos__ = _unop(operator.pos, ast.UAdd)
    __neg__ = _unop(operator.neg, ast.USub)
    __invert__ = _unop(operator.invert, ast.Invert)
    __add__, __radd__ = _binop(operator.add, ast.Add)
    __sub__, __rsub__ = _binop(operator.sub, ast.Sub)
    __mul__, __rmul__ = _binop(operator.mul, ast.Mult)
    __or__, __ror__ = _binop(operator.or_, ast.BitOr)
    __and__, __rand__ = _binop(operator.and_, ast.BitAnd)
    __xor__, __rxor__ = _binop(operator.xor, ast.BitXor)
    __floordiv__, __rfloordiv__ = _binop(operator.floordiv, ast.FloorDiv)
    __truediv__, __rtruediv__ = _binop(operator.truediv, ast.Div)
    __mod__, __rmod__ = _binop(operator.mod, ast.Mod)
    __pow__, __rpow__ = _binop(operator.pow, ast.Pow)
    __matmul__, __rmatmul__ = _binop(operator.matmul, ast.MatMult)
    __lshift__, __rlshift__ = _binop(operator.lshift, ast.LShift)
    __rshift__, __rrshift__ = _binop(operator.rshift, ast.RShift)
    __ge__ = _compare(operator.ge, ast.GtE)
    __gt__ = _compare(operator.gt, ast.Gt)
    __lt__ = _compare(operator.lt, ast.Lt)
    __le__ = _compare(operator.le, ast.LtE)
    __eq__ = _compare(operator.eq, ast.Eq)
    __ne__ = _compare(operator.ne, ast.NotEq)

    def __getattr__(self, item) -> TExpression:
        node = self._node
        node = ast.Attribute(node, item, ctx=ast.Load())
        return Expression(node)

    def __call__(self, *args, **kwargs) -> TExpression:
        node = self._node
        ast_args = [to_ast(arg) for arg in args]
        ast_kwargs = [
            ast.keyword(arg=to_ast(k), value=to_ast(v))
            for k, v in kwargs.items()
        ]
        node = ast.Call(node, args=ast_args, keywords=ast_kwargs)
        return Expression(node)

    def __repr__(self) -> str:
        return f"<{type(self).__name__}: {self}>"

    def __str__(self) -> str:
        node = self._node
        expr = ast.unparse(node)
        return str(expr)


class _NameQuoter:
    """Helper to create symbols."""
    def __getattr__(self, item) -> Expression:
        return self(item)

    def __call__(self, item) -> Expression:
        return Expression(ast.Name(item, ctx=ast.Load()))


quote = _NameQuoter()


def if_(test, body, orelse=None) -> Expression:
    """Create an if expression."""
    test, body, orelse = to_ast(test), to_ast(body), to_ast(orelse)
    if orelse is None:
        node = ast.BoolOp(ast.Or, values=[ast.UnaryOp(ast.Not, test), body])
    else:
        node = ast.IfExp(test, body, orelse)
    return Expression(node)


def for_(element, *generators, type=None) -> Expression:
    """Create a for-comprehension."""
    element = to_ast(element)
    generators = [_comprehension(gen) for gen in generators]

    if type is None or type is iter:
        res = ast.GeneratorExp(element, generators)
    elif type is list:
        res = ast.ListComp(element, generators)
    elif type is set:
        res = ast.SetComp(element, generators)
    elif type is dict:
        key, value = element
        res = ast.DictComp(key, value, generators)
    else:
        raise TypeError(f"Unknown type {type}")
    return Expression(res)


def _comprehension(comp):
    """Convert comprehension to ast.comprehension."""
    if isinstance(comp, ast.comprehension):
        return comp
    elif isinstance(comp, Sequence):
        [target, iter, *ifs] = comp
        target = _ContextReplacer(ast.Store()).visit(to_ast(target))
        ifs = [to_ast(e) for e in ifs]
        return ast.comprehension(to_ast(target), to_ast(iter), ifs, is_async=False)
    elif isinstance(comp, Mapping):
        return ast.comprehension(**comp)
    else:
        raise TypeError("Not a comprehension")


class _ContextReplacer(ast.NodeTransformer):
    """Replace context of whole subtree."""
    def __init__(self, ctx):
        self.ctx = ctx

    def visit_Name(self, node):
        node.ctx = self.ctx
        return node

    def visit_Attribute(self, node):
        self.generic_visit(node)
        node.ctx = self.ctx
        return node


def lambda_(args: Iterable[Expression | ast.Name], body) -> Expression:
    """Generate a lambda expression."""
    if isinstance(args, Iterable):
        args = [ast.arg(arg=to_ast(arg).id) for arg in args]
        args = ast.arguments(posonlyargs=[], args=args, kwonlyargs=[], kw_defaults=[], defaults=[])
    elif not isinstance(args, ast.arguments):
        raise TypeError("args should be a sequence")
    node = ast.Lambda(args, to_ast(body))
    return Expression(node)


def to_expression(expr) -> Expression:
    """Convert str or ast to uneval."""
    if isinstance(expr, Expression):
        return expr

    if isinstance(expr, str):
        expr = ast.parse(expr, 'eval')
    if isinstance(expr, ast.AST):
        return Expression(expr)
    else:
        raise TypeError("String or AST expected")


def to_ast(node) -> ast.AST:
    """Convert str or uneval to ast."""
    if isinstance(node, ast.AST):
        return node
    elif isinstance(node, Expression):
        return node._node
    elif isinstance(node, Hashable):
        return ast.Constant(node)
    elif isinstance(node, List):
        return ast.List(elts=[to_ast(x) for x in node], ctx=ast.Load())
    elif isinstance(node, Set):
        return ast.Set(to_ast(x) for x in node)
    elif isinstance(node, Dict):
        return ast.Dict(keys=[to_ast(k) for k in node.keys()],
                        values=[to_ast(v) for v in node.values()])
    else:
        raise TypeError(f"Unsupported type: {type(node)}")


def to_code(node) -> CodeType:
    """Compile str, expression or ast as expression."""
    node = to_ast(node)
    if not isinstance(node, ast.Expression):
        node = ast.Expression(node)
    ast.fix_missing_locations(node)
    return compile(node, __file__, 'eval')
