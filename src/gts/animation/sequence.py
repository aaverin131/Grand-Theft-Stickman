"""Frame-sequence helper for tick-driven sprite animations."""

from __future__ import annotations

import pygame


class FrameSequence:
    """A list of frames advanced one tick at a time.

    Each frame is held for `frame_hold` ticks. When the last frame is reached,
    a looping sequence wraps to the start; a non-looping sequence latches on
    the last frame and sets `finished` to True.
    """

    def __init__(self, frames: list[pygame.Surface], frame_hold: int, loop: bool = True):
        if not frames:
            raise ValueError("FrameSequence requires at least one frame")
        if frame_hold < 1:
            raise ValueError("frame_hold must be >= 1")
        self.frames = frames
        self.frame_hold = frame_hold
        self.loop = loop
        self._index = 0
        self._tick = 0
        self.finished = False

    def reset(self) -> None:
        self._index = 0
        self._tick = 0
        self.finished = False

    def step(self) -> pygame.Surface:
        """Advance one tick and return the current frame."""
        sprite = self.frames[self._index]
        self._tick += 1
        if self._tick >= self.frame_hold:
            self._tick = 0
            self._index += 1
            if self._index >= len(self.frames):
                if self.loop:
                    self._index = 0
                else:
                    self._index = len(self.frames) - 1
                    self.finished = True
        return sprite

    @property
    def current(self) -> pygame.Surface:
        return self.frames[self._index]
