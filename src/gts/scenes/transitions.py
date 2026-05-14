"""Pure helpers for scene-transition detection."""

from __future__ import annotations

import pygame

from .scene import Scene


def find_scene_transition(scene: Scene, player_rect: pygame.Rect) -> str | None:
    """Return the target_scene of any collidable prop overlapping `player_rect`."""
    for prop in scene.collidable_props():
        if prop.target_scene is None:
            continue
        prop_rect = prop.image.get_bounding_rect().move(int(prop.pos[0]), int(prop.pos[1]))
        if prop_rect.colliderect(player_rect):
            return prop.target_scene
    return None
