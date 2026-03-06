import torch
from .blocker import AlwaysEqualProxy

any_type = AlwaysEqualProxy("*")


def detect_type(value):
    if value is None:
        return "NONE", "空值"
    if isinstance(value, bool):
        return "BOOLEAN", f"值: {value}"
    if isinstance(value, int):
        return "INT", f"值: {value}"
    if isinstance(value, float):
        return "FLOAT", f"值: {value}"
    if isinstance(value, str):
        return "STRING", f"长度: {len(value)}"

    if isinstance(value, torch.Tensor):
        shape = "×".join(str(s) for s in value.shape)
        if value.dim() == 4:
            b, h, w, c = value.shape
            return "IMAGE", f"批次: {b}  尺寸: {w}×{h}  通道: {c}"
        if value.dim() == 3:
            b, h, w = value.shape
            return "MASK", f"批次: {b}  尺寸: {w}×{h}"
        return f"TENSOR_{value.dim()}D", f"形状: {shape}"

    if isinstance(value, dict):
        if "samples" in value:
            s = value["samples"]
            if isinstance(s, torch.Tensor) and s.dim() == 4:
                b, c, h, w = s.shape
                return "LATENT", f"批次: {b}  尺寸: {w}×{h}  通道: {c}"
            return "LATENT", f"keys: {list(value.keys())}"
        keys = list(value.keys())
        preview = ", ".join(str(k) for k in keys[:5])
        return "DICT", f"键数: {len(keys)}  [{preview}{'...' if len(keys) > 5 else ''}]"

    if isinstance(value, (list, tuple)):
        n = len(value)
        if n == 0:
            return "LIST", "空列表"
        first = value[0]
        if isinstance(first, torch.Tensor):
            dim = first.dim()
            if dim == 4:
                return "IMAGE_LIST", f"数量: {n}"
            if dim == 3:
                return "MASK_LIST", f"数量: {n}"
            return "TENSOR_LIST", f"数量: {n}"
        if isinstance(first, str):
            return "STRING_LIST", f"数量: {n}"
        if isinstance(first, bool):
            return "BOOLEAN_LIST", f"数量: {n}"
        if isinstance(first, int):
            return "INT_LIST", f"数量: {n}"
        if isinstance(first, float):
            return "FLOAT_LIST", f"数量: {n}"
        if isinstance(first, dict):
            return "DICT_LIST", f"数量: {n}"
        if isinstance(first, (list, tuple)):
            if len(first) >= 2 and isinstance(first[0], torch.Tensor) and isinstance(first[1], dict):
                return "CONDITIONING", f"数量: {n}"
            return "NESTED_LIST", f"数量: {n}"
        return f"{type(first).__name__.upper()}_LIST", f"数量: {n}"

    return type(value).__name__.upper(), ""


class PreviewType:
    @classmethod
    def INPUT_TYPES(cls):
        return {"required": {"任意": (any_type, {})}}

    RETURN_TYPES = ()
    FUNCTION = "execute"
    OUTPUT_NODE = True
    CATEGORY = "⚡ 逻辑"

    @classmethod
    def IS_CHANGED(cls, **kwargs):
        return float("NaN")

    def execute(self, 任意):
        type_name, detail = detect_type(任意)
        return {"ui": {"type_name": [type_name], "detail": [detail]}}


NODE_CLASS_MAPPINGS = {"Logic_PreviewType": PreviewType}
NODE_DISPLAY_NAME_MAPPINGS = {"Logic_PreviewType": "👁️ 预览任意类型"}
