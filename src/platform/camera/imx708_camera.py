"""IMX708 camera adapter."""

from __future__ import annotations

from .opencv_camera import OpenCVCsiCamera


class Imx708Camera(OpenCVCsiCamera):
    """Jetson CSI adapter for the IMX708 wide-angle module."""
