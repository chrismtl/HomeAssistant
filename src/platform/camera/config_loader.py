"""Camera configuration loading from YAML."""

from __future__ import annotations

from pathlib import Path

from .types import CameraConfig, CameraDriver, CameraRole, FrameSize

try:
    import yaml
except ImportError as exc:  # pragma: no cover - dependency is runtime-specific
    yaml = None
    _YAML_IMPORT_ERROR = exc
else:
    _YAML_IMPORT_ERROR = None


def load_camera_configs(config_path: str | Path) -> dict[str, CameraConfig]:
    if yaml is None:
        raise RuntimeError("PyYAML is required to load camera configuration.") from _YAML_IMPORT_ERROR

    config_file = Path(config_path)
    raw_data = yaml.safe_load(config_file.read_text(encoding="utf-8")) or {}
    raw_cameras = raw_data.get("cameras", {})

    configs: dict[str, CameraConfig] = {}
    for name, values in raw_cameras.items():
        driver = CameraDriver(values["driver"])
        role = CameraRole(values.get("role", CameraRole.GENERIC.value))
        resolution = values.get("resolution", {})
        frame_size = FrameSize(
            width=int(resolution.get("width", 1280)),
            height=int(resolution.get("height", 720)),
        )
        configs[name] = CameraConfig(
            name=name,
            display_name=values.get("display_name"),
            driver=driver,
            role=role,
            sensor_id=int(values.get("sensor_id", 0)),
            enabled=bool(values.get("enabled", True)),
            frame_size=frame_size,
            fps=int(values.get("fps", 30)),
            flip_method=int(values.get("flip_method", 0)),
        )

    return configs
