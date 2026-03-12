import os

import pytest


def pytest_collection_modifyitems(config, items):
    if os.getenv("RUN_HARDWARE_TESTS") == "1":
        return

    skip_marker = pytest.mark.skip(reason="Set RUN_HARDWARE_TESTS=1 to execute hardware tests.")
    for item in items:
        item.add_marker(skip_marker)
