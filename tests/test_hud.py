import pygame

from gts import config
from gts.ui.hud import HUD

SCREEN = (1000, 800)


def test_toolbar_pos():
    assert HUD.toolbar_pos(SCREEN) == (
        SCREEN[0] / 2 + config.TOOLBAR_OFFSET_X,
        SCREEN[1] - config.TOOLBAR_FROM_BOTTOM,
    )


def test_slot_icon_pos_first_slot():
    tx, ty = HUD.toolbar_pos(SCREEN)
    assert HUD.slot_icon_pos(SCREEN, 0) == (
        tx + config.TOOLBAR_ITEM_INSET_X,
        ty + config.TOOLBAR_ITEM_INSET_Y,
    )


def test_slot_icon_pos_advances_by_slot_width():
    base = HUD.slot_icon_pos(SCREEN, 0)
    third = HUD.slot_icon_pos(SCREEN, 3)
    assert third[0] - base[0] == 3 * config.TOOLBAR_SLOT_WIDTH
    assert third[1] == base[1]


def test_slot_frame_pos_offsets_outward():
    tx, ty = HUD.toolbar_pos(SCREEN)
    assert HUD.slot_frame_pos(SCREEN, 0) == (
        tx - config.TOOLBAR_FRAME_INSET,
        ty - config.TOOLBAR_FRAME_INSET,
    )
    assert HUD.slot_frame_pos(SCREEN, 5) == (
        tx - config.TOOLBAR_FRAME_INSET + 5 * config.TOOLBAR_SLOT_WIDTH,
        ty - config.TOOLBAR_FRAME_INSET,
    )


def test_save_button_rect_is_top_right_square():
    rect = HUD.save_button_rect(SCREEN)
    assert isinstance(rect, pygame.Rect)
    assert rect.width == config.SAVE_BUTTON_SIZE
    assert rect.height == config.SAVE_BUTTON_SIZE
    assert rect.right == SCREEN[0]
    assert rect.top == 0


def test_fps_surface_renders_text():
    font = pygame.font.SysFont("Arial", 24)
    hud = HUD(font)
    surface = hud.fps_surface(70)
    assert isinstance(surface, pygame.Surface)
    assert surface.get_width() > 0
    # A different number must produce a visibly different surface.
    other = hud.fps_surface(7)
    assert surface.get_size() != other.get_size() or (
        pygame.image.tobytes(surface, "RGBA") != pygame.image.tobytes(other, "RGBA")
    )
