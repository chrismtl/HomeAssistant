"""OpenCV-backed CSI camera implementation."""

from __future__ import annotations

from pathlib import Path

from .base import BaseCamera
from .pipeline_builder import GStreamerPipelineBuilder
from .types import CameraFrame, SnapshotResult

try:
    import cv2
except ImportError as exc:  # pragma: no cover - dependency is runtime-specific
    cv2 = None
    _CV2_IMPORT_ERROR = exc
else:
    _CV2_IMPORT_ERROR = None


class OpenCVCsiCamera(BaseCamera):
    """Base CSI implementation for Jetson cameras using OpenCV + GStreamer."""

    def __init__(self, config) -> None:
        super().__init__(config)
        self._capture = None

    def open(self) -> None:
        if cv2 is None:
            raise RuntimeError("OpenCV is required for camera capture.") from _CV2_IMPORT_ERROR

        if self.is_open():
            return

        pipeline = GStreamerPipelineBuilder.build_nvargus_pipeline(self.config)
        capture = cv2.VideoCapture(pipeline, cv2.CAP_GSTREAMER)
        if not capture.isOpened():
            raise RuntimeError(
                f"Failed to open camera '{self.config.effective_name}' on sensor-id {self.config.sensor_id}."
            )

        self._capture = capture

    def close(self) -> None:
        if self._capture is not None:
            self._capture.release()
            self._capture = None

    def is_open(self) -> bool:
        return self._capture is not None and bool(self._capture.isOpened())

    def read_frame(self) -> CameraFrame:
        if not self.is_open():
            raise RuntimeError(f"Camera '{self.config.effective_name}' is not open.")

        success, frame = self._capture.read()
        if not success or frame is None:
            raise RuntimeError(f"Failed to read frame from camera '{self.config.effective_name}'.")

        height, width = frame.shape[:2]
        return CameraFrame(
            sequence_id=self._next_sequence_id(),
            frame=frame,
            width=width,
            height=height,
        )

    def save_snapshot(self, output_path: str) -> SnapshotResult:
        if cv2 is None:
            raise RuntimeError("OpenCV is required for snapshot capture.") from _CV2_IMPORT_ERROR

        frame = self.read_frame()
        snapshot_path = Path(output_path)
        snapshot_path.parent.mkdir(parents=True, exist_ok=True)

        success = cv2.imwrite(str(snapshot_path), frame.frame)
        if not success:
            raise RuntimeError(f"Failed to write snapshot to '{snapshot_path}'.")

        return SnapshotResult(path=snapshot_path, width=frame.width, height=frame.height)
