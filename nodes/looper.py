from .blocker import AlwaysEqualProxy

any_type = AlwaysEqualProxy("*")


class Looper:
    _state = {}

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "total": ("INT", {"default": 3, "min": 1, "max": 9999}),
            },
            "optional": {
                "any": (any_type, {}),
            },
            "hidden": {
                "unique_id": "UNIQUE_ID",
            },
        }

    RETURN_TYPES = (any_type, "INT", "INT", "INT")
    RETURN_NAMES = ("any", "index", "total", "remaining")
    FUNCTION = "execute"
    OUTPUT_NODE = True
    CATEGORY = "⚡ Logic"

    @classmethod
    def IS_CHANGED(cls, **kwargs):
        return float("NaN")

    def execute(self, total, unique_id, any=None):
        nid = str(unique_id)

        if nid not in self._state or self._state[nid] >= total:
            self._state[nid] = 0

        current = self._state[nid]
        remaining = total - current - 1
        self._state[nid] = current + 1

        return {
            "ui": {
                "current": [current],
                "total": [total],
                "remaining": [remaining],
            },
            "result": (any, current, total, remaining),
        }


NODE_CLASS_MAPPINGS = {"Logic_Looper": Looper}
NODE_DISPLAY_NAME_MAPPINGS = {"Logic_Looper": "⚙️ Batch Processor"}
