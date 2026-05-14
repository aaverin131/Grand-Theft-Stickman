"""Mouse-button dispatch when the active weapon is the blade.

Blade attacks without aim mode: LMB plays the swing, RMB plays the dash
and translates the world in the direction of the cursor. Non-blade
weapons keep their aim-toggle behavior.
"""

import math

import pygame
import pytest

from gts.game import Game
from gts.inventory.weapons import Blade


@pytest.fixture(scope="module")
def game():
    g = Game()
    g.inventory.put(2, Blade(g.loader, frame_hold=1))
    return g


@pytest.fixture(autouse=True)
def reset_state(game):
    game.player.aiming = False
    game.inventory.selected = 0
    for slot in range(game.inventory.size):
        weapon = game.inventory.slot(slot)
        if isinstance(weapon, Blade):
            weapon._active_mode = None  # noqa: SLF001
            weapon._dash_unit = (0.0, 0.0)  # noqa: SLF001


def _mouse(button: int, pos: tuple[int, int]) -> pygame.event.Event:
    return pygame.event.Event(pygame.MOUSEBUTTONDOWN, {"button": button, "pos": pos})


def test_blade_left_click_starts_primary_swing(game):
    game.inventory.selected = 2
    screen_size = game.screen.get_size()
    cx, cy = screen_size[0] / 2, screen_size[1] / 2

    game._on_mouse_down(_mouse(1, (int(cx + 100), int(cy))), screen_size)

    blade = game.inventory.active
    assert isinstance(blade, Blade)
    assert blade.active_mode == "primary"
    assert game.player.aiming is False


def test_blade_right_click_starts_dash_in_mouse_direction(game):
    game.inventory.selected = 2
    screen_size = game.screen.get_size()
    cx, cy = screen_size[0] / 2, screen_size[1] / 2

    game._on_mouse_down(_mouse(3, (int(cx + 30), int(cy + 40))), screen_size)

    blade = game.inventory.active
    assert isinstance(blade, Blade)
    assert blade.active_mode == "secondary"
    assert game.player.aiming is False

    dx, dy = blade.dash_delta()
    # Direction (30, 40) normalizes to (0.6, 0.8); per-tick deltas
    # have the same sign and proportion as the direction.
    assert dx > 0
    assert dy > 0
    assert math.isclose(dy / dx, 40 / 30, rel_tol=1e-6)


def test_glock_right_click_still_toggles_aim(game):
    game.inventory.selected = 1  # glock
    screen_size = game.screen.get_size()

    game._on_mouse_down(_mouse(3, (10, 10)), screen_size)
    assert game.player.aiming is True

    game._on_mouse_down(_mouse(3, (10, 10)), screen_size)
    assert game.player.aiming is False


def test_blade_re_click_during_swing_is_ignored(game):
    game.inventory.selected = 2
    screen_size = game.screen.get_size()

    game._on_mouse_down(_mouse(1, (10, 10)), screen_size)
    blade = game.inventory.active
    blade.update()
    sprite_mid_swing = blade.aim_sprite()

    game._on_mouse_down(_mouse(1, (10, 10)), screen_size)
    game._on_mouse_down(_mouse(3, (200, 200)), screen_size)

    assert blade.active_mode == "primary"
    assert blade.aim_sprite() is sprite_mid_swing
