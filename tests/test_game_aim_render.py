"""Regression: drawing the aim view at vertical angles must not crash.

The legacy round_rotation helper cropped the rotated image back to its
original rect, which broke at ±90° for non-square sprites because the
crop rect fell outside the rotated surface. The new pivot-based blit
must handle every angle.
"""

import pygame
import pytest

from gts.game import Game


@pytest.fixture(scope="module")
def game():
    return Game()


@pytest.mark.parametrize("angle", [-180, -90, -45, 0, 45, 90, 180])
@pytest.mark.parametrize("facing", ["left", "right"])
def test_draw_aim_does_not_crash(game, angle, facing):
    sprite = pygame.Surface((50, 30), pygame.SRCALPHA)
    game._draw_aim((400, 300), sprite, float(angle), facing)
