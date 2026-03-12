"""Standalone face enrollment tool."""

from __future__ import annotations

import argparse


def configure_parser(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--person-id", required=True, help="Logical person identifier to enroll.")
    parser.add_argument("--name", required=False, help="Optional display name for the person.")


def run(args: argparse.Namespace) -> int:
    raise NotImplementedError("Face enrollment is not implemented yet.")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Enroll a face identity.")
    configure_parser(parser)
    args = parser.parse_args(argv)
    return run(args)


if __name__ == "__main__":
    raise SystemExit(main())
