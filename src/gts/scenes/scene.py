"""Scene and Prop base types."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

import pygame

from ..assets import AssetLoader


@dataclass
class Prop:
    """An image positioned in world coordinates.

    `pos` is mutated each frame as the player moves, so all props translate
    together. `collidable` props block the player; `target_scene`, if set,
    causes the E key to switch to that scene when the player is adjacent.
    """

    image: pygame.Surface
    pos: list[float]
    collidable: bool = False
    target_scene: Optional[str] = None


class Scene:
    """Base class for a named scene with a background color and a list of props."""

    name: str = ""
    bg_color: tuple[int, int, int] = (0, 0, 0)

    def __init__(self) -> None:
        self.props: list[Prop] = []

    def load(self, loader: AssetLoader) -> None:
        """Populate `self.props`. Override in subclasses."""
        raise NotImplementedError

    def translate(self, dx: float, dy: float) -> None:
        for prop in self.props:
            prop.pos[0] += dx
            prop.pos[1] += dy

    def draw_background(self, screen: pygame.Surface) -> None:
        screen.fill(self.bg_color)

    def draw_props(self, screen: pygame.Surface) -> None:
        for prop in self.props:
            screen.blit(prop.image, prop.pos)

    def collidable_props(self) -> list[Prop]:
        return [p for p in self.props if p.collidable]
