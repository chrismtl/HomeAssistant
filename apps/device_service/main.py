"""Runtime entrypoint for the full device service."""

from __future__ import annotations

import argparse


def build_parser() -> argparse.ArgumentParser:
    return argparse.ArgumentParser(description="Run the Home Assistant device service.")


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    parser.parse_args(argv)
    raise NotImplementedError("Device service composition is not implemented yet.")


if __name__ == "__main__":
    raise SystemExit(main())
