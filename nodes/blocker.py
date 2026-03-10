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
            "any": (any_type, {}),
            "enable": ("BOOLEAN", {"default": True, "label_on": "Pass", "label_off": "Block", "on": "Pass", "off": "Block"}),
        }}

    RETURN_TYPES = (any_type,)
    RETURN_NAMES = ("any",)
    FUNCTION = "execute"
    CATEGORY = "⚡ Logic"

    @classmethod
    def IS_CHANGED(cls, **kwargs):
        return float("NaN")

    def execute(self, any, enable):
        return (any,) if enable else (ExecutionBlocker(None),)


NODE_CLASS_MAPPINGS = {"Logic_Blocker": Blocker}
NODE_DISPLAY_NAME_MAPPINGS = {"Logic_Blocker": "🚧 Blocker"}
