"""Typed camera models shared across the camera platform layer."""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path
from typing import Any


class CameraDriver(str, Enum):
    IMX708 = "imx708"
    IMX477 = "imx477"


class CameraRole(str, Enum):
    SCENE_MONITOR = "scene_monitor"
    IDENTITY_FOCUS = "identity_focus"
    GENERIC = "generic"


@dataclass(slots=True, frozen=True)
class FrameSize:
    width: int
    height: int


@dataclass(slots=True, frozen=True)
class CameraConfig:
    name: str
    driver: CameraDriver
    role: CameraRole
    sensor_id: int = 0
    enabled: bool = True
    frame_size: FrameSize = field(default_factory=lambda: FrameSize(width=1280, height=720))
    fps: int = 30
    flip_method: int = 0
    display_name: str | None = None

    @property
    def effective_name(self) -> str:
        return self.display_name or self.name


@dataclass(slots=True, frozen=True)
class CameraInfo:
    name: str
    driver: CameraDriver
    role: CameraRole
    sensor_id: int
    frame_size: FrameSize
    fps: int


@dataclass(slots=True)
class CameraFrame:
    sequence_id: int
    frame: Any
    width: int
    height: int


@dataclass(slots=True, frozen=True)
class SnapshotResult:
    path: Path
    width: int
    height: int
