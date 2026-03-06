from .blocker import AlwaysEqualProxy

any_type = AlwaysEqualProxy("*")


class Looper:
    _state = {}

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "总次数": ("INT", {"default": 3, "min": 1, "max": 9999}),
            },
            "optional": {
                "任意": (any_type, {}),
            },
            "hidden": {
                "unique_id": "UNIQUE_ID",
            },
        }

    RETURN_TYPES = (any_type, "INT", "INT", "INT")
    RETURN_NAMES = ("任意", "索引", "总次数", "剩余")
    FUNCTION = "execute"
    OUTPUT_NODE = True
    CATEGORY = "⚡ 逻辑"

    @classmethod
    def IS_CHANGED(cls, **kwargs):
        return float("NaN")

    def execute(self, 总次数, unique_id, 任意=None):
        nid = str(unique_id)

        if nid not in self._state or self._state[nid] >= 总次数:
            self._state[nid] = 0

        current = self._state[nid]
        remaining = 总次数 - current - 1
        self._state[nid] = current + 1

        return {
            "ui": {
                "current": [current],
                "total": [总次数],
                "remaining": [remaining],
            },
            "result": (任意, current, 总次数, remaining),
        }


NODE_CLASS_MAPPINGS = {"Logic_Looper": Looper}
NODE_DISPLAY_NAME_MAPPINGS = {"Logic_Looper": "⚙️ 批处理器"}
