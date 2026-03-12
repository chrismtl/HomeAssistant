"""Repository root entrypoint for the Home Assistant device project."""

from __future__ import annotations

import sys

from apps.cli.main import main as cli_main
from apps.device_service.main import main as device_service_main


def main(argv: list[str] | None = None) -> int:
    args = list(sys.argv[1:] if argv is None else argv)
    if args and args[0] == "run-device":
        return device_service_main(args[1:])
    return cli_main(args)


if __name__ == "__main__":
    raise SystemExit(main())
