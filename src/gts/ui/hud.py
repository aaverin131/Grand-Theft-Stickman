"""On-screen toolbar, FPS readout, and save-button placement."""

from __future__ import annotations

import pygame

from .. import config

ScreenSize = tuple[int, int]
Pos = tuple[float, float]


class HUD:
    def __init__(self, font: pygame.font.Font):
        self.font = font

    @staticmethod
    def toolbar_pos(screen_size: ScreenSize) -> Pos:
        sw, sh = screen_size
        return (sw / 2 + config.TOOLBAR_OFFSET_X, sh - config.TOOLBAR_FROM_BOTTOM)

    @staticmethod
    def slot_icon_pos(screen_size: ScreenSize, slot: int) -> Pos:
        tx, ty = HUD.toolbar_pos(screen_size)
        return (
            tx + config.TOOLBAR_ITEM_INSET_X + slot * config.TOOLBAR_SLOT_WIDTH,
            ty + config.TOOLBAR_ITEM_INSET_Y,
        )

    @staticmethod
    def slot_frame_pos(screen_size: ScreenSize, selected: int) -> Pos:
        tx, ty = HUD.toolbar_pos(screen_size)
        return (
            tx - config.TOOLBAR_FRAME_INSET + selected * config.TOOLBAR_SLOT_WIDTH,
            ty - config.TOOLBAR_FRAME_INSET,
        )

    @staticmethod
    def save_button_pos(screen_size: ScreenSize) -> Pos:
        sw, _ = screen_size
        return (sw - config.SAVE_BUTTON_SIZE, 0)

    @staticmethod
    def save_button_rect(screen_size: ScreenSize) -> pygame.Rect:
        sw, _ = screen_size
        size = config.SAVE_BUTTON_SIZE
        return pygame.Rect(sw - size, 0, size, size)

    def fps_surface(self, fps: float) -> pygame.Surface:
        return self.font.render(f"FPS: {int(fps)}", True, config.COLOR_TEXT)
