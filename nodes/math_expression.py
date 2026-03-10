import ast
import math
import operator

from .blocker import AlwaysEqualProxy

any_type = AlwaysEqualProxy("*")

MAX_INPUTS = 10
VAR_NAMES = [chr(ord("A") + i) for i in range(MAX_INPUTS)]

SAFE_FUNCTIONS = {
    "sin": math.sin, "cos": math.cos, "tan": math.tan,
    "asin": math.asin, "acos": math.acos, "atan": math.atan, "atan2": math.atan2,
    "abs": abs, "round": round,
    "ceil": math.ceil, "floor": math.floor,
    "sqrt": math.sqrt, "pow": pow,
    "log": math.log, "log2": math.log2, "log10": math.log10,
    "min": min, "max": max,
    "clamp": lambda v, lo, hi: max(lo, min(v, hi)),
}

SAFE_CONSTANTS = {
    "pi": math.pi, "e": math.e, "inf": math.inf,
}

BIN_OPS = {
    ast.Add: operator.add, ast.Sub: operator.sub,
    ast.Mult: operator.mul, ast.Div: operator.truediv,
    ast.FloorDiv: operator.floordiv, ast.Mod: operator.mod,
    ast.Pow: operator.pow,
}

UNARY_OPS = {ast.UAdd: operator.pos, ast.USub: operator.neg}

CMP_OPS = {
    ast.Eq: operator.eq, ast.NotEq: operator.ne,
    ast.Lt: operator.lt, ast.LtE: operator.le,
    ast.Gt: operator.gt, ast.GtE: operator.ge,
}


def _eval_node(node, variables):
    if isinstance(node, ast.Expression):
        return _eval_node(node.body, variables)

    if isinstance(node, ast.Constant):
        if isinstance(node.value, (int, float)):
            return node.value
        raise ValueError(f"Unsupported constant type: {type(node.value).__name__}")

    if isinstance(node, ast.Name):
        name = node.id
        if name in variables:
            return variables[name]
        if name in SAFE_CONSTANTS:
            return SAFE_CONSTANTS[name]
        raise ValueError(f"Unknown variable: {name}")

    if isinstance(node, ast.UnaryOp):
        op = UNARY_OPS.get(type(node.op))
        if op is None:
            raise ValueError(f"Unsupported unary op: {type(node.op).__name__}")
        return op(_eval_node(node.operand, variables))

    if isinstance(node, ast.BinOp):
        op = BIN_OPS.get(type(node.op))
        if op is None:
            raise ValueError(f"Unsupported operator: {type(node.op).__name__}")
        return op(_eval_node(node.left, variables), _eval_node(node.right, variables))

    if isinstance(node, ast.Compare):
        left = _eval_node(node.left, variables)
        for op_node, comparator in zip(node.ops, node.comparators):
            op = CMP_OPS.get(type(op_node))
            if op is None:
                raise ValueError(f"Unsupported comparison: {type(op_node).__name__}")
            right = _eval_node(comparator, variables)
            if not op(left, right):
                return 0.0
            left = right
        return 1.0

    if isinstance(node, ast.Call):
        if not isinstance(node.func, ast.Name):
            raise ValueError("Only direct function calls supported")
        func = SAFE_FUNCTIONS.get(node.func.id)
        if func is None:
            raise ValueError(f"Unknown function: {node.func.id}")
        args = [_eval_node(a, variables) for a in node.args]
        return func(*args)

    if isinstance(node, ast.IfExp):
        cond = _eval_node(node.test, variables)
        return _eval_node(node.body, variables) if cond else _eval_node(node.orelse, variables)

    raise ValueError(f"Unsupported syntax: {type(node).__name__}")


_EXPR_CACHE = {}
_CACHE_MAX = 64


def safe_eval(expression, variables):
    expr = expression.strip()
    if expr not in _EXPR_CACHE:
        if len(_EXPR_CACHE) >= _CACHE_MAX:
            _EXPR_CACHE.clear()
        _EXPR_CACHE[expr] = ast.parse(expr, mode="eval")
    return _eval_node(_EXPR_CACHE[expr], variables)


def _to_number(value):
    if value is None:
        return 0.0
    if isinstance(value, bool):
        return 1.0 if value else 0.0
    if isinstance(value, (int, float)):
        return float(value)
    if isinstance(value, str):
        try:
            return float(value)
        except (ValueError, OverflowError):
            return 0.0
    try:
        import torch
        if isinstance(value, torch.Tensor) and value.numel() == 1:
            return float(value.item())
    except Exception:
        pass
    return 0.0


class MathExpression:
    @classmethod
    def INPUT_TYPES(cls):
        optional = {name: (any_type, {}) for name in VAR_NAMES}
        return {
            "required": {
                "expression": ("STRING", {"default": "A + B", "multiline": False}),
            },
            "optional": optional,
        }

    RETURN_TYPES = ("FLOAT", "INT", "BOOLEAN")
    RETURN_NAMES = ("float", "int", "boolean")
    FUNCTION = "execute"
    OUTPUT_NODE = True
    CATEGORY = "⚡ Logic"

    @classmethod
    def IS_CHANGED(cls, **kwargs):
        return float("NaN")

    def execute(self, expression, **kwargs):
        variables = {}
        for name in VAR_NAMES:
            if name in kwargs:
                variables[name] = _to_number(kwargs[name])

        try:
            result = float(safe_eval(expression, variables))
            error = ""
        except Exception as ex:
            result = 0.0
            error = str(ex)

        int_result = int(result)
        bool_result = result != 0.0

        return {
            "ui": {
                "expression": [expression],
                "float_val": [str(result)],
                "int_val": [str(int_result)],
                "bool_val": [str(bool_result)],
                "error": [error],
            },
            "result": (result, int_result, bool_result),
        }


NODE_CLASS_MAPPINGS = {"Logic_Math": MathExpression}
NODE_DISPLAY_NAME_MAPPINGS = {"Logic_Math": "🧮 Math Expression"}
