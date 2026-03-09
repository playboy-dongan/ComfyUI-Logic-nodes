from fractions import Fraction

import torch

from .blocker import AlwaysEqualProxy

any_type = AlwaysEqualProxy("*")


class VideoCompose:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "图像": ("IMAGE",),
                "帧率": ("FLOAT", {"default": 24.0, "min": 1.0, "max": 120.0, "step": 0.01}),
            },
            "optional": {
                "音频": (any_type, {}),
            },
        }

    RETURN_TYPES = ("VIDEO",)
    RETURN_NAMES = ("视频",)
    FUNCTION = "execute"
    OUTPUT_NODE = True
    CATEGORY = "⚡ 逻辑/🎬 视频"

    @classmethod
    def IS_CHANGED(cls, **kwargs):
        return float("NaN")

    def execute(self, 图像, 帧率, 音频=None):
        from comfy_api.latest._util.video_types import VideoComponents
        from comfy_api.input_impl import VideoFromComponents

        frame_rate = Fraction(帧率).limit_denominator(10000)

        audio_dict = None
        if 音频 is not None:
            if isinstance(音频, dict) and "waveform" in 音频 and "sample_rate" in 音频:
                audio_dict = 音频

        components = VideoComponents(
            images=图像,
            audio=audio_dict,
            frame_rate=frame_rate,
        )
        video = VideoFromComponents(components)

        num_frames = 图像.shape[0]
        h, w = 图像.shape[1], 图像.shape[2]
        duration = num_frames / float(frame_rate) if frame_rate > 0 else 0.0

        return {
            "ui": {
                "resolution": [f"{w}×{h}"],
                "duration": [f"{duration:.2f}"],
                "fps": [f"{float(frame_rate):.2f}"],
                "frames": [str(num_frames)],
                "has_audio": [str(audio_dict is not None)],
            },
            "result": (video,),
        }


NODE_CLASS_MAPPINGS = {"Logic_VideoCompose": VideoCompose}
NODE_DISPLAY_NAME_MAPPINGS = {"Logic_VideoCompose": "🎞️ 合成视频"}
