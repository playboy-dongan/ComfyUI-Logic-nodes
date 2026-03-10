from .blocker import AlwaysEqualProxy

any_type = AlwaysEqualProxy("*")


class Switch:
    @classmethod
    def INPUT_TYPES(cls):
        return {"required": {
            "true_val": (any_type, {}),
            "false_val": (any_type, {}),
            "condition": ("BOOLEAN", {"default": True, "label_on": "True", "label_off": "False", "on": "True", "off": "False"}),
        }}

    RETURN_TYPES = (any_type,)
    RETURN_NAMES = ("output",)
    FUNCTION = "execute"
    CATEGORY = "⚡ Logic"

    @classmethod
    def IS_CHANGED(cls, **kwargs):
        return float("NaN")

    def execute(self, true_val, false_val, condition):
        return (true_val,) if condition else (false_val,)


NODE_CLASS_MAPPINGS = {"Logic_Switch": Switch}
NODE_DISPLAY_NAME_MAPPINGS = {"Logic_Switch": "🔀 Switch"}
