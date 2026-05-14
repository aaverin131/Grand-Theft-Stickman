"""Player entity: sprite, facing, run and dance animation state."""

from __future__ import annotations

from typing import Literal

import pygame

from .. import config
from ..assets import AssetLoader

Facing = Literal["left", "right"]

# Original animation cycled through only the first 3 run frames.
RUN_FRAME_COUNT = 3


class Player:
    """Holds the player's sprite sets, animation timers, and facing."""

    def __init__(self, loader: AssetLoader, *, frame_hold: int = config.ANIMATION_FRAME_HOLD):
        self._normal_run = loader.frames("stickman", prefix="stickman_run")
        self._weapon_run = loader.frames("stickman/weapon", prefix="stickman_weapon_run")
        self._normal_still = loader.image("stickman", "stickman_still2.png")
        self._weapon_still = loader.image("stickman/weapon", "stickman_weapon_still.png")
        self._dance_frames = loader.frames("stickman/fortnite dance", prefix="stickman_dance")

        self.world_pos: list[int] = list(config.INITIAL_PLAYER_POS)
        self.facing: Facing = "right"
        self.aiming: bool = False
        self.dancing: bool = False

        self._frame_hold = frame_hold
        self._run_frame = 0
        self._run_tick = 0
        self._dance_frame = 0
        self._dance_tick = 0

    # --- aim mode -------------------------------------------------------------
    def toggle_aim(self) -> None:
        self.aiming = not self.aiming

    # --- dance ----------------------------------------------------------------
    def start_dance(self) -> None:
        self.dancing = True
        self._dance_frame = 0
        self._dance_tick = 0

    # --- per-tick update ------------------------------------------------------
    def update(self, *, moving: bool, sprint: bool, facing: Facing | None = None) -> pygame.Surface:
        """Advance animation state by one tick and return the sprite to blit.

        `facing` is set when the player moves horizontally; vertical-only motion
        preserves the previous facing.
        """
        if facing is not None:
            self.facing = facing

        if self.dancing:
            return self._advance_dance()
        return self._advance_run(moving=moving, sprint=sprint)

    def _advance_run(self, *, moving: bool, sprint: bool) -> pygame.Surface:
        if not moving:
            sprite = self._weapon_still if self.aiming else self._normal_still
        else:
            hold = max(1, self._frame_hold // 2) if sprint else self._frame_hold
            self._run_tick += 1
            if self._run_tick >= hold:
                self._run_tick = 0
                self._run_frame = (self._run_frame + 1) % RUN_FRAME_COUNT
            frames = self._weapon_run if self.aiming else self._normal_run
            sprite = frames[self._run_frame]

        if self.facing == "left":
            sprite = pygame.transform.flip(sprite, True, False)
        return sprite

    def _advance_dance(self) -> pygame.Surface:
        sprite = self._dance_frames[self._dance_frame]
        self._dance_tick += 1
        if self._dance_tick >= self._frame_hold:
            self._dance_tick = 0
            self._dance_frame += 1
        if self._dance_frame >= len(self._dance_frames):
            self.dancing = False
            self._dance_frame = 0
        return sprite

    # --- sprite size ----------------------------------------------------------
    @property
    def sprite_size(self) -> tuple[int, int]:
        return self._normal_still.get_size()
