from .blocker import AlwaysEqualProxy

any_type = AlwaysEqualProxy("*")

CONDITIONS = [
    "A == B", "A != B", "A > B", "A < B", "A >= B", "A <= B",
    "A contains B", "A is empty", "A is not empty", "A is true", "A is false",
    "length == B", "length > B", "length < B",
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


def _eval_contains(a, b):
    try:
        return b in a
    except TypeError:
        return str(b) in str(a)


_COND_HANDLERS = {
    "A == B": lambda a, b: a == b,
    "A != B": lambda a, b: a != b,
    "A > B": lambda a, b: a > b,
    "A < B": lambda a, b: a < b,
    "A >= B": lambda a, b: a >= b,
    "A <= B": lambda a, b: a <= b,
    "A contains B": _eval_contains,
    "A is empty": lambda a, b: is_empty(a),
    "A is not empty": lambda a, b: not is_empty(a),
    "A is true": lambda a, b: bool(a),
    "A is false": lambda a, b: not bool(a),
    "length == B": lambda a, b: safe_len(a) == int(b),
    "length > B": lambda a, b: safe_len(a) > int(b),
    "length < B": lambda a, b: safe_len(a) < int(b),
}


def evaluate(a, b, cond):
    try:
        fn = _COND_HANDLERS.get(cond)
        return fn(a, b) if fn is not None else False
    except Exception:
        return False


class Judge:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "any_a": (any_type, {}),
                "condition": (CONDITIONS, {"default": "A == B"}),
            },
            "optional": {
                "any_b": (any_type, {}),
            },
        }

    RETURN_TYPES = ("BOOLEAN",)
    RETURN_NAMES = ("result",)
    FUNCTION = "execute"
    OUTPUT_NODE = True
    CATEGORY = "⚡ Logic"

    @classmethod
    def IS_CHANGED(cls, **kwargs):
        return float("NaN")

    def execute(self, any_a, condition, any_b=None):
        result = evaluate(any_a, any_b, condition)
        return {"ui": {"result": [result]}, "result": (result,)}


NODE_CLASS_MAPPINGS = {"Logic_Judge": Judge}
NODE_DISPLAY_NAME_MAPPINGS = {"Logic_Judge": "⚖️ Judge"}
