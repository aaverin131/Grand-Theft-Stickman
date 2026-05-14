from __future__ import annotations

import pygame

from ...assets import AssetLoader
from .base import Weapon


class Glock(Weapon):
    """Pistol that swaps to a muzzle-flash sprite for a few ticks per shot."""

    FLASH_TICKS = 6

    def __init__(self, loader: AssetLoader):
        self.name = "glock"
        self.icon = loader.image("gui/glock.png")
        self.hold = loader.image("stickman/weapon/glock/glockhold.png")
        self._flash = loader.image("stickman/weapon/glock/glockfire.png")
        self._flash_left = 0

    def fire(
        self,
        mode: str = "primary",
        direction: tuple[float, float] | None = None,
    ) -> None:
        self._flash_left = self.FLASH_TICKS

    def update(self) -> None:
        if self._flash_left > 0:
            self._flash_left -= 1

    def aim_sprite(self) -> pygame.Surface:
        return self._flash if self._flash_left > 0 else self.hold
