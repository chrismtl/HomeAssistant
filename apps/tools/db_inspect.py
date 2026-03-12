"""Standalone database inspection tool."""

from __future__ import annotations

import argparse


def configure_parser(parser: argparse.ArgumentParser) -> None:
    parser.set_defaults(command="inspect-db")


def run(args: argparse.Namespace) -> int:
    raise NotImplementedError("Database inspection is not implemented yet.")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Inspect the local database.")
    configure_parser(parser)
    args = parser.parse_args(argv)
    return run(args)


if __name__ == "__main__":
    raise SystemExit(main())
