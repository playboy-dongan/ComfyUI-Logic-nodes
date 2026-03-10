import torch
from .blocker import AlwaysEqualProxy

any_type = AlwaysEqualProxy("*")


def _detect_type(value):
    if value is None:
        return "NONE"
    if isinstance(value, bool):
        return "BOOLEAN"
    if isinstance(value, int):
        return "INT"
    if isinstance(value, float):
        return "FLOAT"
    if isinstance(value, str):
        return "STRING"
    if isinstance(value, torch.Tensor):
        if value.dim() == 4:
            return "IMAGE"
        if value.dim() == 3:
            return "MASK"
        return f"TENSOR_{value.dim()}D"
    if isinstance(value, dict):
        if "samples" in value:
            return "LATENT"
        return "DICT"
    if isinstance(value, (list, tuple)):
        return "LIST"
    return type(value).__name__.upper()


def to_string(value):
    if value is None:
        return ""
    if isinstance(value, bool):
        return "True" if value else "False"
    if isinstance(value, torch.Tensor):
        if value.numel() == 1:
            return str(value.item())
        shape = "\u00d7".join(str(s) for s in value.shape)
        return f"Tensor({shape})"
    if isinstance(value, dict):
        if "samples" in value:
            s = value["samples"]
            if isinstance(s, torch.Tensor):
                shape = "\u00d7".join(str(d) for d in s.shape)
                return f"Latent({shape})"
        return str(value)
    return str(value)


def to_int(value):
    if value is None:
        return 0
    if isinstance(value, bool):
        return int(value)
    if isinstance(value, (int, float)):
        return int(value)
    if isinstance(value, str):
        try:
            return int(value)
        except ValueError:
            try:
                return int(float(value))
            except (ValueError, OverflowError):
                return 0
    if isinstance(value, torch.Tensor):
        if value.numel() == 1:
            return int(value.item())
        return value.numel()
    if isinstance(value, (list, tuple, dict)):
        return len(value)
    return 0


def to_float(value):
    if value is None:
        return 0.0
    if isinstance(value, bool):
        return float(value)
    if isinstance(value, (int, float)):
        return float(value)
    if isinstance(value, str):
        try:
            return float(value)
        except (ValueError, OverflowError):
            return 0.0
    if isinstance(value, torch.Tensor):
        if value.numel() == 1:
            return float(value.item())
        return float(value.numel())
    if isinstance(value, (list, tuple, dict)):
        return float(len(value))
    return 0.0


def to_bool(value):
    if value is None:
        return False
    if isinstance(value, bool):
        return value
    if isinstance(value, str):
        return value.lower() not in ("false", "0", "no", "none", "null", "")
    if isinstance(value, torch.Tensor):
        if value.numel() == 1:
            return bool(value.item())
        return value.numel() > 0
    try:
        return bool(value)
    except Exception:
        return False


class Converter:
    @classmethod
    def INPUT_TYPES(cls):
        return {"required": {
            "any": (any_type, {}),
        }}

    RETURN_TYPES = ("STRING", "INT", "FLOAT", "BOOLEAN")
    RETURN_NAMES = ("string", "int", "float", "boolean")
    FUNCTION = "execute"
    OUTPUT_NODE = True
    CATEGORY = "⚡ Logic"

    @classmethod
    def IS_CHANGED(cls, **kwargs):
        return float("NaN")

    def execute(self, any):
        str_val = to_string(any)
        int_val = to_int(any)
        float_val = to_float(any)
        bool_val = to_bool(any)
        orig_type = _detect_type(any)

        return {
            "ui": {
                "original_type": [orig_type],
                "str_val": [str_val],
                "int_val": [str(int_val)],
                "float_val": [str(float_val)],
                "bool_val": [str(bool_val)],
            },
            "result": (str_val, int_val, float_val, bool_val),
        }


NODE_CLASS_MAPPINGS = {"Logic_Converter": Converter}
NODE_DISPLAY_NAME_MAPPINGS = {"Logic_Converter": "🔄 Type Converter"}
