import random
from .blocker import AlwaysEqualProxy

any_type = AlwaysEqualProxy("*")

MODES = ["random_int", "random_float", "random_seed", "random_bool"]


class RandomTool:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "mode": (MODES, {"default": "random_seed"}),
                "min_val": ("FLOAT", {"default": 0, "min": -1e18, "max": 1e18, "step": 1}),
                "max_val": ("FLOAT", {"default": 100, "min": -1e18, "max": 1e18, "step": 1}),
            },
        }

    RETURN_TYPES = (any_type,)
    RETURN_NAMES = ("random",)
    FUNCTION = "execute"
    OUTPUT_NODE = True
    CATEGORY = "⚡ Logic"

    @classmethod
    def IS_CHANGED(cls, **kwargs):
        return float("NaN")

    def execute(self, mode, min_val=0, max_val=100):
        if mode == "random_int":
            lo, hi = int(min_val), int(max_val)
            value = random.randint(min(lo, hi), max(lo, hi))
        elif mode == "random_float":
            value = round(random.uniform(min_val, max_val), 6)
        elif mode == "random_seed":
            value = random.randint(0, 2**64 - 1)
        elif mode == "random_bool":
            value = random.choice([True, False])
        else:
            value = 0

        return {"ui": {"value": [str(value)]}, "result": (value,)}


NODE_CLASS_MAPPINGS = {"Logic_Random": RandomTool}
NODE_DISPLAY_NAME_MAPPINGS = {"Logic_Random": "🎲 Random Tool"}
