import os
import torch
import numpy as np

from .blocker import AlwaysEqualProxy

any_type = AlwaysEqualProxy("*")

SILENT_AUDIO = {"waveform": torch.zeros((1, 1, 1), dtype=torch.float32), "sample_rate": 44100}


def _decompose_via_av(source, max_frames, step):
    """
    Stream-decode with PyAV: multi-threaded decoding, single-pass
    video+audio extraction, pre-allocated output tensor.
    """
    import av

    limit = max_frames if max_frames > 0 else float("inf")

    with av.open(source, mode="r") as container:
        video_stream = next((s for s in container.streams if s.type == "video"), None)
        if video_stream is None:
            raise RuntimeError("视频中未找到视频流")

        video_stream.thread_type = "AUTO"

        fps = float(video_stream.average_rate) if video_stream.average_rate else 24.0
        w, h = video_stream.width, video_stream.height

        raw_frames = video_stream.frames or 0
        if raw_frames and fps > 0:
            duration = raw_frames / fps
        elif container.duration is not None:
            duration = float(container.duration / av.time_base)
        else:
            duration = 0.0

        audio_stream = next((s for s in container.streams if s.type == "audio"), None)
        has_audio = audio_stream is not None

        if raw_frames > 0 and limit != float("inf"):
            expected = min(int(np.ceil(raw_frames / step)), int(limit))
        elif raw_frames > 0:
            expected = int(np.ceil(raw_frames / step))
        else:
            expected = 0

        if expected > 0:
            images = torch.empty((expected, h, w, 3), dtype=torch.float32)
        else:
            images = None

        decode_streams = [video_stream]
        if audio_stream is not None:
            audio_stream.thread_type = "AUTO"
            decode_streams.append(audio_stream)

        frame_idx = 0
        written = 0
        frame_list = [] if images is None else None
        audio_chunks = []
        audio_sr = 44100

        for packet in container.demux(decode_streams):
            for frame in packet.decode():
                if isinstance(frame, av.VideoFrame):
                    if written >= limit:
                        continue
                    if frame_idx % step == 0:
                        arr = frame.to_ndarray(format="rgb24")
                        t = torch.from_numpy(arr).float().div_(255.0)
                        if images is not None and written < images.shape[0]:
                            images[written] = t
                        elif frame_list is not None:
                            frame_list.append(t)
                        else:
                            frame_list = [t]
                        written += 1
                    frame_idx += 1
                elif isinstance(frame, av.AudioFrame):
                    audio_chunks.append(frame.to_ndarray())
                    audio_sr = frame.sample_rate or audio_sr

        if images is not None:
            if written < images.shape[0]:
                images = images[:written]
        elif frame_list:
            images = torch.stack(frame_list)
        else:
            images = torch.zeros((1, max(h, 1), max(w, 1), 3), dtype=torch.float32)

        if written == 0:
            images = torch.zeros((1, max(h, 1), max(w, 1), 3), dtype=torch.float32)

    audio = SILENT_AUDIO
    if audio_chunks:
        try:
            audio_data = np.concatenate(audio_chunks, axis=1)
            waveform = torch.from_numpy(audio_data.copy()).unsqueeze(0)
            audio = {"waveform": waveform, "sample_rate": audio_sr}
            has_audio = True
        except Exception:
            pass

    return images, audio, duration, fps, images.shape[0], w, h, has_audio


def _decompose_via_cv2(path, max_frames, step):
    """Fallback when PyAV is not available: use OpenCV (no audio)."""
    import cv2

    cap = cv2.VideoCapture(path)
    if not cap.isOpened():
        raise RuntimeError(f"无法打开视频: {path}")

    fps = cap.get(cv2.CAP_PROP_FPS) or 24.0
    total = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    w = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    h = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    duration = total / fps if fps > 0 else 0.0

    limit = max_frames if max_frames > 0 else total
    expected = min(int(np.ceil(total / step)), limit) if total > 0 else 0

    if expected > 0:
        images = np.empty((expected, h, w, 3), dtype=np.float32)
    else:
        images = None

    written = 0
    frame_list = [] if images is None else None
    idx = 0
    while written < limit:
        if idx % step != 0:
            if not cap.grab():
                break
            idx += 1
            continue
        ret, frame = cap.read()
        if not ret:
            break
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB).astype(np.float32) / 255.0
        if images is not None and written < images.shape[0]:
            images[written] = rgb
        elif frame_list is not None:
            frame_list.append(rgb)
        else:
            frame_list = [rgb]
        written += 1
        idx += 1
    cap.release()

    if images is not None:
        if written < images.shape[0]:
            images = images[:written]
        images = torch.from_numpy(images)
    elif frame_list:
        images = torch.from_numpy(np.stack(frame_list))
    else:
        images = torch.zeros((1, max(h, 1), max(w, 1), 3), dtype=torch.float32)

    return images, SILENT_AUDIO, duration, fps, images.shape[0], w, h, False


def _resolve_input(video_input):
    try:
        from comfy_api.input.video_types import VideoInput
        if isinstance(video_input, VideoInput):
            return "api", video_input
    except ImportError:
        pass

    if isinstance(video_input, str) and os.path.isfile(video_input):
        return "path", video_input

    if isinstance(video_input, dict):
        for key in ("path", "file", "video_path", "filename"):
            if key in video_input and isinstance(video_input[key], str):
                p = video_input[key]
                if os.path.isfile(p):
                    return "path", p

    raise ValueError(
        f"不支持的视频输入类型: {type(video_input).__name__}。"
        "请传入视频文件路径(STRING)或 ComfyUI VideoInput 对象。"
    )


class VideoDecompose:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "视频": (any_type, {}),
            },
            "optional": {
                "最大帧数": ("INT", {"default": 0, "min": 0, "max": 99999, "step": 1,
                             "tooltip": "0 = 不限制，提取所有帧"}),
                "跳帧间隔": ("INT", {"default": 1, "min": 1, "max": 100, "step": 1,
                             "tooltip": "每隔 N 帧取一帧，1 = 逐帧"}),
            },
        }

    RETURN_TYPES = ("IMAGE", "AUDIO", "FLOAT", "FLOAT", "INT", "INT", "INT")
    RETURN_NAMES = ("图像", "音频", "时长", "帧率", "总帧数", "宽度", "高度")
    FUNCTION = "execute"
    OUTPUT_NODE = True
    CATEGORY = "⚡ 逻辑/🎬 视频"

    @classmethod
    def IS_CHANGED(cls, **kwargs):
        return float("NaN")

    def execute(self, 视频, 最大帧数=0, 跳帧间隔=1):
        step = max(1, 跳帧间隔)
        kind, source = _resolve_input(视频)

        if kind == "api":
            stream = source.get_stream_source()
            images, audio, duration, fps, count, w, h, has_audio = \
                _decompose_via_av(stream, 最大帧数, step)
        else:
            try:
                import av  # noqa: F401
                images, audio, duration, fps, count, w, h, has_audio = \
                    _decompose_via_av(source, 最大帧数, step)
            except ImportError:
                images, audio, duration, fps, count, w, h, has_audio = \
                    _decompose_via_cv2(source, 最大帧数, step)

        return {
            "ui": {
                "resolution": [f"{w}×{h}"],
                "duration": [f"{duration:.2f}"],
                "fps": [f"{fps:.2f}"],
                "frames": [str(count)],
                "has_audio": [str(has_audio)],
            },
            "result": (images, audio, duration, fps, count, w, h),
        }


NODE_CLASS_MAPPINGS = {"Logic_VideoDecompose": VideoDecompose}
NODE_DISPLAY_NAME_MAPPINGS = {"Logic_VideoDecompose": "✂️ 分解视频"}
