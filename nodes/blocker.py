from comfy_execution.graph_utils import ExecutionBlocker


class AlwaysEqualProxy(str):
    def __eq__(self, _):
        return True
    def __ne__(self, _):
        return False


any_type = AlwaysEqualProxy("*")


class Blocker:
    @classmethod
    def INPUT_TYPES(cls):
        return {"required": {
            "任意": (any_type, {}),
            "启用": ("BOOLEAN", {"default": True, "label_on": "通过", "label_off": "阻断"}),
        }}

    RETURN_TYPES = (any_type,)
    RETURN_NAMES = ("任意",)
    FUNCTION = "execute"
    CATEGORY = "⚡ 逻辑"

    @classmethod
    def IS_CHANGED(cls, **kwargs):
        return float("NaN")

    def execute(self, 任意, 启用):
        return (任意,) if 启用 else (ExecutionBlocker(None),)


NODE_CLASS_MAPPINGS = {"Logic_Blocker": Blocker}
NODE_DISPLAY_NAME_MAPPINGS = {"Logic_Blocker": "🚧 阻断器"}
