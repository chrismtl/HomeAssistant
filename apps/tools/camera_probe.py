"""Standalone camera validation tool."""

from __future__ import annotations

import argparse
from pathlib import Path

from src.platform.camera.config_loader import load_camera_configs
from src.platform.camera.factory import create_camera


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Probe a configured Jetson camera.")
    parser.add_argument("--config", default="config/base/cameras.yaml", help="Path to the camera YAML config.")
    parser.add_argument("--camera", required=True, help="Camera key from the YAML config.")
    parser.add_argument(
        "--frames",
        type=int,
        default=30,
        help="Number of frames to read before exiting.",
    )
    parser.add_argument(
        "--snapshot",
        default=None,
        help="Optional output path for a captured snapshot.",
    )
    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()

    configs = load_camera_configs(args.config)
    if args.camera not in configs:
        available = ", ".join(sorted(configs))
        raise SystemExit(f"Unknown camera '{args.camera}'. Available cameras: {available}")

    camera_config = configs[args.camera]
    if not camera_config.enabled:
        raise SystemExit(f"Camera '{args.camera}' is disabled in config.")

    camera = create_camera(camera_config)
    print(
        f"Opening camera '{camera.info.name}' "
        f"(driver={camera.info.driver.value}, sensor_id={camera.info.sensor_id}, "
        f"resolution={camera.info.frame_size.width}x{camera.info.frame_size.height}, fps={camera.info.fps})"
    )

    with camera:
        last_frame = None
        for _ in range(args.frames):
            last_frame = camera.read_frame()

        if args.snapshot is not None:
            snapshot = camera.save_snapshot(args.snapshot)
            print(
                f"Snapshot saved to {snapshot.path} "
                f"({snapshot.width}x{snapshot.height})"
            )

    if last_frame is None:
        raise SystemExit("No frames were captured.")

    print(
        f"Read {args.frames} frames successfully from '{args.camera}'. "
        f"Last frame size: {last_frame.width}x{last_frame.height}"
    )


if __name__ == "__main__":
    main()
