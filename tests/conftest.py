import os

os.environ.setdefault("SDL_VIDEODRIVER", "dummy")
os.environ.setdefault("SDL_AUDIODRIVER", "dummy")

import pygame  # noqa: E402
import pytest  # noqa: E402

from gts import config  # noqa: E402
from gts.assets import AssetLoader  # noqa: E402


@pytest.fixture(scope="session", autouse=True)
def _pygame_display():
    pygame.display.init()
    pygame.display.set_mode((1, 1))
    yield
    pygame.display.quit()


@pytest.fixture(scope="session")
def loader():
    return AssetLoader(config.ASSET_DIR)
