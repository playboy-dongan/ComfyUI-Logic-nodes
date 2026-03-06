import os
import json
import random
from io import BytesIO

import av
import folder_paths
import numpy as np
import torch
from PIL import Image

from .blocker import AlwaysEqualProxy

any_type = AlwaysEqualProxy("*")


class UniversalPreview:
    def __init__(self):
        self.output_dir = folder_paths.get_temp_directory()
        self.type = "temp"
        self.prefix_append = "_temp_" + ''.join(
            random.choice("abcdefghijklmnopqrstupvxyz") for _ in range(5)
        )
        self.compress_level = 1

    @classmethod
    def INPUT_TYPES(cls):
        return {"required": {"任意": (any_type, {})}}

    RETURN_TYPES = ()
    FUNCTION = "execute"
    OUTPUT_NODE = True
    CATEGORY = "⚡ 逻辑"

    @classmethod
    def IS_CHANGED(cls, **kwargs):
        return float("NaN")

    def execute(self, 任意):
        value = 任意

        if isinstance(value, torch.Tensor):
            if value.dim() == 4:
                images = self._save_images(value)
                return {"ui": {"images": images, "text": [], "audio": []}}
            if value.dim() == 3:
                vis = value.reshape((-1, 1, value.shape[-2], value.shape[-1]))
                vis = vis.movedim(1, -1).expand(-1, -1, -1, 3)
                images = self._save_images(vis)
                return {"ui": {"images": images, "text": [], "audio": []}}

        if isinstance(value, dict):
            if "waveform" in value and "sample_rate" in value:
                audio_files = self._save_audio(value)
                w = value["waveform"]
                sr = value["sample_rate"]
                b = w.shape[0]
                ch = w.shape[1] if w.dim() > 1 else 1
                samples = w.shape[-1]
                duration = samples / sr
                text = f"[AUDIO]  批次: {b}  采样率: {sr}Hz  通道: {ch}  时长: {duration:.2f}s"
                return {"ui": {"audio": audio_files, "text": [text], "images": []}}

            if "samples" in value:
                s = value["samples"]
                if isinstance(s, torch.Tensor) and s.dim() == 4:
                    b, c, h, w = s.shape
                    text = f"[LATENT]  批次: {b}  尺寸: {w}×{h}  通道: {c}"
                    return {"ui": {"text": [text], "images": [], "audio": []}}

        text = self._format_value(value)
        return {"ui": {"text": [text], "images": [], "audio": []}}

    def _save_images(self, images):
        results = []
        prefix = "ComfyUI_logic_preview" + self.prefix_append
        for batch_number, image in enumerate(images):
            i = 255.0 * image.cpu().numpy()
            img = Image.fromarray(np.clip(i, 0, 255).astype(np.uint8))
            full_output_folder, filename, counter, subfolder, _ = (
                folder_paths.get_save_image_path(
                    prefix, self.output_dir,
                    images[0].shape[1], images[0].shape[0],
                )
            )
            file = f"{filename}_{counter:05}_.png"
            img.save(os.path.join(full_output_folder, file), compress_level=self.compress_level)
            results.append({"filename": file, "subfolder": subfolder, "type": self.type})
        return results

    def _save_audio(self, audio):
        results = []
        prefix = "ComfyUI_logic_audio" + self.prefix_append
        waveform = audio["waveform"]
        sample_rate = audio["sample_rate"]

        for batch_number, wave in enumerate(waveform.cpu()):
            full_output_folder, filename, counter, subfolder, _ = (
                folder_paths.get_save_image_path(prefix, self.output_dir)
            )
            file = f"{filename}_{counter:05}_.flac"
            output_path = os.path.join(full_output_folder, file)

            layout = "mono" if wave.shape[0] == 1 else "stereo"
            buf = BytesIO()
            container = av.open(buf, mode="w", format="flac")
            stream = container.add_stream("flac", rate=sample_rate, layout=layout)
            frame = av.AudioFrame.from_ndarray(
                wave.movedim(0, 1).reshape(1, -1).float().numpy(),
                format="flt",
                layout=layout,
            )
            frame.sample_rate = sample_rate
            frame.pts = 0
            container.mux(stream.encode(frame))
            container.mux(stream.encode(None))
            container.close()

            buf.seek(0)
            with open(output_path, "wb") as f:
                f.write(buf.getbuffer())

            results.append({"filename": file, "subfolder": subfolder, "type": self.type})
        return results

    def _format_value(self, value):
        if value is None:
            return "[NONE]  空值"
        if isinstance(value, bool):
            return f"[BOOLEAN]  {value}"
        if isinstance(value, int):
            return f"[INT]  {value}"
        if isinstance(value, float):
            return f"[FLOAT]  {value}"
        if isinstance(value, str):
            preview = value if len(value) <= 500 else value[:500] + "\n... (已截断)"
            return f"[STRING]  长度: {len(value)}\n{preview}"
        if isinstance(value, (list, tuple)):
            n = len(value)
            if n == 0:
                return "[LIST]  空列表"
            first_type = type(value[0]).__name__
            items = []
            for v in value[:10]:
                s = str(v)
                items.append(s if len(s) <= 50 else s[:50] + "...")
            preview = "\n".join(items)
            if n > 10:
                preview += f"\n... (共 {n} 项)"
            return f"[LIST<{first_type}>]  数量: {n}\n{preview}"
        if isinstance(value, dict):
            try:
                preview = json.dumps(value, ensure_ascii=False, indent=2)
                if len(preview) > 500:
                    preview = preview[:500] + "\n... (已截断)"
            except Exception:
                preview = str(value)[:500]
            return f"[DICT]  键数: {len(value)}\n{preview}"
        type_name = type(value).__name__
        return f"[{type_name.upper()}]  {str(value)[:200]}"


NODE_CLASS_MAPPINGS = {"Logic_UniversalPreview": UniversalPreview}
NODE_DISPLAY_NAME_MAPPINGS = {"Logic_UniversalPreview": "🖥️ 通用预览"}
