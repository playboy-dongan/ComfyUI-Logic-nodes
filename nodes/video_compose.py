from fractions import Fraction

import torch

from .blocker import AlwaysEqualProxy

any_type = AlwaysEqualProxy("*")

_FPS_CACHE = {}
_CACHE_MAX = 32


def _fps_to_fraction(fps):
    """Cache Fraction for common fps values to avoid repeated limit_denominator."""
    k = round(fps, 2)
    if k not in _FPS_CACHE:
        if len(_FPS_CACHE) >= _CACHE_MAX:
            _FPS_CACHE.clear()
        _FPS_CACHE[k] = Fraction(fps).limit_denominator(10000)
    return _FPS_CACHE[k]


class VideoCompose:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "images": ("IMAGE",),
                "fps": ("FLOAT", {"default": 24.0, "min": 1.0, "max": 120.0, "step": 0.01}),
            },
            "optional": {
                "audio": (any_type, {}),
            },
        }

    RETURN_TYPES = ("VIDEO",)
    RETURN_NAMES = ("video",)
    FUNCTION = "execute"
    OUTPUT_NODE = True
    CATEGORY = "⚡ Logic/🎬 Video"

    @classmethod
    def IS_CHANGED(cls, **kwargs):
        return float("NaN")

    def execute(self, images, fps, audio=None):
        from comfy_api.latest._util.video_types import VideoComponents
        from comfy_api.input_impl import VideoFromComponents

        frame_rate = _fps_to_fraction(fps)

        audio_dict = None
        if audio is not None:
            if isinstance(audio, dict) and "waveform" in audio and "sample_rate" in audio:
                audio_dict = audio

        components = VideoComponents(
            images=images,
            audio=audio_dict,
            frame_rate=frame_rate,
        )
        video = VideoFromComponents(components)

        num_frames = images.shape[0]
        h, w = images.shape[1], images.shape[2]
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
NODE_DISPLAY_NAME_MAPPINGS = {"Logic_VideoCompose": "🎞️ Compose Video"}
