"""Administrative CLI entrypoint."""

from __future__ import annotations

import argparse

from apps.tools import audio_probe, camera_probe, db_inspect, face_enroll


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Administrative CLI for the Home Assistant device.")
    subparsers = parser.add_subparsers(dest="command", required=True)

    camera_probe.configure_parser(subparsers.add_parser("probe-camera", help="Validate a configured camera."))
    audio_probe.configure_parser(subparsers.add_parser("probe-audio", help="Validate microphone and speaker I/O."))
    db_inspect.configure_parser(subparsers.add_parser("inspect-db", help="Inspect the local database."))
    face_enroll.configure_parser(subparsers.add_parser("enroll-face", help="Enroll a face identity."))

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    handlers = {
        "probe-camera": camera_probe.run,
        "probe-audio": audio_probe.run,
        "inspect-db": db_inspect.run,
        "enroll-face": face_enroll.run,
    }
    return handlers[args.command](args)


if __name__ == "__main__":
    raise SystemExit(main())
