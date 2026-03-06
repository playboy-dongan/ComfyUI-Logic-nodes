import random
from .blocker import AlwaysEqualProxy

any_type = AlwaysEqualProxy("*")

MODES = ["随机整数", "随机浮点数", "随机种子", "随机布尔"]


class RandomTool:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "模式": (MODES, {"default": "随机种子"}),
                "最小值": ("FLOAT", {"default": 0, "min": -1e18, "max": 1e18, "step": 1}),
                "最大值": ("FLOAT", {"default": 100, "min": -1e18, "max": 1e18, "step": 1}),
            },
        }

    RETURN_TYPES = (any_type,)
    RETURN_NAMES = ("随机值",)
    FUNCTION = "execute"
    OUTPUT_NODE = True
    CATEGORY = "⚡ 逻辑"

    @classmethod
    def IS_CHANGED(cls, **kwargs):
        return float("NaN")

    def execute(self, 模式, 最小值=0, 最大值=100):
        if 模式 == "随机整数":
            lo, hi = int(最小值), int(最大值)
            value = random.randint(min(lo, hi), max(lo, hi))
        elif 模式 == "随机浮点数":
            value = round(random.uniform(最小值, 最大值), 6)
        elif 模式 == "随机种子":
            value = random.randint(0, 2**64 - 1)
        elif 模式 == "随机布尔":
            value = random.choice([True, False])
        else:
            value = 0

        return {"ui": {"value": [str(value)]}, "result": (value,)}


NODE_CLASS_MAPPINGS = {"Logic_Random": RandomTool}
NODE_DISPLAY_NAME_MAPPINGS = {"Logic_Random": "🎲 随机工具"}
