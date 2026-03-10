import torch
from .blocker import AlwaysEqualProxy

any_type = AlwaysEqualProxy("*")


def detect_type(value):
    if value is None:
        return "NONE", "null"
    if isinstance(value, bool):
        return "BOOLEAN", f"value: {value}"
    if isinstance(value, int):
        return "INT", f"value: {value}"
    if isinstance(value, float):
        return "FLOAT", f"value: {value}"
    if isinstance(value, str):
        return "STRING", f"length: {len(value)}"

    if isinstance(value, torch.Tensor):
        shape = "×".join(str(s) for s in value.shape)
        if value.dim() == 4:
            b, h, w, c = value.shape
            return "IMAGE", f"batch: {b}  size: {w}×{h}  ch: {c}"
        if value.dim() == 3:
            b, h, w = value.shape
            return "MASK", f"batch: {b}  size: {w}×{h}"
        return f"TENSOR_{value.dim()}D", f"shape: {shape}"

    if isinstance(value, dict):
        if "samples" in value:
            s = value["samples"]
            if isinstance(s, torch.Tensor) and s.dim() == 4:
                b, c, h, w = s.shape
                return "LATENT", f"batch: {b}  size: {w}×{h}  ch: {c}"
            return "LATENT", f"keys: {list(value.keys())}"
        keys = list(value.keys())
        preview = ", ".join(str(k) for k in keys[:5])
        return "DICT", f"keys: {len(keys)}  [{preview}{'...' if len(keys) > 5 else ''}]"

    if isinstance(value, (list, tuple)):
        n = len(value)
        if n == 0:
            return "LIST", "empty"
        first = value[0]
        if isinstance(first, torch.Tensor):
            dim = first.dim()
            if dim == 4:
                return "IMAGE_LIST", f"count: {n}"
            if dim == 3:
                return "MASK_LIST", f"count: {n}"
            return "TENSOR_LIST", f"count: {n}"
        if isinstance(first, str):
            return "STRING_LIST", f"count: {n}"
        if isinstance(first, bool):
            return "BOOLEAN_LIST", f"count: {n}"
        if isinstance(first, int):
            return "INT_LIST", f"count: {n}"
        if isinstance(first, float):
            return "FLOAT_LIST", f"count: {n}"
        if isinstance(first, dict):
            return "DICT_LIST", f"count: {n}"
        if isinstance(first, (list, tuple)):
            if len(first) >= 2 and isinstance(first[0], torch.Tensor) and isinstance(first[1], dict):
                return "CONDITIONING", f"count: {n}"
            return "NESTED_LIST", f"count: {n}"
        return f"{type(first).__name__.upper()}_LIST", f"count: {n}"

    return type(value).__name__.upper(), ""


class PreviewType:
    @classmethod
    def INPUT_TYPES(cls):
        return {"required": {"any": (any_type, {})}}

    RETURN_TYPES = ()
    FUNCTION = "execute"
    OUTPUT_NODE = True
    CATEGORY = "⚡ Logic"

    @classmethod
    def IS_CHANGED(cls, **kwargs):
        return float("NaN")

    def execute(self, any):
        type_name, detail = detect_type(any)
        return {"ui": {"type_name": [type_name], "detail": [detail]}}


NODE_CLASS_MAPPINGS = {"Logic_PreviewType": PreviewType}
NODE_DISPLAY_NAME_MAPPINGS = {"Logic_PreviewType": "👁️ Preview Type"}
