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
    # Walk the swing far enough to guarantee completion regardless of frame count.
    for _ in range(64):
        punch.update()
        seen_during_swing.add(id(punch.aim_sprite()))
        if punch.aim_sprite() is punch.hold:
            break
    assert punch.aim_sprite() is punch.hold
    # At least two distinct sprites observed (multiple swing frames + hold).
    assert len(seen_during_swing) >= 2


def test_glock_fire_shows_flash_for_flash_ticks(loader):
    glock = Glock(loader)
    assert glock.aim_sprite() is glock.hold

    glock.fire()
    for _ in range(Glock.FLASH_TICKS):
        assert glock.aim_sprite() is not glock.hold
        glock.update()
    assert glock.aim_sprite() is glock.hold


def test_blade_fire_completes_full_sequence(loader):
    blade = Blade(loader, frame_hold=1)
    blade.fire()
    for _ in range(64):
        blade.update()
        if blade.aim_sprite() is blade.hold:
            break
    assert blade.aim_sprite() is blade.hold
