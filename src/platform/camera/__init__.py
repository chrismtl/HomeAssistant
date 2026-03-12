"""Camera hardware adapters."""

from .base import BaseCamera
from .factory import create_camera
from .types import CameraConfig, CameraDriver, CameraInfo, CameraRole, FrameSize

__all__ = [
    "BaseCamera",
    "CameraConfig",
    "CameraDriver",
    "CameraInfo",
    "CameraRole",
    "FrameSize",
    "create_camera",
]
