"""Body sprite is suppressed while a melee weapon is mid-animation,
because the swing/dash frames already bake the stickman body in.
"""

import pytest

from gts.game import Game
from gts.inventory.weapons import Blade, Glock, Punch


@pytest.fixture(scope="module")
def game():
    g = Game()
    g.inventory.put(2, Blade(g.loader, frame_hold=1))
    return g


def test_body_drawn_when_no_weapon_active(game):
    game.inventory.selected = 7  # empty slot
    assert game._should_draw_body(game.inventory.active) is True


def test_body_drawn_when_glock_firing(game):
    game.inventory.selected = 1
    glock = game.inventory.active
    assert isinstance(glock, Glock)
    glock.fire()
    assert game._should_draw_body(glock) is True


def test_body_hidden_during_punch_swing(game):
    game.inventory.selected = 0
    punch = game.inventory.active
    assert isinstance(punch, Punch)
    assert game._should_draw_body(punch) is True
    punch.fire()
    assert game._should_draw_body(punch) is False


def test_body_hidden_during_blade_swing(game):
    game.inventory.selected = 2
    blade = game.inventory.active
    assert isinstance(blade, Blade)
    blade._active_mode = None  # noqa: SLF001  reset
    assert game._should_draw_body(blade) is True
    blade.fire("primary")
    assert game._should_draw_body(blade) is False


def test_body_hidden_during_blade_dash(game):
    game.inventory.selected = 2
    blade = game.inventory.active
    blade._active_mode = None  # noqa: SLF001  reset
    blade.fire("secondary", direction=(1.0, 0.0))
    assert game._should_draw_body(blade) is False
