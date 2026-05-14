import pygame
import pytest

from gts import config
from gts.assets import AssetLoader


def test_image_returns_surface(loader):
    surface = loader.image("icon.png")
    assert isinstance(surface, pygame.Surface)


def test_image_is_cached(loader):
    a = loader.image("icon.png")
    b = loader.image("icon.png")
    assert a is b


def test_image_dir_is_cached(loader):
    a = loader.image_dir("stickman")
    b = loader.image_dir("stickman")
    assert a is b
    assert all(isinstance(s, pygame.Surface) for s in a.values())


def test_frames_natural_order_with_prefix(loader):
    frames = loader.frames(
        "stickman/weapon/blade/blade animation 1", prefix="pixil-frame-"
    )
    assert len(frames) > 10
    # If lexicographic order leaked through, frame "10" would come before "2".
    names = sorted(
        loader.image_dir("stickman/weapon/blade/blade animation 1").keys(),
        key=lambda n: int(n.rsplit("-", 1)[1]),
    )
    expected = [
        loader.image_dir("stickman/weapon/blade/blade animation 1")[n] for n in names
    ]
    assert frames == expected


def test_unknown_image_raises():
    fresh = AssetLoader(config.ASSET_DIR)
    with pytest.raises((FileNotFoundError, pygame.error)):
        fresh.image("does/not/exist.png")
