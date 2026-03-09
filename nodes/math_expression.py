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
        raise ValueError(f"不支持的常量类型: {type(node.value).__name__}")

    if isinstance(node, ast.Name):
        name = node.id
        if name in variables:
            return variables[name]
        if name in SAFE_CONSTANTS:
            return SAFE_CONSTANTS[name]
        raise ValueError(f"未知变量: {name}")

    if isinstance(node, ast.UnaryOp):
        op = UNARY_OPS.get(type(node.op))
        if op is None:
            raise ValueError(f"不支持的一元运算: {type(node.op).__name__}")
        return op(_eval_node(node.operand, variables))

    if isinstance(node, ast.BinOp):
        op = BIN_OPS.get(type(node.op))
        if op is None:
            raise ValueError(f"不支持的运算符: {type(node.op).__name__}")
        return op(_eval_node(node.left, variables), _eval_node(node.right, variables))

    if isinstance(node, ast.Compare):
        left = _eval_node(node.left, variables)
        for op_node, comparator in zip(node.ops, node.comparators):
            op = CMP_OPS.get(type(op_node))
            if op is None:
                raise ValueError(f"不支持的比较运算: {type(op_node).__name__}")
            right = _eval_node(comparator, variables)
            if not op(left, right):
                return 0.0
            left = right
        return 1.0

    if isinstance(node, ast.Call):
        if not isinstance(node.func, ast.Name):
            raise ValueError("仅支持直接函数调用")
        func = SAFE_FUNCTIONS.get(node.func.id)
        if func is None:
            raise ValueError(f"未知函数: {node.func.id}")
        args = [_eval_node(a, variables) for a in node.args]
        return func(*args)

    if isinstance(node, ast.IfExp):
        cond = _eval_node(node.test, variables)
        return _eval_node(node.body, variables) if cond else _eval_node(node.orelse, variables)

    raise ValueError(f"不支持的语法: {type(node).__name__}")


def safe_eval(expression, variables):
    tree = ast.parse(expression.strip(), mode="eval")
    return _eval_node(tree, variables)


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
                "表达式": ("STRING", {"default": "A + B", "multiline": False}),
            },
            "optional": optional,
        }

    RETURN_TYPES = ("FLOAT", "INT", "BOOLEAN")
    RETURN_NAMES = ("浮点数", "整数", "布尔值")
    FUNCTION = "execute"
    OUTPUT_NODE = True
    CATEGORY = "⚡ 逻辑"

    @classmethod
    def IS_CHANGED(cls, **kwargs):
        return float("NaN")

    def execute(self, 表达式, **kwargs):
        variables = {}
        for name in VAR_NAMES:
            if name in kwargs:
                variables[name] = _to_number(kwargs[name])

        try:
            result = float(safe_eval(表达式, variables))
            error = ""
        except Exception as ex:
            result = 0.0
            error = str(ex)

        int_result = int(result)
        bool_result = result != 0.0

        return {
            "ui": {
                "expression": [表达式],
                "float_val": [str(result)],
                "int_val": [str(int_result)],
                "bool_val": [str(bool_result)],
                "error": [error],
            },
            "result": (result, int_result, bool_result),
        }


NODE_CLASS_MAPPINGS = {"Logic_Math": MathExpression}
NODE_DISPLAY_NAME_MAPPINGS = {"Logic_Math": "🧮 数学表达式"}
