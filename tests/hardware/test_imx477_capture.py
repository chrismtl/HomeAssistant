from pathlib import Path

import pytest

from src.platform.camera.config_loader import load_camera_configs
from src.platform.camera.factory import create_camera


CONFIG_PATH = Path("config/base/cameras.yaml")


@pytest.mark.hardware
def test_imx477_capture_receives_frame():
    configs = load_camera_configs(CONFIG_PATH)
    camera = create_camera(configs["hq_front"])

    with camera:
        frame = camera.read_frame()

    assert frame.width > 0
    assert frame.height > 0
