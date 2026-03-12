"""IMX477 camera adapter."""

from __future__ import annotations

from .opencv_camera import OpenCVCsiCamera


class Imx477Camera(OpenCVCsiCamera):
    """Jetson CSI adapter for the IMX477 HQ module."""
