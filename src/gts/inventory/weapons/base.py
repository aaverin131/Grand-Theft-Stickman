"""Weapon base class and a reusable swing-animation variant."""

from __future__ import annotations

import math
from abc import ABC, abstractmethod

import pygame

from ...animation import FrameSequence


class Weapon(ABC):
    """A toolbar-equippable item with an aim sprite and a fire action."""

    name: str
    icon: pygame.Surface
    hold: pygame.Surface
    # Weapons that need aim mode are fired only while the player is aiming;
    # weapons that don't (e.g. melee) receive both mouse buttons directly.
    requires_aim: bool = True

    @abstractmethod
    def fire(
        self,
        mode: str = "primary",
        direction: tuple[float, float] | None = None,
    ) -> None:
        """Start the weapon's use animation.

        `mode` selects between named sequences for weapons that have more
        than one (default sequence is "primary"). `direction` is a vector
        from the player toward the desired target; weapons that translate
        the world during their animation normalize it internally.
        """

    @abstractmethod
    def update(self) -> None:
        """Advance internal animation state by one tick."""

    @abstractmethod
    def aim_sprite(self) -> pygame.Surface:
        """Sprite to display in the player's hand this frame."""

    def dash_delta(self) -> tuple[float, float]:
        """World translation to apply this tick. Zero unless dashing."""
        return (0.0, 0.0)


class AnimatedSwingWeapon(Weapon):
    """Weapon whose fire action plays one of one or two named frame sequences.

    A `secondary` sequence is optional. When present and paired with a
    non-zero `dash_distance`, firing it in secondary mode emits a per-tick
    `dash_delta` whose sum over the animation equals
    ``unit(direction) * dash_distance``.
    """

    def __init__(
        self,
        name: str,
        icon: pygame.Surface,
        hold: pygame.Surface,
        swing: FrameSequence,
        secondary: FrameSequence | None = None,
        dash_distance: float = 0.0,
    ):
        if swing.loop:
            raise ValueError("swing animation must be non-looping")
        if secondary is not None and secondary.loop:
            raise ValueError("secondary animation must be non-looping")
        self.name = name
        self.icon = icon
        self.hold = hold
        self._sequences: dict[str, FrameSequence] = {"primary": swing}
        if secondary is not None:
            self._sequences["secondary"] = secondary
        self._dash_distance = float(dash_distance)
        self._active_mode: str | None = None
        self._dash_unit: tuple[float, float] = (0.0, 0.0)

    @property
    def active_mode(self) -> str | None:
        return self._active_mode

    def fire(
        self,
        mode: str = "primary",
        direction: tuple[float, float] | None = None,
    ) -> None:
        if self._active_mode is not None:
            return
        if mode not in self._sequences:
            return
        self._sequences[mode].reset()
        self._active_mode = mode
        if mode == "secondary" and direction is not None:
            dx, dy = direction
            mag = math.hypot(dx, dy)
            self._dash_unit = (dx / mag, dy / mag) if mag > 0 else (0.0, 0.0)
        else:
            self._dash_unit = (0.0, 0.0)

    def update(self) -> None:
        if self._active_mode is None:
            return
        seq = self._sequences[self._active_mode]
        seq.step()
        if seq.finished:
            self._active_mode = None
            self._dash_unit = (0.0, 0.0)

    def aim_sprite(self) -> pygame.Surface:
        if self._active_mode is None:
            return self.hold
        return self._sequences[self._active_mode].current

    def dash_delta(self) -> tuple[float, float]:
        if self._active_mode != "secondary" or self._dash_distance == 0.0:
            return (0.0, 0.0)
        seq = self._sequences["secondary"]
        total_ticks = len(seq.frames) * seq.frame_hold
        per_tick = self._dash_distance / total_ticks
        return (self._dash_unit[0] * per_tick, self._dash_unit[1] * per_tick)
