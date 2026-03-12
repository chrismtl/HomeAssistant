"""Abstract camera contract for Jetson camera adapters."""

from __future__ import annotations

from abc import ABC, abstractmethod

from .types import CameraConfig, CameraFrame, CameraInfo, SnapshotResult


class BaseCamera(ABC):
    """Hardware camera abstraction consumed by higher-level services."""

    def __init__(self, config: CameraConfig) -> None:
        self._config = config
        self._sequence_id = 0

    @property
    def config(self) -> CameraConfig:
        return self._config

    @property
    def info(self) -> CameraInfo:
        return CameraInfo(
            name=self._config.effective_name,
            driver=self._config.driver,
            role=self._config.role,
            sensor_id=self._config.sensor_id,
            frame_size=self._config.frame_size,
            fps=self._config.fps,
        )

    @abstractmethod
    def open(self) -> None:
        """Open the underlying camera stream."""

    @abstractmethod
    def close(self) -> None:
        """Close the underlying camera stream."""

    @abstractmethod
    def is_open(self) -> bool:
        """Return whether the camera stream is open."""

    @abstractmethod
    def read_frame(self) -> CameraFrame:
        """Read the next frame from the stream."""

    @abstractmethod
    def save_snapshot(self, output_path: str) -> SnapshotResult:
        """Capture and persist a single frame."""

    def _next_sequence_id(self) -> int:
        sequence_id = self._sequence_id
        self._sequence_id += 1
        return sequence_id

    def __enter__(self) -> "BaseCamera":
        self.open()
        return self

    def __exit__(self, exc_type, exc, exc_tb) -> None:
        self.close()
