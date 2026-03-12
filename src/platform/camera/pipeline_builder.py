"""GStreamer pipeline construction for Jetson CSI cameras."""

from __future__ import annotations

from .types import CameraConfig


class GStreamerPipelineBuilder:
    """Centralizes Jetson camera pipeline generation."""

    @staticmethod
    def build_nvargus_pipeline(config: CameraConfig) -> str:
        frame_size = config.frame_size
        return (
            "nvarguscamerasrc "
            f"sensor-id={config.sensor_id} ! "
            "video/x-raw(memory:NVMM), "
            f"width=(int){frame_size.width}, "
            f"height=(int){frame_size.height}, "
            "format=(string)NV12, "
            f"framerate=(fraction){config.fps}/1 ! "
            f"nvvidconv flip-method={config.flip_method} ! "
            "video/x-raw, format=(string)BGRx ! "
            "videoconvert ! "
            "video/x-raw, format=(string)BGR ! "
            "appsink drop=true sync=false"
        )
