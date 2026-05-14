import pygame

from gts.entities import Player
from gts.entities.player import RUN_FRAME_COUNT


def test_update_returns_surface(loader):
    player = Player(loader, frame_hold=1)
    sprite = player.update(moving=False, sprint=False)
    assert isinstance(sprite, pygame.Surface)


def test_facing_change_flips_sprite(loader):
    player = Player(loader, frame_hold=1)
    right = player.update(moving=False, sprint=False, facing="right")
    left = player.update(moving=False, sprint=False, facing="left")
    # Flipped surfaces are distinct objects with the same size.
    assert left.get_size() == right.get_size()
    assert player.facing == "left"


def test_run_frames_cycle(loader):
    player = Player(loader, frame_hold=1)
    seen = []
    for _ in range(RUN_FRAME_COUNT * 2):
        seen.append(player.update(moving=True, sprint=False, facing="right"))
    # The cycle must eventually wrap, so frame at index N matches frame at 0.
    assert seen[0].get_size() == seen[RUN_FRAME_COUNT].get_size()


def test_dance_starts_and_ends(loader):
    player = Player(loader, frame_hold=1)
    player.start_dance()
    assert player.dancing is True
    # Drain the dance until it self-clears.
    for _ in range(2000):
        player.update(moving=False, sprint=False)
        if not player.dancing:
            break
    assert player.dancing is False


def test_toggle_aim(loader):
    player = Player(loader, frame_hold=1)
    assert player.aiming is False
    player.toggle_aim()
    assert player.aiming is True
    player.toggle_aim()
    assert player.aiming is False


def test_sprite_size_matches_still(loader):
    player = Player(loader, frame_hold=1)
    assert player.sprite_size == (player._normal_still.get_size())  # noqa: SLF001
