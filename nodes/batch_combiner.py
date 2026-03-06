import torch
from comfy_execution.graph_utils import ExecutionBlocker
from .blocker import AlwaysEqualProxy

any_type = AlwaysEqualProxy("*")
MAX_INPUTS = 10

try:
    import torchaudio
    HAS_TORCHAUDIO = True
except ImportError:
    HAS_TORCHAUDIO = False


class BatchCombiner:
    @classmethod
    def INPUT_TYPES(cls):
        optional = {f"任意{i}": (any_type, {}) for i in range(1, MAX_INPUTS + 1)}
        return {
            "required": {},
            "optional": optional,
        }

    RETURN_TYPES = (any_type,)
    RETURN_NAMES = ("批次",)
    FUNCTION = "execute"
    OUTPUT_NODE = True
    CATEGORY = "⚡ 逻辑"

    @classmethod
    def IS_CHANGED(cls, **kwargs):
        return float("NaN")

    def execute(self, **kwargs):
        items = []
        for i in range(1, MAX_INPUTS + 1):
            key = f"任意{i}"
            if key in kwargs:
                items.append(kwargs[key])

        if not items:
            return {"ui": {"detail": ["无输入"], "type_name": [""]},
                    "result": (ExecutionBlocker(None),)}

        if len(items) == 1:
            result = items[0]
        else:
            result = self._combine(items)

        type_name = self._get_type_name(result)
        detail = self._get_detail(result, type_name)
        return {"ui": {"detail": [detail], "type_name": [type_name]},
                "result": (result,)}

    def _pad_and_cat(self, tensors, dim=0):
        ndim = tensors[0].dim()
        max_sizes = list(tensors[0].shape)
        for t in tensors[1:]:
            for d in range(ndim):
                if d != dim:
                    max_sizes[d] = max(max_sizes[d], t.shape[d])

        padded = []
        for t in tensors:
            need_pad = any(t.shape[d] != max_sizes[d] for d in range(ndim) if d != dim)
            if not need_pad:
                padded.append(t)
                continue
            new_shape = list(max_sizes)
            new_shape[dim] = t.shape[dim]
            p = torch.zeros(new_shape, dtype=t.dtype, device=t.device)
            slices = tuple(slice(0, s) for s in t.shape)
            p[slices] = t
            padded.append(p)
        return torch.cat(padded, dim=dim)

    def _combine(self, items):
        first = items[0]

        if isinstance(first, torch.Tensor):
            return self._pad_and_cat(items, dim=0)

        if isinstance(first, dict):
            if "samples" in first:
                tensors = [it["samples"] for it in items]
                samples = self._pad_and_cat(tensors, dim=0)
                result = {**first, "samples": samples}
                if "batch_index" in first:
                    offset = 0
                    indices = []
                    for it in items:
                        bi = it.get("batch_index", list(range(it["samples"].shape[0])))
                        indices.extend([b + offset for b in bi])
                        offset += it["samples"].shape[0]
                    result["batch_index"] = indices
                return result

            if "waveform" in first and "sample_rate" in first:
                return self._combine_audio(items)

        if isinstance(first, (list, tuple)):
            combined = []
            for it in items:
                if isinstance(it, (list, tuple)):
                    combined.extend(it)
                else:
                    combined.append(it)
            return combined

        return items

    def _combine_audio(self, items):
        target_sr = items[0]["sample_rate"]
        segments = []

        for it in items:
            w = it["waveform"]
            sr = it["sample_rate"]
            if sr != target_sr:
                if HAS_TORCHAUDIO:
                    w = torchaudio.functional.resample(w, sr, target_sr)
                else:
                    ratio = target_sr / sr
                    new_len = int(w.shape[-1] * ratio)
                    w = torch.nn.functional.interpolate(
                        w.float(), size=new_len, mode="linear", align_corners=False
                    )
            for b in range(w.shape[0]):
                segments.append(w[b:b + 1])

        max_ch = max(s.shape[1] for s in segments)
        aligned = []
        for s in segments:
            if s.shape[1] < max_ch:
                repeats = (max_ch + s.shape[1] - 1) // s.shape[1]
                s = s.repeat(1, repeats, 1)[:, :max_ch, :]
            aligned.append(s)

        combined = torch.cat(aligned, dim=-1)
        return {"waveform": combined, "sample_rate": target_sr}

    def _get_detail(self, value, type_name):
        if type_name == "AUDIO" and isinstance(value, dict):
            w = value["waveform"]
            sr = value["sample_rate"]
            duration = w.shape[-1] / sr
            return f"{duration:.2f}s {sr}Hz"
        if isinstance(value, torch.Tensor):
            return f"×{value.shape[0]}"
        if isinstance(value, dict):
            if "samples" in value:
                return f"×{value['samples'].shape[0]}"
        if isinstance(value, (list, tuple)):
            return f"×{len(value)}"
        return "×1"

    def _get_type_name(self, value):
        if isinstance(value, torch.Tensor):
            if value.dim() == 4:
                return "IMAGE"
            if value.dim() == 3:
                return "MASK"
            return "TENSOR"
        if isinstance(value, dict):
            if "samples" in value:
                return "LATENT"
            if "waveform" in value:
                return "AUDIO"
            return "DICT"
        if isinstance(value, (list, tuple)):
            if len(value) > 0 and isinstance(value[0], (list, tuple)):
                return "CONDITIONING"
            return "LIST"
        return type(value).__name__.upper()


NODE_CLASS_MAPPINGS = {"Logic_BatchCombiner": BatchCombiner}
NODE_DISPLAY_NAME_MAPPINGS = {"Logic_BatchCombiner": "📦 组合任意批次"}
