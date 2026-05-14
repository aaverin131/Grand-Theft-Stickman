"""Save-list overlay state machine."""

from __future__ import annotations

import pygame

from .hud import HUD

ScreenSize = tuple[int, int]
Size = tuple[int, int]


class SaveMenu:
    def __init__(self) -> None:
        self._open = False

    @property
    def is_open(self) -> bool:
        return self._open

    def open(self) -> None:
        self._open = True

    def close(self) -> None:
        self._open = False

    @staticmethod
    def overlay_rect(screen_size: ScreenSize, overlay_size: Size) -> pygame.Rect:
        sw, sh = screen_size
        ow, oh = overlay_size
        return pygame.Rect(sw // 2 - ow // 2, sh // 2 - oh // 2, ow, oh)

    def handle_click(
        self,
        pos: tuple[int, int],
        screen_size: ScreenSize,
        overlay_size: Size,
    ) -> None:
        if HUD.save_button_rect(screen_size).collidepoint(pos):
            if not self._open:
                self._open = True
            return
        if self._open and not self.overlay_rect(screen_size, overlay_size).collidepoint(pos):
            self._open = False
