"""One full tick of Game._tick while a blade dash is in flight must
translate the active scene by the dash delta and suppress WASD input.
"""

import pygame
import pytest

from gts.game import Game
from gts.inventory.weapons import Blade


class _NoKeys:
    """Stand-in for pygame.key.get_pressed(): every key reads as not held."""

    def __init__(self) -> None:
        self._down: dict[int, bool] = {}

    def set(self, key: int, value: bool) -> None:
        self._down[key] = value

    def __getitem__(self, key: int) -> bool:
        return self._down.get(key, False)


@pytest.fixture(scope="module")
def game():
    g = Game()
    g.inventory.put(2, Blade(g.loader, frame_hold=1))
    g.inventory.selected = 2
    return g


def _prop_positions(scene):
    return [tuple(p.pos) for p in scene.props]


def test_dash_tick_translates_scene_opposite_dash_delta(game, monkeypatch):
    blade = game.inventory.active
    assert isinstance(blade, Blade)

    blade.fire("secondary", direction=(1.0, 0.0))
    player_dx, player_dy = blade.dash_delta()
    assert player_dx > 0

    scene = game.scenes.current
    before = _prop_positions(scene)

    monkeypatch.setattr(pygame.event, "get", lambda: [])
    monkeypatch.setattr(pygame.key, "get_pressed", lambda: _NoKeys())
    monkeypatch.setattr(pygame.mouse, "get_pos", lambda: game.screen.get_size())

    game._tick()

    after = _prop_positions(scene)
    assert len(after) == len(before)
    # World translates opposite to the player's intended motion.
    for (bx, by), (ax, ay) in zip(before, after, strict=True):
        assert ax == pytest.approx(bx - player_dx, abs=1e-6)
        assert ay == pytest.approx(by - player_dy, abs=1e-6)


def test_dash_tick_suppresses_wasd_translation(game, monkeypatch):
    blade = game.inventory.active
    assert isinstance(blade, Blade)
    # Reset any prior dash from the previous test.
    blade._active_mode = None  # noqa: SLF001
    blade.fire("secondary", direction=(1.0, 0.0))
    player_dx, _ = blade.dash_delta()

    scene = game.scenes.current
    before = _prop_positions(scene)

    pressed = _NoKeys()
    pressed.set(pygame.K_d, True)  # would normally translate the world left too
    monkeypatch.setattr(pygame.event, "get", lambda: [])
    monkeypatch.setattr(pygame.key, "get_pressed", lambda: pressed)
    monkeypatch.setattr(pygame.mouse, "get_pos", lambda: game.screen.get_size())

    game._tick()

    after = _prop_positions(scene)
    # WASD is suppressed during a dash, so the world translates by exactly
    # -player_dx, not -player_dx + (-speed) from the D key.
    for (bx, _), (ax, _) in zip(before, after, strict=True):
        assert ax == pytest.approx(bx - player_dx, abs=1e-6)
