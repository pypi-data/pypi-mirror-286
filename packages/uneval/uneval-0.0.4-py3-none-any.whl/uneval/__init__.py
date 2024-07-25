import ast
from types import CodeType

from .expression import and_, or_, not_, in_
from .expression import if_, for_, lambda_
from .expression import quote, Expression
from .to_ast import to_ast

__all__ = [
    "quote",
    "Expression",
    "if_",
    "for_",
    "lambda_",
    "and_",
    "or_",
    "not_",
    "in_",
    "to_ast",
    "to_code",
]


def to_code(node) -> CodeType:
    """Compile str, expression or ast as expression."""
    node = to_ast(node)
    if not isinstance(node, ast.mod):
        node = ast.Expression(node)
    ast.fix_missing_locations(node)
    return compile(node, "<uneval.Expression>", mode='eval')
