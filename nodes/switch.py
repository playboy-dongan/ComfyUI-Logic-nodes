from .blocker import AlwaysEqualProxy

any_type = AlwaysEqualProxy("*")


class Switch:
    @classmethod
    def INPUT_TYPES(cls):
        return {"required": {
            "真": (any_type, {}),
            "假": (any_type, {}),
            "条件": ("BOOLEAN", {"default": True, "label_on": "真", "label_off": "假"}),
        }}

    RETURN_TYPES = (any_type,)
    RETURN_NAMES = ("输出",)
    FUNCTION = "execute"
    CATEGORY = "⚡ 逻辑"

    @classmethod
    def IS_CHANGED(cls, **kwargs):
        return float("NaN")

    def execute(self, 真, 假, 条件):
        return (真,) if 条件 else (假,)


NODE_CLASS_MAPPINGS = {"Logic_Switch": Switch}
NODE_DISPLAY_NAME_MAPPINGS = {"Logic_Switch": "🔀 条件切换"}
