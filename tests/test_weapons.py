import math

import pygame
import pytest

from gts.animation import FrameSequence
from gts.inventory.weapons import Blade, Glock, Punch
from gts.inventory.weapons.base import AnimatedSwingWeapon


def test_animated_swing_rejects_looping_sequence():
    frame = pygame.Surface((1, 1))
    seq = FrameSequence([frame, frame], frame_hold=1, loop=True)
    with pytest.raises(ValueError):
        AnimatedSwingWeapon(name="x", icon=frame, hold=frame, swing=seq)


def test_punch_fire_cycles_and_returns_to_hold(loader):
    punch = Punch(loader, frame_hold=1)
    assert punch.aim_sprite() is punch.hold

    punch.fire()
    swing_sprite = punch.aim_sprite()
    assert swing_sprite is not punch.hold

    seen_during_swing = {id(swing_sprite)}
    for _ in range(64):
        punch.update()
        seen_during_swing.add(id(punch.aim_sprite()))
        if punch.aim_sprite() is punch.hold:
            break
    assert punch.aim_sprite() is punch.hold
    assert len(seen_during_swing) >= 2


def test_glock_fire_shows_flash_for_flash_ticks(loader):
    glock = Glock(loader)
    assert glock.aim_sprite() is glock.hold

    glock.fire()
    for _ in range(Glock.FLASH_TICKS):
        assert glock.aim_sprite() is not glock.hold
        glock.update()
    assert glock.aim_sprite() is glock.hold


def test_punch_and_glock_require_aim(loader):
    assert Punch(loader, frame_hold=1).requires_aim is True
    assert Glock(loader).requires_aim is True


def test_blade_does_not_require_aim(loader):
    assert Blade(loader, frame_hold=1).requires_aim is False


def test_melee_weapons_mark_animation_includes_body(loader):
    assert Punch(loader, frame_hold=1).animation_includes_body is True
    assert Blade(loader, frame_hold=1).animation_includes_body is True


def test_glock_animation_does_not_include_body(loader):
    assert Glock(loader).animation_includes_body is False


def test_is_animating_reflects_active_mode(loader):
    blade = Blade(loader, frame_hold=1)
    assert blade.is_animating() is False
    blade.fire("primary")
    assert blade.is_animating() is True
    for _ in range(256):
        blade.update()
        if not blade.is_animating():
            break
    assert blade.is_animating() is False


def test_glock_is_not_animating(loader):
    glock = Glock(loader)
    glock.fire()
    assert glock.is_animating() is False


def test_blade_primary_completes_and_returns_to_hold(loader):
    blade = Blade(loader, frame_hold=1)
    blade.fire("primary")
    assert blade.active_mode == "primary"
    assert blade.aim_sprite() is not blade.hold

    for _ in range(128):
        blade.update()
        if blade.active_mode is None:
            break
    assert blade.active_mode is None
    assert blade.aim_sprite() is blade.hold


def test_blade_default_fire_is_primary(loader):
    blade = Blade(loader, frame_hold=1)
    blade.fire()
    assert blade.active_mode == "primary"


def test_blade_secondary_completes_and_returns_to_hold(loader):
    blade = Blade(loader, frame_hold=1)
    blade.fire("secondary", direction=(1.0, 0.0))
    assert blade.active_mode == "secondary"
    assert blade.aim_sprite() is not blade.hold

    for _ in range(128):
        blade.update()
        if blade.active_mode is None:
            break
    assert blade.active_mode is None
    assert blade.aim_sprite() is blade.hold


def test_blade_dash_delta_zero_when_idle(loader):
    blade = Blade(loader, frame_hold=1)
    assert blade.dash_delta() == (0.0, 0.0)


def test_blade_dash_delta_zero_during_primary_swing(loader):
    blade = Blade(loader, frame_hold=1)
    blade.fire("primary")
    assert blade.dash_delta() == (0.0, 0.0)


def test_blade_dash_delta_sums_to_configured_distance(loader):
    blade = Blade(loader, frame_hold=1)
    direction = (3.0, 4.0)  # non-unit; weapon should normalize
    blade.fire("secondary", direction=direction)

    total_x = 0.0
    total_y = 0.0
    safety = 256
    while blade.active_mode == "secondary" and safety > 0:
        dx, dy = blade.dash_delta()
        total_x += dx
        total_y += dy
        blade.update()
        safety -= 1

    distance = Blade.DASH_DISTANCE
    # Normalized direction (3, 4) -> (0.6, 0.8). Sum of per-tick deltas
    # over the whole dash should equal direction * distance.
    assert math.isclose(total_x, 0.6 * distance, rel_tol=1e-6, abs_tol=1e-6)
    assert math.isclose(total_y, 0.8 * distance, rel_tol=1e-6, abs_tol=1e-6)


def test_blade_fire_during_primary_swing_is_ignored(loader):
    blade = Blade(loader, frame_hold=1)
    blade.fire("primary")
    blade.update()  # advance one tick into the swing
    primary_sprite = blade.aim_sprite()

    blade.fire("primary")
    blade.fire("secondary", direction=(1.0, 0.0))

    assert blade.active_mode == "primary"
    # Sprite is still mid-primary, not restarted to frame 0 of any sequence.
    assert blade.aim_sprite() is primary_sprite


def test_blade_fire_during_dash_is_ignored(loader):
    blade = Blade(loader, frame_hold=1)
    blade.fire("secondary", direction=(1.0, 0.0))
    blade.update()

    blade.fire("primary")
    blade.fire("secondary", direction=(0.0, 1.0))

    assert blade.active_mode == "secondary"
    # Direction was not overwritten by the second secondary fire.
    dx, dy = blade.dash_delta()
    assert dx > 0
    assert dy == 0
