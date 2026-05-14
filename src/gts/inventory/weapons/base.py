"""Weapon base class and a reusable swing-animation variant."""

from __future__ import annotations

from abc import ABC, abstractmethod

import pygame

from ...animation import FrameSequence


class Weapon(ABC):
    """A toolbar-equippable item with an aim sprite and a fire action."""

    name: str
    icon: pygame.Surface
    hold: pygame.Surface

    @abstractmethod
    def fire(self) -> None:
        """Start the weapon's use animation."""

    @abstractmethod
    def update(self) -> None:
        """Advance internal animation state by one tick."""

    @abstractmethod
    def aim_sprite(self) -> pygame.Surface:
        """Sprite to display in the player's hand this frame."""


class AnimatedSwingWeapon(Weapon):
    """Weapon whose fire action plays a one-shot frame sequence."""

    def __init__(self, name: str, icon: pygame.Surface, hold: pygame.Surface, swing: FrameSequence):
        if swing.loop:
            raise ValueError("swing animation must be non-looping")
        self.name = name
        self.icon = icon
        self.hold = hold
        self._swing = swing
        self._firing = False

    def fire(self) -> None:
        self._swing.reset()
        self._firing = True

    def update(self) -> None:
        if not self._firing:
            return
        self._swing.step()
        if self._swing.finished:
            self._firing = False

    def aim_sprite(self) -> pygame.Surface:
        return self._swing.current if self._firing else self.hold
