from .blocker import AlwaysEqualProxy

any_type = AlwaysEqualProxy("*")

CONDITIONS = [
    "A == B", "A != B", "A > B", "A < B", "A >= B", "A <= B",
    "A 包含 B", "A 为空", "A 不为空", "A 为真", "A 为假",
    "长度 == B", "长度 > B", "长度 < B",
]


def safe_len(v):
    try:
        return len(v)
    except TypeError:
        return 0


def is_empty(v):
    if v is None:
        return True
    try:
        return len(v) == 0
    except TypeError:
        return False


def evaluate(a, b, cond):
    try:
        if cond == "A == B":    return a == b
        if cond == "A != B":    return a != b
        if cond == "A > B":     return a > b
        if cond == "A < B":     return a < b
        if cond == "A >= B":    return a >= b
        if cond == "A <= B":    return a <= b
        if cond == "A 包含 B":
            try:
                return b in a
            except TypeError:
                return str(b) in str(a)
        if cond == "A 为空":    return is_empty(a)
        if cond == "A 不为空":  return not is_empty(a)
        if cond == "A 为真":    return bool(a)
        if cond == "A 为假":    return not bool(a)
        if cond == "长度 == B": return safe_len(a) == int(b)
        if cond == "长度 > B":  return safe_len(a) > int(b)
        if cond == "长度 < B":  return safe_len(a) < int(b)
    except Exception:
        return False
    return False


class Judge:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "任意A": (any_type, {}),
                "条件": (CONDITIONS, {"default": "A == B"}),
            },
            "optional": {
                "任意B": (any_type, {}),
            },
        }

    RETURN_TYPES = ("BOOLEAN",)
    RETURN_NAMES = ("结果",)
    FUNCTION = "execute"
    OUTPUT_NODE = True
    CATEGORY = "⚡ 逻辑"

    @classmethod
    def IS_CHANGED(cls, **kwargs):
        return float("NaN")

    def execute(self, 任意A, 条件, 任意B=None):
        result = evaluate(任意A, 任意B, 条件)
        return {"ui": {"result": [result]}, "result": (result,)}


NODE_CLASS_MAPPINGS = {"Logic_Judge": Judge}
NODE_DISPLAY_NAME_MAPPINGS = {"Logic_Judge": "⚖️ 判断器"}
