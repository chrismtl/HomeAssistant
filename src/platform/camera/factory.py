"""Camera instantiation from typed configuration."""

from __future__ import annotations

from .base import BaseCamera
from .imx477_camera import Imx477Camera
from .imx708_camera import Imx708Camera
from .types import CameraConfig, CameraDriver


def create_camera(config: CameraConfig) -> BaseCamera:
    if config.driver is CameraDriver.IMX708:
        return Imx708Camera(config)
    if config.driver is CameraDriver.IMX477:
        return Imx477Camera(config)

    raise ValueError(f"Unsupported camera driver: {config.driver}")
