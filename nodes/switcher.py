from comfy_execution.graph_utils import ExecutionBlocker
from .blocker import AlwaysEqualProxy

any_type = AlwaysEqualProxy("*")
MAX_INPUTS = 10


class Switcher:
    @classmethod
    def INPUT_TYPES(cls):
        optional = {f"任意{i}": (any_type, {}) for i in range(1, MAX_INPUTS + 1)}
        return {
            "required": {
                "选择": ("INT", {"default": 1, "min": 1, "max": MAX_INPUTS}),
            },
            "optional": optional,
        }

    RETURN_TYPES = (any_type,)
    RETURN_NAMES = ("输出",)
    FUNCTION = "execute"
    CATEGORY = "⚡ 逻辑"

    @classmethod
    def IS_CHANGED(cls, **kwargs):
        return float("NaN")

    def execute(self, 选择, **kwargs):
        key = f"任意{选择}"
        if key not in kwargs:
            return (ExecutionBlocker(None),)
        return (kwargs[key],)


NODE_CLASS_MAPPINGS = {"Logic_Switcher": Switcher}
NODE_DISPLAY_NAME_MAPPINGS = {"Logic_Switcher": "🎚️ 切换器"}
