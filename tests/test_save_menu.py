from gts.ui.hud import HUD
from gts.ui.save_menu import SaveMenu

SCREEN = (1000, 800)
OVERLAY = (500, 500)


def test_starts_closed():
    assert SaveMenu().is_open is False


def test_save_button_click_opens_when_closed():
    menu = SaveMenu()
    rect = HUD.save_button_rect(SCREEN)
    menu.handle_click(rect.center, SCREEN, OVERLAY)
    assert menu.is_open is True


def test_inside_overlay_click_keeps_open():
    menu = SaveMenu()
    menu.open()
    menu.handle_click((SCREEN[0] // 2, SCREEN[1] // 2), SCREEN, OVERLAY)
    assert menu.is_open is True


def test_outside_overlay_click_closes():
    menu = SaveMenu()
    menu.open()
    menu.handle_click((5, 5), SCREEN, OVERLAY)
    assert menu.is_open is False


def test_explicit_close():
    menu = SaveMenu()
    menu.open()
    menu.close()
    assert menu.is_open is False


def test_click_far_from_button_when_closed_does_nothing():
    menu = SaveMenu()
    menu.handle_click((5, 5), SCREEN, OVERLAY)
    assert menu.is_open is False


def test_overlay_rect_centered():
    rect = SaveMenu.overlay_rect(SCREEN, OVERLAY)
    assert rect.center == (SCREEN[0] // 2, SCREEN[1] // 2)
    assert rect.size == OVERLAY
